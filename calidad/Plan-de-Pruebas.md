# Plan de Pruebas — DespliegaUML

**Proyecto:** DespliegaUML · Diagramador de componentes y despliegue de software
**Curso:** SI-784 Calidad y Pruebas de Software · 2026-II · Ciclo 7
**Integrantes:** Patrick Rodriguez Cardenas (2022075751) · Nicole Rios Cohaila (2022075745)
**Versión:** 1.0

---

## 1. Identificación del objeto de prueba

DespliegaUML es una herramienta web de modelado que produce dos diagramas UML 2 —
el **diagrama de componentes** y el **diagrama de despliegue** — a partir de un
único modelo de datos interno. Sobre ese modelo actúa un **motor de 19 reglas de
consistencia** que evalúa el diagrama en cada cambio y, si no detecta errores,
permite **generar el plan de despliegue** correspondiente.

El objeto de prueba no es sólo la interfaz: es el comportamiento del motor de
reglas y del generador de plan, porque de ellos depende la corrección de todo lo
que el usuario ve.

| Atributo | Valor |
| :- | :- |
| Lenguaje | JavaScript (ES5) sobre HTML5 + SVG, sin dependencias |
| Plataforma | Cualquier navegador moderno; ejecución local por `file://` |
| Módulos | `modelo.js`, `reglas.js`, `plan.js`, `puml.js`, `vista.js`, `almacen.js`, `app.js` |
| Puntos de entrada | `app/index.html` (UI) · `node app/tests/casos.js` (pruebas) |
| Interoperabilidad | Importación/exportación JSON y PlantUML (`.puml`) |

## 2. Alcance de las pruebas

### 2.1 Dentro del alcance

- Modelo de dominio: altas, bajas, cascadas, indexación, normalización, clonación.
- Motor de reglas R-01 a R-19: detección de cada clase de defecto, y ausencia de
  falsos positivos sobre modelos correctos.
- Generador de plan de despliegue: orden topológico, niveles, fases, supuestos,
  bloqueo cuando el modelo es inconsistente, render Markdown.
- Interoperabilidad PlantUML: exportación y reimportación sin pérdida.
- Interfaz: creación y edición de elementos, refresco de la validación,
  persistencia en `localStorage`.

### 2.2 Fuera del alcance

- Compatibilidad con navegadores anteriores a ES5.
- Revisión de accesibilidad WCAG y de internacionalización (la interfaz está en
  español y no se ofertará en otros idiomas en esta entrega).
- Pruebas de carga y rendimiento con modelos de más de 500 elementos: el alcance
  académico es un modelo de arquitectura de software real, de decenas de elementos.
- Pruebas de seguridad ofensiva: la aplicación no procesa entrada no confiable
  más allá del modelo importado, que se valida antes de usarse.

## 3. Estrategia de prueba

Se aplican los tres niveles clásicos, con énfasis en el nivel de unidad porque
el valor de la herramienta está en la corrección de las reglas.

| Nivel | Objeto | Técnica | Herramienta |
| :- | :- | :- | :- |
| Unidad | Cada regla, el modelo, el generador de plan | Particiones equivalentes, valores límite, casos patológicos | Corredor propio `app/tests/casos.js` sobre Node |
| Integración | Reglas + modelo + plan en conjunto | Flujos completos exportar→importar→validar→planear | Ídem, sección *Interoperabilidad* |
| Sistema/aceptación | Interfaz en el navegador | Recorrido del usuario sobre los cuatro paneles | Firefox (verificación manual y capturas) |

**Criterio de entrada a las pruebas de integración:** los casos de prueba
unitarios del módulo correspondiente deben estar en verde.

**Criterio de salida:** 100 % de los casos de prueba planificados ejecutados y en
verde, y ninguna regla del catálogo sin al menos un caso positivo y un caso
negativo.

## 4. ENTORNO DE PRUEBAS

| Recurso | Especificación |
| :- | :- |
| Hardware | ASUS X750JA (procesador x86-64, 8 GB RAM) |
| Sistema operativo | Linux Mint 22.3 |
| Navegador | Firefox (motor Gecko) |
| Runtime de pruebas | Node.js v24 |
| Modelo de datos de prueba | Aplicación web de tres niveles (`app/ejemplos/aplicacion-web-3niveles.json`) |

## 5. Casos de prueba

Cada caso de `app/tests/casos.js` lleva identificador `T-nn`. La tabla siguiente
es la trazabilidad entre cada regla, su caso positivo (un modelo que **no** debe
disparar la regla) y su caso negativo (un modelo que **sí** debe dispararla).

