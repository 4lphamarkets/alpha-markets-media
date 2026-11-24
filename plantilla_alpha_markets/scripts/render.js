// RENDER EN MÁXIMA CALIDAD (obligatorio para exportar):
//   fotogramas PNG sin pérdida → H.264 High, preset slow, CRF 12, BT.709, 1080x1920 @ 30 fps, sin reescalar.
// Uso (desde la carpeta de la plantilla, con index.html ya generado por build.py):
//   node scripts/render.js events                 → tmp/events.json (para sfx.py)
//   node scripts/render.js stills 1.2 5 9.8       → out/still_<t>.png (revisión)
//   node scripts/render.js video [workers]        → tmp/video.mp4 (vídeo completo, renderizado en paralelo)
//   node scripts/render.js portada <t|sinfondo>   → tmp/portada.png (lo llama entrega.py; no hace falta usarlo a mano)
// Requiere: npm i playwright-core  +  Google Chrome instalado (o CHROME=<ruta>), o el paquete 'playwright'.
// v23: detección de Chrome en Windows/Mac/Linux (también Chromium), GPU solo con GPU=1 y con flags según el sistema,
//      espera a que las fuentes Y las imágenes (también las de fondo CSS) estén decodificadas antes del primer fotograma,
//      progreso por consola (cada 10 %) y mensajes de error claros.
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const DIR = path.join(__dirname, '..');
const FPS = 30;
const mode = process.argv[2];
const args = process.argv.slice(3);

