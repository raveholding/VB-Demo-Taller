"""V27.28 · Kit de botones CRUD de Vincular Business en la demo Taller (misma experiencia que AlmacenRAVE y el resto de las demos):
✏️ editar y 🗑 borrar con ícono y leyenda en las tablas; borrado al instante con «Registro eliminado · ↶ Deshacer» (6 s, también
Ctrl/Cmd+Z) que lo vuelve a su lugar exacto; casillas para borrar varios; Esc ya cerraba los modales.
Clientes, vehículos y proveedores sólo se borran si no tienen historial (órdenes, ventas, turnos, compras, saldo o garantías):
si lo tienen, se avisa y se ofrece la baja. Idempotente. Uso: python3 tools/vb_crud.py index.html"""
import sys
p=sys.argv[1];h=open(p,encoding='utf8').read()
M='<!-- vb-crud -->';E='<!-- /vb-crud -->'
if M in h:
    a=h.index(M);b=h.index(E)+len(E);h=h[:a]+h[b:]
blk=M+r'''<style>
.vb-ib{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;padding:0;border:1px solid var(--line,#ccc);border-radius:9px;background:transparent;color:inherit;cursor:pointer;vertical-align:middle;transition:background .15s,color .15s,border-color .15s}
.vb-ib:hover{border-color:var(--acc,#c9963e);color:var(--acc,#c9963e)}.vb-ib:focus-visible{outline:3px solid var(--acc,#c9963e);outline-offset:2px}
.vb-ib.vb-del{opacity:.8}.vb-ib.vb-del:hover{color:#fff;background:#c0392b;border-color:#c0392b;opacity:1}
.vb-ck{width:2.2rem;text-align:center}.vb-ck input{width:18px;height:18px;min-height:0;cursor:pointer}tr.vb-sel td{background:rgba(201,150,62,.12)}
#vb-snack{position:fixed;left:1rem;bottom:1rem;z-index:9999;display:flex;align-items:center;gap:.8rem;background:#1d1b18;color:#fff;border-radius:12px;padding:.7rem .8rem .7rem 1rem;box-shadow:0 10px 30px rgba(0,0,0,.35);max-width:calc(100vw - 2rem);overflow:hidden;font-size:.95rem}
#vb-snack .vb-undo{display:inline-flex;align-items:center;gap:.35rem;background:#c9963e;color:#1a1307;border:0;border-radius:9px;padding:.45rem .75rem;font-weight:800;cursor:pointer;min-height:0}
#vb-snack .vb-bar{position:absolute;left:0;bottom:0;height:3px;background:#c9963e;width:100%;animation:vbBar 6s linear forwards}@keyframes vbBar{from{width:100%}to{width:0}}
.vb-bulk{position:fixed;top:.8rem;left:50%;transform:translateX(-50%);z-index:9998;display:flex;align-items:center;gap:.6rem;background:var(--card,#fff);color:inherit;border:1px solid #c9963e;border-radius:14px;padding:.5rem .7rem;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.vb-bulk .vb-bdel{color:#fff;background:#c0392b;border-color:#c0392b}
@media (prefers-reduced-motion:reduce){#vb-snack .vb-bar{animation:none}}
@media (max-width:560px){#vb-snack{left:.5rem;right:.5rem}.vb-bulk{top:auto;bottom:4.5rem;left:.5rem;right:.5rem;transform:none;justify-content:space-between}}
</style>
<script>(function(){if(window.vbRemove)return;
var IC={edit:'<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>',
 del:'<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/></svg>',
 undo:'<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14 4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/></svg>'};
var Q=[];
function rr(){try{renderView();}catch(e){}}
/* quita ítems de DB[key] y deja la marcha atrás lista */
window.vbRemove=function(o){var arr=DB[o.key]||[],set={},taken=[];o.ids.forEach(function(i){set[String(i)]=1;});
 for(var i=arr.length-1;i>=0;i--)if(set[String(arr[i].id)]){taken.push({i:i,x:arr[i]});arr.splice(i,1);}
 if(!taken.length)return 0;taken.reverse();audit(o.audit||'Registro eliminado',(o.label||'')+' · '+taken.length);save();if(o.after)o.after();else rr();
 push({label:o.label||(taken.length>1?taken.length+' registros eliminados':'Registro eliminado'),undo:function(){var a=DB[o.key]=DB[o.key]||[];taken.forEach(function(t){if(!a.some(function(y){return y.id===t.x.id}))a.splice(Math.min(t.i,a.length),0,t.x);});audit((o.audit||'Registro eliminado')+' (deshecho)',o.label||'');save();if(o.after)o.after();else rr();}});return taken.length;};
/* para cambios que no son quitar de una lista (ej. dar de baja): o.undo restaura */
window.vbUndoable=function(label,undo){push({label:label,undo:undo});};
function push(u){u.t=Date.now();Q.push(u);Q=Q.slice(-10);snack(u);}
function undoLast(){var u=Q.pop();if(!u||Date.now()-u.t>6500)return false;try{u.undo();}catch(e){toast('No se pudo deshacer',1);return false;}var s=document.getElementById('vb-snack');if(s)s.remove();toast('Listo, se deshizo');return true;}
function snack(u){var s=document.getElementById('vb-snack');if(s)s.remove();s=document.createElement('div');s.id='vb-snack';s.setAttribute('role','status');s.setAttribute('aria-live','polite');
 s.innerHTML='<span>'+h(u.label)+'</span><button type="button" class="vb-undo">'+IC.undo+' Deshacer</button><i class="vb-bar"></i>';document.body.appendChild(s);
 s.querySelector('.vb-undo').onclick=function(){var i=Q.indexOf(u);if(i<0)return;Q.splice(i,1);Q.push(u);u.t=Date.now();undoLast();};clearTimeout(snack.k);snack.k=setTimeout(function(){if(s.isConnected)s.remove();},6000);}
document.addEventListener('keydown',function(e){if((e.ctrlKey||e.metaKey)&&!e.shiftKey&&(e.key==='z'||e.key==='Z')){var t=e.target;if(t&&(t.isContentEditable||/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)))return;if(Q.length&&Date.now()-Q[Q.length-1].t<=6500){e.preventDefault();e.stopImmediatePropagation();undoLast();}}
 if(e.key==='Escape'){var b=document.querySelector('.vb-bulk');if(b&&!MODAL)bulkClear();}},true);

/* ---- íconos en las tablas: ✎/Editar → lápiz; ✕/Quitar/Eliminar/Borrar → tacho ---- */
function icons(root){[].forEach.call(root.querySelectorAll('td button.btn, td a.btn, .mf button.btn.d'),function(b){if(b._vbi||b.querySelector('svg'))return;var t=(b.textContent||'').trim(),k='';
 if(/^(✎|✏️?|editar)$/i.test(t))k='edit';else if(/^(✕|×|quitar|eliminar|borrar|🗑️?)$/i.test(t))k='del';if(!k)return;
 if(k==='del'&&(b.dataset.act==='mclose'||/^(lndel|rpdelrow|otdel)$/.test(b.dataset.act||'')&&!b.closest('td')))return;
 b._vbi=1;var lbl=b.getAttribute('aria-label')||(k==='edit'?'Editar':'Eliminar');b.classList.add('vb-ib','vb-'+k);b.title=b.title||lbl;b.setAttribute('aria-label',lbl);b.innerHTML=IC[k];});}
/* ---- selección múltiple: <table data-bulk="tipo">, filas con data-id ---- */
var BULK={};window.VB_BULK=BULK;
function bulkScan(root){[].forEach.call(root.querySelectorAll('table[data-bulk]'),function(t){if(t._vbb)return;var tp=BULK[t.dataset.bulk];if(!tp||(tp.can&&!tp.can()))return;t._vbb=1;
 var hr=t.tHead&&t.tHead.rows[0];if(hr)hr.insertAdjacentHTML('afterbegin','<th class="vb-ck"><input type="checkbox" aria-label="Seleccionar todo" data-vball="1"></th>');
 [].forEach.call(t.tBodies[0]?t.tBodies[0].rows:[],function(r){if(r.dataset.id)r.insertAdjacentHTML('afterbegin','<td class="vb-ck"><input type="checkbox" aria-label="Seleccionar" data-vbck="'+h(r.dataset.id)+'"></td>');else if(r.cells.length)r.cells[0].colSpan=(r.cells[0].colSpan||1)+1;});
 t.addEventListener('change',function(e){if(e.target.dataset.vball)[].forEach.call(t.querySelectorAll('[data-vbck]'),function(c){c.checked=e.target.checked;});if(e.target.dataset.vball||e.target.dataset.vbck)bulkBar(t);});});}
function bulkBar(t){var ids=[].map.call(t.querySelectorAll('[data-vbck]:checked'),function(c){return c.dataset.vbck;});[].forEach.call(t.querySelectorAll('tr'),function(r){var c=r.querySelector('[data-vbck]');r.classList.toggle('vb-sel',!!(c&&c.checked));});
 var b=document.querySelector('.vb-bulk');if(!ids.length){if(b)b.remove();return;}if(!b){b=document.createElement('div');b.className='vb-bulk';b.setAttribute('role','toolbar');b.setAttribute('aria-label','Acciones sobre la selección');document.body.appendChild(b);}
 b.innerHTML='<b>'+ids.length+' seleccionado'+(ids.length>1?'s':'')+'</b><button type="button" class="btn s vb-bdel">'+IC.del+' Eliminar</button><button type="button" class="btn s vb-bx">Cancelar</button>';
 b.querySelector('.vb-bx').onclick=bulkClear;b.querySelector('.vb-bdel').onclick=function(){BULK[t.dataset.bulk].del(ids);b.remove();};}
function bulkClear(){[].forEach.call(document.querySelectorAll('[data-vbck],[data-vball]'),function(c){c.checked=false;});[].forEach.call(document.querySelectorAll('tr.vb-sel'),function(r){r.classList.remove('vb-sel');});var b=document.querySelector('.vb-bulk');if(b)b.remove();}
document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.vb-ck'))e.stopPropagation();},true);
var tm=0;new MutationObserver(function(){clearTimeout(tm);tm=setTimeout(function(){['view','modal'].forEach(function(id){var r=document.getElementById(id);if(r){mark(r);icons(r);bulkScan(r);}});},30);}).observe(document.body,{childList:true,subtree:true});

/* ---- historial que impide borrar ---- */
function cliHist(id){var n=0;n+=DB.ots.filter(function(o){return o.cliId===id;}).length;n+=(DB.ventas||[]).filter(function(v){return v.cliId===id;}).length;n+=(DB.turnos||[]).filter(function(t){return t.cliId===id;}).length;n+=(DB.garantias||[]).filter(function(g){return g.cliId===id;}).length;n+=(DB.ledger||[]).filter(function(l){return l.cliId===id;}).length;var c=cliOf(id);if(c&&Math.abs(+c.saldo||0)>0.005)n++;if(c&&(+c.pts||0)>0)n++;return n;}
function vehHist(id){return DB.ots.some(function(o){return o.vehId===id;})||(DB.turnos||[]).some(function(t){return t.vehId===id;})||(DB.garantias||[]).some(function(g){return g.vehId===id;});}
function provHist(id){return(DB.ocs||[]).some(function(o){return o.provId===id;})||(DB.movs||[]).some(function(m){return m.provId===id;})||(DB.repuestos||[]).some(function(r){return r.provId===id;})||(DB.ledger||[]).some(function(l){return l.provId===id;})||(typeof provDeuda==='function'&&provDeuda(id)>0.005);}
var boss=function(){return ME&&(ME.rol==='dueno'||ME.rol==='jefe');};

/* ---- marcas de filas y botones nuevos ---- */
function mark(root){
 /* clientes: data-id en cada fila (abren la ficha al tocar) + casillas */
 if(VIEW==='clientes'&&root.id==='view'){var t=root.querySelector('table');if(t&&!t.dataset.bulk&&boss()){t.dataset.bulk='cli';var ids=DB.clientes.filter(function(c){var q=norm(UI.cliQ);return !q||norm(c.n+' '+c.tel+' '+(c.doc||'')+' '+cliDom(c)+' '+DB.vehs.filter(function(v){return v.cliId===c.id;}).map(function(v){return v.pat+' '+v.marca+' '+v.mod;}).join(' ')).indexOf(q)>=0;}).map(function(c){return c.id;});
  [].forEach.call(t.tBodies[0].rows,function(r,i){var a=r.querySelector('[data-act=cliopen]');var id=a?a.dataset.id:ids[i];if(id&&cliOf(id))r.dataset.id=id;});}}
 /* proveedores: tacho al lado del lápiz */
 [].forEach.call(root.querySelectorAll('[data-act=pedit][data-id]'),function(b){if(b._vbp||!b.dataset.id)return;b._vbp=1;if(!boss())return;b.insertAdjacentHTML('afterend','<button class="btn s vb-ib vb-del" data-act="vbprovdel" data-id="'+h(b.dataset.id)+'" title="Borrar proveedor" aria-label="Borrar proveedor">'+IC.del+'</button>');});
 /* ficha del cliente: «Eliminar cliente» en el pie */
 if(root.id==='modal'&&MODAL&&MODAL._vbCli&&!root.querySelector('[data-act=vbclidel]')){var f=root.querySelector('.mf');if(f)f.insertAdjacentHTML('afterbegin','<button class="btn d" data-act="vbclidel" data-id="'+h(MODAL._vbCli)+'" style="margin-right:auto">'+IC.del+' Eliminar cliente</button>');}
 /* vehículos dentro de la ficha */
 if(root.id==='modal'){[].forEach.call(root.querySelectorAll('[data-act=vehedit][data-id],[data-act=vehopen][data-id]'),function(b){if(b._vbv||!boss())return;b._vbv=1;b.insertAdjacentHTML('afterend','<button class="btn s vb-ib vb-del" data-act="vbvehdel" data-id="'+h(b.dataset.id)+'" title="Borrar vehículo" aria-label="Borrar vehículo">'+IC.del+'</button>');});}
 /* turnos: tacho para borrar un turno cancelado o cargado por error */
 [].forEach.call(root.querySelectorAll('[data-act=tuest][data-e=Cancelado]'),function(b){if(b._vbt||!boss())return;b._vbt=1;b.insertAdjacentHTML('afterend','<button class="btn s vb-ib vb-del" data-act="vbtudel" data-id="'+h(b.dataset.id)+'" title="Borrar turno" aria-label="Borrar turno">'+IC.del+'</button>');});
}
/* la ficha del cliente recuerda de quién es */
var _co=ACT.cliopen;ACT.cliopen=function(d){var r=_co.apply(this,arguments);if(MODAL&&d&&d.id)MODAL._vbCli=d.id;return r;};

/* ---- borrar con deshacer ---- */
ACT.vbclidel=function(d){if(!boss())return toast('Sólo el dueño o el jefe de taller',1);var c=cliOf(d.id);if(!c)return;var n=cliHist(c.id);
 if(n)return toast('«'+c.n+'» tiene historial (órdenes, ventas, turnos, saldo, puntos o garantías): no se borra para no perder la trazabilidad.',1);
 closeModal();var vs=DB.vehs.filter(function(v){return v.cliId===c.id;}).map(function(v){return v.id;});
 var tv=[];for(var i=DB.vehs.length-1;i>=0;i--)if(vs.indexOf(DB.vehs[i].id)>=0){tv.push({i:i,x:DB.vehs[i]});DB.vehs.splice(i,1);}tv.reverse();
 vbRemove({key:'clientes',ids:[c.id],label:'Cliente eliminado',audit:'Cliente eliminado'});
 if(tv.length){var u=Q[Q.length-1];var u0=u.undo;u.undo=function(){u0();tv.forEach(function(t){if(!DB.vehs.some(function(y){return y.id===t.x.id;}))DB.vehs.splice(Math.min(t.i,DB.vehs.length),0,t.x);});save();rr();};}};
BULK.cli={can:boss,del:function(ids){var ok=ids.filter(function(i){return !cliHist(i);}),no=ids.length-ok.length;if(ok.length){var vs=DB.vehs.filter(function(v){return ok.indexOf(v.cliId)>=0;}).map(function(v){return v.id;});
 var tv=[];for(var i=DB.vehs.length-1;i>=0;i--)if(vs.indexOf(DB.vehs[i].id)>=0){tv.push({i:i,x:DB.vehs[i]});DB.vehs.splice(i,1);}tv.reverse();
 vbRemove({key:'clientes',ids:ok,label:ok.length+' cliente(s) eliminado(s)',audit:'Clientes eliminados'});if(tv.length){var u=Q[Q.length-1];var u0=u.undo;u.undo=function(){u0();tv.forEach(function(t){DB.vehs.splice(Math.min(t.i,DB.vehs.length),0,t.x);});save();rr();};}}
 if(no)setTimeout(function(){toast(no+' cliente(s) con historial no se borraron.',1);},300);}};
ACT.vbvehdel=function(d){if(!boss())return;var v=DB.vehs.find(function(x){return x.id===d.id;});if(!v)return;if(vehHist(v.id))return toast('Ese vehículo tiene órdenes, turnos o garantías: no se borra.',1);
 var cid=MODAL&&MODAL._vbCli;vbRemove({key:'vehs',ids:[v.id],label:'Vehículo '+(v.pat||'')+' eliminado',audit:'Vehículo eliminado',after:function(){if(cid&&MODAL){closeModal();ACT.cliopen({id:cid});}else rr();}});};
ACT.vbprovdel=function(d){if(!boss())return;var p=provOf(d.id);if(!p)return;
 if(provHist(p.id)){if(p.activo===false)return;p.activo=false;audit('Proveedor dado de baja',p.n);save();rr();vbUndoable('«'+p.n+'» dado de baja (tiene compras o deuda)',function(){p.activo=true;audit('Proveedor reactivado',p.n);save();rr();});return;}
 vbRemove({key:'provs',ids:[p.id],label:'Proveedor eliminado',audit:'Proveedor eliminado'});};
ACT.vbtudel=function(d){if(!boss())return;var t=(DB.turnos||[]).find(function(x){return x.id===d.id;});if(!t)return;if(t.otId)return toast('Ese turno ya tiene una orden de trabajo.',1);vbRemove({key:'turnos',ids:[t.id],label:'Turno eliminado',audit:'Turno eliminado'});};
/* los borrados que ya existían pasan a «al instante + deshacer» */
ACT.servdel=function(d){if(!boss())return;var s=DB.servicios.find(function(x){return x.id===d.id;});if(!s)return;vbRemove({key:'servicios',ids:[s.id],label:'Servicio «'+s.n+'» quitado',audit:'Servicio quitado'});};
ACT.predel=function(d){if(!boss())return;vbRemove({key:'premios',ids:[d.id],label:'Premio quitado',audit:'Premio quitado'});};
var _tk=ACT.tkdel;ACT.tkdel=function(d){var k=(DB.tareas||[]).find(function(x){return x.id===d.id;});if(!k)return;closeModal();vbRemove({key:'tareas',ids:[k.id],label:'Tarea eliminada',audit:'Tarea eliminada'});};
})();</script>'''+E
j=h.rindex('</body>');h=h[:j]+blk+h[j:]
open(p,'w',encoding='utf8').write(h);print('vb_crud: ok')
