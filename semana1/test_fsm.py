from semana1.fsm_demo import TrafficLightFSM, TrafficLightState


def test_initial_state_is_red() -> None:
    fsm = TrafficLightFSM()                                     # Creamos una nueva máquina de estados
    assert fsm.state is TrafficLightState.RED                   # Verificamos que comience en rojo

def test_transition_from_red_to_green() -> None:
    fsm = TrafficLightFSM()
    fsm.transition()                                            # Ejecutamos una transición
    assert fsm.state is TrafficLightState.GREEN                 # Verificamos que el estado haya cambiado a verde

def test_complete_cycle_returns_to_red() -> None:
    fsm = TrafficLightFSM()

    # Ejecutamos las tres transiciones que forman un ciclo completo
    fsm.transition()
    fsm.transition()
    fsm.transition()

    assert fsm.state is TrafficLightState.RED                   # Verificamos que el estado haya regresado a rojo   

def test_cycle_count_increases() -> None:
    fsm = TrafficLightFSM()

    for _ in range(6):                                          # Completamos dos ciclos
        fsm.transition()

    assert fsm.cycles == 2                                      # Verificamos que se hayan registrado dos ciclos
    