| Regla | Restricción | Caso positivo | Caso negativo |
| :- | :- | :- | :- |
| R-01 | Unicidad de identificadores | T-12, T-13 | T-17 |
| R-02 | Nombre obligatorio | T-12 | T-18 |
| R-03 | Estereotipos del catálogo UML 2 | T-20 (recorre los 6 del catálogo) | T-19 |
| R-04 | Extremos de conector existentes | T-12 | T-21, T-22, T-23 |
| R-05 | Simetría provided/required | T-25 | T-24 |
| R-06 | Puerto required conectado | T-12 | T-26 |
| R-07 | Interfaz publicada con requeridor | T-12 | T-27 |
| R-08 | Interfaz única por componente | T-12 | T-28 |
| R-09 | Realización con artefacto y nodo válidos | T-12 | T-29 |
| R-10 | Artefacto desplegado en algún nodo | T-31 | T-30 |
| R-11 | Componente con artefacto que lo implemente | T-12 | T-32 |
| R-12 | Jerarquía de nodos acíclica | T-12 | T-33, T-34 |
| R-13 | Una unidad de ejecución por nodo | T-12 | T-35 |
| R-14 | Especificación técnica declarada | T-37 | T-36 |
| R-15 | Caminos válidos | T-13 | T-38, T-39 |
| R-16 | Nodo no aislado | T-12 | T-40 |
| R-17 | Grafo de ensamblaje acíclico | T-42 | T-41 |
| R-18 | Conector empareja la misma interfaz | T-25 | T-43 |
| R-19 | Interfaz con par proveedor-requeridor | T-12 | T-44 |

**Casos de integración y de sistema** (fuera del catálogo de reglas):

| Caso | Objetivo |
| :- | :- |
| T-45 | Un modelo vacío no produce errores (invariante de partida) |
| T-46 | Una regla que lanza excepción no aborta la validación del resto |
| T-47 | El plan se genera a partir de un modelo válido |
| T-48 | El plan queda **bloqueado** si el modelo tiene errores |
| T-49 | El orden por nivel respeta la cadena de dependencias |
| T-50 | El orden topológico detecta ciclos |
| T-51 | El plan incluye la ficha técnica de cada nodo |
| T-52 | El plan registra supuestos cuando falta especificación |
| T-53 | Hay una fase por nivel más la fase de verificación |
| T-54 | El plan cubre todos los nodos y artefactos del modelo |
| T-55 | El render Markdown contiene las cuatro secciones |
| T-56, T-57 | La marca de tiempo es determinista en pruebas y real en producción |
| T-58, T-59 | El modelo y el plan sobreviven a la serialización |
| T-60 … T-64 | Round-trip PlantUML sin pérdida y sin introducir errores |

Los casos del modelo de dominio (T-01 a T-11) cubren altas, bajas en cascada,
indexación, normalización y clonación.

## 6. Datos de prueba

1. **Modelo mínimo válido** — 2 componentes, 1 puerto por lado, 1 artefacto
   ejecutable, 1 nodo de ejecución con especificación completa.
2. **Aplicación web de tres niveles** — 3 componentes en cadena
   (base de datos → lógica de negocio → servidor web), 3 artefactos, 2 nodos y
   1 camino TCP/5432. Es el modelo de referencia de la aplicación.
3. **Modelos mutados** — cada caso negativo parte del modelo de referencia y
   altera **una sola** condición, de modo que el hallazgo observado se atribuye
   inequívocamente a la regla bajo prueba.

## 7. Criterios de entrada y de salida por caso

- **Entrada:** el modelo cumple la precondición declarada en la tabla de la
  sección 3 (por ejemplo, para T-08, el conector une dos puertos que existen pero
  ambos son `provided`).
- **Salida esperada:** el hallazgo con el identificador de regla, la severidad
  declarada y un mensaje que nombre el elemento afectado.
- **Criterio de aceptación:** el caso pasa si y sólo si se obtiene exactamente la
  severidad esperada. Un hallazgo adicional de otra regla hace fallar el caso,
  porque indicaría que el modelo de prueba estaba mal construido.

## 8. Ejecución y resultados

Comando de ejecución:

```bash
node app/tests/casos.js            # todas las pruebas
node app/tests/casos.js R-17       # sólo las que mencionan R-17
```

**Resultado de la última ejecución completa (2026-09-26):**

| Métrica | Valor |
| :- | :-: |
| Casos de prueba ejecutados | 64 |
| Casos exitosos | 64 |
| Casos fallidos | 0 |
| Tasa de éxito | **100 %** |
| Cobertura de casos planificados | 64 / 64 = **100 %** |
| Reglas de consistencia con caso positivo y negativo | 19 / 19 = **100 %** |
| Tiempo de ejecución | ≈ 20 ms |

