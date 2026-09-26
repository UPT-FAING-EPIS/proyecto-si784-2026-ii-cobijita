# DespliegaUML
### Diagramador de componentes y despliegue de software con validación de reglas y generación de plan de despliegue

Integrantes: Patrick Rodriguez Cardenas (2022075751) · Nicole Rios Cohaila (2022075745)

---

## Aplicación

La herramienta está implementada y es ejecutable: **`app/index.html`** (doble clic,
sin instalación ni compilación). 64 pruebas en verde con `node app/tests/casos.js`.

- Manual de uso, catálogo de reglas y estructura: [`app/README.md`](app/README.md)
- Plan de pruebas, casos y métricas de calidad: [`calidad/Plan-de-Pruebas.md`](calidad/Plan-de-Pruebas.md)
- Informes del proyecto: `FD01-EPIS-Informe de Factibilidad-DespliegaUML.docx` ·
  `FD02-EPIS-Informe Vision-DespliegaUML.docx`

---

## 1. Título
DespliegaUML: herramienta para modelar diagramas de componentes y de
despliegue de software, validar su consistencia mediante reglas y
generar el plan de despliegue correspondiente.

## 2. Problema detallado (con fuentes)
El modelado de la arquitectura de software (diagramas de componentes y
de despliegue) suele hacerse con herramientas genéricas de dibujo que
no validan la coherencia de lo modelado: un componente puede quedar
conectado a algo inválido, un nodo de despliegue puede referenciar
artifacts inexistentes, o cerrarse ciclos no permitidos, sin que el
autor se percate hasta la etapa de implementación.

- Radio Uno 93.7 Tacna difunde de forma constante noticias sobre
  servicios y sistemas locales, lo que refleja la actividad de
  desarrollo de software en la región y la necesidad de buenas
  prácticas de despliegue. [Fuente: radiouno.pe]
- Según la metodología de ProblemHunt, un problema es válido cuando
  hay usuarios dispuestos a pagar por su solución; la validación
  automatizada de modelos arquitectónicos es un requerimiento recurrente
  en equipos que gestionan el despliegue de software. [Fuente: problemhunt.pro]
- El repositorio de la Facultad (GitHub UPT-FAING-EPIS) muestra
  antecedentes de proyectos de gestión y desarrollo, pero ninguno
  aborda la validación de diagramas de componentes y despliegue — este
  proyecto propone llenar ese vacío, usando lo previo como base, no
  como copia. [Fuente: github.com/UPT-FAING-EPIS]
- Renati (SUNEDU) se referencia como marco de investigación sobre
  digitalización y trazabilidad, según la guía de fuentes del curso.
  [Fuente: renati.sunedu.gob.pe]

## 3. Objetivos de investigación (medibles)
- OI1: Determinar en qué medida un conjunto de reglas de consistencia
  detecta errores de modelado en diagramas de componentes y despliegue.
  > Medible: pruebas demuestran la detección de cada clase de error
    definida (conexión inválida, artifact faltante, ciclo no permitido).
- OI2: Evaluar la claridad del plan de despliegue generado a partir del
  modelo validado.
  > Medible: el plan generado cubre todos los nodos y artifacts del
    modelo sin referencias pendientes.

## 4. Objetivos de solución (alcance del equipo)
- OS1: Implementar un editor de diagramas de componentes y de despliegue
  que permita definir elementos y relaciones.
  > Medible: se puede crear, editar y eliminar cada tipo de elemento
    del modelo.
- OS2: Implementar un motor de validación de reglas de consistencia.
  > Medible: cada regla definida detecta los casos de prueba
    correspondientes (positivos y negativos).
- OS3: Generar el plan de despliegue a partir del modelo validado.
  > Medible: el plan se produce para los modelos válidos y se omite
    (con reporte de errores) para los inválidos.
- OS4: Desarrollar la lógica del modelo y la validación con pruebas
  automatizadas de sus reglas.
  > Medible: reglas de validación cubiertas por pruebas que pasan.
