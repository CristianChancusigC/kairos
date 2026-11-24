from fastapi import APIRouter, HTTPException, status

from src.adapters.outbound.persistence.db import check_database_connection

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    try:
        check_database_connection()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        ) from exc

    return {"status": "ok", "database": "connected"}