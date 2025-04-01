from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    login: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    login: EmailStr

    model_config = ConfigDict(from_attributes=True)
