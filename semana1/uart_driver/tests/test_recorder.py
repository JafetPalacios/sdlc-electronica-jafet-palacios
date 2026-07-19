import json
from pathlib import Path

from semana1.uart_driver.recorder import JsonLinesRecorder


def test_recorder_creates_json_lines_file(tmp_path: Path) -> None:                              # El recorder cree el archivo y guarde JSON válido
    # Construimos una ruta temporal para no crear archivos en el proyecto
    file_path = tmp_path / "records.jsonl"
    recorder = JsonLinesRecorder(file_path)

    # Guardamos un registro.
    recorder.save(
        {
            "protocol": "nmea",
            "sentence_type": "GPGGA",
        }
    )

    assert file_path.exists()                                               # Verificamos que el archivo se haya creado
    record = json.loads(file_path.read_text(encoding="utf-8"))

    assert record == {
        "protocol": "nmea",
        "sentence_type": "GPGGA",
    }


def test_recorder_appends_multiple_records(tmp_path: Path) -> None:         # Usa modo append y conserve varios registros
    file_path = tmp_path / "records.jsonl"
    recorder = JsonLinesRecorder(file_path)

    # Guardamos dos registros consecutivos
    recorder.save(
        {
            "protocol": "nmea",
        }
    )
    recorder.save(
        {
            "protocol": "modbus",
        }
    )

    # Leemos cada línea como un objeto JSON independiente
    lines = file_path.read_text(encoding="utf-8").splitlines()
    records = [json.loads(line) for line in lines]

    assert records == [
        {"protocol": "nmea"},
        {"protocol": "modbus"},
    ]


def test_recorder_serializes_bytes_as_hexadecimal(                         # Convierta los valores bytes a hexadecimal
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "records.jsonl"
    recorder = JsonLinesRecorder(file_path)

    # Guardamos bytes provenientes de una trama Modbus
    recorder.save(
        {
            "protocol": "modbus",
            "data": b"\x00\x10",
        }
    )

    record = json.loads(file_path.read_text(encoding="utf-8"))

    assert record["data"] == "0010"                                           # Verificamos que los bytes se conviertan a texto hexadecimal