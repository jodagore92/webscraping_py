from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.infrastructure.database.database_provider import DatabaseProvider
from app.core.security import verify_password, create_access_token
from app.models.user import Token


class LoginUserUseCase:
    def __init__(self, db: DatabaseProvider):
        self.db = db

    async def execute(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user = await self.db.get_user_by_email(form_data.username)
        if not user or not verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo",
            )

        access_token = create_access_token(data={"sub": user["email"]})
        return Token(access_token=access_token, token_type="bearer")
