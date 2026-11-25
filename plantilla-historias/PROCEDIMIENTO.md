# PROCEDIMIENTO · historias diarias ALPHA MARKETS (Cripto hoy / Wall Street hoy / BTC 15 MIN) · v26

Carpeta: `plantilla-historias/` del repo `4lphamarkets/alpha-markets-media`. **NO SE BORRA NUNCA** (ver `LEEME_NO_BORRAR.md`).
Actualizado el 26-11-2026 (activos nuevos, lectura por API de CoinMarketCap, gráfica BTC 15 MIN). Probado con datos reales.

## 0. Antes de nada
- Comprobar que el generador funciona: `cd plantilla-historias && python3 build_story.py --selftest` → debe acabar en `SELFTEST OK`.
  Si falla: NO publicar; anotarlo en el registro y avisar en el resumen.
- Los datos SOLO se leen con el **navegador integrado** (`mcp__remote-devices__Claude_Browser__*`). El shell no tiene internet; WebSearch no sirve para precios; CNN devuelve 451 (no usar).
- Si el navegador pide permiso para un sitio: `request_access` con scope `site` (coinmarketcap.com, investing.com).

## 1. Cripto hoy (CoinMarketCap): BTC, ETH, HYPE, SOL, BNB, LIT + Fear & Greed
1. `navigate` a `https://coinmarketcap.com/` (esperar a que cargue).
2. Ejecutar con `javascript_tool` (action `javascript_exec`). Lee los 6 precios y la variación 24 h con la API pública de CMC (mismo origen; el signo viene en el número) y el Fear & Greed de la página. Devuelve JSON como texto o `{"error": ...}`:

```js
(async () => { const S={BTC:['bitcoin','BTC'],ETH:['ethereum','ETH'],HYPE:['hyperliquid','HYPE'],SOL:['solana','SOL'],BNB:['bnb','BNB'],LIT:['lighter','LIT']}; const out={}; for(const [k,[slug,sym]] of Object.entries(S)){ const r=await fetch('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?slug='+slug); if(r.status!==200) return {error:k+' HTTP '+r.status}; const d=(await r.json()).data||{}; const s=d.statistics||{}; if(d.symbol!==sym||typeof s.price!=='number'||typeof s.priceChangePercentage24h!=='number') return {error:k+' datos inesperados'}; const ch=Math.round(s.priceChangePercentage24h*100)/100; out[k]={price:s.price,change:ch,change_text:(ch<0?'':'+')+ch+'%'} } let fng=null; for(const e of document.querySelectorAll('*')){ if(e.children.length==0 && /^Fear\s*&\s*Greed$/i.test(e.textContent.trim())){ const m=(e.parentElement.innerText||'').match(/Greed\s*\n?\s*(\d{1,3})\b/); if(m){fng=+m[1];break;} } } if(fng===null) return {error:'sin Fear & Greed'}; out.FNG=fng; return JSON.stringify(out) })()
```

- LIT = **Lighter** (CoinMarketCap `/currencies/lighter`, símbolo LIT; no está en la tabla principal, por eso se usa la API).
- Si devuelve `error`, recargar la página una vez y repetir. Si vuelve a fallar: NO publicar ese precio y anotarlo.

## 2. Wall Street hoy (Investing.com): S&P 500, Nasdaq, ANT, SPCX, AMZN, GOOGL, AAPL, NVDA, MSFT · SIN Fear & Greed
1. `navigate` a `https://www.investing.com/` (cualquier página del dominio sirve; el script usa `fetch` del mismo origen).
2. Ejecutar este script (lee las 9 fichas, comprueba el título de cada página y calcula el signo). Slugs verificados el 26-11-2026:

```js
(async () => { const P={SPX:['/indices/us-spx-500',/S&P 500/],NDX:['/indices/nasdaq-composite',/NASDAQ Composite/i],ANT:['/equities/anthropic',/Anthropic/],SPCX:['/equities/spacex',/SpaceX/],AMZN:['/equities/amazon-com-inc',/Amazon/],GOOGL:['/equities/google-inc',/GOOGL|Alphabet/],AAPL:['/equities/apple-computer-inc',/Apple/],NVDA:['/equities/nvidia-corp',/Nvidia/i],MSFT:['/equities/microsoft-corp',/Microsoft/]}; const num=s=>parseFloat(String(s).replace(/[^0-9.\-]/g,'')); const out={}; for(const [k,[u,re]] of Object.entries(P)){ const r=await fetch(u,{credentials:'include'}); if(r.status!==200) return {error:k+' HTTP '+r.status}; const d=new DOMParser().parseFromString(await r.text(),'text/html'); if(!re.test(d.title)) return {error:k+' título inesperado: '+d.title}; const g=n=>{const e=d.querySelector('[data-test="'+n+'"]'); return e?e.textContent.trim():null}; const last=g('instrument-price-last'), pct=g('instrument-price-change-percent'); if(!last||!pct) return {error:k+' sin precio/variación'}; const sign=/^\(?\s*-|−/.test(pct)?-1:1; const mag=Math.abs(num(pct)); out[k]={price:num(last), change:sign*mag, change_text:(sign<0?'-':'+')+mag+'%'} } return JSON.stringify(out) })()
```

