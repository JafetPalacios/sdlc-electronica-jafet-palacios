# Backlog del producto — Evaluación 1

## Contexto

Desarrollamos un sistema de monitoreo ambiental para una bodega.

El sistema recibe lecturas de temperatura y humedad provenientes de 10 sensores. Cada sensor genera una lectura cada 30 segundos.

Una lectura se considera anómala cuando cumple al menos una de las siguientes condiciones:

- Temperatura superior a 35 °C.
- Humedad superior a 80 %.

Cuando se detecta una anomalía, el sistema debe generar una alerta mediante una estrategia configurable.

El sistema también debe permitir simular lecturas para probar su funcionamiento sin depender inicialmente de sensores físicos.

## Resumen del backlog

| ID | Historia | MoSCoW | Puntos |
|---|---|---|---:|
| US-E01 | Crear una lectura de sensor | Must | 3 |
| US-E02 | Rechazar lecturas con datos inválidos | Must | 3 |
| US-E03 | Detectar temperatura anómala | Must | 3 |
| US-E04 | Detectar humedad anómala | Must | 3 |
| US-E05 | Configurar umbrales de anomalía | Must | 5 |
| US-E06 | Gestionar alertas mediante una estrategia | Must | 5 |
| US-E07 | Mostrar alertas en consola | Should | 2 |
| US-E08 | Guardar alertas en archivo | Should | 3 |
| US-E09 | Procesar lecturas de diez sensores | Must | 5 |
| US-E10 | Evitar alertas para lecturas normales | Must | 2 |
| US-E11 | Ejecutar ciclos de monitoreo cada 30 segundos | Should | 3 |
| US-E12 | Simular lecturas de los diez sensores | Could | 5 |

**Puntos totales del backlog: 42**

---

## US-E01 — Crear una lectura de sensor

**Historia de usuario**

Como operador de la bodega, quiero representar cada lectura con el identificador del sensor, la temperatura, la humedad y la fecha de captura, para conocer el estado ambiental reportado por cada dispositivo.

**MoSCoW:** Must  
**Puntos:** 3

### Criterios de aceptación

```gherkin
Escenario: Crear una lectura válida
  Dado que el sensor "SENSOR-01" reporta una temperatura de 25.5 °C
  Y reporta una humedad de 60 %
  Cuando se crea la lectura
  Entonces la lectura conserva el identificador "SENSOR-01"
  Y conserva la temperatura de 25.5 °C
  Y conserva la humedad de 60 %
  Y contiene una fecha y hora de captura
```

```gherkin
Escenario: Conservar una lectura sin modificaciones
  Dado que existe una lectura válida
  Cuando se intenta modificar su temperatura
  Entonces la operación es rechazada
  Y la lectura conserva sus valores originales
```

---

## US-E02 — Rechazar lecturas con datos inválidos

**Historia de usuario**

Como responsable del sistema, quiero rechazar lecturas con identificadores vacíos o valores ambientales inválidos, para evitar procesar información incorrecta.

**MoSCoW:** Must  
**Puntos:** 3

### Criterios de aceptación

```gherkin
Escenario: Rechazar una lectura sin identificador
  Dado que se recibe una temperatura de 25 °C
  Y una humedad de 50 %
  Y el identificador del sensor está vacío
  Cuando se intenta crear la lectura
  Entonces se genera un error de validación
```

```gherkin
Escenario: Rechazar una humedad menor que cero
  Dado que el sensor "SENSOR-01" reporta una humedad de -1 %
  Cuando se intenta crear la lectura
  Entonces se genera un error de validación
```

```gherkin
Escenario: Rechazar una humedad superior al rango permitido
  Dado que el sensor "SENSOR-01" reporta una humedad de 101 %
  Cuando se intenta crear la lectura
  Entonces se genera un error de validación
```

---

## US-E03 — Detectar temperatura anómala

**Historia de usuario**

Como operador de la bodega, quiero detectar temperaturas superiores al límite permitido, para actuar antes de que los productos almacenados resulten afectados.

**MoSCoW:** Must  
**Puntos:** 3

### Criterios de aceptación

```gherkin
Escenario: Detectar una temperatura superior al límite
  Dado que el umbral de temperatura es 35 °C
  Y existe una lectura con temperatura de 36 °C
  Cuando se analiza la lectura
  Entonces el resultado indica una anomalía de temperatura
```

