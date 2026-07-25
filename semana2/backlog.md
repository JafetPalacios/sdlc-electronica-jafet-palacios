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


---

## US-02: Rechazar identificadores duplicados

**Como** operador del sistema,
**quiero** impedir el registro de dos sensores con el mismo identificador,
**para** evitar información ambigua o sobrescrita.

### Prioridad

Alta

### Estimación

3 story points

### Criterios de aceptación

```gherkin
Característica: Validación de identificadores de sensores

  Escenario: Rechazar un sensor con identificador duplicado
    Dado que existe un sensor con identificador "TEMP-001" y nombre "Sensor principal"
    Cuando se intenta registrar otro sensor con identificador "TEMP-001" y nombre "Sensor secundario"
    Entonces el sistema debe generar un error de identificador duplicado
    Y la cantidad de sensores registrados debe continuar siendo 1
    Y la consulta por "TEMP-001" debe devolver el sensor con nombre "Sensor principal"
```


---

## US-03: Consultar un sensor por identificador

**Como** operador del sistema,
**quiero** consultar un sensor mediante su identificador único,
**para** revisar su información registrada cuando sea necesario.

### Prioridad

Alta

### Estimación

2 story points

### Criterios de aceptación

```gherkin
Característica: Consulta de sensores

  Escenario: Consultar un sensor existente
    Dado que existe un sensor con identificador "HUM-001" y nombre "Sensor de humedad"
    Cuando se consulta el sensor mediante el identificador "HUM-001"
    Entonces la consulta debe devolver un sensor con identificador "HUM-001"
    Y el sensor consultado debe tener el nombre "Sensor de humedad"
```


---

## US-04: Informar cuando un sensor no existe

**Como** operador del sistema,
**quiero** recibir un error específico cuando consulte un identificador inexistente,
**para** distinguir entre un sensor no registrado y un fallo del sistema.

### Prioridad

Alta

### Estimación

2 story points

### Criterios de aceptación

```gherkin
Característica: Consulta de sensores inexistentes

  Escenario: Consultar un identificador no registrado
    Dado que el registro de sensores está vacío
    Cuando se consulta el sensor con identificador "TEMP-999"
    Entonces el sistema debe generar un error de sensor no encontrado
    Y el registro de sensores debe continuar vacío
```


---

## US-05: Eliminar un sensor registrado

**Como** operador del sistema,
**quiero** eliminar un sensor mediante su identificador,
**para** retirar del registro sensores que ya no deben administrarse.

### Prioridad

Media

### Estimación

3 story points

### Criterios de aceptación

```gherkin
Característica: Eliminación de sensores

  Escenario: Eliminar un sensor existente
    Dado que el registro contiene únicamente un sensor con identificador "TEMP-001" y nombre "Sensor de temperatura"
    Cuando se elimina el sensor con identificador "TEMP-001"
    Entonces una consulta posterior por "TEMP-001" debe generar un error de sensor no encontrado
    Y la cantidad de sensores registrados debe ser 0
```

