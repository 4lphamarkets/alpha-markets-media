// KIT DE PORTADAS v10 — utilidades, no maqueta. Enlazar con <script src="portadas/kit.js"></script>.
// entrega.py inyecta antes  window.D = {...}  con el bloque "portada" de entrega.json (titulo, cifra, persona.src, logos[i].src/color...).
// Puedes usar D o escribir los textos e imágenes directamente en el HTML del diseño (img/logos/..., img/personas/...).
window.D = window.D || {};
const esc = s => String(s ?? '').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const rgba = (hex, a) => { const h = (hex || '#34F5B0').replace('#', ''); const n = parseInt(h.length === 3 ? h.replace(/./g, '$&$&') : h, 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`; };

// Reduce el tamaño de letra de el hasta que quepa en anchoMax (y altoMax si se da). Devuelve el tamaño final.
function ajustar(el, anchoMax, fsMax = 200, fsMin = 30, altoMax = Infinity) {
  if (typeof el === 'string') el = document.querySelector(el);
  if (!el) return 0;
  let fs = fsMax; el.style.fontSize = fs + 'px';
  const disp = getComputedStyle(el).display; if (disp === 'block') el.style.display = 'inline-block';
  while ((el.scrollWidth > anchoMax || el.scrollHeight > altoMax) && fs > fsMin) { fs -= 2; el.style.fontSize = fs + 'px'; }
  if (disp === 'block') el.style.display = 'block';
  return fs;
}
// Marca del canal como HTML (v14: logo de letras con flecha; el parámetro variante se ignora, se mantiene por compatibilidad).
function marca(variante = '', tam = 44) {
  // v14: la marca es SIEMPRE el logo de letras del canal (flecha + ALPHA MARKETS, sin cara), PNG transparente img/logo_alpha_wordmark.png.
  // tam 44 ≈ 84 px de alto (≈ 270 de ancho); en historias usar tam ≈ 82 ≈ 155 px de alto (≈ 500 de ancho).
  return `<img class="marca-logo ${variante}" src="img/logo_alpha_wordmark.png" style="height:${Math.round(tam * 1.9)}px;width:auto">`;
}
// Semilla reproducible (para ruido, velas, estrellas...): const r = azar('slug'); r() → [0,1)
function azar(sem = 'alpha') { let h = 2166136261; for (const c of String(sem)) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return () => ((h = Math.imul(h ^ h >>> 15, 2246822507), h = Math.imul(h ^ h >>> 13, 3266489909), (h ^= h >>> 16) >>> 0) / 4294967296); }

// render.js llama a window.fit() antes de la captura; cada diseño puede definir el suyo (maquetación dinámica).
window.fit = window.fit || (() => 0);
// Para revisar la zona segura del recorte 3:4 del perfil: añade ?guia a la URL o window.GUIA = true.
document.addEventListener('DOMContentLoaded', () => { if (location.search.includes('guia') || window.GUIA) { const g = document.createElement('div'); g.className = 'guia-segura'; document.body.appendChild(g); } });
