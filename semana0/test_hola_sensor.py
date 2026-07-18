from hola_sensor import Sensor

def test_sensor_read() -> None:
    sensor = Sensor()               # Creamos una instancia del sensor.
    assert sensor.read() == 23.5    # Comprobamos que la lectura sea la esperada.