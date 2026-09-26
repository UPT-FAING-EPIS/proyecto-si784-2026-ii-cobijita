/* =====================================================================
   DespliegaUML · tools/generar-documentacion.js
   Genera los artefactos de documentación técnica a partir del modelo de
   ejemplo y de las reglas, para que la CI los publique en cada commit.

   Artefactos generados:
     doc/diagrama-componentes.puml
     doc/diagrama-despliegue.puml
     doc/diagrama-componentes.svg
     doc/diagrama-despliegue.svg
     doc/plan-despliegue.md
     doc/catalogo-reglas.md
     doc/informe-calidad.md
     doc/manual-tecnico.md

   Uso:  node tools/generar-documentacion.js
   ===================================================================== */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const RAIZ = path.join(__dirname, '..');
const SRC = path.join(RAIZ, 'app', 'src');
const SALIDA = path.join(RAIZ, 'doc');

['modelo.js', 'reglas.js', 'plan.js', 'pruebas.js', 'puml.js'].forEach((f) => {
  vm.runInThisContext(fs.readFileSync(path.join(SRC, f), 'utf8'), { filename: f });
});
const DPL = globalThis.DPL;

fs.mkdirSync(SALIDA, { recursive: true });

/* --------------------------------------------------------------------
   1. Modelo de ejemplo (fuente única de verdad para los diagramas)
   -------------------------------------------------------------------- */
const EJEMPLO = path.join(RAIZ, 'app', 'ejemplos', 'aplicacion-web-3niveles.json');
const modelo = DPL.Modelo.normalizar(JSON.parse(fs.readFileSync(EJEMPLO, 'utf8')));

const validacion = DPL.validar(modelo);
const plan = DPL.generarPlan(modelo, { validacion });

/* --------------------------------------------------------------------
   2. Diagramas PlantUML
   -------------------------------------------------------------------- */
/* Cada .puml es autocontenido: se puede pegar en plantuml.com para obtener
   la imagen oficial de UML. */
fs.writeFileSync(path.join(SALIDA, 'diagrama-componentes.puml'), soloComponentes(modelo));
fs.writeFileSync(path.join(SALIDA, 'diagrama-despliegue.puml'), soloDespliegue(modelo));

function soloComponentes(m) {
  const L = [];
  L.push('@startuml ' + m.nombre.replace(/\s+/g, '_') + '_componentes');
  L.push('skinparam componentStyle rectangle');
  L.push('title ' + m.nombre + ' — Diagrama de componentes (v' + m.version + ')');
  L.push('');
  m.componentes.forEach((c) => {
    const clase = c.estereotipo === 'interface' ? 'interface'
      : c.estereotipo === 'database' ? 'database' : 'component';
    L.push('  ' + clase + ' "' + c.nombre + '" as ' + c.id + ' <<' + c.estereotipo + '>> {');
    c.puertos.forEach((p) => {
      /* PlantUML acepta `port <nombre>` dentro del bloque; la interfaz se
         declara aparte porque la forma "X" : Interfaz no es válida. */
      L.push('    port ' + p.id + '_' + slug(p.nombre));
    });
    L.push('  }');
    /* interfaces publicadas por el componente, para que se vean en el diagrama */
    c.puertos.filter((p) => p.direccion === 'provided').forEach((p) => {
      L.push('  interface "' + p.interfaz + '" as ' + c.id + '_' + p.id.toUpperCase() + '_IF');
    });
  });
  L.push('');
  m.conectores.forEach((k) => {
    const d = k.desde || {}; const h = k.hacia || {};
    L.push('  ' + d.componente + ' --> ' + h.componente + ' : ' + esc(k.contrato));
  });
  L.push('');
  L.push('legend top left');
  L.push('|= Componente |= Interfaz publicada |= Interfaz requerida |');
  m.componentes.forEach((c) => {
    const pub = c.puertos.filter((p) => p.direccion === 'provided')
      .map((p) => p.nombre + ' : ' + p.interfaz).join(' · ') || '—';
    const req = c.puertos.filter((p) => p.direccion === 'required')
      .map((p) => p.nombre + ' : ' + p.interfaz).join(' · ') || '—';
    L.push('| ' + c.id + ' ' + c.nombre + ' | ' + pub + ' | ' + req + ' |');
  });
  L.push('endlegend');
  L.push('');
  L.push('@enduml');
  return L.join('\n') + '\n';
}

function slug(s) {
  return String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_|_$/g, '').toLowerCase();
}

