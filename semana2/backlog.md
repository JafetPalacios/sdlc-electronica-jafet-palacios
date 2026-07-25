# Backlog de producto - Semana 2

## Product Goal

Construir un registro de sensores confiable que permita almacenar, consultar y administrar sensores mediante un proceso de desarrollo guiado por pruebas.

## Escala de estimación

Las historias se estimarán con story points usando la secuencia de Fibonacci:

`1, 2, 3, 5, 8, 13`

## Historias de usuario

Las historias de usuario y sus criterios de aceptación se agregarán progresivamente durante el Sprint 0.

---

## US-01: Registrar un sensor

**Como** operador del sistema,
**quiero** registrar un sensor con un identificador único y un nombre,
**para** conservarlo y poder consultarlo posteriormente.

### Prioridad

Alta

### Estimación

3 story points

### Criterios de aceptación

```gherkin
Característica: Registro de sensores

  Escenario: Registrar un sensor válido
    Dado que el registro de sensores está vacío
    Cuando se registra un sensor con identificador "TEMP-001" y nombre "Sensor de temperatura"
    Entonces la consulta por el identificador "TEMP-001" debe devolver el sensor registrado
    Y el sensor consultado debe conservar el nombre "Sensor de temperatura"
```

