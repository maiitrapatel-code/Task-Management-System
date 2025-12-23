import os
import bcrypt
# --- FIX FOR PYTHON 3.12 & PASSLIB ---
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type('about', (object,), {'__version__': bcrypt.__version__})
# -------------------------------------

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db
from models import Users
from schemas import CreateUserRequest, Token

router = APIRouter(prefix='/auth', tags=['auth'])

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

def authenticate_user(username: str, password: str, db: Session) -> Union[Users, bool]:
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    # Cast to str to satisfy type checker
    hashed_pw: str = str(user.hashed_password)
    if not bcrypt_context.verify(password, hashed_pw):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta) -> str:
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get('sub')
        user_id: Optional[int] = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Could not validate user.')

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[Session, Depends(get_db)], 
                      create_user_request: CreateUserRequest):
    # Check if user already exists
    existing_user = db.query(Users).filter(
        (Users.email == create_user_request.email) | 
        (Users.username == create_user_request.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Annotated[Session, Depends(get_db)]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user or isinstance(user, bool):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Invalid username or password.')
    # Extract values to satisfy type checker
    username_val: str = getattr(user, 'username')
    user_id_val: int = getattr(user, 'id')
    token = create_access_token(username_val, user_id_val, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}



@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(user: Annotated[dict, Depends(get_current_user)]):
    return {"message": "Successfully logged out"}