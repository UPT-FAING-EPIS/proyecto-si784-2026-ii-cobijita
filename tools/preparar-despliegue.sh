#!/usr/bin/env bash
# Prepara el directorio de despliegue público de DespliegaUML.
#
# Genera sitio/ con la aplicación en la raíz, la documentación y una portada
# con los enlaces. Es el mismo contenido que publica el pipeline de GitHub
# Pages, para poder usarlo en cualquier servicio de hosting estático.
#
# Uso:  tools/preparar-despliegue.sh
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DESTINO="$RAIZ/sitio"

cd "$RAIZ"

# Los diagramas y el manual se regeneran desde el modelo antes de copiar.
node tools/generar-documentacion.js >/dev/null

rm -rf "$DESTINO"
mkdir -p "$DESTINO"

# La aplicación va en la raíz: sus rutas relativas (css/, src/) son absolutas
# respecto a index.html, así que copiar el archivo suelto rompería la carga.
cp -r app/. "$DESTINO/"
mkdir -p "$DESTINO/app"
cp -r app/. "$DESTINO/app/"

# Documentación generada.
mkdir -p "$DESTINO/doc"
cp -f doc/*.md doc/*.svg doc/*.puml "$DESTINO/doc/" 2>/dev/null || true

# Informes del proyecto.
mkdir -p "$DESTINO/informes"
cp -f FD*.docx "$DESTINO/informes/" 2>/dev/null || true
cp -f unidad1/Proyecto-de-Unidad-1.pdf "$DESTINO/informes/" 2>/dev/null || true

# La portada sustituye al index de la aplicación, que queda como index-app.html.
mv "$DESTINO/index.html" "$DESTINO/index-app.html"
cp "$RAIZ/tools/portada.html" "$DESTINO/index.html"

echo "Contenido de $DESTINO:"
find "$DESTINO" -maxdepth 1 | sort | sed 's/^/  /'
du -sh "$DESTINO" | sed 's/^/  /'
echo
echo "Para probarlo en local:"
echo "  python3 -m http.server 8000 --directory $DESTINO"
echo "  abrir http://localhost:8000/index-app.html"
