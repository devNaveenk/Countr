"""Composition root for v1 — where abstractions are bound to implementations.

This is the ONE place allowed to know both the domain ports and their concrete
infrastructure implementations. Routes ask for a use-case; they never construct
repositories or sessions themselves.
"""

from collections.abc import Iterator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.application.use_cases.authenticate_user import AuthenticateUser
from app.application.use_cases.check_health import CheckHealth
from app.application.use_cases.register_user import RegisterUser
from app.core.config import Settings, get_settings
from app.domain.entities.user import User
from app.domain.security import PasswordHasher, TokenService
from app.infrastructure.db.session import get_session
from app.infrastructure.repositories.sql_health_repository import SqlHealthRepository
from app.infrastructure.repositories.sql_user_repository import SqlUserRepository
from app.infrastructure.security.bcrypt_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_token_service import JwtTokenService


def db_session() -> Iterator[Session]:
    yield from get_session()


# --- shared singletons-per-request (cheap to build) ---

def password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()


def token_service(settings: Settings = Depends(get_settings)) -> TokenService:
    return JwtTokenService(
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        ttl_minutes=settings.access_token_ttl_minutes,
    )


# --- health ---

def check_health_use_case(session: Session = Depends(db_session)) -> CheckHealth:
    return CheckHealth(SqlHealthRepository(session))


# --- auth use-cases ---

def register_user_use_case(
    session: Session = Depends(db_session),
    hasher: PasswordHasher = Depends(password_hasher),
) -> RegisterUser:
    return RegisterUser(SqlUserRepository(session), hasher)


def authenticate_user_use_case(
    session: Session = Depends(db_session),
    hasher: PasswordHasher = Depends(password_hasher),
    tokens: TokenService = Depends(token_service),
) -> AuthenticateUser:
    return AuthenticateUser(SqlUserRepository(session), hasher, tokens)


# --- current user (protects routes) ---

_bearer = HTTPBearer(auto_error=False)


def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    session: Session = Depends(db_session),
    tokens: TokenService = Depends(token_service),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    user_id = tokens.read_subject(credentials.credentials)
    if user_id is None:
        raise unauthorized
    user = SqlUserRepository(session).get_by_id(user_id)
    if user is None:
        raise unauthorized
    return user
