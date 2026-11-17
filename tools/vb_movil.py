"""Celular y tablet (misma mejora que el resto de las demos de Vincular Business):
el menú lateral se cierra al tocar afuera (con la pantalla oscurecida) o con Escape,
y los botones de la barra de arriba no se cortan. Sólo presentación. Uso: python3 tools/vb_movil.py index.html"""
import sys
p=sys.argv[1];h=open(p,encoding='utf8').read()
M='<!-- vb-movil -->'
if M in h:
    a=h.index(M);b=h.index('<!-- /vb-movil -->')+len('<!-- /vb-movil -->');h=h[:a]+h[b:]
blk=M+'''<style>#uxtop .tb{flex-shrink:0;white-space:nowrap}#uxtop .tb.srch{flex-shrink:1;min-width:0;overflow:hidden;text-overflow:ellipsis}
#vb-ov{display:none}@media(max-width:900px){#vb-ov:not([hidden]){display:block;position:fixed;inset:0;z-index:29;background:rgba(0,0,0,.5)}}</style>
<script>(function(){var ov=document.createElement('div');ov.id='vb-ov';ov.hidden=true;document.body.appendChild(ov);
function sync(){var sd=document.getElementById('side');ov.hidden=!(sd&&sd.classList.contains('open'));}
setInterval(sync,500);document.addEventListener('click',function(e){var sd=document.getElementById('side');if(!sd||!sd.classList.contains('open'))return;
if(e.target.closest('#side')||e.target.closest('[data-act=menu]'))return;sd.classList.remove('open');sync();e.preventDefault();e.stopPropagation();},true);
document.addEventListener('click',function(){setTimeout(sync,0);});document.addEventListener('keydown',function(e){if(e.key==='Escape'){var sd=document.getElementById('side');if(sd){sd.classList.remove('open');sync();}}});})();</script><!-- /vb-movil -->'''
# misma regla que las otras demos: sólo se sube arriba al cambiar de pantalla
if "vbPv" not in h: h=h.replace("function go(v){if(!ME)return;","function go(v){if(!ME)return;var vbPv=VIEW,vbPy=window.scrollY||0;",1)
h=h.replace("renderView();window.scrollTo(0,0)}\nfunction renderView()","renderView();window.scrollTo(0,vbPv===v?vbPy:0)}\nfunction renderView()",1)
# V27.6 · teléfono de ejemplo con formato y botón «Reiniciar demo» (borra sólo lo de esta demo: tmvb_*, vb.* y la base vb_copias)
h=h.replace("tel:'3870000000'","tel:'(0387) 400-0123'")
if 'vb-rst-taller' not in h:
    j=h.rindex('</body>')
    h=h[:j]+"""<script id="vb-rst-taller">(function(){if(window.vbDemoReset)return;
window.vbDemoReset=function(){var go=function(){try{var ks=[];for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&(k.indexOf('tmvb_')===0||k.indexOf('vb.')===0))ks.push(k);}ks.forEach(function(k){localStorage.removeItem(k);});}catch(e){}try{sessionStorage.clear();}catch(e){}
 var fin=function(){location.replace(location.pathname);setTimeout(function(){location.reload();},50);};try{var r=indexedDB.deleteDatabase('vb_copias');r.onsuccess=r.onerror=r.onblocked=fin;}catch(e){fin();}setTimeout(fin,1500);};
 var msg='Se borra todo lo que se cargó en esta demo en este navegador y vuelven los datos de ejemplo, fechados hoy. Las otras demos no se tocan.';
 if(typeof confirmBox==='function')confirmBox(msg,go,'Reiniciar');else if(confirm('Reiniciar la demo\\n\\n'+msg))go();};
var css='.vb-rst{display:inline-flex;align-items:center;gap:.4rem;font:inherit;font-size:.85rem;padding:.55rem .9rem;border-radius:10px;border:1px dashed currentColor;background:transparent;color:inherit;opacity:.85;cursor:pointer}.vb-rst:hover{opacity:1}#side .vb-rst{margin:1rem .8rem 1.4rem;width:calc(100% - 1.6rem);justify-content:center}.vb-rst-login{display:flex;justify-content:center;margin:1.2rem 0 .4rem}';
var poner=function(){if(!document.getElementById('vb-rst-css')){var st=document.createElement('style');st.id='vb-rst-css';st.textContent=css;document.head.appendChild(st);}
 var side=document.getElementById('side');if(side&&!side.querySelector('.vb-rst')){var b=document.createElement('button');b.type='button';b.className='vb-rst';b.textContent='↺ Reiniciar demo';b.onclick=function(){window.vbDemoReset();};side.appendChild(b);}
 var lg=document.getElementById('login');if(lg&&!lg.hidden&&!lg.querySelector('.vb-rst-login')){var w=document.createElement('div');w.className='vb-rst-login';w.innerHTML='<button type="button" class="vb-rst">↺ Reiniciar demo (dejarla como nueva)</button>';w.firstChild.onclick=function(){window.vbDemoReset();};lg.appendChild(w);}};
new MutationObserver(poner).observe(document.body,{childList:true,subtree:true});poner();})();</script>
"""+h[j:]
i=h.rindex('</body>');h=h[:i]+blk+'\n'+h[i:]
open(p,'w',encoding='utf8').write(h);print('vb-movil aplicado')
