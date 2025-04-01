from .database import init_db, close_db_connections, get_session
from .schemas import Token, UserCreate, UserOut
from .models import User
from .oauth2 import create_access_token
from .utils import verify, hash

from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def life_span(app: FastAPI):
    await init_db()
    yield
    await close_db_connections()

version = "v1"

auth_app = FastAPI(lifespan=life_span)

@auth_app.get("/")
async def root():
    return {"message": "youre in root"}

@auth_app.post("/create")
async def create_user(new_user: UserCreate, db_session: AsyncSession =  Depends(get_session)):
    new_user.password = await hash(new_user.password)
    new_user = User(login=new_user.login, password=new_user.password)
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)
    return new_user

@auth_app.get("/user/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db_session: AsyncSession =  Depends(get_session)):
    result = await db_session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return UserOut(id=user.id, login=user.login)

@auth_app.post("/login", response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.login == user_credentials.username))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credantials")
    
    ver = await verify(user_credentials.password, user.password)
   
    if not ver:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credantials")

    access_token = await create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer token"}