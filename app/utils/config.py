from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configurações da aplicação carregadas de variáveis de ambiente ou arquivo .env"""
    
    # Configurações do Banco de Dados
    database_url: str = "sqlite:///./url_shortener.db"
    
    # Configurações da API
    base_url: str = "http://localhost:8000"
    api_key: Optional[str] = None
    
    # Configurações de Integração (opcional)
    auth_service_url: Optional[str] = None
    email_service_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Retorna as configurações da aplicação (cacheadas para melhor performance)"""
    return Settings()
