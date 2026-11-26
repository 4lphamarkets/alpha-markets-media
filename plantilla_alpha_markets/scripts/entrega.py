"""ENTREGA POST-RENDER (se ejecuta SIEMPRE justo después de final.py, sin que el usuario lo pida).
uso: python scripts/entrega.py [video=out/video_final.mp4] [datos=entrega.json]

Lee entrega.json (descripción SEO + hashtags + datos de portada, escrito por Claude para cada vídeo) y genera en out/entrega/:
  1) <slug>_descripcion.txt  → título + descripción + hashtags, texto limpio sin rótulos ni palabras clave (v12; bloc de notas, UTF-8, CRLF)
  2) <slug>_portada_1.jpg + <slug>_portada_2.jpg → las DOS portadas diseñadas desde cero para este vídeo
     (v10: portada.disenos de entrega.json; se validan contra el historial anti-repetición; JPG calidad 95, sin submuestreo)
     python scripts/entrega.py --historial  → ver portadas anteriores y conceptos libres ANTES de diseñar
  3) <slug>_video.mp4        → copia del vídeo final
y lo empaqueta todo en out/<slug>_ALPHA_MARKETS.zip."""
import base64, io, json, os, re, shutil, subprocess, sys, unicodedata, zipfile
from PIL import Image, ImageOps

D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from portadas_historial import mostrar, validar_disenos, guardar_historial   # v10: anti-repetición de portadas
if '--historial' in sys.argv: sys.exit(mostrar())
sys.argv = [a for a in sys.argv if not a.startswith('--')]
video =os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(D, 'out', 'video_final.mp4')
datos = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(D, 'entrega.json')
if not os.path.exists(video): sys.exit(f'No existe el vídeo: {video}')
if not os.path.exists(datos): sys.exit(f'No existe {datos}: créalo primero (ver entrega_ejemplo.json)')
E = json.load(open(datos, encoding='utf-8-sig'))   # -sig: acepta JSON con o sin BOM
faltan = [k for k in ('slug', 'titulo_seo', 'descripcion', 'hashtags', 'portada') if not E.get(k)]   # v23: error claro en vez de KeyError
if faltan: sys.exit(f'{os.path.basename(datos)}: faltan campos obligatorios: {faltan} (ver entrega_ejemplo.json)')

slug = re.sub(r'[^a-z0-9_]+', '_', E['slug'].lower()).strip('_')
P = E['portada']
tags = ['#' + h.lstrip('#').replace(' ', '') for h in E['hashtags']]

# --- comprobaciones SEO (Instagram: máx. 2.200 caracteres y 30 hashtags; primera línea = gancho visible) ---
desc = E['descripcion'].strip()
gancho = desc.splitlines()[0]
texto_post = desc + '\n\n' + ' '.join(tags)
avisos = []
if len(gancho) > 125: avisos.append(f'el gancho (1ª línea) tiene {len(gancho)} caracteres; Instagram corta a ~125')
if len(texto_post) > 2200: avisos.append(f'descripción + hashtags = {len(texto_post)} caracteres (> 2.200)')
if not 8 <= len(tags) <= 15: avisos.append(f'{len(tags)} hashtags (recomendado 8-15)')   # v23: alineado con LEEME (antes avisaba solo fuera de 5-15)
if len(set(t.lower() for t in tags)) != len(tags): avisos.append('hay hashtags repetidos')
if not 40 <= len(E['titulo_seo']) <= 75: avisos.append(f'titulo_seo de {len(E["titulo_seo"])} caracteres (recomendado 50-70)')
if '@4lphamarkets' not in desc: avisos.append('falta el CTA «Sígueme en @4lphamarkets…»')
if 'consejo financiero' not in desc.lower(): avisos.append('falta el aviso "Esto no es consejo financiero"')
for a in avisos: print('AVISO:', a)

out = os.path.join(D, 'out', 'entrega'); os.makedirs(out, exist_ok=True); os.makedirs(os.path.join(D, 'tmp'), exist_ok=True)

# --- 1) descripción en bloc de notas ---
txt = os.path.join(out, f'{slug}_descripcion.txt')
# v12: texto LIMPIO, listo para copiar y pegar: título + descripción + hashtags, SIN rótulos y SIN palabras clave
partes = [E['titulo_seo'].strip(), '', texto_post]
with open(txt, 'w', encoding='utf-8-sig', newline='\r\n') as f: f.write('\n'.join(partes) + '\n')

