from fastapi import APIRouter

from app.schemas import ReadingCreate
from app.services.reading_service import ReadingService

router = APIRouter(
    prefix="/readings",
    tags=["Lecturas"],
)

reading_service = ReadingService()


@router.post("/")
def create_reading(reading: ReadingCreate) -> ReadingCreate:

    return reading_service.create_reading(reading)      # Recibe una lectura y delega su procesamiento al servicio