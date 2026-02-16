from fastapi import HTTPException, status
from app.infrastructure.database.database_provider import DatabaseProvider
from app.models.user import UserCreate, UserInDB, UserRole
from app.core.security import get_password_hash


class RegisterUserUseCase:
    def __init__(self, db: DatabaseProvider):
        self.db = db

    async def execute(self, user_in: UserCreate):
        # Verificar si el usuario ya existe
        existing_user = await self.db.get_user_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya está registrado",
            )

        # Preparar datos para BD
        user_dict = user_in.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = get_password_hash(password)

        # Guardar en BD
        user_id = await self.db.save_user(user_dict)
        return user_id
