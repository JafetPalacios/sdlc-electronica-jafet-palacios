from app.schemas import ReadingCreate


# Representa la lógica del negocio
# No sabe nada de HTTP ni de SQL
class ReadingService:

    # Contiene las reglas de negocio relacionadas con las lecturas
    def create_reading(self, reading: ReadingCreate) -> ReadingCreate:

        return reading          # Procesa una nueva lectura