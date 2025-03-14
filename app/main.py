from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.models.database import Base, engine, get_db
from app.api.routes import router as api_router

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar aplicação FastAPI
app = FastAPI(
    title="URL Shortener API",
    description="API para encurtar URLs e rastrear estatísticas de acesso",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas da API
app.include_router(api_router, prefix="/api", tags=["API"])

# Rota para redirecionar URLs encurtadas
@app.get("/{short_url}")
async def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
    from app.services.url_service import get_original_url, increment_access_count

    original_url = await get_original_url(short_url, db)
    if original_url:
        # Incrementar contador de acessos de forma assíncrona
        await increment_access_count(short_url, db)
        # Retornar a URL original para redirecionamento
        return {"url": original_url}

    # Se a URL não for encontrada, retornar erro 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL with code {short_url} not found or expired"
    )

# Rota raiz
@app.get("/", tags=["Root"])
async def root():
    """Rota raiz da API"""
    return {
        "message": "URL Shortener API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
