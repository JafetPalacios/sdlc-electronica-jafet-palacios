from enum import Enum

class TrafficLightState(Enum):
    # Definimos los únicos estados permitidos para el semáforo.
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"

class TrafficLightFSM:
    def __init__(self) -> None:
        self.state: TrafficLightState = TrafficLightState.RED               # Inicializamos la máquina en el estado rojo
        self.cycles: int = 0                                                # Inicializamos el número de ciclos completados

    def transition(self) -> None:
        # Cambiamos al siguiente estado según el estado actual
        if self.state is TrafficLightState.RED:
            self.state = TrafficLightState.GREEN
        elif self.state is TrafficLightState.GREEN:
            self.state = TrafficLightState.YELLOW
        else:
            # Regresamos a rojo y registramos un ciclo completo
            self.state = TrafficLightState.RED
            self.cycles += 1