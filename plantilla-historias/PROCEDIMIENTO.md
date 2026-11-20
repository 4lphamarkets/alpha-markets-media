# PROCEDIMIENTO · historias diarias ALPHA MARKETS (Cripto hoy / Wall Street hoy)

Carpeta: `plantilla-historias/` del repo `4lphamarkets/alpha-markets-media`. **NO SE BORRA NUNCA** (ver `LEEME_NO_BORRAR.md`).
Probado el 20-11-2026 con datos reales de CoinMarketCap e Investing.com.

## 0. Antes de nada
- Comprobar que el generador funciona: `cd plantilla-historias && python3 build_story.py --selftest` → debe acabar en `SELFTEST OK`.
  Si falla: NO publicar; avisar a Antonio por notificación con el error.
- Los datos SOLO se leen con el **navegador integrado** (`mcp__remote-devices__Claude_Browser__*`). El shell no tiene internet; WebSearch no sirve para precios; CNN devuelve 451 (no usar).
- Si el navegador pide permiso para un sitio: `request_access` con scope `site`.

## 1. Cripto hoy (CoinMarketCap)
1. `navigate` a `https://coinmarketcap.com/` (esperar a que cargue la tabla).
2. Ejecutar con `javascript_tool` (action `javascript_exec`) este script. Devuelve un JSON como texto, o `{"error": ...}`:

```js
(() => { const num=s=>parseFloat(String(s).replace(/[$,%\s]/g,'').replace(/,/g,'')); const hs=[...document.querySelectorAll('table thead th')].map(h=>h.innerText.trim()); const i=hs.findIndex(h=>/^24h/.test(h)); if(i<0) return {error:'sin columna 24h'}; const want=['BTC','HYPE','ETH','SOL','BNB','ZEC']; const out={}; for(const r of document.querySelectorAll('table tbody tr')){const s=(r.querySelector('p.coin-item-symbol')||{}).textContent; if(!want.includes(s)||out[s])continue; const t=r.querySelectorAll('td'); const c=t[i]; const dn=!!c.querySelector('.icon-Caret-down'), up=!!c.querySelector('.icon-Caret-up'); if(!dn&&!up) return {error:'sin flecha en '+s}; const mag=Math.abs(num(c.innerText)); out[s]={price:num(t[3].innerText), change:dn?-mag:mag, change_text:(dn?'-':'+')+mag+'%'}} const miss=want.filter(w=>!out[w]); if(miss.length) return {error:'faltan '+miss.join(',')}; let fng=null; for(const e of document.querySelectorAll('*')){ if(e.children.length==0 && /^Fear\s*&\s*Greed$/i.test(e.textContent.trim())){ const m=(e.parentElement.innerText||'').match(/Greed\s*\n?\s*(\d{1,3})\b/); if(m){fng=+m[1];break;} } } if(fng===null) return {error:'sin Fear & Greed'}; out.FNG=fng; return JSON.stringify(out)})()
```

- El **signo** sale de la flecha `icon-Caret-up/down` de la columna 24h (el texto plano no lleva signo). El script ya lo aplica.
- Si devuelve `error`, recargar la página una vez y repetir. Si vuelve a fallar: NO publicar y avisar.

## 2. Wall Street hoy (Investing.com) · SIN Fear & Greed
1. `navigate` a `https://www.investing.com/` (cualquier página del dominio sirve; el script usa `fetch` del mismo origen).
2. Ejecutar este script (lee las 8 fichas, comprueba que el título de cada página es el esperado y calcula el signo):

