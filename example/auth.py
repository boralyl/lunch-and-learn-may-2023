from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader


api_key_header = APIKeyHeader(name="x-api-key")


def require_api_key(
    api_key: str = Depends(api_key_header)
) -> None:
    if api_key != "super-secret-api-key":
        raise HTTPException(status_code=401)
