# Definition of Done — Semana 2

Una historia de usuario se considera terminada únicamente cuando cumple todos los siguientes criterios.

## Requisitos funcionales

- Todos los criterios de aceptación de la historia están satisfechos.
- Los escenarios Gherkin relacionados funcionan correctamente.
- El comportamiento implementado corresponde al alcance definido en la historia.
- No se agregaron funcionalidades fuera del alcance solicitado.

## Desarrollo guiado por pruebas

- La prueba fue escrita antes de la implementación.
- Existe un commit de prueba fallida que demuestra la fase Red.
- Existe un commit posterior con la implementación mínima que demuestra la fase Green.
- Las pruebas verifican comportamiento observable y no detalles internos innecesarios.
- No se realizaron refactors que alteren el comportamiento esperado.

## Calidad del código

- Todo el código tiene anotaciones de tipo.
- `mypy` termina sin errores.
- `ruff` termina sin errores.
- El código utiliza nombres claros y responsabilidades bien delimitadas.
- Las excepciones representan conceptos del dominio y no exponen errores internos.
- Las clases, métodos y decisiones no evidentes están documentados.

## Pruebas y cobertura

- Todas las pruebas automatizadas pasan.
- La cobertura de Semana 2 es igual o superior al 80 %.
- No existen pruebas deshabilitadas o ignoradas sin justificación.
- Los casos principales y los errores esperados están cubiertos.

## Control de versiones

- El trabajo se desarrolló en una rama específica.
- Los commits tienen mensajes claros y describen una sola intención.
- El historial conserva evidencia del ciclo Red, Green y Refactor cuando corresponde.
- Se creó un pull request hacia `main`.
- El pull request no presenta conflictos.
- La rama fue eliminada después de integrar el cambio.

## Gestión del trabajo

- La historia pasó por Backlog, Sprint, In Progress, Review y Done según correspondía.
- El issue relacionado quedó cerrado.
- El pull request referencia la historia o issue correspondiente.
- El tablero refleja el estado real del trabajo.

## Validación final

Antes de integrar una historia ejecutamos:

```powershell
python -m pytest
python -m mypy
python -m ruff check .\semana2
```

La historia solamente puede pasar a Done cuando los tres comandos terminan correctamente.
