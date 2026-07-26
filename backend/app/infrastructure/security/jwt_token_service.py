"""PyJWT implementation of the TokenService port."""

from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from app.domain.security import TokenService


class JwtTokenService(TokenService):
    def __init__(self, *, secret: str, algorithm: str, ttl_minutes: int) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._ttl = timedelta(minutes=ttl_minutes)

    def issue_access_token(self, *, subject: UUID) -> str:
        now = datetime.now(UTC)
        payload = {"sub": str(subject), "iat": now, "exp": now + self._ttl}
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def read_subject(self, token: str) -> UUID | None:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            return UUID(payload["sub"])
        except (jwt.PyJWTError, KeyError, ValueError):
            return None