function chromeExe() {
  const home = process.env.LOCALAPPDATA || '';
  const cands = [process.env.CHROME,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    home && path.join(home, 'Google', 'Chrome', 'Application', 'chrome.exe'),
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser'].filter(Boolean);
  return cands.find(p => fs.existsSync(p));
}
function launch() {
  let pw;
  try { pw = require('playwright-core'); } catch { try { pw = require('playwright'); } catch {
    throw new Error('Falta Playwright: ejecuta  npm i playwright-core  en la carpeta de la plantilla.'); } }
  const exe = chromeExe();
  if (!exe) console.warn('AVISO: no encuentro Google Chrome; uso el Chromium de Playwright (si no está instalado: npx playwright install chromium). Puedes fijar CHROME=<ruta>.');
  // GPU opcional (GPU=1). Windows usa ANGLE/D3D11; en otros sistemas basta con activar la rasterización por GPU.
  // Comprobar que los fotogramas salen idénticos antes de dejarlo fijo.
  const gpu = process.env.GPU ? (process.platform === 'win32' ? ['--use-angle=d3d11'] : []).concat(['--enable-gpu-rasterization', '--ignore-gpu-blocklist']) : [];
  return pw.chromium.launch({ ...(exe ? { executablePath: exe } : {}), args: ['--allow-file-access-from-files', '--force-color-profile=srgb', ...gpu] });
}
// Espera a fuentes + imágenes (<img> y fondos CSS) para que ningún fotograma salga con un logo o una foto sin pintar.
async function assetsListos(page) {
  await page.evaluate(async () => {
    await document.fonts.ready;
    const urls = new Set();
    document.querySelectorAll('img').forEach(i => i.src && urls.add(i.src));
    document.querySelectorAll('*').forEach(el => {
      const m = getComputedStyle(el).backgroundImage.match(/url\(["']?([^"')]+)["']?\)/g) || [];
      m.forEach(u => urls.add(u.replace(/^url\(["']?|["']?\)$/g, '')));
    });
    await Promise.all([...urls].map(u => new Promise(res => { const im = new Image(); im.onload = im.onerror = () => res(); im.src = u; })));
    await Promise.all([...document.images].map(i => (i.decode ? i.decode().catch(() => {}) : 0)));
  });
}
async function openPage(browser, file = 'index.html') {
  const full = path.join(DIR, file);
  if (!fs.existsSync(full)) throw new Error(`No existe ${file}: ejecuta primero  python scripts/build.py [analista]  (o scripts/montar.py).`);
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto('file:///' + full.replace(/\\/g, '/'));
  await assetsListos(page);
  await page.waitForTimeout(300);
  if (errs.length) throw new Error(`Errores en ${file}:\n` + errs.join('\n'));
  return page;
}
const ENC = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-profile:v', 'high', '-tune', 'animation',
  '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
  '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-r', String(FPS)];

let hechos = 0, totalFrames = 0, ultimoPct = -1;
function progreso() {
  hechos++;
  const pct = Math.floor(hechos * 100 / totalFrames / 10) * 10;
  if (pct !== ultimoPct) { ultimoPct = pct; console.log(`  render ${pct} %  (${hechos}/${totalFrames} fotogramas)`); }
}

async function renderRange(browser, f0, f1, out) {
  const page = await openPage(browser);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', ...ENC, out],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => { ff.on('error', rej); ff.on('exit', c => c === 0 ? res() : rej(new Error('ffmpeg salió con código ' + c))); });
  done.catch(() => {});   // el error se propaga al hacer await done más abajo
  // v20: captura PNG sin pérdida vía CDP con optimizeForSpeed (píxeles idénticos a page.screenshot, ~2,5x más rápida)
  const cdp = await page.context().newCDPSession(page);
  for (let i = f0; i < f1; i++) {
    await page.evaluate(t => seek(t), i / FPS);
    const buf = Buffer.from((await cdp.send('Page.captureScreenshot', { format: 'png', optimizeForSpeed: true })).data, 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    progreso();
  }
  ff.stdin.end(); await done; await page.close();
}

(async () => {
  fs.mkdirSync(path.join(DIR, 'tmp'), { recursive: true }); fs.mkdirSync(path.join(DIR, 'out'), { recursive: true });
  if (!['events', 'stills', 'video', 'portada'].includes(mode)) {
    console.error('Uso: node scripts/render.js events | stills <t...> | video [workers] | portada <t|sinfondo>'); process.exit(2);
  }
  const browser = await launch();
  if (mode === 'events') {
    const page = await openPage(browser);
    const e = await page.evaluate(() => EVJ);
    fs.writeFileSync(path.join(DIR, 'tmp', 'events.json'), JSON.stringify(e));
    console.log(e.length, 'eventos');
  } else if (mode === 'stills') {
    if (!args.length) throw new Error('Indica los segundos: node scripts/render.js stills 1.5 4 8');
    const page = await openPage(browser);
    for (const a of args) {
      await page.evaluate(t => seek(t), parseFloat(a));
      await page.screenshot({ path: path.join(DIR, 'out', `still_${a}.png`), type: 'png' });
    }
  } else if (mode === 'portada') {
    // 1) fondo: fotograma del vídeo en el segundo <t>, sin subtítulos ni cabecera → tmp/portada_bg.png
    //    (solo estilo "clasico"; con 'sinfondo' se salta y no hace falta index.html)
    if (args[0] !== 'sinfondo') {
      const t = parseFloat(args[0] || '3');
      const page = await openPage(browser);
      await page.addStyleTag({ content: '#cap,#hdr{visibility:hidden!important}' });
      await page.evaluate(t => seek(t), t);
      await page.screenshot({ path: path.join(DIR, 'tmp', 'portada_bg.png'), type: 'png' });
      await page.close();
    }
    // 2) portada: portada_index.html (generada por entrega.py) → tmp/portada.png
    const p2 = await openPage(browser, 'portada_index.html');
    const fs_ = await p2.evaluate(() => (typeof fit === 'function' ? fit() : 0));
    await p2.waitForTimeout(250);
    await p2.screenshot({ path: path.join(DIR, 'tmp', 'portada.png'), type: 'png' });
    console.log('portada ok (titular a', fs_, 'px)');
  } else if (mode === 'video') {
    // v21: por defecto usa la mitad de los hilos de la CPU (entre 4 y 12 workers); se puede forzar con el número: node scripts/render.js video 8
    const N = Math.max(1, parseInt(args[0] || String(Math.min(12, Math.max(4, Math.floor(os.cpus().length / 2)))), 10));
    const page = await openPage(browser);
    const end = await page.evaluate(() => (window.TLEND || SC[SC.length - 1].b));
    await page.close();
    const total = Math.round(end * FPS), per = Math.ceil(total / N), parts = [];
    totalFrames = total;
    console.log(`workers: ${N} · ${end.toFixed(2)} s · ${total} fotogramas`);
    const jobs = [];
    for (let k = 0; k < N; k++) {
      const f0 = k * per, f1 = Math.min(total, f0 + per); if (f0 >= f1) break;
      const out = path.join(DIR, 'tmp', `part${k}.mp4`); parts.push(out);
      jobs.push(renderRange(browser, f0, f1, out));
    }
    await Promise.all(jobs);
    const list = path.join(DIR, 'tmp', 'parts.txt');
    fs.writeFileSync(list, parts.map(p => `file '${p.replace(/\\/g, '/')}'`).join('\n'));
    await new Promise((res, rej) => spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy',
      path.join(DIR, 'tmp', 'video.mp4')], { stdio: 'inherit' }).on('exit', c => c === 0 ? res() : rej(new Error('concat ' + c))));
    parts.forEach(p => { try { fs.unlinkSync(p); } catch {} });   // v23: no dejar las partes sueltas (ocupan cientos de MB)
    try { fs.unlinkSync(path.join(DIR, 'tmp', 'video_sin_insertos.mp4')); } catch {}   // v23: el original de insertos.py era de OTRO vídeo → se usaría de base por error
    console.log('listo tmp/video.mp4', total, 'frames');
  }
  await browser.close();
})().catch(e => { console.error(e.message || e); process.exit(1); });