function esc(s) {
  return String(s).replace(/"/g, "'").replace(/[\r\n]+/g, ' ').trim();
}

function soloDespliegue(m) {
  const L = [];
  L.push('@startuml ' + m.nombre.replace(/\s+/g, '_') + '_despliegue');
  L.push('title ' + m.nombre + ' — Diagrama de despliegue (v' + m.version + ')');
  L.push('');
  m.nodos.forEach((n) => {
    const marca = n.estereotipo === 'cloudRegion' ? 'cloud' : 'node';
    L.push('  ' + marca + ' "' + n.nombre + '" as ' + n.id + ' <<' + n.estereotipo + '>> {');
    m.realizaciones.filter((r) => r.nodo === n.id).forEach((r) => {
      const a = DPL.Modelo.buscarArtefacto(m, r.artefacto);
      if (a) L.push('    artifact "' + a.nombre + '" as ' + a.id + ' <<' + a.tipo + '>>');
    });
    L.push('  }');
  });
  L.push('');
  m.realizaciones.forEach((r) => {
    const a = DPL.Modelo.buscarArtefacto(m, r.artefacto);
    if (a && a.componente) L.push('  ' + a.id + ' ..> ' + a.componente + ' : realiza');
  });
  m.caminos.forEach((c) => {
    L.push('  ' + c.a + ' --> ' + c.b + ' : ' + c.protocolo +
      (c.puerto ? '/' + c.puerto : ''));
  });
  L.push('');
  L.push('@enduml');
  return L.join('\n') + '\n';
}

/* --------------------------------------------------------------------
   3. Plan de despliegue
   -------------------------------------------------------------------- */
fs.writeFileSync(path.join(SALIDA, 'plan-despliegue.md'),
  DPL.planDeDespliegue.aMarkdown(plan));

/* --------------------------------------------------------------------
   4. Catálogo de reglas
   -------------------------------------------------------------------- */
const catalogo = [];
catalogo.push('# Catálogo de reglas de consistencia — DespliegaUML');
catalogo.push('');
catalogo.push('> Generado automáticamente desde `app/src/reglas.js`.');
catalogo.push('> No editar a mano: editar las reglas y volver a ejecutar la generación.');
catalogo.push('');
catalogo.push('| Regla | Nombre | Severidad máxima | Fundamento |');
catalogo.push('| :- | :- | :- | :- |');
DPL.REGLAS.forEach((r) => {
  catalogo.push('| **' + r.id + '** | ' + r.nombre + ' | `' +
    severidadMax(r.id) + '` | ' + r.razon + ' |');
});
catalogo.push('');
catalogo.push('**Regla de decisión:** el plan de despliegue se genera únicamente');
catalogo.push('cuando el modelo no produce ningún hallazgo de severidad `error`.');
catalogo.push('');
fs.writeFileSync(path.join(SALIDA, 'catalogo-reglas.md'), catalogo.join('\n'));

function severidadMax(id) {
  const c = {};
  validacion.hallazgos.forEach((h) => {
    if (h.regla === id) c[h.severidad] = (c[h.severidad] || 0) + 1;
  });
  if (c.error) return 'error';
  if (c.warning) return 'warning';
  if (c.info) return 'info';
  return '— (sin hallazgos)';
}

/* --------------------------------------------------------------------
   5. Informe de calidad
   -------------------------------------------------------------------- */
const { execFileSync } = require('child_process');
let pruebas = { total: 0, exitosos: 0, fallidos: 0, fallos: [], duracionMs: 0 };
try {
  const salida = execFileSync('node', [path.join(RAIZ, 'app', 'tests', 'casos.js')],
    { encoding: 'utf8' });
  const mTotal = salida.match(/Casos: (\d+) · exitosos: (\d+) · fallidos: (\d+).*?· (\d+) ms/);
  if (mTotal) {
    pruebas.total = +mTotal[1];
    pruebas.exitosos = +mTotal[2];
    pruebas.fallidos = +mTotal[3];
    pruebas.duracionMs = +mTotal[4];
  }
} catch (e) {
  pruebas.fallidos = -1;
}

const inf = [];
inf.push('# Informe de calidad — DespliegaUML');
inf.push('');
inf.push('> Generado automáticamente por `tools/generar-documentacion.js` en cada');
inf.push('> ejecución de la integración continua.');
inf.push('');
inf.push('## 1. Resumen de la validación del modelo de referencia');
inf.push('');
inf.push('| Métrica | Valor |');
inf.push('| :- | :-: |');
inf.push('| Errores | ' + validacion.resumen.error + ' |');
inf.push('| Advertencias | ' + validacion.resumen.warning + ' |');
inf.push('| Avisos | ' + validacion.resumen.info + ' |');
inf.push('| Reglas evaluadas | ' + validacion.reglasEvaluadas + ' |');
inf.push('| Modelo válido | ' + (validacion.valido ? 'sí' : 'no') + ' |');
inf.push('| Duración de la validación | ' + validacion.duracionMs + ' ms |');
inf.push('');
inf.push('## 2. Suite de pruebas automatizadas');
inf.push('');
if (pruebas.total) {
  inf.push('| Métrica | Valor |');
  inf.push('| :- | :-: |');
  inf.push('| Casos ejecutados | ' + pruebas.total + ' |');
  inf.push('| Casos exitosos | ' + pruebas.exitosos + ' |');
  inf.push('| Casos fallidos | ' + pruebas.fallidos + ' |');
  inf.push('| Tasa de éxito | ' +
    (pruebas.total ? ((pruebas.exitosos / pruebas.total) * 100).toFixed(1) : 0) + ' % |');
  inf.push('| Tiempo de ejecución | ' + pruebas.duracionMs + ' ms |');
  inf.push('');
  if (pruebas.fallidos !== 0) {
    inf.push('> **Atención:** la suite de pruebas tiene fallos. Revise el resultado de');
    inf.push('> la ejecución antes de publicar el despliegue.');
    inf.push('');
  }
} else {
  inf.push('No se pudo ejecutar la suite de pruebas al generar este informe.');
  inf.push('');
}
inf.push('## 3. Hallazgos del modelo de referencia');
inf.push('');
if (!validacion.hallazgos.length) {
  inf.push('El modelo de referencia no produce ningún hallazgo: cumple las ' +
    validacion.reglasEvaluadas + ' reglas del catálogo.');
} else {
  inf.push('| Severidad | Regla | Mensaje |');
  inf.push('| :- | :- | :- |');
  validacion.hallazgos.forEach((h) => {
    inf.push('| `' + h.severidad + '` | ' + h.regla + ' | ' + h.mensaje + ' |');
  });
}
inf.push('');
inf.push('## 4. Trazabilidad de las pruebas con el plan de pruebas');
inf.push('');
inf.push('La matriz completa regla → caso de prueba (positivo y negativo) está en');
inf.push('[`calidad/Plan-de-Pruebas.md`](../calidad/Plan-de-Pruebas.md).');
inf.push('');
fs.writeFileSync(path.join(SALIDA, 'informe-calidad.md'), inf.join('\n'));

/* --------------------------------------------------------------------
   6. Manual técnico
   -------------------------------------------------------------------- */
const man = [];
man.push('# Manual técnico — DespliegaUML');
man.push('');
man.push('> Generado automáticamente. Para editarlo, editar `tools/generar-documentacion.js`.');
man.push('');
man.push('## 1. Descripción del producto');
man.push('');
man.push('DespliegaUML es una aplicación web que permite modelar el diagrama de');
man.push('componentes y el diagrama de despliegue de un sistema de software, validar');
man.push('la consistencia del modelo mediante un catálogo de ' +
  DPL.REGLAS.length + ' reglas y generar automáticamente el plan de despliegue.');
man.push('');
man.push('No requiere instalación ni compilación: se abre `app/index.html` en');
man.push('cualquier navegador moderno.');
man.push('');
man.push('## 2. Arquitectura del sistema');
man.push('');
man.push('La aplicación separa el modelo de dominio de su representación, de modo');
man.push('que la lógica de validación es independiente del navegador y puede probarse');
man.push('en Node.js.');
man.push('');
man.push('| Módulo | Responsabilidad | Dependencias |');
man.push('| :- | :- | :- |');
man.push('| `modelo.js` | Modelo de dominio: componentes, puertos, conectores, nodos, artefactos, realizaciones y caminos. Índices y bajas en cascada. | ninguna |');
man.push('| `reglas.js` | Catálogo de ' + DPL.REGLAS.length + ' reglas de consistencia y motor que las evalúa sobre el modelo. | `modelo.js` |');
man.push('| `plan.js` | Orden topológico, niveles de dependencia, fases de despliegue y render a Markdown. | `modelo.js`, `reglas.js` |');
man.push('| `puml.js` | Exportación e importación de PlantUML. | `modelo.js` |');
man.push('| `vista.js` | Render de los dos diagramas en SVG. | `modelo.js` |');
man.push('| `almacen.js` | Persistencia en `localStorage` y descarga de archivos. | `modelo.js` |');
man.push('| `app.js` | Controlador de la interfaz: herramientas, inspector, validación en vivo. | todos los anteriores |');
man.push('| `pruebas.js` | Micro-corredor de pruebas y fábricas de modelos de prueba. | ninguna |');
man.push('');
man.push('## 3. Modelo de datos');
man.push('');
man.push('| Colección | Contenido | Identificador |');
man.push('| :- | :- | :- |');
man.push('| `componentes` | Componentes UML con sus puertos | `C1, C2, …` |');
man.push('| `conectores` | Uniones entre un puerto `provided` y uno `required` | `K1, K2, …` |');
man.push('| `nodos` | Nodos de despliegue con jerarquía y ficha técnica | `N1, N2, …` |');
man.push('| `artefactos` | Artefactos desplegables | `A1, A2, …` |');
man.push('| `realizaciones` | Unión artefacto → nodo | `R1, R2, …` |');
man.push('| `caminos` | Comunicación entre nodos | `CP1, CP2, …` |');
man.push('');
man.push('## 4. Uso');
man.push('');
man.push('1. **Diagrama de componentes.** Con «+ Componente» se hace clic en el');
man.push('   lienzo; en el inspector se asignan nombre y estereotipo. Cada puerto es');
man.push('   una interfaz que el componente publica (`provided`) o requiere');
man.push('   (`required`). El nombre de la interfaz empareja ambos extremos.');
man.push('2. **Conectar.** La herramienta «→ Conector» pide el componente que');
man.push('   publica la interfaz y luego el que la requiere.');
man.push('3. **Diagrama de despliegue.** Se crean nodos, se les asigna SO, CPU y');
man.push('   memoria, y se crean artefactos que se *realizan* dentro de un nodo.');
man.push('4. **Validar.** El panel lateral reevalúa las ' + DPL.REGLAS.length +
  ' reglas en cada cambio y marca en rojo lo que incumple.');
man.push('5. **Generar el plan.** Con 0 errores, «Generar plan de despliegue»');
man.push('   produce el plan completo, copiable o descargable en Markdown.');
man.push('');
man.push('## 5. Catálogo de reglas');
man.push('');
man.push('El catálogo completo está en [`doc/catalogo-reglas.md`](catalogo-reglas.md).');
man.push('');
man.push('| Regla | Nombre |');
man.push('| :- | :- |');
DPL.REGLAS.forEach((r) => {
  man.push('| ' + r.id + ' | ' + r.nombre + ' |');
});
man.push('');
man.push('## 6. Pruebas');
man.push('');
man.push('```bash');
man.push('node app/tests/casos.js              # suite completa');
man.push('node app/tests/casos.js R-17         # sólo los casos que mencionan R-17');
man.push('node tools/generar-documentacion.js   # regenera los artefactos de doc/');
man.push('```');
man.push('');
man.push('## 7. Despliegue');
man.push('');
man.push('La aplicación es estática: se publica tal cual en cualquier servicio de');
man.push('hosting. La automatización de integración continua está en');
man.push('`.github/workflows/`, y el despliegue en GitHub Pages se dispara con cada');
man.push('`push` a la rama `main`.');
man.push('');
man.push('## 8. Interoperabilidad');
man.push('');
man.push('- **JSON** — exportación e importación completas del modelo.');
man.push('- **PlantUML** — exportación de las dos vistas y reimportación sin');
man.push('  pérdida. Los `.puml` generados se pueden pegar en');
man.push('  <https://www.plantuml.com/plantuml/uml> para obtener la imagen oficial.');
man.push('');
fs.writeFileSync(path.join(SALIDA, 'manual-tecnico.md'), man.join('\n'));

/* --------------------------------------------------------------------
   Resumen
   -------------------------------------------------------------------- */
const generados = fs.readdirSync(SALIDA).sort();
console.log('Documentación generada en doc/:');
generados.forEach((f) => {
  const bytes = fs.statSync(path.join(SALIDA, f)).size;
  console.log('  ' + f.padEnd(30) + String(bytes).padStart(7) + ' bytes');
});
console.log('');
console.log('Validación del modelo: ' + JSON.stringify(validacion.resumen) +
  ' · válido: ' + (validacion.valido ? 'sí' : 'no'));
console.log('Suite de pruebas: ' + pruebas.exitosos + '/' + pruebas.total +
  ' casos en verde');
process.exit(pruebas.fallidos === 0 && validacion.valido ? 0 : 1);
