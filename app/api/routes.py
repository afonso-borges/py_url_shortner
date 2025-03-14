from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db
from app.schemas import URLCreate, URLResponse, URLStats
from app.services.url_service import (
    create_short_url,
    get_url_stats,
    list_urls
)
from app.api.dependencies import verify_api_key

router = APIRouter()

@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def shorten_url(
    url_data: URLCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Cria uma URL encurtada a partir de uma URL original.
    
    - **original_url**: URL original a ser encurtada (obrigatório)
    - **expires_in_days**: Número de dias até a expiração da URL (opcional)
    - **custom_code**: Código personalizado para a URL encurtada (opcional)
    - **created_by**: Identificador do criador da URL (opcional)
    """
    try:
        return await create_short_url(url_data, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/stats/{short_code}", response_model=URLStats)
async def get_stats(
    short_code: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Retorna estatísticas sobre uma URL encurtada.
    
    - **short_code**: Código da URL encurtada
    """
    stats = await get_url_stats(short_code, db)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    return stats

@router.get("/list", response_model=List[URLResponse])
async def get_urls(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Lista todas as URLs encurtadas.
    
    - **skip**: Número de registros para pular (opcional, padrão: 0)
    - **limit**: Número máximo de registros para retornar (opcional, padrão: 100)
    """
    return await list_urls(skip, limit, db)
