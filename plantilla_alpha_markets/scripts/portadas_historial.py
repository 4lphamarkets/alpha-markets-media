"""HISTORIAL ANTI-REPETICIÓN DE PORTADAS (v10)
uso: python scripts/portadas_historial.py        → muestra las últimas portadas y los conceptos libres del catálogo
     (también: python scripts/entrega.py --historial)

El historial se guarda en DOS sitios para que sobreviva entre chats y versiones de la plantilla:
  - %USERPROFILE%/.alpha_markets/historial_portadas.json  (+ copia de cada HTML en .alpha_markets/portadas/)
  - portadas/historial.json dentro de la plantilla        (+ copia en portadas/historial/)
entrega.py lo usa para BLOQUEAR la entrega si:
  - las dos portadas usan el mismo arquetipo, o uno de los prohibidos (estructuras v8-v9),
  - algún arquetipo se usó en las últimas VENTANA portadas,
  - el HTML se parece demasiado (estructura) a otra portada anterior o a la otra del mismo vídeo."""
import datetime, difflib, glob, json, os, re, shutil, sys

D = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
U = os.path.join(os.path.expanduser('~'), '.alpha_markets')
HIST = [os.path.join(U, 'historial_portadas.json'), os.path.join(D, 'portadas', 'historial.json')]
COPIAS = [os.path.join(U, 'portadas'), os.path.join(D, 'portadas', 'historial')]
PROHIBIDOS = {'plantilla_v8', 'impacto_v8', 'plantilla', 'impacto', 'globo_tarjeta', 'grieta_duelo'}
ESTILOS_FIJOS = {'foto_epica'}   # v11: estilos favoritos del usuario → SE PUEDEN repetir en todos los vídeos (no cuentan para la ventana ni el parecido con anteriores)
VENTANA = 8          # nº de portadas anteriores (≈ 4 vídeos) cuyos arquetipos no se pueden repetir
UMBRAL = 0.55        # parecido estructural máximo permitido entre dos HTML (0 = nada que ver, 1 = idénticos)
FORZAR = '--forzar-repeticion' in sys.argv   # solo si el USUARIO pide repetir un diseño concreto

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

def cargar():
    vistos, res = set(), []
    for h in HIST:
        try: datos = json.load(open(h, encoding='utf-8'))
        except Exception: continue
        for e in datos:
            k = (e.get('slug'), e.get('arquetipo'), e.get('fecha'))
            if k not in vistos: vistos.add(k); res.append(e)
    return sorted(res, key=lambda e: e.get('fecha', ''))

def firma(html):
    """Estructura del diseño sin textos ni números: etiquetas, clases, propiedades CSS y funciones JS."""
    h = re.sub(r'<!--.*?-->|/\*.*?\*/', ' ', html, flags=re.S)
    h = re.sub(r'<script>window\.D = .*?</script>', ' ', h, flags=re.S)
    h = re.sub(r'>[^<>{}]*<', '><', h)                       # fuera textos visibles
    h = re.sub(r'(["\'`]).*?\1', ' ', h, flags=re.S)          # fuera cadenas (titulares, rutas, colores)
    h = re.sub(r'[0-9.#]+[a-z%]*', ' ', h.lower())            # fuera números, medidas y colores
    return re.findall(r'[a-z][a-z\-_]+', h)

