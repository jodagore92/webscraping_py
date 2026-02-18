from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase
from app.models.user import UserCreate, Token, UserResponse
from app.api.dependencies import get_register_user_use_case, get_login_user_use_case

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(
    user_in: UserCreate,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
):
    user_id = await use_case.execute(user_in)
    return {"message": "Usuario registrado exitosamente", "id": user_id}


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: LoginUserUseCase = Depends(get_login_user_use_case),
):
    return await use_case.execute(form_data)