```gherkin
Escenario: Aceptar una temperatura igual al límite
  Dado que el umbral de temperatura es 35 °C
  Y existe una lectura con temperatura de 35 °C
  Cuando se analiza la lectura
  Entonces el resultado no indica una anomalía de temperatura
```

---

## US-E04 — Detectar humedad anómala

**Historia de usuario**

Como operador de la bodega, quiero detectar niveles de humedad superiores al límite permitido, para prevenir daños asociados con condensación o exceso de humedad.

**MoSCoW:** Must  
**Puntos:** 3

### Criterios de aceptación

```gherkin
Escenario: Detectar una humedad superior al límite
  Dado que el umbral de humedad es 80 %
  Y existe una lectura con humedad de 81 %
  Cuando se analiza la lectura
  Entonces el resultado indica una anomalía de humedad
```

```gherkin
Escenario: Aceptar una humedad igual al límite
  Dado que el umbral de humedad es 80 %
  Y existe una lectura con humedad de 80 %
  Cuando se analiza la lectura
  Entonces el resultado no indica una anomalía de humedad
```

---

## US-E05 — Configurar umbrales de anomalía

**Historia de usuario**

Como administrador del sistema, quiero proporcionar los umbrales de temperatura y humedad al detector, para adaptar las reglas de anomalía sin modificar su implementación.

**MoSCoW:** Must  
**Puntos:** 5

### Criterios de aceptación

```gherkin
Escenario: Utilizar un umbral de temperatura personalizado
  Dado un detector configurado con una temperatura máxima de 30 °C
  Y existe una lectura con temperatura de 31 °C
  Cuando se analiza la lectura
  Entonces el resultado indica una anomalía de temperatura
```

```gherkin
Escenario: Utilizar un umbral de humedad personalizado
  Dado un detector configurado con una humedad máxima de 70 %
  Y existe una lectura con humedad de 71 %
  Cuando se analiza la lectura
  Entonces el resultado indica una anomalía de humedad
```

```gherkin
Escenario: Cambiar la configuración sin modificar el detector
  Dado un detector configurado con una temperatura máxima de 40 °C
  Y existe una lectura con temperatura de 36 °C
  Cuando se analiza la lectura
  Entonces el resultado no indica una anomalía de temperatura
```

---

## US-E06 — Gestionar alertas mediante una estrategia

**Historia de usuario**

Como responsable del sistema, quiero que el gestor de alertas utilice una estrategia inyectada, para cambiar la forma de notificación sin modificar el gestor.

**MoSCoW:** Must  
**Puntos:** 5

### Criterios de aceptación

```gherkin
Escenario: Enviar una alerta mediante la estrategia configurada
  Dado un gestor con una estrategia de alerta
  Y existe una anomalía de temperatura
  Cuando el gestor recibe la anomalía
  Entonces delega el envío a la estrategia configurada
```

```gherkin
Escenario: Sustituir la estrategia de alerta
  Dado que existe una estrategia de consola
  Y existe una estrategia de archivo
  Cuando cualquiera de las estrategias es proporcionada al gestor
  Entonces el gestor puede utilizarla sin modificar su implementación
```

---

## US-E07 — Mostrar alertas en consola

**Historia de usuario**

Como operador durante el desarrollo, quiero mostrar las alertas en consola, para observar inmediatamente las anomalías detectadas.

**MoSCoW:** Should  
**Puntos:** 2

### Criterios de aceptación

```gherkin
Escenario: Mostrar una alerta de temperatura
  Dado que existe una anomalía de temperatura para "SENSOR-01"
  Cuando la estrategia de consola envía la alerta
  Entonces la salida contiene el identificador "SENSOR-01"
  Y contiene el tipo de anomalía
  Y contiene el valor detectado
```

```gherkin
Escenario: Mostrar una alerta de humedad
  Dado que existe una anomalía de humedad para "SENSOR-02"
  Cuando la estrategia de consola envía la alerta
  Entonces la salida contiene el identificador "SENSOR-02"
  Y contiene el tipo de anomalía
  Y contiene el valor detectado
```

---

## US-E08 — Guardar alertas en archivo

**Historia de usuario**

Como responsable de auditoría, quiero guardar las alertas en un archivo, para conservar evidencia de las anomalías detectadas.

**MoSCoW:** Should  
**Puntos:** 3

### Criterios de aceptación

