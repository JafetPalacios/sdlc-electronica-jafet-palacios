## Semblanza
Mi nombre es Jafet de los Angeles Palacios Guatzozón
Actualmente, soy estudiante de último semestre de Ingeniería Biomédica y pasante en el laboratorio de Robótica Médica y Bioseñales del Instituto Politecnico Nacional (IPN). Previamente, inicié estudiando Instrumentación Electrónica pero cambié de carrera en 2023. 
Tengo experiencia en electrónica y programación. He trabajado con microcontroladores, sensores, comunicación de datos, desarrollo de software y lenguajes como C, C#, Python y un poco de Java. También he participado en proyectos relacionados con instrumentación biomédica, análisis de señales, sistemas IoT y visualización 3D. 
Ademas de mi experiencia técnica, he desarrollado habilidades de liderazgo y organización como presidenta de la Rama Estudiantil IEEE FIE-UV, he participando en la coordinación de eventos académicos, impartido talleres, concursos tecnológicos y actividades de divulgación científica. 
Del programa EDSIA espero fortalecer mis conocimientos en programación, pruebas, documentación y desarrollo estructurado de proyectos. Mi objetivo es mejorar mi capacidad para crear código más confiable, seguro y eficientes, además de adquirir experiencia práctica que pueda aplicar en proyectos profesionales y de investigación.



## Reflexión sobre SOLID

Durante esta semana aplicamos los principios SOLID al dominio de sensores y al desarrollo de un driver UART modernizado.

S - El principio de responsabilidad única permitió separar la configuración, el procesamiento de mensajes, los parsers y la persistencia en clases independientes. Esto facilita comprender, probar y modificar cada componente sin afectar responsabilidades no relacionadas.

O - El principio abierto/cerrado se aplicó mediante la clase abstracta `MessageParser`. El dispositivo UART puede trabajar con diferentes protocolos, como Modbus y NMEA, sin modificar la implementación de `UartDevice`. Para agregar un protocolo nuevo solamente sería necesario crear otro parser que implemente el método `parse()`.

L - La sustitución de Liskov se cumple porque `ModbusParser` y `NMEAParser` pueden utilizarse donde se espera un `MessageParser`. Ambos respetan el mismo contrato de entrada y salida.

I - La segregación de interfaces evita que las clases dependan de operaciones que no necesitan. En el driver, el dispositivo únicamente requiere que el parser proporcione el método `parse()`.

D - La inversión de dependencias se aplicó al inyectar la configuración y el parser en `UartDevice`. La clase no crea internamente un parser concreto, por lo que depende de una abstracción y no directamente de Modbus o NMEA.

La principal ventaja observada es que el sistema resulta más fácil de probar y extender. Cada clase puede validarse de forma aislada y es posible incorporar nuevos protocolos o mecanismos de persistencia con cambios mínimos.
