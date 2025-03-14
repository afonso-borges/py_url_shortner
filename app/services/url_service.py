import string
import random
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.url import URL
from app.schemas import URLCreate, URLResponse, URLStats

# Função para gerar código aleatório
def generate_random_code(length: int = 6) -> str:
    """Gera um código aleatório para a URL encurtada"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Criar URL encurtada
async def create_short_url(url_data: URLCreate, db: Session) -> URLResponse:
    """
    Cria uma URL encurtada a partir dos dados fornecidos
    
    Args:
        url_data: Dados da URL a ser encurtada
        db: Sessão do banco de dados
        
    Returns:
        URLResponse: Dados da URL encurtada criada
        
    Raises:
        ValueError: Se o código personalizado já estiver em uso
    """
    # Usar código personalizado ou gerar um novo
    short_code = url_data.custom_code or generate_random_code()
    
    # Calcular data de expiração se fornecida
    expires_at = None
    if url_data.expires_in_days is not None:
        expires_at = datetime.now(timezone.utc) + timedelta(days=url_data.expires_in_days)
    
    # Criar objeto URL
    url = URL(
        original_url=url_data.original_url,
        short_code=short_code,
        expires_at=expires_at,
        created_by=url_data.created_by
    )
    
    try:
        # Adicionar ao banco de dados
        db.add(url)
        db.commit()
        db.refresh(url)
        
        # Retornar resposta
        return URLResponse.model_validate(url)
    except IntegrityError:
        # Rollback em caso de erro
        db.rollback()
        
        # Se o código personalizado já estiver em uso
        if url_data.custom_code:
            raise ValueError(f"Custom code '{short_code}' is already in use")
        
        # Tentar novamente com um novo código aleatório
        return await create_short_url(url_data, db)

# Obter URL original a partir do código curto
async def get_original_url(short_code: str, db: Session) -> Optional[str]:
    """
    Obtém a URL original a partir do código curto
    
    Args:
        short_code: Código curto da URL
        db: Sessão do banco de dados
        
    Returns:
        str: URL original ou None se não encontrada ou expirada
    """
    url = db.query(URL).filter(URL.short_code == short_code).first()
    
    if not url or not url.is_active or url.is_expired:
        return None
        
    return url.original_url

# Incrementar contador de acessos
async def increment_access_count(short_code: str, db: Session) -> None:
    """
    Incrementa o contador de acessos de uma URL
    
    Args:
        short_code: Código curto da URL
        db: Sessão do banco de dados
    """
    url = db.query(URL).filter(URL.short_code == short_code).first()
    
    if url:
        url.access_count += 1
        db.add(url)  # Explicitamente adicionar o objeto modificado à sessão
        db.commit()
        db.refresh(url)  # Atualizar o objeto com os dados do banco de dados

# Obter estatísticas de uma URL
async def get_url_stats(short_code: str, db: Session) -> Optional[URLStats]:
    """
    Obtém estatísticas de uma URL encurtada
    
    Args:
        short_code: Código curto da URL
        db: Sessão do banco de dados
        
    Returns:
        URLStats: Estatísticas da URL ou None se não encontrada
    """
    url = db.query(URL).filter(URL.short_code == short_code).first()
    
    if not url:
        return None
        
    return URLStats.model_validate(url)

# Listar URLs
async def list_urls(skip: int = 0, limit: int = 100, db: Session = None) -> List[URLResponse]:
    """
    Lista todas as URLs encurtadas
    
    Args:
        skip: Número de registros para pular
        limit: Número máximo de registros para retornar
        db: Sessão do banco de dados
        
    Returns:
        List[URLResponse]: Lista de URLs encurtadas
    """
    urls = db.query(URL).offset(skip).limit(limit).all()
    return [URLResponse.model_validate(url) for url in urls]
