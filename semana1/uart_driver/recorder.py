import json
from pathlib import Path


class JsonLinesRecorder:
    def __init__(self, filename: str | Path) -> None:
        self.filename = Path(filename)                                              # Guardamos la ruta donde persistiremos los registros

    def save(self, record: dict[str, object]) -> None:
        # Creamos las carpetas necesarias si todavía no existen
        self.filename.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Abrimos el archivo en modo append para conservar registros anteriores
        with self.filename.open("a", encoding="utf-8") as file:
            json.dump(
                record,
                file,
                ensure_ascii=False,
                default=self._serialize_value,
            )

            file.write("\n")                                                       # Separamos cada registro mediante un salto de línea

    @staticmethod
    def _serialize_value(value: object) -> object:
        # Convertimos los bytes a hexadecimal para almacenarlos como JSON
        if isinstance(value, bytes):
            return value.hex()

        raise TypeError(
            f"Object of type {type(value).__name__} is not JSON serializable"
        )