- Tickers: Anthropic = **ANT** (Nasdaq, desde 19-11-2026); SpaceX = **SPCX** (Nasdaq, desde 12-6-2026); Google = GOOGL (Alphabet clase A).
- Mercado de EEUU abierto de 15:30 a 22:00 (Madrid). Festivo o fin de semana: **no se hace esta historia** (modo 100 % cripto, ver `RUTINA_DIARIA.md` §6).
- Si algo falla o un valor falta: NO publicar esa historia. Nunca inventar ni reutilizar datos viejos.

## 3. Generar la imagen
1. Con el JSON obtenido, escribir `data.json` dentro de `plantilla-historias/` y **añadir la clave `capturado`** con la hora real de lectura (si falta, el generador usa la hora de escritura de `data.json`; en ambos casos rechaza datos de más de 45 min):
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
3. Si imprime `ERROR: ...` (código 1): **NO publicar nada**; anotarlo y terminar ese paso.
4. Si imprime `OK ...`: revisar la imagen con `Read`:
   - 1080x1920, cabecera con logo y fecha de HOY, titular, **6 filas + Fear & Greed** (cripto) o **9 filas** (bolsa), signos y colores correctos (verde sube, rojo baja), pie con la hora.

## 4. Publicar (Metricool, sin pedir OK; Antonio lo autorizó)
1. Copiar a `stories/AAAA-MM-DD-cripto.png` (o `-bolsa.png`) en la raíz del repo, `git pull --rebase`, `git add`, commit, `git push origin main` (el aviso "push negotiation failed" es normal).
2. `createScheduledPost`: blogId `8199629`, Instagram, type `STORY`, sin texto, media = URL `https://raw.githubusercontent.com/4lphamarkets/alpha-markets-media/main/stories/<archivo>.png`, a la hora de la tabla (L-V: Cripto 21:30 y Bolsa 21:31; Sáb/Dom: Cripto 22:00). Si ya es esa hora o faltan <3 min, ahora + 3 minutos.
3. `getScheduledPosts`: comprobar que existe y que el media ya apunta a `static.metricool.com`; entonces `git rm` del PNG de `stories/`, commit y push (la carpeta `stories/` se puede limpiar; **la plantilla no**).
4. Tras la hora verificar que está PUBLISHED; si no, anotarlo.

## 5. Reglas de oro
- Datos siempre recién leídos del navegador; nunca de memoria, nunca de un día anterior.
- Si cualquier paso falla, no se publica ese elemento y se anota en el registro.
- Si hay que cambiar el diseño: editar `build_story.py` / `make_fondo.py` (el fondo es `assets/fondo_historia.png`). Para poner un icono propio basta con dejar `assets/icons/<CLAVE>.png` (cuadrado, preferible con fondo transparente).

## 6. Historia BITCOIN 15 MIN (gráfica de velas)
1. `navigate` a `https://coinmarketcap.com/` y ejecutar:

```js
(async()=>{const r=await fetch('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=1&range=1D&convertId=2781');if(r.status!==200)return {error:'HTTP '+r.status};const j=await r.json();const pts=Object.entries(j.data.points).map(([t,o])=>[+t,o.v[0]]);if(pts.length<250)return {error:'pocos puntos '+pts.length};return JSON.stringify({capturado:new Date().toISOString(),pts})})()
```

   Devuelve ~289 puntos (uno cada 5 min, 24 h). Guardar el texto como `/tmp/chart.json` (el JSON es la cadena devuelta).
2. `python3 btc15m_story.py /tmp/chart.json /tmp/btc15m.png HH:MM 6 [ref=HH:MM]`
   - `HH:MM` = hora de Madrid de la lectura; `6` = horas de ventana (3-12); `ref` = hora a comparar con el precio de ahora (opcional; por defecto el inicio de la ventana).
   - Rechaza datos con >30 min. Si imprime `ERROR`, hacer una historia de noticia normal en su lugar.
3. Revisar la imagen (`Read`) y publicarla como una historia más (§4, con nombre único `stories/AAAA-MM-DD_HHMM-btc15m.png`).
