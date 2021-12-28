from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/")
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = None):
    # query = db.query(models.Post).order_by(models.Post.id.desc())
    # if search: query = query.filter(models.Post.title.contains(search))
    # posts = query.limit(limit).offset(skip).all()

    posts = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("likes")).join(
            models.Vote, models.Vote.post_id == models.Post.id,
            isouter=True).group_by(models.Post.id).order_by(
                models.Post.id.desc()).limit(limit).offset(skip).all()
    # print(results)
    return posts


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post,
                    func.count(models.Vote.post_id).label("likes")).join(
                        models.Vote,
                        models.Vote.post_id == models.Post.id,
                        isouter=True).group_by(models.Post.id).filter(
                            models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return post


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.PostOut)
def update_post(id: int,
                post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):

    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")

    if updated_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()
