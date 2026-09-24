# Catálogo AR · Serpientes de Colombia

Catálogo de realidad aumentada (web, sin instalar apps) de serpientes
representativas de Colombia. Al apuntar la cámara del celular a una carta
impresa (marcador + QR) aparece el modelo 3D de la especie con su ficha.

## Cómo funciona

- Cada especie tiene un **marcador AR** (patrón `.patt`) impreso en una carta.
- Además, cada carta tiene un **QR** que abre la ficha directamente.
- La página web (`index.html`) usa AR.js + A-Frame: al detectar el marcador,
  muestra el modelo 3D encima de la carta con **rotar / acercar** y una ficha
  con peligro, hábitat, distribución, tamaño y más.
- Permite entrar por QR o por menú, y conectar un **visor 3D sin AR** (arrastrar
  para girar) si la cámara no está disponible.

## Especies (8)

| id          | Nombre común                       | Venenosa |
|-------------|------------------------------------|----------|
| coral       | Coral (Serpiente coral)            | Sí       |
| cascabel    | Cascabel                              | Sí       |
| mapana      | Mapaná / Rabo de ají                | Sí       |
| verrugosa   | Verrugosa                             | Sí       |
| rombifera   | Rombífera                             | No       |
| boa         | Boa constrictora                      | No       |
| arcoiris    | Cazadora arcoíris                    | No       |
| lora        | Lora / Falsa coral (Loro)             | No       |

La lista de ids se usa para enlazar modelo, marcador, QR y ficha.

## Estructura

```
catalogo-ar/
├── index.html                 # App AR + visor 3D
├── style.css                  # Estilos de la interfaz
├── datos.json                 # Fichas de las especies (fuente de verdad)
├── modelos/<id>.glb           # Modelos 3D
├── patterns/<id>.patt         # Marcadores AR
├── cartas/
│   ├── cartas.html            # 8 cartas A4 listas para imprimir
│   └── marcadores/<id>-marcador.svg
└── herramientas/
    └── generar_cartas.py      # Regenera las cartas con el QR
```

## Publicar (GitHub Pages)

La cámara solo funciona por **HTTPS**. GitHub Pages lo da gratis:

1. Sube el contenido de `catalogo-ar/` (modelos, patterns, cartas…) a la raíz
   del repositorio `catalogo-ar`.
2. En *Settings → Pages*, elige la rama y la carpeta `/ (root)`.
3. La URL será:
   `https://adrixn1140.github.io/catalogo-ar/index.html`

> Ya está configurada en `herramientas/generar_cartas.py` (default). Solo queda
> subir la carpeta y activar Pages.

## Cartas

Las cartas ya están generadas (`cartas/cartas.html`). Impresión:

- Abre `cartas/cartas.html` en el navegador y usa *Imprimir*.
- El marcador negro tiene **10 cm de lado** (2 reglas definidas en extremos del
  SVG). Úsalo para verificar escala y re-imprimir si es necesario.
- Recomendado: imprimir a escala real (100 %), papel A4 y plastificar.

Si cambias la URL (por ejemplo tras publicar) o el orden de especies,
regenera las cartas:

```
python3 herramientas/generar_cartas.py
```

Para poner la URL definitiva en los QR:

```
BASE_URL="https://adrixn1140.github.io/catalogo-ar/index.html" \
  python3 herramientas/generar_cartas.py
```

Cada QR abre `index.html#<id>` y activa la ficha de esa especie.

## Probar en el celular

1. Imprime una carta (mejor a 100 %).
2. Abre la página publicada en el celular (Chrome/Safari).
3. Acepta el permiso de cámara y apunta a la carta.
4. La serpiente aparece sobre la carta: usa los botones para rotar/acercar.

## Añadir una especie

Requiere tres archivos con el mismo `id` (una palabra en minúsculas,
ej.: `tigra`):

1. **Modelo**: crea `modelos/<id>.glb`. El cuerpo debe quedar en el plano XZ
   (acostado sobre el marcador); la punta apunta a `+Z` y +Y es la vertical.
   (El generador usado está en `/tmp/opencode/tools/gen/gen.mjs`; crea un
   archivo por especie y ejecuta `node gen.mjs <archivo>`.)
2. **Marcador**: coloca `patterns/<id>.patt` (16×16, 3072 tokens, solo blanco
   y negro; 4 bloques: B,G,R; valor = 255 − gris) y crea el SVG de la carta
   copiando el patrón anterior en `herramientas/generar_cartas.py`.
3. **Ficha**: agrega el objeto en `datos.json` y el id en
   `ordenDeLaColeccion()` en `index.html` (también en el generador de cartas).

Verifica el modelo que renderiza A-Frame con tres.js:

```
node /tmp/opencode/tools/gen/preview.mjs
```

## Probar localmente

```
python3 -m http.server 8901
# luego abre http://localhost:8901/ en el navegador
```

(Opcional, validación sin cámara): `python3 -m http.server 8901` y abrir la
página en un navegador; si no hay cámara, el botón *Vista sin AR* sirve para
revisar los modelos.

## Recursos

- A-Frame 1.2.0: `https://aframe.io/releases/1.2.0/aframe.min.js`
- AR.js 3.4.8: `https://cdn.jsdelivr.net/gh/AR-js-org/AR.js@3.4.8/aframe/build/aframe-ar.js`
- three.js 0.160 (visor 3D, con importmap)