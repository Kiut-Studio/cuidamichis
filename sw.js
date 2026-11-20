// Copia sin conexión de Cuidamichis (Kiut Studio).
// Ojo: este juego comparte el sitio (kiut-studio.github.io) con Dina Run y Dina Beat,
// así que solo borra sus propias cachés (las que empiezan con PRE), nunca las de los otros juegos.
// La lista FILES y el número de versión los actualiza `python3 tools/construir.py` (no editar a mano).
const PRE='cuidamichis-';
const C=PRE+'v24';
const FILES=["./", "index.html", "manifest.json", "icon-192.png", "icon-512.png", "favicon-32.png", "assets/arte.json", "assets/cinthia.webp", "assets/deisy.webp", "assets/frutilla.webp", "assets/leandro.webp", "assets/nora.webp", "assets/pancito.webp", "assets/sofi.webp", "assets/gato_sofia/contento.webp", "assets/gato_sofia/contento_n.webp", "assets/gato_sofia/feliz.webp", "assets/gato_sofia/feliz_n.webp", "assets/gato_sofia/triste.webp", "assets/gato_sofia/triste_n.webp", "assets/gato/banio.webp", "assets/gato/banio_n.webp", "assets/gato/bostezo.webp", "assets/gato/bostezo_n.webp", "assets/gato/cara_amor.webp", "assets/gato/cara_amor_n.webp", "assets/gato/cara_enojo.webp", "assets/gato/cara_enojo_n.webp", "assets/gato/cara_feliz.webp", "assets/gato/cara_feliz_n.webp", "assets/gato/cara_sorpresa.webp", "assets/gato/cara_sorpresa_n.webp", "assets/gato/cara_sueno.webp", "assets/gato/cara_sueno_n.webp", "assets/gato/cara_triste.webp", "assets/gato/cara_triste_n.webp", "assets/gato/comiendo.webp", "assets/gato/comiendo_n.webp", "assets/gato/contento.webp", "assets/gato/contento_n.webp", "assets/gato/dormido1.webp", "assets/gato/dormido1_n.webp", "assets/gato/dormido2.webp", "assets/gato/dormido2_n.webp", "assets/gato/edad_abuelo.webp", "assets/gato/edad_abuelo_n.webp", "assets/gato/edad_adulto.webp", "assets/gato/edad_adulto_n.webp", "assets/gato/edad_bebe.webp", "assets/gato/edad_bebe_n.webp", "assets/gato/edad_joven.webp", "assets/gato/edad_joven_n.webp", "assets/gato/enfermo.webp", "assets/gato/enfermo_n.webp", "assets/gato/feliz.webp", "assets/gato/feliz_n.webp", "assets/gato/hambre.webp", "assets/gato/hambre_n.webp", "assets/gato/jugando.webp", "assets/gato/jugando_n.webp", "assets/gato/miedo.webp", "assets/gato/miedo_n.webp", "assets/gato/triste.webp", "assets/gato/triste_n.webp", "assets/fonts/caveat-latin-600-normal.woff2", "assets/fonts/caveat-latin-700-normal.woff2", "assets/fonts/fredoka-latin-500-normal.woff2", "assets/fonts/fredoka-latin-600-normal.woff2"];
// huella:29242b8362
// cache:'reload' baja cada archivo de nuevo (sin copias viejas del navegador) al instalar una versión nueva
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(FILES.map(f=>new Request(f,{cache:'reload'})))));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith(PRE)&&k!==C).map(k=>caches.delete(k)))));self.clients.claim()});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const url=new URL(e.request.url);
  if(url.origin!==location.origin)return;
  if(e.request.mode==='navigate'){ // la página: primero internet (para ver cambios); sin conexión, la guardada
    e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(C).then(x=>x.put('index.html',c));return r}).catch(()=>caches.match('index.html')));return}
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp));return res})));
});

// Avisos: tocar una notificación abre el juego; y, si el navegador deja (Chrome instalado como app), un aviso periódico
// mira lo que la página anotó en la caché 'cc-aviso' (ojo: no empieza con "cuidamichis-" para que la limpieza de arriba no la borre).
self.addEventListener('notificationclick',e=>{e.notification.close();e.waitUntil(self.clients.matchAll({type:'window',includeUncontrolled:true}).then(cs=>{for(const c of cs){if('focus' in c)return c.focus()}return self.clients.openWindow('./')}))});
self.addEventListener('periodicsync',e=>{if(e.tag!=='cc-aviso')return;e.waitUntil((async()=>{const c=await caches.open('cc-aviso'),r=await c.match('cc-aviso.json');if(!r)return;const a=await r.json();
  if(Date.now()>=a.due){await self.registration.showNotification('Cuidamichis 🐱',{body:a.txt,icon:'icon-192.png',badge:'favicon-32.png',tag:'cc-aviso',lang:'es'});await c.delete('cc-aviso.json')}})())});
