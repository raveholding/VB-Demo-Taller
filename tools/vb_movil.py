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
i=h.rindex('</body>');h=h[:i]+blk+'\n'+h[i:]
open(p,'w',encoding='utf8').write(h);print('vb-movil aplicado')
