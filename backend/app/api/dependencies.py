from typing import Generator

from fastapi import Depends
from sqlmodel import Session

from ..core.database import get_session


def get_db_session() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    with get_session() as session:
        yield session