```js
(async () => { const P={SPX:['/indices/us-spx-500',/S&P 500/],NDX:['/indices/nasdaq-composite',/NASDAQ Composite/i],AAPL:['/equities/apple-computer-inc',/Apple/],AMZN:['/equities/amazon-com-inc',/Amazon/],NVDA:['/equities/nvidia-corp',/Nvidia/i],INTC:['/equities/intel-corp',/Intel/],AMD:['/equities/adv-micro-device',/AMD/],ANT:['/equities/anthropic',/Anthropic/]}; const num=s=>parseFloat(String(s).replace(/[^0-9.\-]/g,'')); const out={}; for(const [k,[u,re]] of Object.entries(P)){ const r=await fetch(u,{credentials:'include'}); if(r.status!==200) return {error:k+' HTTP '+r.status}; const d=new DOMParser().parseFromString(await r.text(),'text/html'); if(!re.test(d.title)) return {error:k+' título inesperado: '+d.title}; const g=n=>{const e=d.querySelector('[data-test="'+n+'"]'); return e?e.textContent.trim():null}; const last=g('instrument-price-last'), pct=g('instrument-price-change-percent'); if(!last||!pct) return {error:k+' sin precio/variación'}; const sign=/^\(?\s*-|−/.test(pct)?-1:1; const mag=Math.abs(num(pct)); out[k]={price:num(last), change:sign*mag, change_text:(sign<0?'-':'+')+mag+'%'} } return JSON.stringify(out) })()
```

- Mercado de EEUU abierto de 15:30 a 22:00 (Madrid). Festivos de la bolsa de EEUU (p. ej. Acción de Gracias, jueves 26-11-2026): **no publicar** y avisar.
- Si algo falla o un valor falta: NO publicar y avisar. Nunca inventar ni reutilizar datos viejos.

## 3. Generar la imagen
1. Con el JSON obtenido, escribir `data.json` dentro de `plantilla-historias/` y **añadir la clave `capturado`** con la hora real de lectura (recomendado; si falta, el generador usa la hora de escritura de `data.json`; en ambos casos rechaza datos de más de 45 min):
   ```bash
   cd /home/claude/alpha-markets-media/plantilla-historias
   python3 - <<'PY'
   import json, datetime as dt
   d = json.loads(r'''<<PEGAR AQUÍ EL JSON DEL NAVEGADOR>>''')
   d["capturado"] = dt.datetime.now(dt.timezone.utc).isoformat()
   json.dump(d, open("data.json", "w"), ensure_ascii=False)
   PY
   ```
2. Ejecutar (la hora es la de lectura, formato HH:MM, p. ej. 21:20):
   - Cripto: `python3 build_story.py cripto data.json historia.png 21:20`
   - Bolsa: `python3 build_story.py bolsa data.json historia.png 21:20`
3. Si imprime `ERROR: ...` (código 1): **NO publicar nada**; avisar por notificación con el motivo y terminar.
4. Si imprime `OK ...`: revisar la imagen con `Read`:
   - 1080x1920, cabecera con logo y fecha de HOY, titular, **6 filas + Fear & Greed** (cripto) u **8 filas** (bolsa), signos y colores correctos (verde sube, rojo baja), pie con la hora.
   - Las cifras de la línea `OK` son las que hay que resumir a Antonio.

## 4. Publicar (Metricool, sin pedir OK; Antonio lo autorizó)
1. Copiar a `stories/AAAA-MM-DD-cripto.png` (o `-bolsa.png`) en la raíz del repo, `git add`, commit, `git push origin main` (el aviso "push negotiation failed" es normal).
2. `createScheduledPost`: blogId `8199629`, Instagram, type `STORY`, sin texto, media = URL `https://raw.githubusercontent.com/4lphamarkets/alpha-markets-media/main/stories/<archivo>.png`, fecha de hoy 21:30 Europe/Madrid (si ya son las 21:27 o más, ahora + 3 minutos).
3. `getScheduledPosts`: comprobar que existe y que el media ya apunta a `static.metricool.com`; entonces `git rm` del PNG de `stories/`, commit y push (la carpeta `stories/` se puede limpiar; **la plantilla no**).
4. Tras las 21:31 verificar que está PUBLISHED; si no, avisar.

## 5. Reglas de oro
- Datos siempre recién leídos del navegador; nunca de memoria, nunca de un día anterior.
- Si cualquier paso falla, no se publica nada y se avisa por notificación.
- Al final, responder en 2-3 líneas: cifras clave, hora programada y estado.
- Si hay que cambiar el diseño: editar `build_story.py` / `make_fondo.py` (el fondo es `assets/fondo_historia.png`). Para poner un icono propio basta con dejar `assets/icons/<CLAVE>.png` (p. ej. `NVDA.png`, cuadrado, preferible con fondo transparente).
