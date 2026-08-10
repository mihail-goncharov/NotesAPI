from fastapi import APIRouter, HTTPException
from schemas.user import UserCreate, UserResponse, UserLogin, Token
from database.session import SessionDep
from models.user import User
from services.auth import hash_password, verify_password, create_access_token
from sqlalchemy import select

router = APIRouter()


@router.post("/register", tags=["auth"], status_code=201)
def create_user(user_data: UserCreate, session: SessionDep) -> UserResponse:
    email_exist = session.scalar(select(User).where(User.email == user_data.email))

    if not email_exist:
        new_user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password.get_secret_value())
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return UserResponse.model_validate(new_user)

    raise HTTPException(status_code=409, detail="User with this email already exists")


@router.post("/login", tags=["auth"], status_code=200)
def login(user_data: UserLogin, session: SessionDep) -> Token:
    user: User = session.scalar(select(User).where(User.email == user_data.email))

    if user is not None:
        password_correct = verify_password(user_data.password.get_secret_value(), user.hashed_password)
        if password_correct:
            access_token = create_access_token(data={"sub": user.id})
            return Token(access_token=access_token, token_type="bearer")


    raise HTTPException(status_code=401, detail="Could not validate credentials")
