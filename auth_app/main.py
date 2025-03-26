from .database import init_db, close_db_connections, get_session
from .schemas import Token
from .models import User

from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
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

@auth_app.post("/login", response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await db.query(User).filter(User.login == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, data="Invalid Credantials")
    
    verify = await verify(user_credentials.password, user.password)
   
    if not verify:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, data="Invalid Credantials")

    access_token = await create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer token"}