def parecido(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()

def referencias(excluir_slug):
    """HTML anteriores contra los que comparar: estructuras antiguas v8-v9 + diseños guardados de otros vídeos."""
    refs = {os.path.basename(p): p for p in glob.glob(os.path.join(D, 'portadas', 'antiguas', '*.html'))}
    for c in COPIAS:
        for p in glob.glob(os.path.join(c, '*.html')):
            if not os.path.basename(p).startswith(excluir_slug + '__'): refs.setdefault(os.path.basename(p), p)
    return refs

def mostrar():
    H = cargar()
    print(f'ÚLTIMAS PORTADAS (no repetir los arquetipos de las {VENTANA} más recientes):')
    for e in H[-12:]: print(f"  {e.get('fecha', '')[:10]}  {e.get('slug', ''):<32} {e.get('arquetipo', ''):<24} {e.get('concepto', '')}")
    if not H: print('  (vacío)')
    usados = ({e.get('arquetipo') for e in H[-VENTANA:]} - ESTILOS_FIJOS) | PROHIBIDOS
    try:
        cat = re.findall(r'^\| `([a-z_]+)` \|', open(os.path.join(D, 'portadas', 'CATALOGO.md'), encoding='utf-8').read(), flags=re.M)
        print('\nCONCEPTOS LIBRES DEL CATÁLOGO (o inventa uno nuevo):'); print('  ' + ', '.join(a for a in cat if a not in usados))
    except OSError: pass
    print('\nESTILOS FIJOS (repetibles en cada vídeo): ' + ', '.join(sorted(ESTILOS_FIJOS)) + '  → portadas/estilos/')
    print('PROHIBIDOS SIEMPRE:', ', '.join(sorted(PROHIBIDOS)))
    return 0

def validar_disenos(disenos, slug):
    def fallo(m): sys.exit('PORTADAS RECHAZADAS: ' + m + '\n→ Diseña portadas nuevas desde cero (ver portadas/CATALOGO.md y python scripts/entrega.py --historial).')
    if not isinstance(disenos, list) or len(disenos) < 2:
        fallo('falta "portada.disenos" en entrega.json con DOS diseños propios: '
              '[{"html": "portadas/disenos/<slug>_a.html", "arquetipo": "...", "concepto": "...", "tipografia": "...", "paleta": "..."}, {...}]')
    disenos = disenos[:2]
    for d in disenos:
        for k in ('html', 'arquetipo', 'concepto'):
            if not d.get(k): fallo(f'a un diseño le falta "{k}"')
        if not os.path.isfile(os.path.join(D, d['html'])): fallo(f'no existe {d["html"]}')
        d['arquetipo'] = re.sub(r'[^a-z0-9_]+', '_', d['arquetipo'].lower()).strip('_')
        if d['arquetipo'] in PROHIBIDOS: fallo(f'el arquetipo "{d["arquetipo"]}" está prohibido (estructura antigua repetida)')
    a, b = disenos
    if a['arquetipo'] == b['arquetipo']: fallo('las dos portadas usan el mismo arquetipo')
    for k in ('tipografia', 'paleta'):
        if a.get(k) and a.get(k) == b.get(k): fallo(f'las dos portadas tienen la misma {k} ("{a[k]}"): cámbiala en una')
    fijos = [i for i, d in enumerate(disenos) if d['arquetipo'] in ESTILOS_FIJOS]
    recientes = [e for e in cargar() if e.get('slug') != slug][-VENTANA:]
    usados = {e.get('arquetipo') for e in recientes}
    for d in disenos:
        if d['arquetipo'] in usados and d['arquetipo'] not in ESTILOS_FIJOS and not FORZAR:
            fallo(f'el arquetipo "{d["arquetipo"]}" se usó en las últimas {VENTANA} portadas')
    firmas = [firma(open(os.path.join(D, d['html']), encoding='utf-8').read()) for d in disenos]
    p = parecido(*firmas)
    print(f'parecido entre portada 1 y 2: {p:.2f} (máx. {UMBRAL})')
    if p > UMBRAL: fallo('las dos portadas tienen casi la misma estructura HTML')
    for nombre, ruta in referencias(slug).items():
        f = firma(open(ruta, encoding='utf-8').read())
        for i, fi in enumerate(firmas):
            if i in fijos: continue
            q = parecido(fi, f)
            if q > UMBRAL and not FORZAR: fallo(f'la portada {i + 1} se parece demasiado ({q:.2f}) a una anterior: {nombre}')
    return disenos

def guardar_historial(disenos, slug):
    ahora = datetime.datetime.now().isoformat(timespec='seconds')
    nuevas = [{'fecha': ahora, 'slug': slug, 'arquetipo': d['arquetipo'], 'concepto': d.get('concepto', ''),
               'tipografia': d.get('tipografia', ''), 'paleta': d.get('paleta', '')} for d in disenos]
    H = [e for e in cargar() if e.get('slug') != slug] + nuevas
    for h, c in zip(HIST, COPIAS):
        try:
            os.makedirs(os.path.dirname(h), exist_ok=True); os.makedirs(c, exist_ok=True)
            json.dump(H, open(h, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            for i, d in enumerate(disenos):
                shutil.copyfile(os.path.join(D, d['html']), os.path.join(c, f'{slug}__{i + 1}_{d["arquetipo"]}.html'))
        except OSError as e: print('AVISO: no se pudo guardar el historial en', h, e)

if __name__ == '__main__':
    sys.exit(mostrar())


def guardar_historial_simple(items, slug):
    """v28: anota en el historial las portadas hechas con los diseños de historias/estilos (sin HTML propio)."""
    ahora = datetime.datetime.now().isoformat(timespec='seconds')
    nuevas = [{'fecha': ahora, 'slug': slug, 'arquetipo': d['arquetipo'], 'concepto': d.get('concepto', ''), 'tipografia': '', 'paleta': ''} for d in items]
    H = [e for e in cargar() if e.get('slug') != slug] + nuevas
    for h in HIST:
        try:
            os.makedirs(os.path.dirname(h), exist_ok=True); json.dump(H, open(h, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        except OSError as e: print('AVISO: no se pudo guardar el historial en', h, e)
