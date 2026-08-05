from fastapi import APIRouter

from app.schemas import ReadingCreate

router = APIRouter(prefix="/readings", tags=["Lecturas"])


@router.post("/")
def create_reading(reading: ReadingCreate) -> ReadingCreate:      # Recibe una lectura y la devuelve
    return reading