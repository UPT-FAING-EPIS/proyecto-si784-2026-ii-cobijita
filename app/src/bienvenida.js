/* ============================================================
   DespliegaUML · bienvenida, modo simple y modo detallado
   El usuario elige. El modo simple usa palabras cotidianas y
   ejemplos de la vida real. El modo detallado es el original.
   ============================================================ */

(function () {
  'use strict';

  var M = window.DPL.Modelo;

  /* ---------- estado del modo ---------- */
  var modo = 'detallado';   // 'simple' | 'detallado'
  var ETIQUETAS = {
    simple: {
      componente: 'Pieza',
      puerto: 'Conector',
      conector: 'Cable',
      nodo: 'Servidor',
      artefacto: 'Archivo',
      realizacion: 'Instalar',
      camino: 'Ruta',
      'agregar-componente': '+ Pieza',
      'agregar-puerto': '+ Conector',
      'agregar-conector': '→ Cable',
      'agregar-nodo': '+ Servidor',
      'agregar-artefacto': '+ Archivo',
      'agregar-realizacion': '⊕ Instalar',
      'agregar-camino': '⇄ Ruta',
      'vista-componentes': 'Mis piezas',
      'vista-despliegue': 'Mis servidores',
      'vista-reglas': 'Reglas',
      'vista-plan': 'Plan de instalación'
    },
    detallado: {
      componente: 'Componente',
      puerto: 'Puerto',
      conector: 'Conector',
      nodo: 'Nodo',
      artefacto: 'Artefacto',
      realizacion: 'Realización',
      camino: 'Camino',
      'agregar-componente': '+ Componente',
      'agregar-puerto': '+ Puerto',
      'agregar-conector': '→ Conector',
      'agregar-nodo': '+ Nodo',
      'agregar-artefacto': '+ Artefacto',
      'agregar-realizacion': '⊕ Realizar',
      'agregar-camino': '⇄ Camino',
      'vista-componentes': 'Diagrama de componentes',
      'vista-despliegue': 'Diagrama de despliegue',
      'vista-reglas': 'Reglas de consistencia',
      'vista-plan': 'Plan de despliegue'
    }
  };

  function etiqueta(clave) {
    return (ETIQUETAS[modo] && ETIQUETAS[modo][clave]) || clave;
  }

  /* ---------- pantalla de bienvenida ---------- */
  function hayBienvenida() {
    return !!document.getElementById('bienvenida');
  }

  function mostrarBienvenida() {
    if (hayBienvenida()) return;
    var b = document.createElement('div');
    b.className = 'bienvenida';
    b.id = 'bienvenida';
    b.innerHTML =
      '<div class="bienvenida-caja">' +
        '<h2>▲ DespliegaUML</h2>' +
        '<p class="sub">Dibuja cómo está hecho un sistema, revisa que esté bien y genera el plan de instalación.</p>' +
        '<div class="pasos">' +
          '<div class="paso"><span class="paso-num">1</span>' +
            '<div class="paso-txt"><strong>Dibuja las piezas</strong>' +
            '<span>Pon los elementos en el lienzo: una app, una base de datos, un servidor.</span></div></div>' +
          '<div class="paso"><span class="paso-num">2</span>' +
            '<div class="paso-txt"><strong>Conéctalas</strong>' +
            '<span>Une las piezas con cables para decir quién habla con quién.</span></div></div>' +
          '<div class="paso"><span class="paso-num">3</span>' +
            '<div class="paso-txt"><strong>Genera el plan</strong>' +
            '<span>El programa revisa tu diagrama y te dice cómo instalarlo.</span></div></div>' +
        '</div>' +
        '<div class="modos">' +
          '<button class="modo recomendado" data-modo="simple">' +
            '<span class="etiq">Recomendado para empezar</span>' +
            '<strong>Modo simple</strong>' +
            '<span>Piezas y cables. Ejemplos de la vida cotidiana: una tienda, una biblioteca, un cine.</span></button>' +
          '<button class="modo" data-modo="detallado">' +
            '<span class="etiq">Para quien ya sabe</span>' +
            '<strong>Modo detallado</strong>' +
            '<span>Componentes, puertos, nodos, artefactos y conectores con toda la técnica.</span></button>' +
        '</div>' +
        '<div class="bienvenida-acciones">' +
          '<button class="pri" id="empezar-modo">Empezar</button>' +
          '<button class="omitir" id="omitir-bienvenida">Ya sé usar esto, omitir</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(b);

    var sel = 'simple';
    b.querySelectorAll('.modo').forEach(function (btn) {
      btn.addEventListener('click', function () {
        sel = btn.dataset.modo;
        b.querySelectorAll('.modo').forEach(function (x) { x.classList.remove('recomendado'); });
        btn.classList.add('recomendado');
      });
    });

    b.querySelector('#empezar-modo').addEventListener('click', function () {
      b.classList.add('oculta');
      window.DespliegaModos.definir(sel);
    });
    b.querySelector('#omitir-bienvenida').addEventListener('click', function () {
      b.classList.add('oculta');
      window.DespliegaModos.definir('detallado');
    });
  }

  /* ---------- selector de ejemplos (modo simple) ---------- */
  function mostrarEjemplos() {
    var cont = document.getElementById('selector-ejemplos');
    if (!cont) return;
    cont.innerHTML = '';
    window.EJEMPLOS_SIMPLES.forEach(function (ej) {
      var t = document.createElement('button');
      t.className = 'ejemplo-tarjeta';
      t.innerHTML = '<strong>' + ej.nombre + '</strong><span>' + ej.historia + '</span>';
      t.addEventListener('click', function () { cargarEjemploSimple(ej); });
      cont.appendChild(t);
    });
  }

  function cargarEjemploSimple(ej) {
    var app = window.__app;
    if (!app || !app.nuevoModelo) return;
    app.nuevoModelo(ej.nombre);
    var m = app.modelo();
    ej.piezas.forEach(function (p) {
      M.agregarComponente(m, { nombre: p.nombre, x: p.x, y: p.y, estereotipo: p.estereotipo });
    });
    ej.conectores.forEach(function (c) {
      M.agregarConector(m, {
        desde: { componente: 'C' + (c.desde + 1), puerto: null },
        hacia: { componente: 'C' + (c.hacia + 1), puerto: null },
        contrato: c.contrato
      });
    });
    ej.servidores.forEach(function (s) {
      M.agregarNodo(m, { nombre: s.nombre, x: s.x, y: s.y, estereotipo: s.estereotipo });
    });
    app.refrescar();
    if (app.avisar) app.avisar(ej.pregunta, 'info');
  }

  /* ---------- API pública ---------- */
  window.DespliegaModos = {
    definir: function (m) {
      modo = (m === 'simple') ? 'simple' : 'detallado';
      var etiqueta = document.getElementById('etiqueta-modo');
      if (etiqueta) {
        etiqueta.innerHTML = (modo === 'simple' ? 'Modo simple' : 'Modo detallado') +
          ' <button title="Cambir de modo" id="cambiar-modo">⇄</button>';
        var btn = document.getElementById('cambiar-modo');
        if (btn) btn.addEventListener('click', function () {
          window.DespliegaModos.definir(modo === 'simple' ? 'detallado' : 'simple');
        });
      }
      var sel = document.getElementById('selector-ejemplos');
      if (sel) sel.style.display = (modo === 'simple') ? '' : 'none';
      if (modo === 'simple') mostrarEjemplos();
      if (window.__app && window.__app.alCambiarModo) window.__app.alCambiarModo(modo);
    },
    actual: function () { return modo; },
    etiqueta: etiqueta,
    mostrarBienvenida: mostrarBienvenida
  };
  
  /* ---------- arranque ---------- */
  function iniciar() {
    if (window.DespliegaModos) window.DespliegaModos.mostrarBienvenida();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();
