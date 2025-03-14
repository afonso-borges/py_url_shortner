from pydantic import BaseModel, HttpUrl, field_validator, Field
from typing import Optional
from datetime import datetime

class URLBase(BaseModel):
    """Esquema base para URLs"""
    original_url: str
    
    @field_validator('original_url')
    def validate_url(cls, v):
        """Valida se a URL é válida"""
        # Podemos usar HttpUrl diretamente, mas isso pode ser muito restritivo
        # Então fazemos uma validação básica
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

class URLCreate(URLBase):
    """Esquema para criação de URLs encurtadas"""
    expires_in_days: Optional[int] = Field(default=None, ge=0)
    custom_code: Optional[str] = Field(default=None, min_length=3, max_length=20)
    created_by: Optional[str] = None

class URLResponse(URLBase):
    """Esquema para resposta de URLs encurtadas"""
    short_code: str
    short_url: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool
    access_count: int = 0
    
    class Config:
        from_attributes = True

class URLStats(BaseModel):
    """Esquema para estatísticas de URLs encurtadas"""
    short_code: str
    original_url: str
    short_url: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool
    access_count: int
    created_by: Optional[str] = None
    
    class Config:
        from_attributes = True
