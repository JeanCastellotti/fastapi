from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post('/register',
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash_password(user.password)
    new_user = models.User(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This email already exists")

    return new_user


@router.post('/login', response_model=schemas.Token)
def login(login: schemas.UserCreate, db: Session = Depends(get_db)):
    # Get user from database
    user = db.query(
        models.User).filter(models.User.email == login.email).first()

    # If email does not exist
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")

    # If passwords do not match
    if not utils.verify_password(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")

    # Create Token
    token = oauth2.create_jwt_token(data={"user_id": user.id})

    return {"token": token, "type": "bearer"}
