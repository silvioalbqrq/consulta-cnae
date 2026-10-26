const CACHE="consulta-cnae-20261025-01";
const ASSETS=["./","./index.html","./logic.js?v=20261025-01","./dados.js?v=20261025-01"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET")return;
  const url=new URL(e.request.url);
  if(url.origin!==location.origin)return;
  const data=/\/(dados|logic)\.js$/.test(url.pathname);
  if(e.request.mode==="navigate"||data){
    e.respondWith(fetch(e.request).then(r=>{
      if(r&&r.status===200){const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));}
      return r;
    }).catch(()=>caches.match(e.request).then(r=>r||caches.match("./index.html"))));
    return;
  }
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(resp=>{
    if(resp&&resp.status===200&&resp.type==="basic"){const c=resp.clone();caches.open(CACHE).then(x=>x.put(e.request,c));}
    return resp;
  })));
});
