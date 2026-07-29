from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


# Register User
def register_user(user: UserRegister, db: Session):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return None

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        role_id=user.role_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login User
def login_user(user: UserLogin, db: Session):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        return None

    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        return None

    token = create_access_token(
        {
            "user_id": existing_user.user_id,
            "role_id": existing_user.role_id,
            "email": existing_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }