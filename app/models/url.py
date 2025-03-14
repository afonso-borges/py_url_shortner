from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import expression
from datetime import datetime, timezone
from typing import Optional

from app.models.database import Base

class URL(Base):
    """Modelo de URL encurtada no banco de dados"""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, server_default=expression.true(), nullable=False)
    access_count = Column(Integer, default=0, nullable=False)
    created_by = Column(String, nullable=True)

    @property
    def is_expired(self) -> bool:
        """Verifica se a URL está expirada"""
        if not self.expires_at:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def short_url(self) -> Optional[str]:
        """Retorna a URL encurtada completa"""
        from app.utils.config import get_settings

        settings = get_settings()
        if not settings.base_url:
            return None

        return f"{settings.base_url}/{self.short_code}"
