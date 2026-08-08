from fastapi import APIRouter, HTTPException
from schemas.user import UserCreate, UserResponse
from database.session import SessionDep
from models.user import User
from services.auth import hash_password, verify_password
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


