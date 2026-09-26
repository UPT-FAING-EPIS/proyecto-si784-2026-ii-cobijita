#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera FD03 (Especificación de Requerimientos, SRS) y FD04 (Arquitectura,
SAD) de DespliegaUML a partir del modelo real de la aplicación y de su
catálogo de reglas, para que la documentación no se desincronice del código.

Uso:  python3 tools/build_fd03_fd04.py
"""
import json
import subprocess
import sys
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AZUL = RGBColor(0x1F, 0x4E, 0x79)
GRIS = RGBColor(0x59, 0x59, 0x59)
VERDE = RGBColor(0x0F, 0x76, 0x6E)

EQUIPO = [
    "RODRIGUEZ CARDENAS, Patrick — 2022075751",
    "RIOS COHAILA, Nicole — 2022075745",
]
PROYECTO = "DespliegaUML"
CURSO = "Calidad y Pruebas de Software (SI-784)"
DOCENTE = "CUADROS QUIROGA, Patrick Jose"
CICLO = "Ciclo 7 · 2026-II"

# --------------------------------------------------------------------------
# Datos extraídos del código: el catalogo de reglas y el modelo de ejemplo
# --------------------------------------------------------------------------
def reglas_desde_codigo():
    js = """
    const fs=require('fs'),vm=require('vm');
    ['modelo.js','reglas.js','plan.js','pruebas.js','puml.js']
      .forEach(f=>vm.runInThisContext(
        fs.readFileSync('app/src/'+f,'utf8'),{filename:f}));
    const DPL=globalThis.DPL;
    const salida={reglas:DPL.REGLAS.map(r=>({
        id:r.id, nombre:r.nombre, razon:r.razon})),
      estereotipos:{
        componente:DPL.STEREOTIPOS_COMPONENTE,
        nodo:DPL.STEREOTIPOS_NODO,
        artefacto:DPL.TIPOS_ARTIFACTO}};
    console.log(JSON.stringify(salida));
    """
    r = subprocess.run(["node", "-e", js], cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR al leer el catálogo de reglas:\n" + r.stderr, file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout)


def modelo_desde_ejemplo():
    ruta = os.path.join(RAIZ, "app", "ejemplos", "aplicacion-web-3niveles.json")
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
# Helpers de estilo
# --------------------------------------------------------------------------
def nuevo_doc():
    d = Document()
    for s in d.sections:
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
        s.top_margin = Cm(2.5)
        s.bottom_margin = Cm(2.0)
        s.left_margin = Cm(2.5)
        s.right_margin = Cm(2.0)
    n = d.styles["Normal"]
    n.font.name = "Calibri"
    n.font.size = Pt(11)
    n._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    return d


def sombrear(celda, color="1F4E79"):
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def h(doc, texto, nivel=1, salto=False):
    if salto:
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    p = doc.add_heading(texto, level=nivel)
    for r in p.runs:
        r.font.color.rgb = AZUL
        r.font.name = "Calibri"
    return p


def p(doc, texto="", size=11, bold=False, italic=False, color=None,
      align=None, space_after=6, sangria=None):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    par.paragraph_format.line_spacing = 1.15
    if align:
        par.alignment = align
    if sangria:
        par.paragraph_format.left_indent = Cm(sangria)
    r = par.add_run(texto)
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    if color:
        r.font.color.rgb = color
    return par


def vinetas(doc, items, sangria=0.6):
    for it in items:
        par = doc.add_paragraph(style="List Bullet")
        par.paragraph_format.left_indent = Cm(sangria)
        par.paragraph_format.space_after = Pt(3)
        r = par.add_run(it)
        r.font.size = Pt(11)


def numeradas(doc, items, sangria=0.6):
    for it in items:
        par = doc.add_paragraph(style="List Number")
        par.paragraph_format.left_indent = Cm(sangria)
        par.paragraph_format.space_after = Pt(3)
        r = par.add_run(it)
        r.font.size = Pt(11)


def tabla(doc, encabezados, filas, anchos=None, size=9.5):
    t = doc.add_table(rows=1, cols=len(encabezados))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    t._tbl.tblPr.append(layout)
    hdr = t.rows[0].cells
    for i, texto in enumerate(encabezados):
        hdr[i].text = ""
        run = hdr[i].paragraphs[0].add_run(texto)
        run.bold = True
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        sombrear(hdr[i])
    for fila in filas:
        c = t.add_row().cells
        for i, texto in enumerate(fila):
            c[i].text = ""
            run = c[i].paragraphs[0].add_run(str(texto))
            run.font.size = Pt(size)
    if anchos:
        for fila in t.rows:
            for i, w in enumerate(anchos):
                fila.cells[i].width = Cm(w)
        for i, w in enumerate(anchos):
            t.columns[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t


def portada(doc, titulo, subtitulo, sistema_linea):
    p(doc, "UNIVERSIDAD PRIVADA DE TACNA", size=14, bold=True, color=AZUL,
      align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    p(doc, "FACULTAD DE INGENIERÍA", size=14, bold=True, color=AZUL,
      align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    p(doc, "Escuela Profesional de Ingeniería de Sistemas", size=12, color=GRIS,
      align=WD_ALIGN_PARAGRAPH.CENTER, space_after=30)
    p(doc, "Proyecto " + PROYECTO, size=13, bold=True,
      align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    p(doc, titulo, size=19, bold=True, color=AZUL,
      align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    p(doc, subtitulo, size=11.5, italic=True, color=GRIS,
      align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    p(doc, sistema_linea, size=11, bold=True,
      align=WD_ALIGN_PARAGRAPH.CENTER, space_after=26)
    p(doc, "Curso: " + CURSO, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p(doc, "Docente: " + DOCENTE, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p(doc, CICLO, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    p(doc, "Integrantes:", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
      space_after=4)
    for e in EQUIPO:
        p(doc, e, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p(doc, "Tacna – Perú · 2026", size=11, align=WD_ALIGN_PARAGRAPH.CENTER,
      space_after=0)


def control_versiones(doc):
    tabla(doc,
          ["Versión", "Hecha por", "Revisada por", "Aprobada por", "Fecha", "Motivo"],
          [["1.0", "Rodriguez P. / Rios N.", "Docente del curso",
            "Docente del curso", "26/09/2026", "Versión original"]],
          anchos=[1.8, 3.6, 3.2, 3.2, 2.3, 3.0], size=9)


# ==========================================================================
# FD03 · Especificación de Requerimientos de Software (SRS)
# ==========================================================================
def build_fd03(reglas, modelo, destino):
    d = nuevo_doc()
    portada(d,
            "Informe de Especificación de Requerimientos de Software",
            "Documento de Especificación de Requerimientos de Software (SRS)",
            "Sistema " + PROYECTO + " — Documento de Especificación de Requerimientos "
            "de Software, Versión 1.0")

    # --------------------------------------------------------------- índice
    h(d, "Control de versiones", 1, salto=True)
    control_versiones(d)
    h(d, "Índice general", 1)
    p(d, "1. Introducción", bold=True, space_after=2)
    p(d, "2. Descripción general", bold=True, space_after=2)
    p(d, "3. Requerimientos específicos", bold=True, space_after=2)
    p(d, "4. Requerimientos no funcionales", bold=True, space_after=2)
    p(d, "5. Reglas de consistencia del modelo", bold=True, space_after=2)
    p(d, "6. Casos de uso", bold=True, space_after=2)
    p(d, "7. Trazabilidad", bold=True, space_after=2)
    p(d, "8. Referencias", bold=True, space_after=2)

    # --------------------------------------------------------------- 1
    h(d, "1. Introducción", 1, salto=True)
    h(d, "1.1 Propósito", 2)
    p(d, "Este documento especifica los requisitos funcionales y no funcionales de " +
        PROYECTO + ", la herramienta que modela el diagrama de componentes y el " +
        "diagrama de despliegue de un sistema de software, valida la consistencia " +
        "del modelo mediante un catálogo de " + str(len(reglas)) + " reglas y genera " +
        "el plan de despliegue correspondiente. Es el contrato entre el equipo de " +
        "desarrollo y el docente evaluador: lo que no está aquí no se verifica.")
    h(d, "1.2 Alcance", 2)
    p(d, "El alcance cubre el modelo de dominio, el motor de validación, el " +
        "generador de plan de despliegue, la interfaz de edición y la " +
        "interoperabilidad con JSON y PlantUML. Quedan fuera: la publicación " +
        "como servicio multiusuario, el control de versiones collaborative del " +
        "modelo y la integración con gestionores de infraestructura en la nube.")
    h(d, "1.3 Definiciones, siglas y abreviaturas", 2)
    tabla(d, ["Término", "Definición"],
          [["UML", "Unified Modeling Language, lenguaje estándar de modelado de software."],
           ["Diagrama de componentes", "Vista UML que describe los componentes, sus interfaces y sus relaciones."],
           ["Diagrama de despliegue", "Vista UML que describe los nodos físicos y los artefactos que se despliegan en ellos."],
           ["Componente", "Unidad de software con interfaces publishes o requeridas."],
           ["Puerto", "Punto de conexión de un componente: «provided» si publica la interfaz, «required» si la requiere."],
           ["Nodo", "Ejecución de un programa sobre un recurso físico; en UML 2 un nodo representa una máquina."],
           ["Artefacto", "Archivo desplegable: ejecutable, biblioteca, dato o documento."],
           ["Realización", "Unión entre un artefacto y el nodo donde se despliega."],
           ["Camino de comunicación", "Enlace entre dos nodos con un protocolo y un puerto."],
           ["Motor de validación", "Componente que evalúa el modelo contra un catálogo de reglas."],
           ["Falso positivo", "Alerta que señala un defecto donde el modelo es correcto."]],
          anchos=[4.6, 11.9])
    h(d, "1.4 Visión general", 2)
    p(d, PROYECTO + " integra tres capacidades: un editor de los dos diagramas, un " +
        "motor de validación de reglas y un generador de plan de despliegue. La " +
        "decisión de arquitectura central es separar el modelo de dominio de su " +
        "representación, de modo que la lógica de validación es independiente del " +
        "navegador y puede probarse de forma automatizada en Node.js.")

    # --------------------------------------------------------------- 2
    h(d, "2. Descripción general", 1, salto=True)
    h(d, "2.1 Perspectiva del producto", 2)
    p(d, "Aplicación web independiente, de ejecución local o servida como sitio " +
        "estático. No requiere servidor de aplicaciones ni base de datos: el modelo " +
        "reside en el navegador y se persiste en el almacenamiento local.")
    h(d, "2.2 Descripción de la arquitectura", 2)
    p(d, "El sistema se organiza en dos capas. La capa de dominio —modelo, motor de " +
        "reglas, generador de plan e interoperabilidad— no depende del navegador y es " +
        "la que se somete a las pruebas automatizadas. La capa de presentación —render " +
        "en SVG, persistencia y controlador de la interfaz— depende de la anterior y " +
        "sólo la utiliza. Esta separación es lo que permite verificar la lógica sin " +
        "arrancar un navegador.")
    h(d, "2.3 Identidad de los elementos del modelo", 2)
    p(d, "Cada elemento del modelo lleva un identificador estable, generado " +
        "correlativamente y con prefijo según su tipo. Los identificadores son la base " +
        "de la trazabilidad: un hallazgo de validación apunta al elemento concreto que " +
        "lo provoca.")
    tabla(d, ["Colección", "Contenido", "Prefijo del identificador"],
          [["componentes", "Componentes UML con sus puertos", "C"],
           ["conectores", "Uniones entre un puerto published y uno requerido", "K"],
           ["nodos", "Nodos de despliegue con jerarquía y ficha técnica", "N"],
           ["artefactos", "Artefactos desplegables", "A"],
           ["realizaciones", "Unión artefacto → nodo", "R"],
           ["caminos", "Comunicación entre nodos", "CP"]],
          anchos=[4.0, 9.4, 3.1])
    h(d, "2.4 Entorno de usuario", 2)
    p(d, "Aplicación ejecutada en el navegador. La interfaz muestra cuatro paneles: " +
        "diagrama de componentes, diagrama de despliegue, catálogo de reglas y plan " +
        "de despliegue. El usuario esperado conoce los conceptos de UML, pero la " +
        "interfaz muestra siempre el estereotipo y el identificador de cada elemento " +
        "para que no dependa del conocimiento previo de la notación.")
    h(d, "2.5 Restricciones", 2)
    vinetas(d, [
        "Sin dependencias externas ni paso de compilación: la aplicación debe " +
        "poder abrirse con doble clic sobre el archivo HTML.",
        "El código debe ser compatible con navegadores que soporten ES5.",
        "La lógica de dominio debe poder ejecutarse en Node.js sin navegador.",
        "La documentación técnica se genera desde el código, no se edita a mano.",
    ])

    # --------------------------------------------------------------- 3
    h(d, "3. Requerimientos específicos", 1, salto=True)
    p(d, "Cada requerimiento lleva un identificador estable. La columna de " +
        "verificación indica la evidencia objetiva que demuestra su cumplimiento.",
        italic=True, color=GRIS)
    h(d, "3.1 Requerimientos funcionales del modelo de dominio", 2)
    tabla(d, ["ID", "Requerimiento", "Prioridad", "Verificación"],
          [["RF-01", "El sistema debe crear componentes con identificador único, nombre, estereotipo y descripción.", "Alta", "Casos T-01, T-02"],
           ["RF-02", "El sistema debe declarar puertos en un componente, cada uno con nombre, interfaz y dirección provided o required.", "Alta", "Casos T-05, T-06"],
           ["RF-03", "El sistema debe crear conectores que unan un puerto provided con uno required.", "Alta", "Casos T-24, T-25"],
           ["RF-04", "El sistema debe crear nodos con jerarquía opcional y ficha técnica de sistema operativo, CPU y memoria.", "Alta", "Casos T-33, T-34"],
           ["RF-05", "El sistema debe crear artefactos con tipo, ruta de archivo y versión.", "Alta", "Casos T-30, T-31"],
           ["RF-06", "El sistema debe registrar qué artefacto se realiza en qué nodo.", "Alta", "Caso T-29"],
           ["RF-07", "El sistema debe crear caminos de comunicación entre nodos con protocolo y puerto.", "Media", "Casos T-38, T-39"],
           ["RF-08", "Al eliminar un componente, el sistema debe eliminar en cascada sus conectores.", "Alta", "Caso T-07"],
           ["RF-09", "Al eliminar un artefacto, el sistema debe eliminar en cascada sus realizaciones.", "Alta", "Caso T-08"],
           ["RF-10", "Al eliminar un nodo, el sistema debe eliminar sus realizaciones y caminos, y liberar a sus hijos.", "Media", "Caso T-09"],
           ["RF-11", "El sistema debe indexar el modelo en una sola pasada para alimentar la validación.", "Alta", "Caso T-06"],
           ["RF-12", "El sistema debe normalizar los modelos que lleguen incompletos, completando las colecciones ausentes.", "Media", "Caso T-10"],
           ["RF-13", "El sistema debe clonar un modelo sin compartir estructura con el original.", "Baja", "Caso T-11"]],
          anchos=[1.6, 9.2, 2.0, 3.7])

    h(d, "3.2 Requerimientos funcionales de la validación", 2)
    tabla(d, ["ID", "Requerimiento", "Prioridad", "Verificación"],
          [["RF-14", "El motor debe evaluar la totalidad del catálogo de reglas ante cualquier cambio del modelo.", "Alta", "Caso T-16"],
           ["RF-15", "El motor debe clasificar cada hallazgo como error, warning o info.", "Alta", "Caso T-15"],
           ["RF-16", "El motor debe ordenar los hallazgos por severidad descendente.", "Media", "Caso T-15"],
           ["RF-17", "El motor debe señalar el elemento concreto que provoca cada hallazgo.", "Alta", "Casos T-17 a T-44"],
           ["RF-18", "El motor debe declarar el modelo válido cuando no produce hallazgos de severidad error.", "Alta", "Casos T-12, T-13"],
           ["RF-19", "Si una regla lanza una excepción, el motor debe registrar el fallo y continuar evaluando las demás.", "Alta", "Caso T-46"],
           ["RF-20", "Un modelo vacío no debe producir hallazgos de severidad error.", "Media", "Caso T-45"]],
          anchos=[1.6, 9.2, 2.0, 3.7])

    h(d, "3.3 Requerimientos funcionales de la generación del plan", 2)
    tabla(d, ["ID", "Requerimiento", "Prioridad", "Verificación"],
          [["RF-21", "El generador debe calcular el orden topológico de los componentes a partir del grafo de ensamblaje.", "Alta", "Casos T-49, T-50"],
           ["RF-22", "El generador debe asignar a cada componente su nivel de dependencia.", "Alta", "Caso T-49"],
           ["RF-23", "El generador debe producir una fase de despliegue por nivel, más una fase de verificación final.", "Alta", "Caso T-53"],
           ["RF-24", "El generador debe incluir la ficha técnica de cada nodo en el plan.", "Alta", "Caso T-51"],
           ["RF-25", "El generador debe registrar como supuestos los datos técnicos que el modelo no declara.", "Media", "Caso T-52"],
           ["RF-26", "El plan debe cubrir todos los nodos y artefactos del modelo sin referencias pendientes.", "Alta", "Caso T-54"],
           ["RF-27", "El generador debe bloquear el plan y reportar los errores cuando el modelo es inconsistente.", "Alta", "Caso T-48"],
           ["RF-28", "El plan debe renderizarse en Markdown con topología, orden, fases y supuestos.", "Media", "Caso T-55"]],
          anchos=[1.6, 9.2, 2.0, 3.7])

    h(d, "3.4 Requerimientos funcionales de la interfaz", 2)
    tabla(d, ["ID", "Requerimiento", "Prioridad", "Verificación"],
          [["RF-29", "El usuario debe crear cada tipo de elemento del modelo desde la herramienta correspondiente.", "Alta", "Prueba de humo"],
           ["RF-30", "El usuario debe editar y eliminar cualquier elemento desde el inspector.", "Alta", "Prueba de humo"],
           ["RF-31", "La interfaz debe marcar en rojo los elementos que incumplen una regla.", "Alta", "Verificación visual"],
           ["RF-32", "La interfaz debe reevaluar la validación ante cada cambio del modelo.", "Alta", "Prueba de humo"],
           ["RF-33", "El usuario debe poder filtrar el catálogo de reglas por estado de hallazgo.", "Baja", "Verificación visual"],
           ["RF-34", "La interfaz debe ofrecer un enlace directo a cada panel mediante parámetros de la URL.", "Baja", "Verificación visual"]],
          anchos=[1.6, 9.2, 2.0, 3.7])

    h(d, "3.5 Requerimientos funcionales de interoperabilidad y persistencia", 2)
    tabla(d, ["ID", "Requerimiento", "Prioridad", "Verificación"],
          [["RF-35", "El usuario debe exportar e importar el modelo completo en JSON.", "Alta", "Caso T-58"],
           ["RF-36", "El sistema debe exportar el modelo a PlantUML, en dos archivos autocontenidos.", "Alta", "Caso T-60"],
           ["RF-37", "El sistema debe reimportar su propia exportación PlantUML sin pérdida de información.", "Alta", "Casos T-61 a T-64"],
           ["RF-38", "El sistema debe persistir el modelo automáticamente en el almacenamiento local del navegador.", "Media", "Verificación visual"],
           ["RF-39", "El plan de despliegue debe poder copiarse al portapapeles y descargarse en Markdown.", "Media", "Verificación visual"]],
          anchos=[1.6, 9.2, 2.0, 3.7])

    # --------------------------------------------------------------- 4
    h(d, "4. Requerimientos no funcionales", 1, salto=True)
    tabla(d, ["ID", "Atributo de calidad", "Requerimiento", "Verificación"],
          [["RNF-01", "Usabilidad", "La aplicación debe abrirse con doble clic, sin instalación, compilación ni servidor.", "Verificación manual"],
           ["RNF-02", "Rendimiento", "La validación de las " + str(len(reglas)) + " reglas sobre el modelo de referencia debe completarse en menos de 50 ms.", "Informe de calidad"],
           ["RNF-03", "Mantenibilidad", "La lógica de dominio no debe depender del navegador, para poder probarse en Node.js.", "Caso T-63"],
           ["RNF-04", "Trazabilidad", "Todo hallazgo de validación debe identificar el elemento y la regla que lo provoca.", "Casos T-17 a T-44"],
           ["RNF-05", "Portabilidad", "El código debe ser compatible con navegadores que soporten ES5.", "Verificación en Firefox"],
           ["RNF-06", "Consistencia de documentación", "La documentación técnica debe generarse desde el código mediante unaCI, no editarse a mano.", "Verificación del pipeline"],
           ["RNF-07", "Fiabilidad", "Ninguna regla debe producir falsos positivos sobre un modelo válido.", "Casos positivos de cada regla"],
           ["RNF-08", "Recuperabilidad", "Un modelo importado incompleto o malformado debe normalizarse en lugar de fallar.", "Casos T-10, T-58"]],
          anchos=[1.6, 3.4, 8.4, 3.1])

    # --------------------------------------------------------------- 5
    h(d, "5. Reglas de consistencia del modelo", 1, salto=True)
    p(d, "El motor de validación se apoya en un catálogo de " + str(len(reglas)) +
        " reglas. Cada una tiene un identificador estable, un nombre, un fundamento " +
        "explícito y una severidad. La regla de decisión del sistema es: el plan de " +
        "despliegue se genera únicamente cuando el modelo no produce ningún " +
        "hallazgo de severidad «error».", space_after=10)
    tabla(d, ["ID", "Regla", "Fundamento"],
          [[r["id"], r["nombre"], r["razon"]] for r in reglas],
          anchos=[1.6, 6.4, 8.5], size=9)
    h(d, "5.1 Vocabulario controlado", 2)
    p(d, "Para mantener la coherencia del modelo, el sistema restringe el " +
        "vocabulario de estereotipos a los definidos por OMG UML 2.x. Cualquier " +
        "valor fuera de este catálogo es rechazado por la regla R-03.")
    tabla(d, ["Elemento", "Valores admitidos"],
          [["Componente", "application, service, library, interface, database, external"],
           ["Nodo", "device, executionEnvironment, deploymentUnit, container, cloudRegion"],
           ["Artefacto", "executable, library, data, document"],
           ["Puerto", "provided, required"]],
          anchos=[3.4, 13.1])

    # --------------------------------------------------------------- 6
    h(d, "6. Casos de uso", 1, salto=True)
    h(d, "6.1 UC-01 Modelar el diagrama de componentes", 2)
    tabla(d, ["Elemento", "Descripción"],
          [["Actor", "Desarrollador o arquitecto de software."],
           ["Precondición", "Ninguna."],
           ["Disparador", "El usuario selecciona la herramienta de creación de componente."],
           ["Flujo principal",
            "1. El usuario selecciona «+ Componente».\n"
            "2. El usuario hace clic en el lienzo.\n"
            "3. El sistema crea el componente con identificador correlativo.\n"
            "4. El usuario edita nombre y estereotipo en el inspector.\n"
            "5. El sistema reevalúa las " + str(len(reglas)) + " reglas."],
           ["Extensiones",
            "a. Si el nombre queda vacío, la regla R-02 lo señala como error.\n"
            "b. Si el estereotipo no pertenece al catálogo, la regla R-03 lo rechaza.\n"
            "c. Si el componente no tiene artefacto que lo implemente, R-11 lo avisa."]],
          anchos=[3.2, 13.3])
    h(d, "6.2 UC-02 Validar el modelo y generar el plan de despliegue", 2)
    tabla(d, ["Elemento", "Descripción"],
          [["Actor", "Desarrollador o arquitecto de software."],
           ["Precondición", "Existe un modelo con componentes, nodos y artefactos."],
           ["Disparador", "El usuario pulsa «Generar plan de despliegue»."],
           ["Flujo principal",
            "1. El sistema evalúa las " + str(len(reglas)) + " reglas sobre el modelo.\n"
            "2. Si hay hallazgos de severidad «error», el plan queda bloqueado y se "
            "muestran los errores con su regla y su elemento.\n"
            "3. Si no hay errores, el sistema calcula el orden topológico y los "
            "niveles de dependencia.\n"
            "4. El sistema genera una fase por nivel más la fase de verificación.\n"
            "5. El sistema registra los supuestos pendientes.\n"
            "6. El usuario copia o descarga el plan en Markdown."],
           ["Extensiones",
            "a. Si faltan datos técnicos en un nodo, se registran como supuesto (R-14).\n"
            "b. Si el grafo de componentes tiene un ciclo, el orden no está definido "
            "para esos componentes y se reporta como supuesto (R-17)."]],
          anchos=[3.2, 13.3])

    # --------------------------------------------------------------- 7
    h(d, "7. Trazabilidad", 1, salto=True)
    p(d, "La matriz completa que relaciona cada regla con su caso de prueba " +
        "positivo y negativo está en el plan de pruebas del proyecto. El esquema " +
        "de trazabilidad es:")
    tabla(d, ["Nivel", "Relación", "Evidencia"],
          [["Objetivo de investigación", "OI-1 → eficacia de detección de las reglas",
            "Casos de prueba negativos, uno por regla"],
           ["Objetivo de investigación", "OI-2 → cobertura del plan de despliegue",
            "Caso T-54"],
           ["Objetivo de solución", "OS-1 → cobertura funcional del editor",
            "Prueba de humo de flujo completo"],
           ["Objetivo de solución", "OS-2 → cobertura del catálogo de reglas",
            "Un caso positivo y uno negativo por regla"],
           ["Objetivo de solución", "OS-3 → generación y bloqueo del plan",
            "Casos T-47 y T-48"],
           ["Objetivo de solución", "OS-4 → pruebas automatizadas de la lógica",
            "Suite completa, " + str(len(reglas)) + " reglas cubiertas"]],
          anchos=[3.8, 6.4, 6.3])

    # --------------------------------------------------------------- 8
    h(d, "8. Referencias", 1)
    p(d, "Normas y estándares")
    vinetas(d, [
        "OMG. Unified Modeling Language (UML) Specification, versión 2.x — "
        "estructura de los diagramas de componentes y de despliegue, y semántica "
        "de los estereotipos y de las interfaces.",
        "IEEE 830 (recomendación de la ISO/IEC/IEEE 29148) — Especificación de "
        "requerimientos de software: estructura y criterios de calidad de un SRS.",
    ])
    p(d, "Documentos del proyecto", bold=True, space_after=4)
    vinetas(d, [
        "FD01 — Informe de Factibilidad de " + PROYECTO,
        "FD02 — Documento de Visión de " + PROYECTO,
        "FD04 — Informe de Arquitectura de Software de " + PROYECTO,
        "calidad/Plan-de-Pruebas.md — plan de pruebas con trazabilidad regla → caso",
    ])
    p(d, "Fuentes consultadas para la definición del problema", bold=True, space_after=4)
    vinetas(d, [
        "https://github.com/UPT-FAING-EPIS/ — antecedentes de la facultad.",
        "https://problemhunt.pro/ — criterio de validación del problema.",
        "https://radiouno.pe/ — actividad regional de desarrollo de software.",
        "https://renati.sunedu.gob.pe/ — registro nacional de trabajos de investigación.",
    ])

    d.save(destino)
    return destino


# ==========================================================================
# FD04 · Informe de Arquitectura de Software (SAD)
# ==========================================================================
def build_fd04(reglas, modelo, destino):
    d = nuevo_doc()
    portada(d,
            "Informe de Arquitectura de Software",
            "Documento de Arquitectura de Software (SAD)",
            "Sistema " + PROYECTO + " — Documento de Arquitectura de Software, "
            "Versión 1.0")

    h(d, "Control de versiones", 1, salto=True)
    control_versiones(d)

    h(d, "Índice general", 1)
    p(d, "1. Introducción", bold=True, space_after=2)
    p(d, "2. Objetivos y restricciones arquitectónicas", bold=True, space_after=2)
    p(d, "3. Vista de casos de uso", bold=True, space_after=2)
    p(d, "4. Vista lógica", bold=True, space_after=2)
    p(d, "5. Vista de implementación", bold=True, space_after=2)
    p(d, "6. Vista de despliegue", bold=True, space_after=2)
    p(d, "7. Decisiones de diseño", bold=True, space_after=2)
    p(d, "8. Atributos de calidad", bold=True, space_after=2)

    # --------------------------------------------------------------- 1
    h(d, "1. Introducción", 1, salto=True)
    h(d, "1.1 Propósito", 2)
    p(d, "Este documento describe la arquitectura de " + PROYECTO + ": cómo se " +
        "descompone el sistema, qué decisiones de diseño rigen esa descomposición " +
        "y cómo se relaciona la arquitectura con los requisitos del SRS. Se " +
        "acompaña de los diagramas de componentes y de despliegue, que se generan " +
        "automáticamente desde el propio modelo mediante la integración continua.")
    h(d, "1.2 Alcance", 2)
    p(d, "Cubre la vista lógica, la vista de implementación y la vista de " +
        "despliegue, que son las pertinentes para una aplicación de modelado con " +
        "lógica determinista y despliegue estático. Se omite la vista de procesos " +
        "porque el sistema no tiene concurrencia: cada operación se ejecuta de " +
        "forma síncrona sobre el modelo en memoria.")
    h(d, "1.3 Definición, siglas y abreviaturas", 2)
    p(d, "Las siglas empleadas son las definidas en el SRS: UML, CI (integración " +
        "continua), ES5 ( ECMAScript 5, versión del lenguaje JavaScript " +
        "admitida), SVG (formato vectorial de imagen) y DOM (modelo de objetos de " +
        "documento).")
    h(d, "1.4 Organización del documento", 2)
    p(d, "La sección 2 fija los objetivos y restricciones que condicionan el " +
        "diseño. La sección 3 describe los casos de uso que la arquitectura debe " +
        "soportar. Las secciones 4 a 6 presentan las tres vistas de la arquitectura. " +
        "La sección 7 documenta las decisiones de diseño con sus alternativas " +
        "descartadas, y la sección 8 cómo la arquitectura satisface los atributos " +
        "de calidad.")

    # --------------------------------------------------------------- 2
    h(d, "2. Objetivos y restricciones arquitectónicas", 1, salto=True)
    h(d, "2.1 Priorización de requerimientos", 2)
    p(d, "La prioridad de los requerimientos determina el orden de " +
        "implementación. La tabla siguiente resume los requerimientos del SRS por " +
        "prioridad.")
    tabla(d, ["Prioridad", "Requerimientos", "Implicación arquitectónica"],
          [["Alta", "RF-01 a RF-13, RF-14 a RF-20, RF-24, RF-25, RF-29 a RF-31, RF-35 a RF-37",
            "El modelo de dominio y el motor de validación se implementan primero; "
            "determinan la estructura de todo lo demás."],
           ["Media", "RF-07, RF-10, RF-12, RF-16, RF-18, RF-23, RF-26, RF-32, RF-38, RF-39",
            "Funcionalidad de apoyo que puede añadirse sin alterar la arquitectura."],
           ["Baja", "RF-11, RF-13, RF-33, RF-34",
            "Optimizaciones y comodidades de uso."]],
          anchos=[2.0, 6.6, 7.9])
    h(d, "2.2 Restricciones", 2)
    vinetas(d, [
        "Sin dependencias externas ni paso de compilación.",
        "Compatible con navegadores que soporten ES5.",
        "La lógica de dominio debe ser ejecutable en Node.js, sin navegador.",
        "La documentación técnica se genera desde el código por integración continua.",
    ])

    # --------------------------------------------------------------- 3
    h(d, "3. Vista de casos de uso", 1, salto=True)
    h(d, "3.1 Actores", 2)
    tabla(d, ["Actor", "Descripción"],
          [["Desarrollador", "Modela la arquitectura del sistema que está construyendo."],
           ["Arquitecto", "Valida la coherencia del modelo antes de aprobar un despliegue."],
           ["Docente evaluador", "Revisa la documentación y los resultados de la validación."]],
          anchos=[3.6, 12.9])
    h(d, "3.2 Diagrama de casos de uso", 2)
    p(d, "El sistema tiene dos casos de uso principales, detallados en el SRS: " +
        "«UC-01 Modelar el diagrama de componentes» y «UC-02 Validar el modelo y " +
        "generar el plan de despliegue». Ambos comparten el mismo modelo de datos, " +
        "de modo que la arquitectura los soporta con una única estructura interna.")

    # --------------------------------------------------------------- 4
    h(d, "4. Vista lógica", 1, salto=True)
    h(d, "4.1 Descomposición en módulos", 2)
    p(d, "El sistema se descompone en dos capas con una dependencia unidireccional: " +
        "la capa de presentación conoce a la capa de dominio, nunca al revés. La " +
        "capa de dominio no importa nada del navegador, lo que la hace verificable " +
        "de forma automatizada.")
    tabla(d, ["Módulo", "Capa", "Responsabilidad", "Depende de"],
          [["modelo.js", "Dominio", "Entidades del modelo, índices y bajas en cascada.", "—"],
           ["reglas.js", "Dominio", "Catálogo de " + str(len(reglas)) + " reglas y motor que las evalúa.", "modelo.js"],
           ["plan.js", "Dominio", "Orden topológico, niveles, fases y render del plan.", "modelo.js, reglas.js"],
           ["puml.js", "Dominio", "Exportación e importación de PlantUML.", "modelo.js"],
           ["pruebas.js", "Dominio", "Micro-corredor de pruebas y fábricas de modelos.", "—"],
           ["vista.js", "Presentación", "Render de los dos diagramas en SVG.", "modelo.js"],
           ["almacen.js", "Presentación", "Persistencia local y descarga de archivos.", "modelo.js"],
           ["app.js", "Presentación", "Controlador de la interfaz y atajos de teclado.", "todos los anteriores"]],
          anchos=[3.0, 2.2, 8.0, 3.3])
    h(d, "4.2 Modelo de dominio", 2)
    p(d, "El modelo es un objeto con seis colecciones: componentes, conectores, " +
        "nodos, artefactos, realizaciones y caminos. Los componentes contienen " +
        "puertos, y los nodos pueden anidarse formando una jerarquía. La " +
        "indexación se realiza en una sola pasada y produce cinco índices " +
        "auxiliares que evitan la búsqueda lineal repetida durante la validación.")
    h(d, "4.3 Diagrama de componentes", 2)
    p(d, "El diagrama de componentes del propio " + PROYECTO + " se genera desde el " +
        "modelo y se publica en el repositorio como imagen. Refleja la relación " +
        "entre los módulos de la capa de dominio: el motor de reglas depende del " +
        "modelo, y el generador de plan depende de ambos.")

    # --------------------------------------------------------------- 5
    h(d, "5. Vista de implementación", 1, salto=True)
    h(d, "5.1 Estructura de archivos", 2)
    tabla(d, ["Ruta", "Contenido"],
          [["`app/index.html`", "Interfaz: barra de acciones, cuatro paneles, inspector y diálogo del plan."],
           ["`app/css/estilos.css`", "Hoja de estilos, sin framework."],
           ["`app/src/*.js`", "Módulos descritos en la vista lógica."],
           ["`app/tests/casos.js`", "Suite de pruebas unitarias e integración."],
           ["`app/tests/humo.html`", "Prueba de humo que ejercita el flujo de edición completo."],
           ["`tools/generar-documentacion.js`", "Generador de diagramas y manuales técnicos."],
           ["`doc/`", "Artefactos generados: diagramas SVG, plan, catálogo e informe de calidad."],
           ["`.github/workflows/ci-cd.yml`", "Pipeline de integración continua y publicación."]],
          anchos=[6.0, 10.5])
    h(d, "5.2 Correspondencia entre módulos y componentes", 2)
    p(d, "La correspondencia es directa: cada módulo de la vista lógica se " +
        "corresponde con un archivo, y cada archivo con una responsabilidad. No " +
        "hay código compartido entre módulos fuera del modelo de dominio.")
    h(d, "5.3 Manejo de errores", 2)
    p(d, "El motor de reglas aísla cada regla en su propio bloque de ejecución: si " +
        "una lanza una excepción, el fallo se registra como hallazgo y la " +
        "evaluación continúa. La normalización del modelo garantiza que un " +
        "archivo importado incompleto no provoque un error fatal.")

    # --------------------------------------------------------------- 6
    h(d, "6. Vista de despliegue", 1, salto=True)
    h(d, "6.1 Topología de referencia", 2)
    p(d, "La aplicación es estática: no requiere servidor de aplicaciones ni base " +
        "de datos. Se publica como sitio estático, lo que permite desplegarla en " +
        "cualquier servicio de hosting sin configuración adicional.")
    tabla(d, ["Nodo", "Función", "Contenido"],
          [["Cliente (navegador)", "Ejecuta la capa de presentación y el motor de validación.",
            "index.html, estilos y módulos JavaScript."],
           ["Repositorio git", "Almacena el código, la documentación y los informes.",
            "Historial completo y artefactos generados."],
           ["Integración continua", "Verifica, genera documentación y publica.",
            "Ejecutores efímeros de GitHub Actions."],
           ["Alojamiento estático", "Sirve la aplicación y la documentación al público.",
            "GitHub Pages."]],
          anchos=[4.0, 6.2, 6.3])
    h(d, "6.2 Proceso de despliegue", 2)
    numeradas(d, [
        "El desarrollador publica los cambios en la rama main.",
        "La integración continua ejecuta la suite de pruebas; si falla, el proceso se detiene.",
        "Se verifica que el modelo de ejemplo cumpla el catálogo completo de reglas.",
        "Se regeneran los diagramas, el plan de despliegue, el manual técnico y el informe de calidad.",
        "Los diagramas se renderizan a imagen SVG.",
        "La aplicación y la documentación se publican en el alojamiento estático.",
    ])
    h(d, "6.3 Plan de despliegue del modelo de ejemplo", 2)
    p(d, "Además de desplegar la propia aplicación, " + PROYECTO + " genera el plan " +
        "de despliegue de cualquier modelo que el usuario construya. El plan " +
        "comprende la topología de nodos con su ficha técnica, el orden de " +
        "despliegue por nivel de dependencia, una fase por nivel más la de " +
        "verificación, y el registro de los supuestos pendientes. El plan completo " +
        "del modelo de ejemplo está en el repositorio.")

    # --------------------------------------------------------------- 7
    h(d, "7. Decisiones de diseño", 1, salto=True)
    tabla(d, ["ID", "Decisión", "Alternativa descartada", "Justificación"],
          [["AD-01", "JavaScript ES5 sobre HTML5 y SVG, sin dependencias ni compilación.",
            "React o Vue con un empaquetador.",
            "La consigna exige que la aplicación funcione sin instalación: sin paso de compilación, abrir el archivo es suficiente y no hay riesgo de fallo en una demostración."],
           ["AD-02", "Separar la lógica de dominio de la representación.",
            "Escribir la validación acoplada al DOM.",
            "Permite probar el motor de forma automatizada en Node.js, sin navegador. De ahí que 64 de las pruebas se ejecuten en unos milisegundos."],
           ["AD-03", "El plan de despliegue se bloquea si el modelo tiene errores.",
            "Generar el plan con advertencias.",
            "Un plan generado a partir de un modelo inconsistente induce a desplegar algo que no se ha verificado."],
           ["AD-04", "El nivel de despliegue se calcula como «uno más el máximo nivel de las dependencias», resuelto en orden topológico.",
            "Iterar sobre los conectores hasta estabilizar el valor.",
            "Una sola pasada en orden topológico es suficiente y evita el cómputo inflado de niveles que producía la versión iterativa."],
           ["AD-05", "La documentación se genera desde el código.",
            "Redactar y mantener la documentación a mano.",
            "Una documentación escrita a mano se desincroniza del código. Al generarla, el manual técnico y los diagramas siempre reflejan el estado real."],
           ["AD-06", "Interoperabilidad con PlantUML mediante metadatos en comentarios.",
            "Exportar sólo a JSON.",
            "Permite obtener la imagen oficial de UML con la notación estándar, y a la vez reimportar el archivo sin pérdida."]],
          anchos=[1.4, 4.6, 3.6, 6.9], size=9)

    # --------------------------------------------------------------- 8
    h(d, "8. Atributos de calidad", 1, salto=True)
    p(d, "La sección 8.1 de la guía pide desplegar los requerimientos no " +
        "funcionales como atributos de calidad medibles. La arquitectura los " +
        "atiende así:")
    tabla(d, ["Atributo", "Cómo lo atiende la arquitectura", "Evidencia"],
          [["Portabilidad", "Sin dependencias ni compilación; la lógica de dominio es independiente del navegador.",
            "Se abre con doble clic; las pruebas corren en Node."],
           ["Mantenibilidad", "Módulos con responsabilidad única y dependencia unidireccional; la documentación se genera desde el código.",
            "Cobertura de pruebas por módulo."],
           ["Fiabilidad", "Aislamiento de fallos por regla y normalización de modelos importados.",
            "Casos T-46 y T-10."],
           ["Rendimiento", "Indexación en una sola pasada y evaluación de " + str(len(reglas)) + " reglas sin dependencias entre ellas.",
            "Validación por debajo de 50 ms."],
           ["Trazabilidad", "Identificadores estables en todos los elementos; cada hallazgo apunta a su elemento y a su regla.",
            "Casos de prueba por regla."],
           ["Usabilidad", "El modelo muestra siempre el estereotipo y el identificador; la validación marca los elementos directamente en el diagrama.",
            "Verificación visual."],
           ["Seguridad", "El sistema no procesa entrada no confiable más allá del modelo importado, que se normaliza y se valida antes de usarse.",
            "Normalización previa a la validación."]],
          anchos=[2.8, 9.0, 4.7])

    d.save(destino)
    return destino


# --------------------------------------------------------------------------
if __name__ == "__main__":
    print("Leyendo el catálogo de reglas y el modelo de ejemplo…")
    cat = reglas_desde_codigo()
    reglas = cat["reglas"]
    modelo = modelo_desde_ejemplo()
    print("  · %d reglas, %d componentes, %d nodos, %d artefactos" % (
        len(reglas), len(modelo["componentes"]), len(modelo["nodos"]),
        len(modelo["artefactos"])))

    d3 = build_fd03(reglas, modelo,
                   os.path.join(RAIZ, "FD03-EPIS-Informe SRS-DespliegaUML.docx"))
    print("OK -> " + os.path.basename(d3))
    d4 = build_fd04(reglas, modelo,
                   os.path.join(RAIZ, "FD04-EPIS-Informe SAD-DespliegaUML.docx"))
    print("OK -> " + os.path.basename(d4))