```gherkin
Escenario: Guardar una alerta en un archivo
  Dado un archivo de alertas vacío
  Y existe una anomalía de humedad para "SENSOR-02"
  Cuando la estrategia de archivo envía la alerta
  Entonces el archivo contiene el identificador "SENSOR-02"
  Y contiene el tipo de anomalía
  Y contiene el valor detectado
```

```gherkin
Escenario: Conservar alertas anteriores
  Dado un archivo que ya contiene una alerta
  Cuando se guarda una segunda alerta
  Entonces ambas alertas permanecen en el archivo
```

---

## US-E09 — Procesar lecturas de diez sensores

**Historia de usuario**

Como operador de la bodega, quiero procesar lecturas provenientes de diez sensores, para monitorear simultáneamente las diferentes áreas del almacén.

**MoSCoW:** Must  
**Puntos:** 5

### Criterios de aceptación

```gherkin
Escenario: Procesar una lectura de cada sensor
  Dado que existen diez sensores identificados de "SENSOR-01" a "SENSOR-10"
  Y cada sensor genera una lectura
  Cuando el sistema procesa las lecturas
  Entonces se analizan diez lecturas
  Y cada lectura conserva el identificador del sensor que la generó
```

```gherkin
Escenario: Procesar lecturas normales y anómalas
  Dado un conjunto de diez lecturas
  Y algunas lecturas superan los umbrales permitidos
  Cuando el sistema procesa el conjunto
  Entonces todas las lecturas son analizadas
  Y se generan alertas únicamente para las lecturas anómalas
```

---

## US-E10 — Evitar alertas para lecturas normales

**Historia de usuario**

Como operador de la bodega, quiero que las lecturas dentro de los límites permitidos no generen alertas, para evitar notificaciones innecesarias.

**MoSCoW:** Must  
**Puntos:** 2

### Criterios de aceptación

```gherkin
Escenario: No alertar una lectura normal
  Dado que el umbral de temperatura es 35 °C
  Y el umbral de humedad es 80 %
  Y existe una lectura con temperatura de 25 °C
  Y humedad de 60 %
  Cuando se analiza y gestiona la lectura
  Entonces no se envía ninguna alerta
```

```gherkin
Escenario: No alertar valores iguales a los límites
  Dado que existe una lectura con temperatura de 35 °C
  Y humedad de 80 %
  Cuando se analiza y gestiona la lectura
  Entonces no se envía ninguna alerta
```

---

## US-E11 — Ejecutar ciclos de monitoreo cada 30 segundos

**Historia de usuario**

Como operador de la bodega, quiero que el sistema ejecute ciclos de monitoreo cada 30 segundos, para recibir información ambiental de manera periódica.

**MoSCoW:** Should  
**Puntos:** 3

### Criterios de aceptación

```gherkin
Escenario: Configurar el intervalo de monitoreo
  Dado que el sistema realiza lecturas periódicas
  Cuando se configura el intervalo de captura
  Entonces el intervalo establecido es de 30 segundos
```

```gherkin
Escenario: Ejecutar un nuevo ciclo después del intervalo
  Dado que terminó un ciclo de monitoreo
  Cuando transcurren 30 segundos
  Entonces comienza un nuevo ciclo de lectura
```

```gherkin
Escenario: Permitir sustituir el intervalo durante las pruebas
  Dado que el sistema se ejecuta en un entorno de pruebas
  Cuando se proporciona un intervalo diferente
  Entonces el monitoreo utiliza el intervalo proporcionado
  Y las pruebas no necesitan esperar 30 segundos reales
```

---

## US-E12 — Simular lecturas de los diez sensores

**Historia de usuario**

Como desarrollador del sistema, quiero simular lecturas de temperatura y humedad para diez sensores, para probar el monitoreo sin depender de dispositivos físicos.

**MoSCoW:** Could  
**Puntos:** 5

### Criterios de aceptación

```gherkin
Escenario: Generar una lectura para cada sensor
  Dado un simulador configurado con diez identificadores
  Cuando se ejecuta un ciclo de simulación
  Entonces se generan diez lecturas
  Y cada lectura pertenece a un sensor diferente
```

```gherkin
Escenario: Generar valores ambientales realistas
  Dado un simulador configurado con valores medios de temperatura y humedad
  Cuando se generan las lecturas
  Entonces los valores presentan variaciones alrededor de los valores configurados
```

```gherkin
Escenario: Repetir una simulación de manera controlada
  Dado un simulador configurado con una semilla conocida
  Cuando se ejecutan dos simulaciones con la misma semilla
  Entonces ambas producen la misma secuencia de lecturas
```