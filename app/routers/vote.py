from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import oauth2, database, models, schemas

router = APIRouter()


#  Path operation POST /vote
# user id extracted from JWT TOKEN
# body contains post id and vote dir (1 = add or 0 = delete)
@router.post('/vote', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         db: Session = Depends(database.get_db),
         current_user=Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist")

    query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id)

    voted = query.first()

    if vote.dir == 1:
        if voted:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=
                f"User with id {current_user.id} has already voted on post {vote.post_id}"
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not voted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")
        query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
