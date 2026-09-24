#!/usr/bin/env python3
"""Genera cartas imprimibles del catálogo AR.

Cada carta A4 contiene: ficha de la especie, QR (abre la página web de esa
especie) y el marcador AR que sirve de ancla al modelo 3D.

Uso:
    python3 herramientas/generar_cartas.py
    # opcional: BASE_URL=https://adrixn1140.github.io/catalogo-ar python3 herramientas/generar_cartas.py
"""
import json
import os
import qrcode
from qrcode.image.svg import SvgPathImage

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = os.environ.get("BASE_URL", "https://adrixn1140.github.io/catalogo-ar/index.html")
SALIDA = os.path.join(RAIZ, "cartas", "cartas.html")


def qr_svg(texto, borde=2):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=borde)
    qr.add_data(texto)
    qr.make(fit=True)
    im = qr.make_image(image_factory=SvgPathImage)
    return im.to_string().decode()


def marcador_svg(especie_id):
    ruta = os.path.join(RAIZ, "cartas", "marcadores", especie_id + "-marcador.svg")
    with open(ruta) as f:
        return f.read()


def escap(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("—", "&#8212;"))


def tarjeta_html(e):
    perma = BASE_URL + "#" + e["id"]
    acc = e.get("color", "#2a9d2a")
    acc_osc = e.get("color", "#2a9d2a")
    nivel = "VENENOSA" if e["venenosa"] else "NO VENENOSA"
    pill_class = "ven" if e["venenosa"] else "seguro"
    qr = qr_svg(perma)
    mk = marcador_svg(e["id"])

    return f"""
<div class="card" style="--acc:{acc};--acc-osc:{acc_osc};">
  <div class="cabecera">
    <span class="logo">SERPIENTES DE COLOMBIA</span>
    <span class="sub">Catálogo en Realidad Aumentada</span>
  </div>
  <div class="cuerpo">
    <div class="col-info">
      <span class="pill {pill_class}">{nivel}</span>
      <h1 class="nombre">{escap(e['nombre'])}</h1>
      <p class="cient">{(escap(e['cientifico']))}</p>
      <p class="familia">Familia: {escap(e['familia'])}</p>
      <ul class="mini-ficha">
        <li><b>Hábitat:</b> {escap(e['habitat'])}</li>
        <li><b>Tamaño:</b> {escap(e['tamano'])}</li>
        <li><b>Alimentación:</b> {escap(e['dieta'])}</li>
      </ul>
      <div class="qr">
        <div class="qr-img">{qr}</div>
        <div class="qr-txt">Escanea el QR o entra a<br><code>{escap(perma)}</code></div>
      </div>
    </div>
    <div class="col-marker">
      <div class="marco">
        <div class="marker">{mk}</div>
      </div>
      <div class="marcar-txt">▼ Apunta la cámara aquí ▼</div>
    </div>
  </div>
  <div class="pie">Permite el acceso a la cámara en el navegador y apunta este marcador para ver el modelo 3D.</div>
</div>
"""


def main():
    with open(os.path.join(RAIZ, "datos.json")) as f:
        especies = json.load(f)
    orden = ["coral", "cascabel", "mapana", "verrugosa",
             "rombifera", "boa", "arcoiris", "lora"]
    tarjetas = []
    for e in especies:
        if e["id"] != "coral" and e["id"] not in orden:
            continue
    by_id = {e["id"]: e for e in especies}
    for sid in orden:
        tarjetas.append(tarjeta_html(by_id[sid]))

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Cartas AR · Serpientes de Colombia</title>
<style>
  * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  body {{ margin: 0; background: #e8ece8; font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
  .card {{
    width: 210mm; height: 297mm;
    margin: 0 auto;
    background: #fdfcf7;
    page-break-after: always;
    break-after: page;
    display: flex; flex-direction: column;
    overflow: hidden;
  }}
  .card:last-child {{ page-break-after: auto; }}
  .cabecera {{
    background: var(--acc-osc);
    color: #fff;
    padding: 26px 28px 22px;
    display: flex; align-items: baseline; justify-content: space-between;
  }}
  .logo {{ font-size: 30px; font-weight: 900; letter-spacing: 2px; }}
  .sub {{ font-size: 14px; opacity: .9; }}
  .cuerpo {{ flex: 1; display: flex; gap: 20px; padding: 26px 28px; }}
  .col-info {{ flex: 1; min-width: 0; display: flex; flex-direction: column; }}
  .pill {{
    align-self: flex-start; padding: 7px 16px; border-radius: 999px;
    font-weight: 800; font-size: 15px; letter-spacing: .6px; color: #fff;
    background: var(--acc);
  }}
  .pill.ven {{ background: #c1121f; }}
  .pill.seguro {{ background: #2a9d2a; }}
  .nombre {{ margin: 12px 0 4px; font-size: 40px; line-height: 1.05; color: #1d2b24; }}
  .cient {{ margin: 0; font-style: italic; font-size: 19px; color: #4a5560; }}
  .familia {{ margin: 8px 0 14px; font-weight: 600; color: var(--acc-osc); }}
  .mini-ficha {{ margin: 0; padding: 0; list-style: none; font-size: 15px; line-height: 1.5; color: #333; }}
  .mini-ficha li {{ margin-bottom: 8px; }}
  .qr {{ margin-top: auto; padding-top: 18px; display: flex; align-items: center; gap: 14px; }}
  .qr-img {{ width: 94px; height: 94px; flex-shrink: 0; }}
  .qr-img svg {{ width: 94px; height: 94px; }}
  .qr-txt {{ font-size: 12.5px; color: #4a5560; line-height: 1.35; }}
  .qr-txt code {{ font-size: 11px; word-break: break-all; }}
  .col-marker {{ width: 40%; flex-shrink: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; }}
  .marco {{
    width: 102mm; height: 102mm;
    padding: 6mm;
    border: 2.5mm solid var(--acc-osc);
    background: #fff;
    box-shadow: 0 4px 18px rgba(0,0,0,.18);
    border-radius: 3mm;
  }}
  .marker {{ width: 100%; height: 100%; }}
  .marker svg {{ width: 100%; height: 100%; display: block; }}
  .marcar-txt {{ font-weight: 700; font-size: 13px; letter-spacing: 1.5px; color: var(--acc-osc); }}
  .pie {{
    padding: 14px 28px;
    font-size: 12.5px; color: #6b7280; text-align: center;
    border-top: 1px solid #e5e3da;
  }}
  @media print {{ body {{ background: none; }} }}
</style>
</head>
<body>
{''.join(tarjetas)}
</body>
</html>
"""
    with open(SALIDA, "w") as f:
        f.write(html)
    print("Cartas generadas:", SALIDA)


if __name__ == "__main__":
    main()