# Traza tu Suerte
### Sistema de asignación imparcial con auditoría criptográfica verificable

Integrantes: Patrick Rodriguez Cardenas (2022075751) · Nicole Rios Cohaila (2022075745)

---

## 1. Título
Traza tu Suerte: sistema de asignación imparcial de cupos y resultados
con auditoría criptográfica verificable mediante cadena de hash.

## 2. Problema detallado (con fuentes)
Las rifas, sorteos y asignación de cupos (becas, stands, beneficencia)
en instituciones y eventos de Tacna se ejecutan habitualmente de forma
opaca: el resultado se comunica sin evidencia que permita a los
participantes verificar que no fue manipulado ni predeterminado.

- Radio Uno 93.7 Tacna difunde de forma constante eventos de
  beneficencia y rifas en la región, lo que evidencia que la práctica
  es frecuente y masiva, pero ninguna ofrece un medio de auditoría
  ciudadana. [Fuente: radiouno.pe]
- Según la metodología de ProblemHunt, un problema es válido cuando
  hay usuarios dispuestos a pagar por su solución; la transparencia en
  procesos aleatorios es un requerimiento recurrente en organismos que
  manejan recursos concursables. [Fuente: problemhunt.pro]
- El repositorio de la Facultad (GitHub UPT-FAING-EPIS) muestra
  antecedentes de proyectos de gestión, pero ninguno aborda la
  verificabilidad criptográfica del resultado — este proyecto propone
  llenar ese vacío, usando lo previo como base, no como copia.
  [Fuente: github.com/UPT-FAING-EPIS]
- Renati (SUNEDU) se referencia como marco de investigación sobre
  digitalización y trazabilidad, según la guía de fuentes del curso.
  [Fuente: renati.sunedu.gob.pe]

## 3. Objetivos de investigación (medibles)
- OI1: Determinar en qué medida una cadena de hash (hash-chain)
  garantiza la inmutabilidad y trazabilidad de cada asignación.
  > Medible: cada asignación sellada con el hash de la anterior;
    pruebas demuestran que alterar un registro invalida la cadena.
- OI2: Evaluar la imparcialidad del generador de números aleatorios
  utilizado.
  > Medible: prueba sobre al menos 1000 ejecuciones sin sesgo
    detectable en la distribución de resultados.

## 4. Objetivos de solución (medibles, alcance del equipo)
- OS1: Implementar un módulo de sellado hash-chain que registre
  semilla, timestamp y hash del registro anterior.
  > Medible: 100% de asignaciones selladas y verificables.
- OS2: Implementar una función de verificación que permita a cualquier
  persona comprobar un resultado a partir de los datos sellados.
  > Medible: verificación funcional para los casos de prueba definidos.
- OS3: Desarrollar la lógica de asignación con pruebas automatizadas
  de sus reglas.
  > Medible: reglas de asignación cubiertas por pruebas que pasan.
