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
from app.application.use_cases.product_catalog import (
    AdjustStock,
    ArchiveProduct,
    CreateProduct,
    GetProduct,
    ListProducts,
    UpdateProduct,
)
from app.application.use_cases.checkout import Checkout
from app.application.use_cases.register_user import RegisterUser
from app.application.use_cases.sales_history import GetSale, ListRecentSales
from app.application.use_cases.store_report import GetStoreReport
from app.core.config import Settings, get_settings
from app.domain.entities.user import User
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.report_repository import ReportRepository
from app.domain.repositories.sale_repository import SaleRepository
from app.domain.security import PasswordHasher, TokenService
from app.infrastructure.db.session import get_session
from app.infrastructure.repositories.sql_health_repository import SqlHealthRepository
from app.infrastructure.repositories.sql_product_repository import SqlProductRepository
from app.infrastructure.repositories.sql_report_repository import SqlReportRepository
from app.infrastructure.repositories.sql_sale_repository import SqlSaleRepository
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


# --- products ---

def product_repository(session: Session = Depends(db_session)) -> ProductRepository:
    return SqlProductRepository(session)


def create_product_use_case(
    repo: ProductRepository = Depends(product_repository),
) -> CreateProduct:
    return CreateProduct(repo)


def list_products_use_case(
    repo: ProductRepository = Depends(product_repository),
) -> ListProducts:
    return ListProducts(repo)


def get_product_use_case(repo: ProductRepository = Depends(product_repository)) -> GetProduct:
    return GetProduct(repo)


def update_product_use_case(
    repo: ProductRepository = Depends(product_repository),
) -> UpdateProduct:
    return UpdateProduct(repo)


def archive_product_use_case(
    repo: ProductRepository = Depends(product_repository),
) -> ArchiveProduct:
    return ArchiveProduct(repo)


def adjust_stock_use_case(repo: ProductRepository = Depends(product_repository)) -> AdjustStock:
    return AdjustStock(repo)


# --- sales / checkout ---

def sale_repository(session: Session = Depends(db_session)) -> SaleRepository:
    return SqlSaleRepository(session)


def checkout_use_case(
    products: ProductRepository = Depends(product_repository),
    sales: SaleRepository = Depends(sale_repository),
    settings: Settings = Depends(get_settings),
) -> Checkout:
    return Checkout(products, sales, tax_rate=settings.default_tax_rate)


def list_sales_use_case(sales: SaleRepository = Depends(sale_repository)) -> ListRecentSales:
    return ListRecentSales(sales)


def get_sale_use_case(sales: SaleRepository = Depends(sale_repository)) -> GetSale:
    return GetSale(sales)


# --- reports ---

def report_repository(session: Session = Depends(db_session)) -> ReportRepository:
    return SqlReportRepository(session)


def store_report_use_case(
    reports: ReportRepository = Depends(report_repository),
    products: ProductRepository = Depends(product_repository),
) -> GetStoreReport:
    return GetStoreReport(reports, products)


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