# --- 2) portada ---
def icono(n):
    if not n: return ''
    d = re.search(r'<path d="([^"]+)"', open(os.path.join(D, 'img', f'{n}.svg'), encoding='utf-8').read()).group(1)
    return f'<svg viewBox="0 0 24 24" width="100%" height="100%"><path fill="currentColor" d="{d}"/></svg>'
# --- v8: persona + logos en la portada ---
def norm(s): return re.sub(r'[^a-z0-9]+', '_', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()).strip('_')
EXT = ('.png', '.webp', '.jpg', '.jpeg', '.svg')
def buscar(nombre, carpetas):
    """Busca <nombre>.<ext> (o una ruta directa) en las carpetas dadas. Devuelve la ruta o None."""
    if not nombre: return None
    for c in [nombre, os.path.join(D, nombre)]:
        if os.path.isfile(c): return c
    for carpeta in carpetas:
        for e in EXT:
            p = os.path.join(D, carpeta, norm(os.path.splitext(nombre)[0]) + e)
            if os.path.isfile(p): return p
    return None
def color_dominante(im):
    """Color más saturado y frecuente de un logo (para el aro y el brillo)."""
    cuenta = {}
    px = im.convert('RGBA').resize((64, 64))
    for r, g, b, a in (px.get_flattened_data() if hasattr(px, 'get_flattened_data') else px.getdata()):
        if a < 200 or max(r, g, b) < 60 or max(r, g, b) - min(r, g, b) < 60: continue   # descarta transparente, negro, blanco y gris
        k = (r // 32, g // 32, b // 32); n, *_ = cuenta.get(k, (0,)); cuenta[k] = (n + 1, r, g, b)
    if not cuenta: return '#34F5B0'
    _, r, g, b = max(cuenta.values())
    return '#%02X%02X%02X' % (r, g, b)
def data_uri_raster(path, maxlado=1200):
    im = ImageOps.exif_transpose(Image.open(path)); im.thumbnail((maxlado, maxlado))
    if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGBA')
    b = io.BytesIO(); im.save(b, 'PNG'); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode(), im
def data_uri_svg(path, color):
    s = open(path, encoding='utf-8').read()
    if 'fill=' not in s and 'fill:' not in s:            # SVG monocromo (simple-icons): se pinta con su color de marca
        s = re.sub(r'<svg\b', f'<svg fill="{color}"', s, count=1)
    return 'data:image/svg+xml;base64,' + base64.b64encode(s.encode('utf-8')).decode()
def tiene_recorte(im):
    if im.mode != 'RGBA': return False
    a = im.getchannel('A'); w, h = a.size
    borde = [a.getpixel((x, 0)) for x in range(0, w, 4)] + [a.getpixel((0, y)) for y in range(0, h, 4)] + [a.getpixel((w - 1, y)) for y in range(0, h, 4)]
    return sum(v < 128 for v in borde) > len(borde) * .5   # fondo transparente en los bordes = foto recortada

def resolver_persona(pe):
    pe = pe if isinstance(pe, dict) else {'nombre': pe}
    nombre = pe.get('nombre', '')
    ruta = buscar(pe.get('foto') or nombre, ['img/personas'])
    if not ruta:
        sys.exit(f'FALTA LA FOTO DE "{nombre or pe.get("foto")}": pídesela al usuario, guárdala en img/personas/{norm(nombre or "persona")}.jpg '
                 '(o .png recortada sin fondo) y vuelve a ejecutar entrega.py.')
    src, im = data_uri_raster(ruta)
    print('persona:', os.path.relpath(ruta, D), '(recortada)' if pe.get('recorte', tiene_recorte(im)) else '(círculo)')
    return {'src': src, 'nombre': pe.get('mostrar_nombre', nombre) if pe.get('etiqueta_nombre', True) else '',
            'recorte': pe.get('recorte', tiene_recorte(im)), 'encuadre': pe.get('encuadre', '50% 30%')}
persona = resolver_persona(P['persona']) if P.get('persona') else None
# v11: estilo "foto_epica" → varias personas (hasta 3) en portada.personas
personas = [resolver_persona(x) for x in (P.get('personas') or [])][:3]
if personas and not persona: persona = personas[0]

logos = []
lista = P.get('logos') or ([P['icono']] if P.get('icono') else [])   # compatibilidad v7: "icono" = un logo
for L in lista:
    L = L if isinstance(L, dict) else {'archivo': L}
    ruta = buscar(L.get('archivo'), ['img/logos', 'img'])
    if not ruta:
        sys.exit(f'FALTA EL LOGO "{L.get("archivo")}": descárgalo con  python scripts/logos.py {L.get("archivo")}  '
                 '(o guárdalo en img/logos/) y vuelve a ejecutar entrega.py.')
    if ruta.lower().endswith('.svg'):
        color = L.get('color') or (P.get('icono_color') if L.get('archivo') == P.get('icono') else None) or '#34F5B0'
        logos.append({'src': data_uri_svg(ruta, color), 'color': color, 'modo': L.get('modo', 'insignia')})
    else:
        src, im = data_uri_raster(ruta, 600)
        logos.append({'src': src, 'color': L.get('color') or color_dominante(im), 'modo': L.get('modo', 'moneda')})
    print('logo   :', os.path.relpath(ruta, D), logos[-1]['color'], logos[-1]['modo'])

data = {'titulo': P.get('titulo', []), 'etiqueta': P.get('etiqueta', ''), 'cifra': P.get('cifra', ''), 'pie': P.get('pie', ''),
        'cifra_etiqueta': P.get('cifra_etiqueta', ''), 'cifra_nombre': P.get('cifra_nombre', ''), 'semilla': slug,
        'icono_svg': icono(P.get('icono')), 'icono_color': P.get('icono_color', '#34F5B0'),
        'persona': persona, 'logos': logos, 'union': P.get('union', 'VS'),
        'fondo': P.get('fondo', ''), 'tono': P.get('tono', ''),
        'personas': personas, 'banderas': P.get('banderas', []), 'fecha_sede': P.get('fecha_sede', ''), 'skyline': P.get('skyline', True)}
# estilo por defecto = 'plantilla' (v7/v8: globo + tarjeta de cifra + persona/logos). 'clasico' = v6 con fotograma del vídeo de fondo.
clasico = P.get('estilo') == 'clasico'
plantilla_html = 'portada_clasica.html' if clasico else 'portada.html'
def render_portada(html, datos, jpg, arg):
    h = open(os.path.join(D, html), encoding='utf-8').read()
    js = json.dumps(datos, ensure_ascii=False)
    if '{{DATA}}' in h: h = h.replace('{{DATA}}', js)                       # plantillas antiguas
    else: h = re.sub(r'<head[^>]*>', lambda m: m.group(0) + f'<script>window.D = {js};</script>', h, count=1)   # v10: window.D
    open(os.path.join(D, 'portada_index.html'), 'w', encoding='utf-8').write(h)
    subprocess.run(['node', os.path.join(D, 'scripts', 'render.js'), 'portada', arg], check=True, cwd=D)
    Image.open(os.path.join(D, 'tmp', 'portada.png')).convert('RGB').save(jpg, 'JPEG', quality=95, subsampling=0, optimize=True)
    return jpg

if P.get('estilo') in ('v8', 'clasico'):
    # Estilos antiguos: SOLO si el usuario lo pide expresamente (repetían siempre la misma estructura).
    A = os.path.join('portadas', 'antiguas')
    jpg1 = render_portada(os.path.join(A, plantilla_html), data, os.path.join(out, f'{slug}_portada_1.jpg'), str(P.get('fotograma', 3)) if clasico else 'sinfondo')
    P2 = P.get('portada2', {})
    data2 = dict(data, **{k: P2[k] for k in ('titulo', 'cifra', 'cifra_etiqueta', 'cifra_nombre', 'pie', 'tono') if k in P2}); data2['duelo'] = P2.get('duelo')
    jpg2 = render_portada(os.path.join(A, 'portada_impacto.html'), data2, os.path.join(out, f'{slug}_portada_2.jpg'), 'sinfondo')
    portadas = (jpg1, jpg2)
elif not P.get('disenos'):
    # v28 (26-11-2026, orden de Antonio): PORTADAS con los 10 diseños radicalmente distintos de las historias (historias/estilos/).
    # La antigua "foto_epica" (BITCOIN BLOQUEADO con globo y moneda) está retirada: pasada de moda.
    # portada en entrega.json: {"t1":"BITCOIN","t2":"BLOQUEADO 20 AÑOS","tag":"RESERVA EEUU","sub":"...","rows":[{"n":"BTC","s":"GOBIERNO","p":"306.795","c":"","cc":"v"}], "estilos":["gigante","periodico"] (opcional)}
    # (si falta t1/t2 se usa portada.titulo; máx. 2 filas; cada portada del vídeo usa un diseño DISTINTO y no se repiten los de los últimos 4 vídeos)
    sys.path.insert(0, os.path.join(D, 'historias', 'estilos')); import make_story_estilos as ms
    tit = [re.sub(r'[*]', '', t) for t in (P.get('titulo') or [])]
    base = {'t1': P.get('t1') or (tit[0] if tit else ''), 't2': P.get('t2') or ' '.join(tit[1:]), 'tag': P.get('tag') or P.get('etiqueta', ''),
            'sub': P.get('sub', ''), 'fuente': P.get('fuente', ''), 'rows': (P.get('rows') or ([{'n': P.get('cifra_nombre', ''), 's': P.get('cifra_etiqueta', ''), 'p': P.get('cifra', ''), 'c': '', 'cc': 'r' if P.get('tono') == 'rojo' else 'v'}] if P.get('cifra') else []))[:2]}
    if P.get('iconos'): base['icono'] = P['iconos']          # v29: pegatinas que ilustran la portada (lock bank bomb magnet rocket fire shield doc ...)
    if P.get('logo'): base['logo'] = P['logo']                # btc|eth|sol (moneda)
    if P.get('dir'): base['dir'] = P['dir']
    usados = {e.get('arquetipo') for e in __import__('portadas_historial').cargar()[-8:]}
    libres = [e for e in ms.ORDEN if 'est_' + e not in usados] or list(ms.ORDEN)
    elegidos = [e for e in (P.get('estilos') or []) if e in ms.FN][:2]
    if len(elegidos) < 2:
        k = sum(map(ord, slug)) % len(libres); elegidos = elegidos + [e for e in (libres[k:] + libres[:k]) if e not in elegidos]
        if len(elegidos) > 2: elegidos = [elegidos[0], elegidos[len(elegidos) // 2 if len(elegidos) > 3 else 1]] if not P.get('estilos') else elegidos[:2]
    portadas = []
    for i, est in enumerate(elegidos[:2]):
        png = os.path.join(D, 'tmp', f'portada_est_{i}.png'); ms.render(base, png, est)
        jpg = os.path.join(out, f'{slug}_portada_{i + 1}.jpg'); Image.open(png).convert('RGB').save(jpg, 'JPEG', quality=95, subsampling=0, optimize=True); os.remove(png); portadas.append(jpg)
        print('portada', i + 1, '→ diseño', est)
    portadas = tuple(portadas)
    guardar_historial([{'html': 'historias/estilos/make_story_estilos.py', 'arquetipo': 'est_' + e, 'concepto': f'Portada diseño {e}: ' + base['t1'] + ' ' + base['t2'], 'tipografia': e, 'paleta': e} for e in elegidos[:2]], slug) if False else __import__('portadas_historial').guardar_historial_simple([{'arquetipo': 'est_' + e, 'concepto': f'Portada diseño {e}: ' + base['t1'] + ' ' + base['t2']} for e in elegidos[:2]], slug)
else:
    # v10: DOS portadas DISEÑADAS DESDE CERO para este vídeo (portada.disenos en entrega.json), validadas contra el historial.
    disenos = validar_disenos(P.get('disenos'), slug)
    portadas = tuple(render_portada(d['html'], data, os.path.join(out, f'{slug}_portada_{i + 1}.jpg'), 'sinfondo') for i, d in enumerate(disenos))
    guardar_historial(disenos, slug)

# --- 3) vídeo + zip ---
mp4 = os.path.join(out, f'{slug}_video.mp4')
if os.path.abspath(video) != mp4: shutil.copyfile(video, mp4)
zp = os.path.join(D, 'out', f'{slug}_ALPHA_MARKETS.zip')
archivos = (mp4, *portadas, txt)
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in archivos: z.write(p, f'{slug}_ALPHA_MARKETS/{os.path.basename(p)}')

try: os.remove(os.path.join(D, 'portada_index.html'))   # v23: archivo temporal de 2-3 MB con las imágenes incrustadas; no debe quedarse en la plantilla
except OSError: pass
print('ENTREGA LISTA')
print('  video :', video)
print('  zip   :', zp, '(opcional: al usuario se le envían los 4 archivos sueltos, sin comprimir)')
for p in archivos: print('   -', os.path.basename(p), f'{os.path.getsize(p)/1e6:.2f} MB')
