# Menú digital: envío a domicilio en el pedido y botón «Escribinos» por WhatsApp
# Uso: python3 tools/pruebas/envio1.py /ruta/a/index.html
import sys
from urllib.parse import unquote_plus as uq
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'index.html'
res=[]
def chk(c,m):print(('OK   ' if c else 'FALLA ')+m);res.append(bool(c))
with sync_playwright() as p:
    b=p.chromium.launch(args=['--no-proxy-server']);pg=b.new_page(viewport={'width':390,'height':844});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.goto('file://'+F+'#menu');pg.wait_for_timeout(2500)
    chk(pg.locator('#pub .chatb').is_visible() and 'wa.me' in pg.locator('#pub .chatb').get_attribute('href'),'botón «Escribinos» por WhatsApp')
    pg.locator('[data-act=pubadd]:not([disabled])').first.click();pg.wait_for_timeout(300)
    pg.locator('.cartb').click();pg.wait_for_timeout(300)
    pg.select_option('#pc_e','envio');pg.wait_for_timeout(200)
    chk(pg.locator('#pc_d').is_visible(),'opción «Envío a domicilio» pide la dirección')
    pg.fill('#pc_n','Juan Prueba');pg.fill('#pc_t','3875123456')
    pg.evaluate("window.__op=[];window.open=function(u){window.__op.push(String(u));return null;}")
    pg.click('[data-act=pubsend]');pg.wait_for_timeout(300)
    chk(pg.evaluate("window.__op.filter(x=>x.indexOf('wa.me')>=0).length")==0,'sin dirección no envía')
    pg.fill('#pc_d','Belgrano 123, Centro');pg.click('[data-act=pubsend]');pg.wait_for_timeout(300)
    u=uq(pg.evaluate("window.__op.filter(x=>x.indexOf('wa.me')>=0)[0]||''"))
    chk('Envío a domicilio: Belgrano 123' in u,'el WhatsApp lleva la dirección')
    chk(pg.evaluate("DB.pedidos[0].entrega==='envio'&&DB.pedidos[0].dir.indexOf('Belgrano')===0"),'el pedido queda en el sistema con la dirección')
    pg.screenshot(path='/tmp/taller_m.png')
    chk(pg.evaluate("document.documentElement.scrollWidth")<=390,'entra en el celular')
    chk(not errs,'sin errores %s'%errs[:2])
    b.close()
print('%d/%d'%(sum(res),len(res)))