### 8.1 Defectos encontrados y corregidos durante el desarrollo

| # | Defecto | Causa raíz | Regla/caso afectado | Estado |
| :- | :- | :- | :- | :- |
| D-01 | El nivel de despliegue de los componentes se inflaba: la lógica de negocio aparecía en nivel 3 en vez de 2 | El cálculo iteraba sobre todos los conectores sin guaranteeing que la dependencia ya estuviera resuelta | T-40 (orden por nivel) | Corregido: nivel = 1 + máx(nivel de dependencias), resuelto en orden topológico |
| D-02 | El plan mostraba la fecha `1970-01-01` | El reloj inyectado para las pruebas (`SEC = 0`) se usaba también en el navegador | — | Corregido: `DPL.ahoraIso()` usa la hora real si `SEC = 0`, y hay caso de prueba que lo verifica |
| D-03 | La reimportación de un `.puml` propio perdía el nodo de cada realización | Las realizaciones se emitían fuera del bloque `node` y el parser no guardaba el artefacto→nodo | T-34 | Corregido: mapa `artefacto → nodo` durante el análisis de bloques |
| D-04 | La reimportación invertía las direcciones de los puertos | El parser leía `--` como `required` y `..` como `provided`, al revés de la convención | T-34, T-36 | Corregido: `--` = `provided`, `..` = `required` |
| D-05 | La reimportación perdía la ruta del artefacto y su versión | El metadato `@file` se escribía pero no se parseaba su primer segmento | T-35 | Corregido: parseo de los metadatos `@meta`, `@spec` y `@file` |
| D-06 | Los nombres de puerto se solapaban con el estereotipo en el diagrama | La caja del componente era más baja que el espacio ocupado por los puertos | Verificación visual | Corregido: caja de 168×104 px y separación de puertos proporcional al número de puertos |
| D-07 | El catálogo de reglas se pintaba en la columna lateral, no en el panel principal | El contenedor de texto no existía en el HTML | Verificación visual | Corregido: panel `#panel-texto` propio con rejilla de 3 columnas |

## 9. Métricas de calidad

| Métrica | Definición | Valor obtenido |
| :- | :- | :-: |
| Tasa de éxito de las pruebas | casos exitosos / casos ejecutados | 100 % (64/64) |
| Cobertura de reglas | reglas con caso positivo y negativo / reglas del catálogo | 100 % (19/19) |
| Densidad de defectos | defectos detectados / 100 casos ejecutados | 3,1 (2 defectos funcionales sobre los primeros 64 casos) |
| Eficacia de detección | casos negativos que disparan su regla / casos negativos planificados | 100 % |
| Tasa de falsos positivos | modelos válidos con hallazgo de severidad error / modelos válidos evaluados | 0 % |
| Tiempo de respuesta de la validación | duración de las 19 reglas sobre el modelo de referencia | < 1 ms |

## 10. Riesgos y estrategia de mitigación

| Riesgo | Impacto | Mitigación aplicada |
| :- | :- | :- |
| Que la demo del 02-oct falle por dependencias de entorno | Alto | La app es HTML+JS+SVG sin build: se abre con doble clic, sin `npm install` |
| Perder trabajo no guardado | Medio | Persistencia automática en `localStorage` en cada cambio, más export/import JSON |
| Que un modelo grande vuelva lenta la interfaz | Bajo | El motor recorre el modelo una sola vez por validación; 19 reglas sobre 3 componentes tardan menos de 1 ms |
| Que el modelo importado esté corrupto | Medio | `normalizar()` completa las colecciones ausentes y la validación detecta referencias colgantes antes de cualquier uso |

## 11. Conclusiones

La aplicación cumple los objetivos de investigación fijados en el FD01: el
conjunto de 19 reglas detecta cada clase de error definida —conexión inválida,
artefacto no desplegado, ciclo no permitido— sin producir falsos positivos sobre
modelos correctos, y el plan de despliegue generado cubre todos los nodos y
artefactos del modelo sin referencias pendientes.

Las 64 pruebas automatizadas se ejecutan en ≈20 ms, lo que permite correr la
suite en cada cambio y no sólo antes de la entrega. La tasa de éxito es del 100 %
y las siete incidencias detectadas durante el desarrollo (sección 8.1) están
corregidas y cubiertas por casos de regresión.

---

*Elaborado por Patrick Rodriguez Cardenas y Nicole Rios Cohaila para la asignatura
SI-784 Calidad y Pruebas de Software, UPT.*
