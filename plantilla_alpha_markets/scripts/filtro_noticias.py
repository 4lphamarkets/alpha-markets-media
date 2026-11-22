"""FILTRO DE NOTICIAS 4LPHA MARKETS (v22): puntúa candidatas de 0 a 100 y dice qué hacer con cada una.
uso: python scripts/filtro_noticias.py candidatas.json [--n 3]      (ejemplo: filtro_ejemplo.json)

Cada candidata (lista JSON de objetos). Rellenar tras BUSCAR la noticia (no antes):
 titulo            texto corto
 tema              clave para variedad: "nvidia", "bitcoin", "fed", "anthropic", "trump-china"...
 tipo              "evento" (algo que ocurre en las próximas 48 h) | "noticia" (ya ocurrió, <24 h)
                   | "patron_actual" (patrón histórico aplicado al precio de HOY) | "educativo_atemporal" | "marca"
 hora_exacta       true si hay día/hora concretos en las próximas 48 h (cierre, Fed, resultados, salida a bolsa...)
 cifra_historica   true si hay un récord/rareza verificable ("la peor semana desde 2008", "no pasaba desde el covid")
 cifra_concreta    true si la primera frase puede llevar un número exacto
 protagonista      0 ninguno · 1 conocido (índice, empresa grande, cripto top) · 2 gigante (Nvidia, Anthropic, Fed, Trump/Xi/Putin, Bitcoin)
 impacto_bolsillo  0 no · 1 indirecto · 2 "afecta a tu cartera / qué pasa mañana"
 pregunta_abierta  true si el desenlace es incierto y invita a opinar ("¿sube o cae?")
 visual            "calendario" | "grafico" | "comparacion" | "numero" | "ninguno"
 horas             antigüedad de la noticia en horas
 fuentes           nº de fuentes fiables que confirman la cifra
Pesos (hipótesis sacadas del análisis de @h.analistasoficial y @lacartabursatil; se recalibran cada viernes con nuestras vistas y "enviados/vistas").
"""
import json, sys

def puntua(c):
    p, why = 0, []
    def add(v, t):
        nonlocal p
        if v: p += v; why.append(f'{v:+d} {t}')
    add(20 if c.get('hora_exacta') else 0, 'hora/día exacto')
    add(20 if c.get('cifra_historica') else 0, 'cifra histórica/rara')
    add({0: 0, 1: 8, 2: 15}[c.get('protagonista', 0)], 'protagonista')
    add({0: 0, 1: 8, 2: 15}[c.get('impacto_bolsillo', 0)], 'impacto en el bolsillo')
    add(10 if c.get('pregunta_abierta') else 0, 'pregunta abierta')
    add(10 if c.get('visual', 'ninguno') in ('calendario', 'grafico', 'comparacion', 'numero') else 0, 'se visualiza con 1 widget')
    h = c.get('horas', 99); add(10 if h < 24 else 5 if h < 48 else 0, 'novedad')
    if not c.get('cifra_concreta'): add(-20, 'sin cifra concreta')
    t = c.get('tipo', 'noticia')
    if t == 'educativo_atemporal': add(-15, 'educativo sin gancho de hoy')
    if t == 'marca': add(-30, 'contenido de marca/autopromo')
    if c.get('fuentes', 0) < 2: add(-100, 'NO verificada (<2 fuentes)')
    return max(p, 0) if p > -50 else 0, why

def decide(s): return 'VÍDEO' if s >= 70 else 'HISTORIA/CARRUSEL' if s >= 55 else 'DESCARTAR'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 3
    if '--n' in sys.argv: args = [a for a in args if a != str(n)]
    cands = json.load(open(args[0], encoding='utf-8'))
    res = []
    for c in cands:
        s, why = puntua(c); res.append((s, c, why))
    res.sort(key=lambda x: -x[0])
    print(f'{"PTS":>3}  {"DECISIÓN":<18} TEMA / TÍTULO')
    for s, c, why in res: print(f'{s:>3}  {decide(s):<18} [{c.get("tema","-")}] {c["titulo"]}\n     ' + ' · '.join(why))
    # selección de los N vídeos: mayor puntuación (>=60), máx. 1 por tema
    sel, temas = [], set()
    for s, c, _ in res:
        if s >= 60 and c.get('tema') not in temas: sel.append(c['titulo']); temas.add(c.get('tema'))
        if len(sel) == n: break
    print('\nVÍDEOS DE HOY (máx. 1 por tema):'); [print(' ·', t) for t in sel] or print(' (ninguna llega a 60: hoy mejor menos vídeos pero buenos)')
