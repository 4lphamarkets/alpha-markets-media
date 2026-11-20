// RENDER EN MÃXIMA CALIDAD (obligatorio para exportar):
//   fotogramas PNG sin pÃ©rdida â†’ H.264 High, preset slow, CRF 12, BT.709, 1080x1920 @ 30 fps, sin reescalar.
// Uso (desde la carpeta de la plantilla, con index.html ya generado por build.py):
//   node scripts/render.js events                 â†’ tmp/events.json (para sfx.py)
//   node scripts/render.js stills 1.2 5 9.8       â†’ out/still_<t>.png (revisiÃ³n)
//   node scripts/render.js video [workers=4]      â†’ tmp/video.mp4 (vÃ­deo completo, renderizado en paralelo)
//   node scripts/render.js portada <t>            â†’ tmp/portada.png (lo llama entrega.py; no hace falta usarlo a mano)
// Requiere: npm i playwright-core  +  Google Chrome instalado (o CHROME=<ruta>), o el paquete 'playwright'.
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const DIR = path.join(__dirname, '..');
const FPS = 30;
const mode = process.argv[2];
const args = process.argv.slice(3);

function launch() {
  let pw; try { pw = require('playwright-core'); } catch { pw = require('playwright'); }
  const cands = [process.env.CHROME, 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome'].filter(Boolean);
  const exe = cands.find(p => fs.existsSync(p));
  return pw.chromium.launch({ ...(exe ? { executablePath: exe } : {}), args: ['--allow-file-access-from-files', '--force-color-profile=srgb'] });
}
async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto('file:///' + path.join(DIR, 'index.html').replace(/\\/g, '/'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  if (errs.length) throw new Error('Errores en index.html:\n' + errs.join('\n'));
  return page;
}
const ENC = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-profile:v', 'high', '-tune', 'animation',
  '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
  '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-r', String(FPS)];

async function renderRange(browser, f0, f1, out) {
  const page = await openPage(browser);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', ...ENC, out],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((res, rej) => ff.on('exit', c => c === 0 ? res() : rej(new Error('ffmpeg exit ' + c))));
  for (let i = f0; i < f1; i++) {
    await page.evaluate(t => seek(t), i / FPS);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await done; await page.close();
}

(async () => {
  fs.mkdirSync(path.join(DIR, 'tmp'), { recursive: true }); fs.mkdirSync(path.join(DIR, 'out'), { recursive: true });
  const browser = await launch();
  if (mode === 'events') {
    const page = await openPage(browser);
    const e = await page.evaluate(() => EVJ);
    fs.writeFileSync(path.join(DIR, 'tmp', 'events.json'), JSON.stringify(e));
    console.log(e.length, 'eventos');
  } else if (mode === 'stills') {
    const page = await openPage(browser);
    for (const a of args) {
      await page.evaluate(t => seek(t), parseFloat(a));
      await page.screenshot({ path: path.join(DIR, 'out', `still_${a}.png`), type: 'png' });
    }
  } else if (mode === 'portada') {
    // 1) fondo: fotograma del vÃ­deo en el segundo <t>, sin subtÃ­tulos ni cabecera â†’ tmp/portada_bg.png
    //    (solo estilo "clasico"; con 'sinfondo' se salta y no hace falta index.html)
    if (args[0] !== 'sinfondo') {
      const t = parseFloat(args[0] || '3');
      const page = await openPage(browser);
      await page.addStyleTag({ content: '#cap,#hdr{visibility:hidden!important}' });
      await page.evaluate(t => seek(t), t);
      await page.screenshot({ path: path.join(DIR, 'tmp', 'portada_bg.png'), type: 'png' });
      await page.close();
    }
    // 2) portada: portada_index.html (generada por entrega.py) â†’ tmp/portada.png
    const p2 = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    const errs = []; p2.on('pageerror', e => errs.push(String(e)));
    await p2.goto('file:///' + path.join(DIR, 'portada_index.html').replace(/\\/g, '/'));
    await p2.evaluate(() => document.fonts.ready);
    await p2.waitForLoadState('load');
    if (errs.length) throw new Error('Errores en portada:\n' + errs.join('\n'));
    const fs_ = await p2.evaluate(() => (typeof fit === 'function' ? fit() : 0));
    await p2.waitForTimeout(250);
    await p2.screenshot({ path: path.join(DIR, 'tmp', 'portada.png'), type: 'png' });
    console.log('portada ok (titular a', fs_, 'px)');
  } else if (mode === 'video') {
    const N = parseInt(args[0] || '4', 10);
    const page = await openPage(browser);
    const end = await page.evaluate(() => (window.TLEND || SC[SC.length - 1].b));
    await page.close();
    const total = Math.round(end * FPS), per = Math.ceil(total / N), parts = [];
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
    console.log('listo tmp/video.mp4', total, 'frames');
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
