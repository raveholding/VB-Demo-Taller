"""V27.29 · Atención al cliente en la demo Taller: «Hoy» y «Agenda» (la misma idea que AlmacenRAVE y el resto de las demos).
Hoy: seguimientos vencidos y del día, turnos de hoy y sugerencias automáticas del taller (próximo service, presupuestos
esperando respuesta y postventa de autos entregados). Agenda: semana con turnos y seguimientos, «+» para agendar en un día.
Cada seguimiento se cierra con un resultado y propone el próximo paso. Borrar con «Deshacer» y selección múltiple (kit vb-crud).
Idempotente. Uso: python3 tools/vb_agenda.py index.html (después de vb_crud.py)."""
import sys
p=sys.argv[1];h=open(p,encoding='utf8').read()
M='<!-- vb-agenda -->';E='<!-- /vb-agenda -->'
if M in h:
    a=h.index(M);b=h.index(E)+len(E);h=h[:a]+h[b:]
blk=M+r'''<style>
.ag-k{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}
.ag-k .kpi.bad .v{color:#c0392b}
.ag-it{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px solid #eef1f4}
.ag-it:last-child{border-bottom:0}.ag-it .ag-ic{font-size:1.25rem;width:30px;text-align:center}
.ag-it .ag-tx{flex:1;min-width:0}.ag-it .ag-tx b{display:block}.ag-it .ag-ac{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}
.ag-it.vencido .ag-tx b{color:#c0392b}
.ag-wk{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px}
.ag-day{background:#fff;border:1px solid var(--bd);border-radius:var(--r);min-height:170px;display:flex;flex-direction:column}
.ag-day.hoy{border-color:#1f6fd1;box-shadow:0 0 0 2px rgba(31,111,209,.18)}
.ag-dh{display:flex;align-items:center;justify-content:space-between;padding:7px 8px;border-bottom:1px solid #eef1f4;font-weight:700;font-size:.9rem}
.ag-dh button{min-height:28px;padding:0 9px}
.ag-db{padding:6px;display:flex;flex-direction:column;gap:5px}
.ag-ev{display:block;width:100%;text-align:left;border:0;border-radius:8px;padding:5px 7px;font-size:.8rem;cursor:pointer;line-height:1.25;background:#eef4ff;color:#173a6b}
.ag-ev.t{background:#fff4e0;color:#6b4a12}.ag-ev.ok{background:#e9f7ee;color:#1d5c34;text-decoration:line-through;opacity:.75}.ag-ev.bad{background:#fdecea;color:#8a1f15}
.ag-leg{display:flex;gap:12px;flex-wrap:wrap;margin:8px 0 0;font-size:.82rem}.ag-leg i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:4px;vertical-align:-1px}
@media (max-width:640px){.ag-it{flex-wrap:wrap}.ag-it .ag-ac{width:100%;justify-content:flex-start;padding-left:40px}}
@media (max-width:980px){.ag-wk{grid-template-columns:1fr}.ag-day{min-height:0}.ag-k{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>
<script>(function(){if(window.agOn)return;window.agOn=1;
var TIP=[['llamada','📞','Llamar'],['wa','💬','WhatsApp'],['presu','📝','Seguir presupuesto'],['post','⭐','Postventa'],['recor','🔔','Recordatorio'],['visita','🚗','Retiro / entrega']];
var TI={};TIP.forEach(function(t){TI[t[0]]=t;});
var DEL='<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/></svg>',
 EDT='<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>';
var DIAS=['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'];
function may(){return ME&&(ME.rol==='dueno'||ME.rol==='jefe'||ME.rol==='recepcion');}
function boss(){return ME&&(ME.rol==='dueno'||ME.rol==='jefe');}
function pad(n){return String(n).padStart(2,'0');}
function first(n){return String(n||'').split(' ')[0];}
/* ---- datos (se crean solos; en la demo, con ejemplos) ---- */
function L(){if(!Array.isArray(DB.ctareas)){DB.ctareas=[];if(MODO==='practica')seedAg();}return DB.ctareas;}
function seedAg(){var C=DB.clientes||[],V=DB.vehs||[];if(!C.length)return;var me=(DB.users[0]||{}).n||'';
 function vOf(c){var v=V.find(function(x){return x.cliId===c.id;});return v?v.id:'';}
 var ej=[[-2,'10:00','presu','Confirmar presupuesto de frenos',0],[-1,'17:30','llamada','Avisar que llegó el repuesto',1],[0,'09:30','wa','Recordar turno de mañana',2],[0,'12:00','post','Preguntar cómo anda el auto después del service',3],[0,'16:00','llamada','Ofrecer alineación y balanceo',4],[1,'11:00','recor','Vence la VTV: ofrecer revisión previa',5],[2,'10:30','visita','Retiro del auto a domicilio',6],[4,'15:00','presu','Seguir presupuesto de embrague',7]];
 ej.forEach(function(e,i){var c=C[e[4]%C.length];DB.ctareas.push({id:uid('ag'),fecha:addDays(e[0]),hora:e[1],tipo:e[2],tit:e[3],cliId:c.id,vehId:vOf(c),otId:'',notas:'',resp:me,est:'pend',res:'',cre:Date.now()-i*1e5});});
 var c=C[1%C.length];DB.ctareas.push({id:uid('ag'),fecha:addDays(-3),hora:'11:00',tipo:'post',tit:'Postventa: cambio de aceite',cliId:c.id,vehId:vOf(c),otId:'',notas:'',resp:me,est:'hecha',res:'Conforme, pidió turno para alineación',hechaPor:me,hechaEn:addDays(-3),cre:Date.now()-9e6});save();}
function abiertas(){return L().filter(function(t){return t.est!=='hecha';});}
function venc(){var h0=TODAY(),n=new Date(),hm=pad(n.getHours())+':'+pad(n.getMinutes());return abiertas().filter(function(t){return t.fecha<h0||(t.fecha===h0&&t.hora&&t.hora<hm&&false);});}
function deHoy(){var h0=TODAY();return abiertas().filter(function(t){return t.fecha===h0;}).sort(function(a,b){return (a.hora||'99')<(b.hora||'99')?-1:1;});}
function abiertaPara(k,v){return abiertas().some(function(t){return t[k]===v;});}
/* ---- sugerencias del taller ---- */
function sugerencias(){var S=[];
 (DB.vehs||[]).forEach(function(v){if(!v.proxFecha)return;var d=daysTo(v.proxFecha);if(d>14||d<-30||abiertaPara('vehId',v.id))return;var c=cliOf(v.cliId);if(!c)return;
  S.push({ic:'🔧',t:'recor',x:'Próximo service '+v.pat+' ('+v.marca+' '+v.mod+')',s:d<0?'vencido hace '+(-d)+' días':'en '+d+' días',c:c,v:v,o:'',bad:d<0,msg:'Hola '+first(c.n)+', te recordamos que tu '+v.marca+' '+v.mod+' ('+v.pat+') tiene el próximo service el '+fdate(v.proxFecha)+'. ¿Te reservamos un turno? '+DB.cfg.nombre});});
 (DB.ots||[]).forEach(function(o){var c=cliOf(o.cliId),v=vehOf(o.vehId)||{};if(!c)return;
  if(o.estado==='Presupuesto'&&!abiertaPara('otId',o.id))S.push({ic:'📝',t:'presu',x:'Presupuesto esperando respuesta · '+(v.pat||''),s:otNum(o),c:c,v:v,o:o.id,msg:'Hola '+first(c.n)+', ¿pudiste ver el presupuesto de tu '+(v.marca||'vehículo')+' '+(v.pat||'')+'? Cualquier duda te la respondemos. '+DB.cfg.nombre});
  if(o.estado==='Entregado'&&o.entregada){var d=-daysTo(o.entregada);if(d>=2&&d<=10&&!L().some(function(t){return t.otId===o.id&&t.tipo==='post';}))S.push({ic:'⭐',t:'post',x:'Postventa · '+(v.pat||'')+' entregado hace '+d+' días',s:otNum(o),c:c,v:v,o:o.id,msg:'Hola '+first(c.n)+', ¿cómo anda tu '+(v.marca||'vehículo')+' después del trabajo que hicimos? Cualquier cosa, escribinos. '+DB.cfg.nombre});}});
 return S;}
/* ---- pantalla ---- */
UI.agTab=UI.agTab||'hoy';
function lunes(f){var d=new Date((f||TODAY())+'T12:00:00');var w=(d.getDay()+6)%7;d.setDate(d.getDate()-w);return ymd(d);}
function it(t){var c=cliOf(t.cliId)||{},v=vehOf(t.vehId)||{},tp=TI[t.tipo]||TIP[0],ve=t.est!=='hecha'&&t.fecha<TODAY();
 return '<div class="ag-it'+(ve?' vencido':'')+'"><span class="ag-ic" aria-hidden="true">'+tp[1]+'</span><span class="ag-tx"><b>'+h(t.tit)+'</b><span class="mut sm">'+(t.hora?h(t.hora)+' · ':'')+(t.fecha!==TODAY()?fdate(t.fecha)+' · ':'')+h(c.n||'Sin cliente')+(v.pat?' · '+h(v.pat):'')+(t.resp?' · '+h(t.resp):'')+'</span>'+(t.notas?'<span class="sm">'+h(t.notas)+'</span>':'')+'</span>'+
  '<span class="ag-ac">'+(c.tel?'<a class="btn s" target="_blank" rel="noopener" href="'+h(wa(c.tel,'Hola '+first(c.n)+', '))+'">💬</a>':'')+
  '<button class="btn s p" data-act="agdone" data-id="'+t.id+'">✔ Hecho</button><button class="btn s vb-ib" data-act="agedit" data-id="'+t.id+'" title="Editar" aria-label="Editar seguimiento">'+EDT+'</button><button class="btn s vb-ib vb-del" data-act="agdel" data-id="'+t.id+'" title="Borrar" aria-label="Borrar seguimiento">'+DEL+'</button></span></div>';}
function kpi(v,l,tab,bad){return '<button class="kpi'+(bad?' bad':'')+'" data-act="agtab" data-t="'+tab+'"><div class="v">'+v+'</div><div class="l">'+l+'</div></button>';}
V.atencion=function(){if(!may())return '<p>Sin permiso.</p>';L();var T=UI.agTab;
 var bar='<div class="bar"><h2>Atención al cliente</h2><div class="chips">'+[['hoy','Hoy'],['agenda','Agenda'],['hechos','Hechos']].map(function(x){return '<button class="chip'+(T===x[0]?' on':'')+'" data-act="agtab" data-t="'+x[0]+'">'+x[1]+'</button>';}).join('')+'</div><span class="sp"></span><button class="btn p" data-act="agnew">➕ Nuevo seguimiento</button></div>';
 if(T==='agenda')return bar+agenda();if(T==='hechos')return bar+hechos();
 var ve=venc(),hy=deHoy(),tu=(DB.turnos||[]).filter(function(t){return t.fecha===TODAY()&&t.estado!=='Cancelado';}).sort(function(a,b){return a.hora-b.hora;}),sg=sugerencias();
 var r='<div class="ag-k">'+kpi(ve.length,'Seguimientos vencidos','hoy',ve.length)+kpi(hy.length,'Para hoy','hoy')+kpi(tu.length,'Turnos de hoy','agenda')+kpi(sg.length,'Sugerencias del taller','hoy')+'</div>';
 if(ve.length)r+='<div class="card" style="margin-bottom:12px"><h3>⏰ Vencidos</h3>'+ve.sort(function(a,b){return a.fecha<b.fecha?-1:1;}).map(it).join('')+'</div>';
 r+='<div class="g2" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px">';
 r+='<div class="card"><h3>📋 Para hoy · '+fdate(TODAY())+'</h3>'+(hy.length?hy.map(it).join(''):'<p class="mut">No hay seguimientos para hoy. Tocá «➕ Nuevo seguimiento» o agendá una sugerencia.</p>')+'</div>';
 r+='<div class="card"><h3>📅 Turnos de hoy</h3>'+(tu.length?tu.map(function(t){var v=vehOf(t.vehId)||{},c=cliOf(t.cliId)||{};return '<div class="ag-it"><span class="ag-ic" style="width:46px"><b>'+pad(t.hora)+':00</b></span><span class="ag-tx"><b>'+h(v.pat||'')+' · '+h(t.srv)+'</b><span class="mut sm">'+h(c.n||'')+' · '+h(RECURSOS[t.rec]||'')+'</span></span><span class="ag-ac"><span class="badge '+(t.estado==='Confirmado'?'ok':t.estado==='Pendiente'?'warn':'')+'">'+h(t.estado)+'</span><button class="btn s" data-act="tuopen" data-id="'+t.id+'">Abrir</button></span></div>';}).join(''):'<p class="mut">Sin turnos para hoy.</p>')+'</div></div>';
 r+='<div class="card" style="margin-top:12px"><h3>💡 Sugerencias del taller</h3><p class="mut sm" style="margin-top:-4px">El sistema las arma solo: services que se acercan, presupuestos sin respuesta y postventa de autos entregados.</p>'+(sg.length?sg.map(function(s,i){return '<div class="ag-it'+(s.bad?' vencido':'')+'"><span class="ag-ic" aria-hidden="true">'+s.ic+'</span><span class="ag-tx"><b>'+h(s.x)+'</b><span class="mut sm">'+h(s.c.n)+' · '+h(s.s)+'</span></span><span class="ag-ac">'+(s.c.tel?'<a class="btn s" target="_blank" rel="noopener" href="'+h(wa(s.c.tel,s.msg))+'">💬 WhatsApp</a>':'')+'<button class="btn s p" data-act="agsug" data-i="'+i+'">📅 Agendar</button></span></div>';}).join(''):'<p class="mut">Todo al día: no hay sugerencias pendientes.</p>')+'</div>';
 return bar+r;};
function agenda(){var m=UI.agWk||lunes(),r='<div class="bar" style="margin-bottom:10px"><button class="btn" data-act="agwk" data-n="-7" aria-label="Semana anterior">◀</button><button class="btn" data-act="agwk" data-n="0">Esta semana</button><button class="btn" data-act="agwk" data-n="7" aria-label="Semana siguiente">▶</button><b>Semana del '+fdate(m)+' al '+fdate(addDays(6,m))+'</b></div><div class="ag-wk">';
 for(var i=0;i<7;i++){var f=addDays(i,m),d=new Date(f+'T12:00:00');
  var tu=(DB.turnos||[]).filter(function(t){return t.fecha===f&&t.estado!=='Cancelado';}).sort(function(a,b){return a.hora-b.hora;});
  var tk=L().filter(function(t){return t.fecha===f;}).sort(function(a,b){return (a.hora||'99')<(b.hora||'99')?-1:1;});
  r+='<div class="ag-day'+(f===TODAY()?' hoy':'')+'"><div class="ag-dh"><span>'+DIAS[d.getDay()]+' '+f.slice(8)+'/'+f.slice(5,7)+'</span><button class="btn s" data-act="agnew" data-f="'+f+'" aria-label="Agendar el '+fdate(f)+'">+</button></div><div class="ag-db">'+
   tu.map(function(t){var v=vehOf(t.vehId)||{};return '<button class="ag-ev t" data-act="tuopen" data-id="'+t.id+'">'+pad(t.hora)+':00 🔧 '+h(v.pat||'')+' · '+h(t.srv)+'</button>';}).join('')+
   tk.map(function(t){var c=cliOf(t.cliId)||{},cl=t.est==='hecha'?' ok':(f<TODAY()?' bad':'');return '<button class="ag-ev'+cl+'" data-act="'+(t.est==='hecha'?'agver':'agedit')+'" data-id="'+t.id+'">'+(t.hora?h(t.hora)+' ':'')+(TI[t.tipo]||TIP[0])[1]+' '+h(first(c.n))+' · '+h(t.tit)+'</button>';}).join('')+
   (!tu.length&&!tk.length?'<span class="mut sm" style="padding:4px">Libre</span>':'')+'</div></div>';}
 return r+'</div><div class="ag-leg"><span><i style="background:#fff4e0"></i>Turnos del taller</span><span><i style="background:#eef4ff"></i>Seguimientos</span><span><i style="background:#fdecea"></i>Vencidos</span><span><i style="background:#e9f7ee"></i>Hechos</span></div>';}
function hechos(){var H=L().filter(function(t){return t.est==='hecha';}).sort(function(a,b){return (b.hechaEn||'')<(a.hechaEn||'')?-1:1;});
 if(!H.length)return '<div class="card"><p class="mut">Todavía no hay seguimientos cerrados.</p></div>';
 return '<div class="card"><div class="tw"><table data-bulk="ag"><thead><tr><th>Fecha</th><th>Tipo</th><th>Cliente</th><th>Seguimiento</th><th>Resultado</th><th>Hecho por</th><th></th></tr></thead><tbody>'+H.map(function(t){var c=cliOf(t.cliId)||{},tp=TI[t.tipo]||TIP[0];return '<tr data-id="'+t.id+'"><td>'+fdate(t.hechaEn||t.fecha)+'</td><td>'+tp[1]+' '+h(tp[2])+'</td><td>'+h(c.n||'')+'</td><td>'+h(t.tit)+'</td><td>'+h(t.res||'')+'</td><td>'+h(t.hechaPor||'')+'</td><td><button class="btn s vb-ib vb-del" data-act="agdel" data-id="'+t.id+'" title="Borrar" aria-label="Borrar seguimiento">'+DEL+'</button></td></tr>';}).join('')+'</tbody></table></div></div>';}
/* ---- acciones ---- */
ACT.agtab=function(d){UI.agTab=d.t;renderView();};
ACT.agwk=function(d){var n=+d.n;UI.agWk=n?addDays(n,UI.agWk||lunes()):lunes();renderView();};
function form(t){var C=(DB.clientes||[]).slice().sort(function(a,b){return a.n<b.n?-1:1;});var us=(DB.users||[]).filter(function(u){return u.activo!==false&&u.rol!=='limpieza';});
 return '<div class="g4" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px"><div class="f"><label for="ag_t">Tipo</label><select id="ag_t">'+opts(TIP,t.tipo,function(x){return [x[0],x[1]+' '+x[2]];})+'</select></div><div class="f"><label for="ag_f">Fecha</label><input type="date" id="ag_f" value="'+h(t.fecha)+'"></div><div class="f"><label for="ag_h">Hora (opcional)</label><input type="time" id="ag_h" value="'+h(t.hora||'')+'"></div><div class="f"><label for="ag_r">Responsable</label><select id="ag_r">'+opts(us,t.resp,function(u){return [u.n,u.n];})+'</select></div></div>'+
  '<div class="f"><label for="ag_c">Cliente</label><select id="ag_c">'+opts(C,t.cliId,function(c){return [c.id,c.n+(c.tel?' · '+c.tel:'')];},'— Elegí el cliente —')+'</select></div>'+
  '<div class="f"><label for="ag_v">Vehículo (opcional)</label><select id="ag_v"></select></div>'+
  '<div class="f"><label for="ag_x">¿Qué hay que hacer?</label><input id="ag_x" value="'+h(t.tit||'')+'" placeholder="Ej.: llamar para confirmar el presupuesto"></div>'+
  '<div class="f"><label for="ag_n">Notas</label><textarea id="ag_n" rows="2">'+h(t.notas||'')+'</textarea></div>';}
function fillV(sel){var c=val('ag_c'),s=document.getElementById('ag_v');if(!s)return;var vs=(DB.vehs||[]).filter(function(v){return v.cliId===c;});s.innerHTML='<option value="">— Sin vehículo —</option>'+vs.map(function(v){return '<option value="'+h(v.id)+'"'+(v.id===sel?' selected':'')+'>'+h(v.pat+' · '+v.marca+' '+v.mod)+'</option>';}).join('');}
function read(t){var f=val('ag_f'),x=val('ag_x').trim();if(!f)throw new Error('Elegí la fecha.');if(!val('ag_c'))throw new Error('Elegí el cliente.');if(x.length<3)throw new Error('Escribí qué hay que hacer.');
 t.tipo=val('ag_t');t.fecha=f;t.hora=val('ag_h');t.resp=val('ag_r');t.cliId=val('ag_c');t.vehId=val('ag_v');t.tit=x;t.notas=val('ag_n').trim();return t;}
function abrir(t,nuevo){modal({title:nuevo?'Nuevo seguimiento':'Editar seguimiento',ok:nuevo?'Agendar':'Guardar',wide:true,body:form(t),
 calc:function(){fillV(t.vehId);var c=document.getElementById('ag_c');if(c)c.addEventListener('change',function(){fillV('');});},
 onOk:function(){try{read(t);if(nuevo){L().push(t);audit('Seguimiento agendado',t.tit);}else audit('Seguimiento editado',t.tit);save();closeModal();renderView();toast(nuevo?'Seguimiento agendado para el '+fdate(t.fecha):'Cambios guardados');return false;}catch(e){merr(e.message);return false;}}});}
function nuevo(o){o=o||{};return {id:uid('ag'),fecha:o.fecha||TODAY(),hora:'',tipo:o.tipo||'llamada',tit:o.tit||'',cliId:o.cliId||'',vehId:o.vehId||'',otId:o.otId||'',notas:'',resp:ME?ME.n:'',est:'pend',res:'',cre:Date.now()};}
ACT.agnew=function(d){if(!may())return;abrir(nuevo({fecha:d.f,cliId:d.c,vehId:d.v}),true);};
ACT.agedit=function(d){var t=L().find(function(x){return x.id===d.id;});if(t)abrir(t,false);};
ACT.agver=function(d){var t=L().find(function(x){return x.id===d.id;});if(!t)return;var c=cliOf(t.cliId)||{};modal({title:'Seguimiento hecho',hideOk:true,cancel:'Cerrar',body:'<p><b>'+h(t.tit)+'</b><br>'+h(c.n||'')+' · '+fdate(t.fecha)+'</p><p>Resultado: '+h(t.res||'—')+'<br><span class="mut sm">'+h(t.hechaPor||'')+' · '+fdate(t.hechaEn)+'</span></p>'});};
ACT.agsug=function(d){var s=sugerencias()[+d.i];if(!s)return;abrir(nuevo({tipo:s.t,cliId:s.c.id,vehId:s.v&&s.v.id||'',otId:s.o,tit:s.x}),true);};
ACT.agdel=function(d){if(!may())return;var t=L().find(function(x){return x.id===d.id;});if(!t)return;if(MODAL)closeModal();vbRemove({key:'ctareas',ids:[t.id],label:'Seguimiento eliminado',audit:'Seguimiento eliminado'});};
ACT.agdone=function(d){var t=L().find(function(x){return x.id===d.id;});if(!t)return;
 modal({title:'¿Cómo salió? · '+t.tit,ok:'Guardar',body:'<div class="f"><label for="ag_res">Resultado</label><input id="ag_res" placeholder="Ej.: aceptó el presupuesto · no atendió · pidió turno"></div>'+
  '<label style="display:flex;gap:8px;align-items:center;margin:8px 0"><input type="checkbox" id="ag_sig" checked style="width:18px;height:18px;min-height:0"> Agendar el próximo paso</label>'+
  '<div class="g4" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px"><div class="f"><label for="ag_sf">Fecha</label><input type="date" id="ag_sf" value="'+addDays(3)+'"></div><div class="f"><label for="ag_st">Tipo</label><select id="ag_st">'+opts(TIP,t.tipo,function(x){return [x[0],x[1]+' '+x[2]];})+'</select></div></div>'+
  '<div class="f"><label for="ag_sx">Próximo paso</label><input id="ag_sx" value="'+h(t.tit)+'"></div>',
  onOk:function(){var res=val('ag_res').trim(),prev={est:t.est,res:t.res,hechaPor:t.hechaPor,hechaEn:t.hechaEn},sig=null;
   t.est='hecha';t.res=res;t.hechaPor=ME?ME.n:'';t.hechaEn=TODAY();
   if(chk('ag_sig')){if(!val('ag_sf')){merr('Elegí la fecha del próximo paso.');t.est=prev.est;return false;}sig=nuevo({fecha:val('ag_sf'),tipo:val('ag_st'),cliId:t.cliId,vehId:t.vehId,otId:t.otId,tit:val('ag_sx').trim()||t.tit});sig.resp=t.resp||sig.resp;L().push(sig);}
   audit('Seguimiento hecho',t.tit+(res?' · '+res:''));save();closeModal();renderView();
   if(window.vbUndoable)vbUndoable(sig?'Hecho · próximo paso el '+fdate(sig.fecha):'Seguimiento hecho',function(){for(var k in prev)t[k]=prev[k];if(sig){var a=L(),i=a.indexOf(sig);if(i>=0)a.splice(i,1);}save();renderView();});return false;}});};
if(window.VB_BULK)VB_BULK.ag={can:may,del:function(ids){vbRemove({key:'ctareas',ids:ids,label:ids.length+' seguimiento(s) eliminado(s)',audit:'Seguimientos eliminados'});}};
/* ---- menú, permisos, alertas y ficha del cliente ---- */
var ix=NAV.findIndex(function(n){return n[0]==='clientes';});NAV.splice(ix+1,0,['atencion','💬','Atención al cliente']);
['jefe','recepcion'].forEach(function(r){if(Array.isArray(PERM[r])&&PERM[r].indexOf('atencion')<0)PERM[r].push('atencion');});
UXSEC.forEach(function(s){if(s[0]==='cli'&&s[2].indexOf('atencion')<0)s[2].splice(s[2].indexOf('clientes')+1,0,'atencion');});
if(typeof UXKW==='object')UXKW.atencion='agenda calendario seguimiento llamar postventa presupuesto crm hoy';
var _al=alertas;alertas=function(){var A=_al();try{if(may()){var n=venc().length;if(n)A.unshift({t:'bad',x:n+' seguimiento(s) de clientes vencido(s)',go:'atencion'});var k=deHoy().length;if(k)A.push({t:'ok',x:k+' seguimiento(s) de clientes para hoy',go:'atencion'});}}catch(e){}return A;};
new MutationObserver(function(){var m=document.getElementById('modal');if(!m||m.hidden||!MODAL||!MODAL._vbCli||!may()||m.querySelector('[data-act=agnew]'))return;var f=m.querySelector('.mf');if(f){var b=document.createElement('button');b.className='btn';b.dataset.act='agnew';b.dataset.c=MODAL._vbCli;b.textContent='📅 Agendar seguimiento';var cn=f.querySelector('[data-act=mclose]');f.insertBefore(b,cn);}}).observe(document.body,{childList:true,subtree:true});
var _ag=ACT.agnew;ACT.agnew=function(d){if(MODAL&&d.c)closeModal();_ag(d);};
})();</script>'''+E
j=h.rindex('</body>');h=h[:j]+blk+h[j:]
open(p,'w',encoding='utf8').write(h);print('vb_agenda: ok')
