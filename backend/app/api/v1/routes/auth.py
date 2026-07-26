"""Auth routes — thin. Delegate to use-cases; map application errors to HTTP."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.deps import (
    authenticate_user_use_case,
    current_user,
    register_user_use_case,
)
from app.application.errors import EmailAlreadyRegistered, InvalidCredentials
from app.application.use_cases.authenticate_user import AuthenticateUser
from app.application.use_cases.register_user import RegisterUser, RegisterUserCommand
from app.domain.entities.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new store owner and sign in",
)
def register(
    body: RegisterRequest,
    register_uc: RegisterUser = Depends(register_user_use_case),
    auth_uc: AuthenticateUser = Depends(authenticate_user_use_case),
) -> TokenResponse:
    try:
        register_uc.execute(
            RegisterUserCommand(
                email=body.email,
                full_name=body.full_name,
                password=body.password,
                role=body.role,
            )
        )
    except EmailAlreadyRegistered as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from exc

    result = auth_uc.execute(email=body.email, password=body.password)
    return TokenResponse(
        access_token=result.access_token,
        user=UserResponse.model_validate(result.user, from_attributes=True),
    )


@router.post("/login", response_model=TokenResponse, summary="Sign in")
def login(
    body: LoginRequest,
    auth_uc: AuthenticateUser = Depends(authenticate_user_use_case),
) -> TokenResponse:
    try:
        result = auth_uc.execute(email=body.email, password=body.password)
    except InvalidCredentials as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        ) from exc
    return TokenResponse(
        access_token=result.access_token,
        user=UserResponse.model_validate(result.user, from_attributes=True),
    )


@router.get("/me", response_model=UserResponse, summary="Current signed-in user")
def me(user: User = Depends(current_user)) -> UserResponse:
    return UserResponse.model_validate(user, from_attributes=True)
