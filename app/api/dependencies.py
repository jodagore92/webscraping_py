from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.services.queue_factory import QueueFactory
from app.services.database_factory import DatabaseFactory
from app.application.use_cases.search_products_use_case import SearchProductsUseCase
from app.application.use_cases.get_search_result_use_case import GetSearchResultUseCase
from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.get_history import GetSearchHistoryUseCase
from app.core.config import settings
from app.models.user import UserInDB, TokenData, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_search_products_use_case() -> SearchProductsUseCase:
    """Inyecta el caso de uso de búsqueda con su infraestructura"""
    queue_provider = QueueFactory.get()
    return SearchProductsUseCase(queue_provider)


def get_search_result_use_case() -> GetSearchResultUseCase:
    """Inyecta el caso de uso de obtención de resultados"""
    queue_provider = QueueFactory.get()
    return GetSearchResultUseCase(queue_provider)


def get_register_user_use_case() -> RegisterUserUseCase:
    db = DatabaseFactory.get_database()
    return RegisterUserUseCase(db)


def get_login_user_use_case() -> LoginUserUseCase:
    db = DatabaseFactory.get_database()
    return LoginUserUseCase(db)


def get_history_use_case() -> GetSearchHistoryUseCase:
    db = DatabaseFactory.get_database()
    return GetSearchHistoryUseCase(db)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    db = DatabaseFactory.get_database()
    user = await db.get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception

    # Mongo _id a string para compatibilidad
    user["_id"] = str(user["_id"])
    return UserInDB(**user)


def check_admin_role(current_user: UserInDB = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación no permitida para este usuario",
        )
    return current_user
