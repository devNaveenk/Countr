"""AuthenticateUser use-case — verify credentials and issue an access token.

Returns the same InvalidCredentials error whether the email is unknown or the password is
wrong, so the API never leaks which emails exist.
"""

from dataclasses import dataclass

from app.application.errors import InvalidCredentials
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.security import PasswordHasher, TokenService


@dataclass(frozen=True)
class AuthResult:
    user: User
    access_token: str


class AuthenticateUser:
    def __init__(
        self, users: UserRepository, hasher: PasswordHasher, tokens: TokenService
    ) -> None:
        self._users = users
        self._hasher = hasher
        self._tokens = tokens

    def execute(self, *, email: str, password: str) -> AuthResult:
        email = email.strip().lower()
        stored_hash = self._users.get_password_hash(email)
        if stored_hash is None or not self._hasher.verify(password, stored_hash):
            raise InvalidCredentials()

        user = self._users.get_by_email(email)
        assert user is not None  # hash existed, so the user exists
        token = self._tokens.issue_access_token(subject=user.id)
        return AuthResult(user=user, access_token=token)
