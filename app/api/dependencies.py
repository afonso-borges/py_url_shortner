from fastapi import HTTPException, status, Header
from app.utils.config import get_settings

async def verify_api_key(x_api_key: str = Header(None)):
    """
    Verifica se a API key fornecida é válida.
    Se nenhuma API key estiver configurada, permite o acesso.

    Args:
        x_api_key: API key fornecida no cabeçalho da requisição

    Returns:
        str: API key válida

    Raises:
        HTTPException: Se a API key for inválida ou não fornecida
    """
    settings = get_settings()

    if not settings.api_key:
        return "no_api_key_required"

    # Verifica se a API key foi fornecida
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # Verifica se a API key é válida
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return x_api_key
