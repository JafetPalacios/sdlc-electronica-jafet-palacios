# Sprint 1 Retrospective

## Qué salió bien

- Se aplicó TDD respetando el orden Red, Green y validación para cada comportamiento
- Las historias técnicas se dividieron en cambios pequeños y verificables
- Los componentes se diseñaron con responsabilidades separadas
- Los umbrales y las estrategias se inyectaron externamente para facilitar cambios y pruebas
- Cada componente alcanzó una cobertura del 100 %
- La cobertura global de la Semana 2 se mantuvo por encima del mínimo requerido
- Las validaciones con pytest, mypy y Ruff se ejecutaron antes de integrar cada componente
- Los Pull Requests conservaron los commits separados de prueba e implementación

## Qué se puede mejorar

- Definir desde el inicio un formato reutilizable para los mensajes de alerta
- Reducir pasos manuales repetitivos durante las validaciones de cada ciclo TDD
- Agregar pruebas para escenarios límite, como valores exactamente iguales a los umbrales
- Revisar previamente el formato de imports para evitar correcciones posteriores con Ruff
- Mantener mensajes de commit más uniformes entre todos los ciclos

## Acción para el siguiente Sprint

Crear un comando único de validación que ejecute pruebas, cobertura, mypy y Ruff antes de cada Pull Request

## Resultado del Sprint

Se completaron los tres componentes técnicos obligatorios de la evaluación:

1. `SensorReading`
2. `AnomalyDetector`
3. `AlertManager`

El código quedó validado con 11 pruebas aprobadas, cobertura global de 97.67 %, mypy sin errores y Ruff sin errores