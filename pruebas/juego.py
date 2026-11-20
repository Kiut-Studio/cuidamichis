#!/usr/bin/env python3
"""Pruebas automáticas de Cuidamichis (Playwright + Chromium).

Uso:   python3 pruebas/juego.py            # corre todo
       python3 pruebas/juego.py -k minijuego   # solo las pruebas cuyo nombre incluye "minijuego"
       python3 pruebas/juego.py --capturas     # además guarda capturas en pruebas/capturas/

Levanta solo un servidor local, abre el juego con `#prueba` (que expone `window.CC`) y simula:
tiempo (con un reloj falso, así los resultados no dependen de la hora en que corrés la prueba),
cuidados, finales, guardado, minijuegos, tienda, copia sin conexión y distintos tamaños de pantalla.
Termina con código 1 si algo falla.
"""
import argparse, functools, http.server, os, socketserver, sys, threading, time, datetime, json
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPT = os.path.join(RAIZ, 'pruebas', 'capturas')
ap = argparse.ArgumentParser()
ap.add_argument('-k', default='')
ap.add_argument('--capturas', action='store_true')
ARGS = ap.parse_args()
if ARGS.capturas: os.makedirs(CAPT, exist_ok=True)

# ---------- servidor local ----------
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()
socketserver.TCPServer.allow_reuse_address = True
SRV = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Q, directory=RAIZ))
PORT = SRV.server_address[1]
threading.Thread(target=SRV.serve_forever, daemon=True).start()
URL = f'http://localhost:{PORT}/index.html#prueba'

# ---------- reloj falso: 18/11/2026 10:00 en Asunción, avanzando normal ----------
INICIO = int(datetime.datetime(2026, 11, 18, 13, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
RELOJ = """(()=>{const R=Date,real=R.now.bind(R),off=%d-real();
class D extends R{constructor(...a){if(a.length)super(...a);else super(real()+off)} static now(){return real()+off}}
window.Date=D})()""" % INICIO

RES = []
def check(nombre, ok, detalle=''):
    RES.append((nombre, bool(ok), detalle))
    print(('  ✅ ' if ok else '  ❌ ') + nombre + (f'  → {detalle}' if detalle and not ok else ''))

PRUEBAS = []
def prueba(f):
    PRUEBAS.append(f); return f

class Sesion:
    """Una pestaña con captura de errores."""
    def __init__(s, br, vp=(390, 844), movil=True, reloj=True, offline_ok=False):
        s.ctx = br.new_context(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=2 if movil else 1,
                               is_mobile=movil, has_touch=movil, timezone_id='America/Asuncion', locale='es-PY')
        if reloj: s.ctx.add_init_script(RELOJ)
        s.pg = s.ctx.new_page(); s.errs = []; s.malas = []
        s.pg.on('console', lambda m: s.errs.append(m.text) if m.type == 'error' else None)
        s.pg.on('pageerror', lambda e: s.errs.append('PAGEERROR ' + str(e)))
        s.pg.on('requestfailed', lambda r: s.malas.append('FALLÓ ' + r.url))
        s.pg.on('response', lambda r: s.malas.append(f'{r.status} {r.url}') if r.status >= 400 else None)
    def abrir(s, empezar=True, avatar='sofi', nombre='Michi'):
        s.pg.goto(URL); s.pg.wait_for_function('window.CC&&document.readyState==="complete"'); s.pg.wait_for_timeout(500)
        if empezar: s.empezar(avatar, nombre)
        return s
    def empezar(s, avatar='sofi', nombre='Michi'):
        s.pg.click(f'.ch[data-id={avatar}]'); s.pg.click('#introNext')
        if nombre: s.pg.fill('#nameIn', nombre)
        s.pg.click('#introGo'); s.pg.wait_for_timeout(300)
    def ev(s, js): return s.pg.evaluate(js)
    def foto(s, nombre):
        if ARGS.capturas: s.pg.screenshot(path=os.path.join(CAPT, nombre + '.png'))
    def cerrar(s): s.ctx.close()

def tocar(s, sel):  # clic real del DOM (los botones del portón y la luz se mueven a propósito)
    s.ev("document.querySelector('%s').click()" % sel); s.pg.wait_for_timeout(80)

def editar_guardado(s, js):
    """Cambia el guardado como si el juego estuviera cerrado (si no, al recargar se pisa solo) y lo vuelve a abrir."""
    s.pg.goto(f'http://localhost:{PORT}/favicon-32.png')
    s.pg.evaluate("(f)=>{const x=JSON.parse(localStorage.getItem('conCuidado.v1'));(new Function('x',f))(x);localStorage.setItem('conCuidado.v1',JSON.stringify(x))}", js)
    s.pg.goto(URL); s.pg.wait_for_function('window.CC&&document.readyState==="complete"'); s.pg.wait_for_timeout(700)

def dias(s, n, paso=.25):  # n días de gatito, dándole de comer entre medio
    for _ in range(int(round(n / paso))):
        if s.ev('CC.S.terminado'): break
        cuidar(s); s.ev('CC.age(%s)' % paso)

def cuidar(s):  # deja todo en 100 (para simular días sin que el gatito se muera)
    s.ev("(()=>{const S=CC.S;for(const k in S.pet)S.pet[k]=100;for(const k in S.avatar)S.avatar[k]=100;S.cacas=[];S.idle=0;S.tAband=0})()")

# =====================================================================
@prueba
def carga_sin_errores(br):
    for nombre, vp, movil in [('móvil', (390, 844), True), ('compu', (1280, 820), False)]:
        s = Sesion(br, vp, movil).abrir(empezar=False)
        s.pg.wait_for_timeout(800)
        check(f'carga {nombre}: sin errores de consola', not s.errs, str(s.errs))
        check(f'carga {nombre}: ninguna descarga fallida ni 404', not s.malas, str(s.malas))
        check(f'carga {nombre}: aparece la elección de avatar', s.ev("!document.getElementById('intro').hidden"))
        n = s.ev("document.querySelectorAll('.ch').length")
        check(f'carga {nombre}: 5 avatares', n == 5, n)
        f = s.ev("document.fonts.check('600 20px Fredoka')&&document.fonts.check('700 20px Caveat')")
        check(f'carga {nombre}: las tipografías son locales (no dependen de Google)', f and not any('fonts.g' in m for m in s.malas), (f, s.malas))
        s.foto(f'01-avatar-{nombre}'); s.cerrar()

@prueba
def inicio_y_nombre(br):
    s = Sesion(br).abrir(avatar='deisy', nombre='')
    check('avatar elegido queda guardado', s.ev('CC.S.char') == 'deisy')
    check('sin nombre → "Michi"', s.ev('CC.S.name') == 'Michi')
    s.cerrar()
    s = Sesion(br).abrir(avatar='nora', nombre='  Luna   de   Miel  muy largo')
    nm = s.ev('CC.S.name')
    check('el nombre se limpia los espacios dobles y se corta a 14 letras', nm == 'Luna de Miel m', nm)
    s.cerrar()
    # un nombre con HTML no puede inyectar nada
    s = Sesion(br).abrir(nombre='<img src=x onerror=window.__xss=1>')
    s.ev("CC.endGame('descuido')"); s.pg.wait_for_timeout(3800)
    check('nombre con HTML: no se ejecuta (XSS)', s.ev('window.__xss') is None)
    check('nombre con HTML: se muestra como texto', '<img' in s.ev("document.getElementById('finalMsg').textContent"))
    s.cerrar()

@prueba
def cuidados_basicos(br):
    s = Sesion(br).abrir()
    s.ev("CC.S.pet.hambre=50;CC.S.pet.limpieza=50;CC.S.avatar.hambre=50;CC.S.avatar.higiene=50;CC.render()")
    s.pg.click('#aFeed'); h = s.ev('CC.S.pet.hambre')
    check('Alimentar sube la comida +20', 69 < h <= 70.5, h)
    s.pg.click('#aBath'); l = s.ev('CC.S.pet.limpieza')
    check('Bañar sube la limpieza +25', 74 < l <= 75.5, l)
    s.pg.click('#tabAv'); s.pg.click('#aEat'); s.pg.click('#aShower')
    a = s.ev('[CC.S.avatar.hambre,CC.S.avatar.higiene]')
    check('el avatar come (+20) y se baña (+25)', 69 < a[0] <= 70.5 and 74 < a[1] <= 75.5, a)
    s.ev("CC.S.pet.hambre=95"); s.pg.click('#tabPet'); s.pg.click('#aFeed')
    check('las barras no pasan de 100', s.ev('CC.S.pet.hambre') <= 100)
    # mimar tocando al gatito
    s.ev("CC.S.pet.felicidad=50"); g = s.ev('CC.geo()'); box = s.ev("(()=>{const r=document.getElementById('cv').getBoundingClientRect();return [r.left,r.top]})()")
    s.pg.mouse.click(box[0] + g['cx'] + g['cs'] / 2, box[1] + g['cy'] + g['cs'] * .6); s.pg.wait_for_timeout(200)
    f = s.ev('CC.S.pet.felicidad')
    check('tocar al gatito lo mima (+3 felicidad)', f > 51, f)
    # cacas: aparece una, se limpia tocándola
    s.ev("CC.S.cacas.push({x:.3,y:.8})"); fr = s.ev('CC.S.fru')
    s.pg.mouse.click(box[0] + .3 * s.ev('innerWidth') if False else box[0] + .3 * s.ev("document.getElementById('cv').getBoundingClientRect().width"),
                     box[1] + .8 * s.ev("document.getElementById('cv').getBoundingClientRect().height"))
    s.pg.wait_for_timeout(200)
    check('tocar una caca la limpia y da 🍓', s.ev('CC.S.cacas.length') == 0 and s.ev('CC.S.fru') > fr, (s.ev('CC.S.cacas.length'), fr, s.ev('CC.S.fru')))
    check('sin errores', not s.errs, str(s.errs)); s.cerrar()

@prueba
def tiempo_y_desgaste(br):
    s = Sesion(br).abrir(); h0 = s.ev('CC.S.pet.hambre'); l0 = s.ev('CC.S.pet.limpieza')
    s.ev('CC.age(1/24)')   # 1 hora de gatito, de día
    h, l = s.ev('[CC.S.pet.hambre,CC.S.pet.limpieza]')
    check('1 h: la comida baja ≈7,2 (0,06×3600/30)', abs((h0 - h) - 7.2) < .6, h0 - h)
    check('1 h: la limpieza baja ≈3,6', abs((l0 - l) - 3.6) < .6, l0 - l)
    e = s.ev('CC.S.edad'); check('1 h: la edad avanza 1/24 de día', abs(e - 1 / 24) < .002, e)
    s.cerrar()

@prueba
def finales(br):
    # descuido: sin darle nada se muere
    s = Sesion(br).abrir(); s.ev('CC.age(1)')
    st = s.ev('[CC.S.terminado,CC.S.final]')
    check('final por descuido (nada de cuidados en un día)', st == [True, 'descuido'], st)
    s.pg.wait_for_timeout(3800)
    check('aparece la pantalla de fin', s.ev("!document.getElementById('final').hidden"))
    check('el mensaje dice que se fue apagando', 'apagando' in s.ev("document.getElementById('finalMsg').textContent"))
    s.foto('final-descuido')
    s.pg.click('#againBtn'); s.pg.wait_for_timeout(300)
    check('"Jugar de nuevo" lleva a nombrar al nuevo gatito', s.ev("!document.getElementById('introB').hidden"))
    s.cerrar()
    # portón
    s = Sesion(br).abrir(); s.ev("CC.S.porton=true"); s.ev('CC.age(0.01)')
    st = s.ev('[CC.S.terminado,CC.S.final]')
    check('final por portón abierto (>5 min)', st == [True, 'porton'], st)
    s.pg.wait_for_timeout(3800)
    check('el mensaje dice atropellado', 'atropellado' in s.ev("document.getElementById('finalMsg').textContent"))
    s.foto('final-porton'); s.cerrar()
    # portón abierto poco tiempo: no pasa nada
    s = Sesion(br).abrir(); s.ev("CC.S.porton=true"); s.ev('CC.age(0.003)')   # ~4 min
    check('portón abierto 4 min: todavía seguro', s.ev('CC.S.terminado') is False)
    tocar(s, '#gateBtn'); check('cerrar el portón reinicia el contador', s.ev('CC.S.tPorton') == 0 and s.ev('CC.S.porton') is False)
    s.cerrar()

@prueba
def crecimiento_y_vejez(br):
    s = Sesion(br).abrir(); etapas = []
    s.ev("CC.S.care.juego=500")
    for dia in range(14):
        dias(s, 1); etapas.append(s.ev('CC.S.stage'))
        if s.ev('CC.S.terminado'): break
    st = s.ev('[CC.S.terminado,CC.S.final,CC.S.pers]')
    check('con buenos cuidados llega a la vejez (día 14)', st[:2] == [True, 'vejez'], (st, etapas))
    est = lambda e: 0 if e < 1 else 1 if e < 3 else 2 if e < 8 else 3
    # justo en el límite de un día la edad puede quedar 0,99999: se acepta el valor de un lado o del otro
    check('etapas: bebé hasta el día 1, joven hasta el 3, adulto hasta el 8, abuelo hasta el 14',
          len(etapas) >= 13 and all(e in (est(d - 1e-6), est(d)) for d, e in enumerate(etapas, 1)), etapas)
    check('personalidad por cómo lo criaste (juego → juguetón)', st[2] == 'jugueton', st)
    check('el final de vejez da +50 🍓 (y los premios de crecer)', s.ev('CC.S.fru') >= 10 + 50 + 15 * 3, s.ev('CC.S.fru'))
    s.pg.wait_for_timeout(3800); check('pantalla de vida feliz', 'para siempre' in s.ev("document.getElementById('finalMsg').textContent"))
    s.cerrar()
    s = Sesion(br).abrir(); s.ev("CC.S.care.descuido=1e7")
    for d in range(9):
        dias(s, 1)
        if s.ev('CC.S.stage') >= 2: break
    check('callejero si lo descuidaste de joven', s.ev('CC.S.pers') == 'callejero', s.ev('CC.S.pers'))
    s.cerrar()

@prueba
def guardado_y_regreso(br):
    s = Sesion(br).abrir(avatar='cinthia', nombre='Pelusa')
    s.ev("CC.S.fru=77;CC.S.own.pelota=1;CC.S.pet.hambre=80"); s.pg.click('#aFeed'); s.pg.wait_for_timeout(150)
    s.pg.reload(); s.pg.wait_for_function('window.CC'); s.pg.wait_for_timeout(600)
    d = s.ev('[CC.S.name,CC.S.char,CC.S.fru,!!CC.S.own.pelota]')
    check('al recargar se conserva nombre, avatar, frutillas y compras', d == ['Pelusa', 'cinthia', 77, True], d)
    check('al recargar no vuelve a pedir el avatar', s.ev("document.getElementById('intro').hidden"))
    # estuve 2 horas afuera
    h0 = s.ev('CC.S.pet.hambre')
    editar_guardado(s, "x.last-=7200*1000")
    h = s.ev('CC.S.pet.hambre')
    check('2 h afuera: la comida baja ≈14,4', abs((h0 - h) - 14.4) < 1.5, h0 - h)
    check('aviso "Estuviste 2 h afuera"', 'afuera' in s.ev("document.getElementById('toast').textContent"), s.ev("document.getElementById('toast').textContent"))
    # reloj corrido al futuro (celular con la fecha mal): no debe congelar al gatito
    editar_guardado(s, "x.last+=86400*1000")
    fut = s.ev('CC.S.last-Date.now()')
    check('si el guardado quedó en el futuro, se corrige (no congela al gatito)', fut < 5000, fut)
    # guardado corrupto
    s.pg.goto(f'http://localhost:{PORT}/favicon-32.png'); s.pg.evaluate("localStorage.setItem('conCuidado.v1','{esto no es json')")
    s.pg.goto(URL); s.pg.wait_for_function('window.CC'); s.pg.wait_for_timeout(500)
    check('un guardado dañado no rompe el juego (empieza de cero)', s.ev("!document.getElementById('intro').hidden") and not [e for e in s.errs if 'PAGEERROR' in e], s.errs)
    s.cerrar()

@prueba
def dia_y_noche(br):
    s = Sesion(br).abrir()
    s.ev("CC.S.mode='prueba';CC.S.edad=.5;CC.render()")   # prueba: las 21:00
    check('a las 21:00 es de noche', s.ev('CC.isNight()') is True)
    check('de noche aparece el botón de la luz', s.ev("!document.getElementById('lightBtn').hidden"))
    tocar(s, '#lightBtn'); check('se apaga la luz', s.ev('CC.S.luz') is False)
    e0 = s.ev("CC.S.pet.energia=40;CC.S.pet.energia"); s.ev('CC.age(0.05)'); e1 = s.ev('CC.S.pet.energia')
    check('durmiendo recupera energía', e1 > e0, (e0, e1)); s.foto('noche-luz-apagada')
    # molestarlo dormido
    s.ev("CC.S.pet.felicidad=80"); s.pg.click('#aFeed'); f = s.ev('CC.S.pet.felicidad')
    check('alimentarlo dormido lo enoja (−3 felicidad)', f < 80 + 1 and f > 0 and f != 80, f)
    s.pg.click('#aPlay'); check('de noche con la luz apagada no se puede jugar', s.ev("document.getElementById('games').hidden"))
    s.ev("CC.S.edad=0.9;CC.render()"); s.ev('CC.age(0.1)')
    check('al amanecer la luz se prende sola', s.ev('CC.S.luz') is True, [s.ev('CC.S.luz'), s.ev('CC.isNight()')])
    s.cerrar()

@prueba
def tienda_y_mochila(br):
    s = Sesion(br).abrir()
    s.pg.click('#shopBtn'); check('abre la tienda', s.ev("!document.getElementById('shop').hidden"))
    dis = s.ev("[...document.querySelectorAll('[data-buy]')].filter(b=>b.disabled).length")
    check('con 10 🍓 lo que no alcanza está deshabilitado (12 de 16 cosas)', dis == 12, dis)
    s.pg.click('[data-buy=atun]'); check('comprar atún: −6 🍓 y 1 en la mochila', s.ev('[CC.S.fru,CC.S.inv.atun]') == [4, 1], s.ev('[CC.S.fru,CC.S.inv.atun]'))
    s.ev("CC.S.fru=1000"); s.pg.click('#shopBack'); s.pg.click('#shopBtn')
    for k in ['cama', 'mono', 'corona', 'gorra', 'birrete']: s.pg.click(f'[data-buy={k}]')
    check('compras permanentes quedan en own', s.ev('[!!CC.S.own.cama,!!CC.S.own.mono,!!CC.S.own.corona]') == [True, True, True])
    check('la ropa nueva (de trabajo) también se compra y se pone', s.ev('[!!CC.S.own.gorra,!!CC.S.own.birrete,CC.S.wear]') == [True, True, 'birrete'], s.ev('[CC.S.own,CC.S.wear]'))
    check('lo último que comprás para vestir se lo pone', s.ev('CC.S.wear') == 'birrete', s.ev('CC.S.wear'))
    s.pg.click('#shopBack'); s.pg.click('#bagBtn'); s.pg.click('[data-wear=corona]'); s.pg.click('#bagBack'); s.pg.click('#shopBtn')
    s.pg.click('#shopBack'); s.foto('gatito-corona')
    s.ev("CC.S.pet.hambre=30"); s.pg.click('#bagBtn'); s.pg.click('[data-use=atun]'); s.pg.wait_for_timeout(200)
    check('usar atún de la mochila: +35 comida', s.ev('CC.S.pet.hambre') >= 64 and s.ev('CC.S.inv.atun') == 0, s.ev('CC.S.pet.hambre'))
    s.pg.click('#bagBtn'); s.pg.click('[data-wear=mono]'); check('cambiar de moño en el ropero', s.ev('CC.S.wear') == 'mono')
    s.pg.click('[data-wear=mono]'); check('sacarse la ropa', s.ev('CC.S.wear') == '')
    check('sin errores', not s.errs, str(s.errs)); s.cerrar()

def esperar_juego(s, seg=4):
    s.pg.wait_for_function('CC.MG&&CC.MG.t>=0', timeout=seg * 1000)

@prueba
def minijuegos(br):
    for kind in ['lana', 'laser', 'cajas']:
        s = Sesion(br).abrir(); s.ev("CC.S.pet.felicidad=40")
        s.pg.click('#aPlay'); s.pg.click(f'[data-g={kind}]'); esperar_juego(s)
        check(f'{kind}: arranca tras la cuenta regresiva', s.ev('!!CC.MG') is True)
        r = s.ev("(()=>{const r=document.getElementById('mgCv').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
        if kind == 'lana':
            s.pg.mouse.move(r[0] + r[2] / 2, r[1] + r[3] * .8); s.pg.mouse.down()
            for i in range(120):
                x = s.ev('CC.MG.items.filter(i=>i.k!=="drop").sort((a,b)=>b.y-a.y)[0]?.x')
                if x is not None: s.pg.mouse.move(r[0] + x, r[1] + r[3] * .8)
                s.pg.wait_for_timeout(100)
                if s.ev('CC.MG.score') >= 4: break
            s.pg.mouse.up()
            check('lana: mover al gatito atrapa lanas y suma puntos', s.ev('CC.MG.score') >= 4, s.ev('CC.MG.score'))
            s.ev('CC.MG.t=24.8')
        if kind == 'laser':
            hits = 0
            for i in range(40):
                d = s.ev('CC.MG.dot&&[CC.MG.dot.x,CC.MG.dot.y]')
                if d: s.pg.mouse.click(r[0] + d[0], r[1] + d[1]); hits += 1
                s.pg.wait_for_timeout(100)
                if hits >= 6: break
            check('laser: tocar el puntito suma puntos', s.ev('CC.MG.score') >= 4, s.ev('CC.MG.score'))
            s.ev('CC.MG.t=19.8')
        if kind == 'cajas':
            for ronda in range(5):
                s.pg.wait_for_function('CC.MG.phase==="pick"', timeout=15000)
                bx = s.ev('CC.MG.w*(.2+CC.MG.slot[CC.MG.cat]*.3)')
                s.pg.mouse.click(r[0] + bx, r[1] + r[3] * .6); s.pg.wait_for_timeout(1500)
        s.pg.wait_for_function('!document.getElementById("mgRes").hidden', timeout=8000)
        sc = s.ev('CC.MG.score'); fel = s.ev('CC.S.pet.felicidad')
        check(f'{kind}: muestra el resultado y hay puntaje', sc > 0, sc)
        check(f'{kind}: sube la felicidad del gatito', fel > 40, fel)
        check(f'{kind}: guarda el récord', s.ev('CC.S.best.%s' % kind) == sc, s.ev('CC.S.best'))
        s.foto(f'minijuego-{kind}')
        s.pg.click('#mgDone'); check(f'{kind}: "¡Listo!" vuelve al patio', s.ev("document.getElementById('mg').hidden"))
        check(f'{kind}: sin errores', not s.errs, str(s.errs)); s.cerrar()
    # salir con la ✕ durante la cuenta regresiva no da premios
    s = Sesion(br).abrir(); f0 = s.ev('CC.S.pet.felicidad'); s.ev("CC.S.pet.felicidad=40")
    s.pg.click('#aPlay'); s.pg.click('[data-g=lana]'); s.pg.click('#mgQuit')
    check('salir en la cuenta regresiva no da premios ni rompe', s.ev("document.getElementById('mg').hidden") and s.ev('CC.S.pet.felicidad') <= 40.5)
    s.cerrar()

def rect_mg(s):
    return s.ev("(()=>{const r=document.getElementById('mgCv').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")

def jugar_kiosco(s, r, objetivo=6):
    for i in range(150):
        i_ = s.ev('CC.MG.cust.findIndex(c=>c)')
        if i_ >= 0:
            item = s.ev('CC.MG.cust[%d].item' % i_); x = s.ev('CC.MG.w*(.2+%d*.3)' % item)
            s.pg.mouse.click(r[0] + x, r[1] + r[3] * .8)
        s.pg.wait_for_timeout(80)
        if s.ev('CC.MG.score') >= objetivo: break

def jugar_reparto(s, r, objetivo=4):
    for i in range(200):
        x = s.ev('(()=>{const b=CC.MG.items.filter(i=>i.k==="box"&&!i.done).sort((a,b)=>b.y-a.y)[0];return b?b.x:null})()')
        if x is not None: s.pg.mouse.click(r[0] + x, r[1] + r[3] * .6)
        s.pg.wait_for_timeout(60)
        if s.ev('CC.MG.score') >= objetivo: break

def jugar_voley(s, golpes=3):
    for i in range(1500):
        falta = s.ev('CC.MG.b.dir==="toAv"?CC.MG.b.d-CC.MG.b.t:99')
        if 0 < falta < .12: s.pg.mouse.click(60, 60); s.pg.wait_for_timeout(120)
        if s.ev('CC.MG.rally') >= golpes: break
        s.pg.wait_for_timeout(15)

@prueba
def trabajo(br):
    s = Sesion(br).abrir()
    s.pg.click('#tabAv')
    # --- cuándo NO se puede ir a trabajar
    s.ev("CC.S.porton=true;CC.render()"); s.pg.click('#aWork')
    check('con el portón abierto no podés irte a trabajar', s.ev("document.getElementById('jobs').hidden") and 'portón' in s.ev('CC.workBlock()'))
    s.ev("CC.S.porton=false;CC.S.avatar.hambre=10;CC.render()")
    check('con hambre no podés trabajar', 'hambre' in s.ev('CC.workBlock()'))
    s.ev("CC.S.avatar.hambre=100;CC.S.avatar.animo=10;CC.render()")
    check('sin ánimo no podés trabajar (hay que jugar con el gatito)', 'ganas' in s.ev('CC.workBlock()'))
    s.ev("CC.S.avatar.animo=100;CC.S.pet.salud=10;CC.render()")
    check('con el gatito enfermo no te vas', s.ev('CC.workBlock()') != '')
    s.ev("CC.S.pet.salud=100;CC.S.mode='prueba';CC.S.edad=.5;CC.render()")
    check('de noche no hay trabajo', 'noche' in s.ev('CC.workBlock()'))
    s.ev("CC.S.edad=.1;CC.render()")
    check('de día y con todo bien, sí se puede', s.ev('CC.workBlock()') == '', s.ev('CC.workBlock()'))
    # --- el kiosco
    cuidar(s); s.ev("CC.S.fru=0;CC.render()")
    s.pg.click('#aWork'); check('abre la pantalla de trabajos', s.ev("!document.getElementById('jobs').hidden"))
    s.pg.click('[data-j=kiosco]'); esperar_juego(s)
    check('kiosco: no se puede "volver a jugar" un turno', s.ev("document.getElementById('mgAgain').hidden"))
    r = rect_mg(s); jugar_kiosco(s, r)
    check('kiosco: atender clientes suma puntos', s.ev('CC.MG.score') >= 5, s.ev('CC.MG.score'))
    s.foto('trabajo-kiosco')
    s.ev('CC.MG.t=29.8'); s.pg.wait_for_function('!document.getElementById("mgRes").hidden', timeout=8000)
    sc = s.ev('CC.MG.score'); pay = round(2 + sc * 1.1)
    check('kiosco: paga frutillas según el puntaje', s.ev('CC.S.fru') == pay, [s.ev('CC.S.fru'), pay])
    check('el turno cansa: −18 comida, −12 higiene, −12 ánimo', s.ev('[CC.S.avatar.hambre,CC.S.avatar.higiene,CC.S.avatar.animo].map(Math.round)') == [82, 88, 88], s.ev('[CC.S.avatar.hambre,CC.S.avatar.higiene,CC.S.avatar.animo]'))
    check('el gatito te extraña (−6 felicidad)', 93 <= s.ev('CC.S.pet.felicidad') <= 94.5, s.ev('CC.S.pet.felicidad'))
    check('trabajar le baja la afinidad (−4)', 95 <= s.ev('CC.S.pet.afinidad') <= 96.5, s.ev('CC.S.pet.afinidad'))
    check('al volver el portón queda abierto (hay que cerrarlo)', s.ev('CC.S.porton') is True)
    s.foto('trabajo-resultado')
    s.pg.click('#mgDone'); s.pg.wait_for_timeout(1300)
    check('al volver avisa que hay que cerrar el portón', 'portón' in s.ev("document.getElementById('toast').textContent"), s.ev("document.getElementById('toast').textContent"))
    check('no se puede otro turno hasta cerrar el portón', 'portón' in s.ev('CC.workBlock()'))
    tocar(s, '#gateBtn'); check('cerrando el portón se puede trabajar de nuevo', s.ev('CC.workBlock()') == '' and s.ev('CC.S.porton') is False)
    # el portón abierto al volver sigue siendo peligroso, como siempre
    s.ev("CC.S.porton=true;CC.S.tPorton=0;CC.S.pet.hambre=100"); s.ev("CC.S.last-=3600*1000")
    s.pg.click('#tabPet'); s.pg.click('#aFeed'); s.pg.wait_for_timeout(300)
    check('si te olvidás de cerrar el portón, igual hay riesgo', s.ev('CC.S.terminado') is True and s.ev('CC.S.final') == 'porton', s.ev('[CC.S.terminado,CC.S.final]'))
    check('sin errores', not s.errs, str(s.errs)); s.cerrar()
    # --- el reparto
    s = Sesion(br).abrir(); cuidar(s); s.ev("CC.S.fru=0")
    s.pg.click('#tabAv'); s.pg.click('#aWork'); s.pg.click('[data-j=reparto]'); esperar_juego(s)
    r = rect_mg(s); jugar_reparto(s, r)
    check('reparto: juntar paquetes suma puntos', s.ev('CC.MG.score') >= 3, s.ev('CC.MG.score'))
    s.foto('trabajo-reparto')
    s.ev('CC.MG.t=29.8'); s.pg.wait_for_function('!document.getElementById("mgRes").hidden', timeout=8000)
    check('reparto: paga frutillas y guarda el récord', s.ev('CC.S.fru') > 0 and s.ev('CC.S.best.reparto') == s.ev('CC.MG.score'), s.ev('[CC.S.fru,CC.S.best]'))
    s.pg.click('#mgDone'); check('reparto: sin errores', not s.errs, str(s.errs)); s.cerrar()
    # --- salir con la ✕ en la cuenta regresiva: no pasa nada (no te fuiste)
    s = Sesion(br).abrir(); cuidar(s)
    s.pg.click('#tabAv'); s.pg.click('#aWork'); s.pg.click('[data-j=kiosco]'); s.pg.click('#mgQuit')
    check('arrepentirse antes de empezar no cuesta nada ni deja el portón abierto', s.ev('CC.S.porton') is False and s.ev('CC.S.avatar.animo') >= 99.5)
    # --- cerrar el juego en medio del turno no deja el portón abierto
    s.pg.click('#aWork'); s.pg.click('[data-j=kiosco]'); esperar_juego(s)
    s.pg.reload(); s.pg.wait_for_function('window.CC&&document.readyState==="complete"'); s.pg.wait_for_timeout(500)
    check('si se cierra la app en pleno turno, el portón sigue cerrado', s.ev('CC.S.porton') is False)
    s.cerrar()

@prueba
def voley(br):
    s = Sesion(br).abrir(); s.ev("CC.S.pet.felicidad=40;CC.S.avatar.animo=50;CC.S.fru=0")
    s.pg.click('#aPlay'); check('el vóley está en el menú de juegos', s.ev("!!document.querySelector('[data-g=voley]')"))
    s.pg.click('[data-g=voley]'); esperar_juego(s)
    check('vóley: empieza con 3 vidas', s.ev('CC.MG.lives') == 3)
    jugar_voley(s, 3)
    check('vóley: tocar a tiempo devuelve la pelota y suma', s.ev('CC.MG.rally') >= 3 and s.ev('CC.MG.score') >= 3, s.ev('[CC.MG.rally,CC.MG.score]'))
    s.foto('juego-voley')
    # dejar pasar la pelota: pierde una vida
    v0 = s.ev('CC.MG.lives'); s.pg.wait_for_function('CC.MG.lives<%d' % v0, timeout=8000)
    check('vóley: si no la devolvés perdés una vida y se corta la racha', s.ev('CC.MG.lives') == v0 - 1 and s.ev('CC.MG.rally') == 0)
    s.ev('CC.MG.lives=1'); s.pg.wait_for_function('!document.getElementById("mgRes").hidden', timeout=8000)
    sc = s.ev('CC.MG.score')
    check('vóley: sin vidas termina y muestra el resultado', sc >= 3, sc)
    check('vóley: sube la felicidad del gatito y el ánimo de vos (más que otros juegos)', s.ev('CC.S.pet.felicidad') > 40 and s.ev('CC.S.avatar.animo') >= 50 + 8 + 12 - 1, s.ev('[CC.S.pet.felicidad,CC.S.avatar.animo]'))
    check('vóley: guarda el récord', s.ev('CC.S.best.voley') == sc)
    s.pg.click('#mgDone'); check('vóley: sin errores', not s.errs, str(s.errs)); s.cerrar()
    # no se juega con el gatito muy cansado, igual que los otros
    s = Sesion(br).abrir(); s.ev("CC.S.pet.energia=5"); s.pg.click('#aPlay')
    check('con el gatito cansado tampoco hay vóley', s.ev("document.getElementById('games').hidden"))
    s.cerrar()

def mimar(s):
    g = s.ev('CC.geo()'); box = s.ev("(()=>{const r=document.getElementById('cv').getBoundingClientRect();return [r.left,r.top]})()")
    s.pg.mouse.click(box[0] + g['cx'] + g['cs'] / 2 + s.ev('CC.S.pet.afinidad<CC.AFI.lejos?g.cs*.16:0') if False else box[0] + g['cx'] + g['cs'] / 2, box[1] + g['cy'] + g['cs'] * .6)
    s.pg.wait_for_timeout(250)

@prueba
def afinidad(br):
    s = Sesion(br).abrir()
    check('empieza en 40 y tiene su barra', s.ev('CC.S.pet.afinidad') == 40 and s.ev("!!document.getElementById('p_afinidadB')"), s.ev('CC.S.pet.afinidad'))
    # --- cómo sube
    s.ev("CC.S.pet.felicidad=50"); a0 = s.ev('CC.S.pet.afinidad'); mimar(s); a1 = s.ev('CC.S.pet.afinidad')
    check('un mimo sube la afinidad', a1 > a0, [a0, a1])
    s.pg.wait_for_timeout(800); mimar(s)
    check('mimar sin parar no la sube más (hay que esperar)', abs(s.ev('CC.S.pet.afinidad') - a1) < .01, [a1, s.ev('CC.S.pet.afinidad')])
    s.ev("CC.S.pet.hambre=40"); a = s.ev('CC.S.pet.afinidad'); s.pg.click('#aFeed')
    check('darle de comer cuando lo necesita la sube', s.ev('CC.S.pet.afinidad') > a, [a, s.ev('CC.S.pet.afinidad')])
    a = s.ev('CC.S.pet.afinidad'); s.pg.click('#aPlay'); s.pg.click('#quickPlay'); s.pg.wait_for_timeout(200)
    check('jugar con él la sube más', s.ev('CC.S.pet.afinidad') > a + 1.5, [a, s.ev('CC.S.pet.afinidad')])
    s.cerrar()
    # --- cómo baja
    s = Sesion(br).abrir(); cuidar(s); s.ev("CC.S.pet.afinidad=60;CC.S.pet.felicidad=10")
    s.ev('CC.age(0.1)')
    check('descuidarlo (necesidades en rojo) le baja la afinidad', s.ev('CC.S.pet.afinidad') < 58, s.ev('CC.S.pet.afinidad'))
    cuidar(s); s.ev("CC.S.pet.afinidad=60;CC.S.idle=9*3600"); s.ev('CC.age(0.25)')
    check('si hace horas que no le das cariño (aunque coma), baja', s.ev('CC.S.pet.afinidad') < 56, s.ev('CC.S.pet.afinidad'))
    cuidar(s); s.ev("CC.S.pet.afinidad=60;CC.S.idle=0"); s.ev('CC.age(0.25)')
    check('con cariño reciente no baja', s.ev('CC.S.pet.afinidad') > 59, s.ev('CC.S.pet.afinidad'))
    check('sin errores', not s.errs, str(s.errs)); s.cerrar()
    # --- consecuencias de la afinidad baja
    s = Sesion(br).abrir(); cuidar(s)
    s.ev("CC.S.pet.afinidad=50;CC.S.pet.felicidad=50"); u50 = s.ev('CC.umbral()')
    s.ev("CC.S.pet.afinidad=80"); u80 = s.ev('CC.umbral()'); s.ev("CC.S.pet.afinidad=10"); u10 = s.ev('CC.umbral()')
    check('con poca afinidad el portón le tienta el doble; con mucha, menos', u10 == u50 / 2 and u80 == u50 * 1.5, [u10, u50, u80])
    s.ev("CC.S.pet.afinidad=40;CC.S.pet.felicidad=50"); f0 = s.ev('CC.S.pet.felicidad'); s.pg.wait_for_timeout(800); mimar(s)
    check('con afinidad media los mimos valen la mitad', 0 < s.ev('CC.S.pet.felicidad') - f0 <= 1.8, s.ev('CC.S.pet.felicidad') - f0)
    s.ev("CC.S.pet.afinidad=10"); s.pg.wait_for_timeout(4600)
    tx = s.ev("document.getElementById('toast').textContent")
    check('con poca afinidad avisa que está solo', 'solo' in tx or 'irse' in tx, tx)
    s.ev("CC.S.pet.felicidad=50;Math.random=()=>0"); s.pg.wait_for_timeout(3300); mimar(s)
    check('con muy poca afinidad a veces rechaza los mimos', s.ev('CC.S.pet.felicidad') <= 50.5 and 'no quiere' in s.ev("document.getElementById('toast').textContent"), [s.ev('CC.S.pet.felicidad'), s.ev("document.getElementById('toast').textContent")])
    s.ev("CC.S.pet.afinidad=90;CC.S.pet.felicidad=90"); s.pg.wait_for_timeout(2000)
    check('con mucha afinidad la carita de la pestaña es de amor', 'cara_amor' in s.ev("document.getElementById('tabCat').src"), s.ev("document.getElementById('tabCat').src"))
    s.foto('afinidad-baja'); check('sin errores', not s.errs, str(s.errs)); s.cerrar()
    # --- ausencia larga: pierde como máximo 25 y no se va por eso
    s = Sesion(br).abrir(); cuidar(s)
    s.ev("CC.AFI.ausente=50;CC.S.pet.afinidad=60;CC.S.idle=9*3600;CC.S.last-=5*3600*1000;CC.catchUp()")
    check('mientras no estás, la afinidad pierde como máximo 25', 34.5 <= s.ev('CC.S.pet.afinidad') <= 36, s.ev('CC.S.pet.afinidad'))
    s.ev("CC.S.pet.afinidad=20;CC.S.tAband=0;CC.S.idle=9*3600;CC.S.last-=30*3600*1000;CC.S.pet.hambre=100;CC.catchUp()")
    check('una ausencia larga no te hace perder al gatito por abandono', s.ev('CC.S.final') != 'abandono', s.ev('[CC.S.terminado,CC.S.final,CC.S.pet.afinidad]'))
    s.cerrar()
    # --- el final: se va de casa
    s = Sesion(br).abrir(); cuidar(s)
    s.ev("CC.S.pet.afinidad=0;CC.S.tAband=47.9;CC.S.idle=0"); s.ev('CC.age(0.2)')
    check('con afinidad 0 durante días se va de casa (final "abandono")', s.ev('CC.S.terminado') is True and s.ev('CC.S.final') == 'abandono', s.ev('[CC.S.terminado,CC.S.final]'))
    s.pg.wait_for_timeout(4500)
    check('aparece la pantalla final con su mensaje', s.ev("!document.getElementById('final').hidden") and 'no volvió' in s.ev("document.getElementById('finalMsg').textContent"), s.ev("document.getElementById('finalMsg').textContent"))
    s.foto('final-abandono')
    s.pg.click('#againBtn'); s.pg.wait_for_timeout(300); s.pg.fill('#nameIn', 'Nuevo'); s.pg.click('#introGo'); s.pg.wait_for_timeout(300)
    check('el gatito nuevo empieza con su propia afinidad (40)', s.ev('CC.S.pet.afinidad') == 40, s.ev('CC.S.pet.afinidad'))
    check('sin errores', not s.errs, str(s.errs)); s.cerrar()

@prueba
def dibujos_de_sofia_y_detalles(br):
    s = Sesion(br).abrir()
    # --- los dibujos de Sofía se pueden activar o no desde Ajustes
    s.pg.click('#setBtn'); s.pg.wait_for_timeout(300)
    check('Ajustes muestra la opción de los dibujos de Sofía', s.ev("!document.getElementById('artBox').hidden"))
    check('por defecto están activados', s.ev("document.querySelector('#artSeg [data-a=\"1\"]').getAttribute('aria-pressed')") == 'true')
    txt = s.ev("document.getElementById('artTxt').textContent")
    check('dice cuántas poses ya son de Sofía', '3 de 12' in txt, txt)
    check('activado: las poses de Sofía usan su carpeta y el resto, la provisoria', s.ev("[CC.catSrc('feliz'),CC.catSrc('triste'),CC.catSrc('hambre'),CC.catSrc('feliz',true)]") ==
          ['assets/gato_sofia/feliz.webp', 'assets/gato_sofia/triste.webp', 'assets/gato/hambre.webp', 'assets/gato_sofia/feliz_n.webp'], s.ev("[CC.catSrc('feliz'),CC.catSrc('hambre')]"))
    s.pg.click('#setsBack'); s.pg.wait_for_timeout(1500); s.foto('dibujos-sofia-si')
    s.pg.click('#setBtn'); s.pg.click('#artSeg [data-a="0"]')
    check('desactivado: todo vuelve a los dibujos provisorios', s.ev("[CC.catSrc('feliz'),CC.catSrc('triste'),CC.sofiaOn('feliz')]") == ['assets/gato/feliz.webp', 'assets/gato/triste.webp', False])
    check('el texto de Ajustes lo explica', 'provisorios' in s.ev("document.getElementById('artTxt').textContent"))
    s.pg.click('#setsBack'); s.pg.wait_for_timeout(1500); s.foto('dibujos-sofia-no')
    s.pg.reload(); s.pg.wait_for_function('window.CC&&document.readyState==="complete"'); s.pg.wait_for_timeout(600)
    check('la elección se guarda al cerrar y abrir el juego', s.ev('CC.S.arteSofia') is False and s.ev("CC.catSrc('feliz')") == 'assets/gato/feliz.webp')
    s.pg.click('#setBtn'); s.pg.click('#resetBtn'); s.pg.click('#resetYes'); s.pg.wait_for_timeout(300)
    s.pg.fill('#nameIn', 'Otro'); s.pg.click('#introGo'); s.pg.wait_for_timeout(300)
    check('empezar con otro gatito no cambia la elección', s.ev('CC.S.arteSofia') is False)
    s.pg.click('#setBtn'); s.pg.click('#artSeg [data-a="1"]'); s.pg.click('#setsBack')
    check('se puede volver a activar', s.ev("CC.sofiaOn('feliz')") is True)
    check('sin errores', not s.errs, str(s.errs)); s.cerrar()
    # --- la cuenta regresiva de los minijuegos aparece siempre en el mismo lugar
    s = Sesion(br).abrir(); s.pg.click('#aPlay'); s.pg.click('[data-g=lana]')
    centros = []
    for i in range(40):
        c = s.ev("(()=>{const m=document.getElementById('mgMsg');if(m.hidden)return null;const r=m.getBoundingClientRect(),v=document.getElementById('mgCv').getBoundingClientRect();return [r.left+r.width/2-(v.left+v.width/2),r.top+r.height/2-(v.top+v.height/2),m.textContent]})()")
        if c: centros.append(c)
        s.pg.wait_for_timeout(60)
    nums = {c[2] for c in centros}
    check('se ven los números de la cuenta regresiva', {'3', '2', '1'} <= nums, nums)
    check('todos aparecen centrados, en el mismo lugar', all(abs(c[0]) < 3 and abs(c[1]) < 3 for c in centros), [c for c in centros if abs(c[0]) >= 3 or abs(c[1]) >= 3][:3])
    s.cerrar()
    # --- la burbuja de pensamiento queda arriba del gatito, sin tapar la cara
    s = Sesion(br).abrir(); cuidar(s)
    for nombre, js in [('sueño', 'p.energia=10'), ('triste', 'p.felicidad=10'), ('enfermo', 'p.salud=10'), ('sucio', 'p.limpieza=10')]:
        for sofia in ['true', 'false']:
            s.ev("(()=>{const S=CC.S,p=S.pet;for(const k in p)p[k]=100;S.arteSofia=%s;S.mode='prueba';S.edad=.1;S.luz=true;%s})()" % (sofia, js)); s.pg.wait_for_timeout(900)
            th = s.ev('CC.thoughtPos()'); box = s.ev('CC.catBox()'); w = s.ev("document.getElementById('cv').getBoundingClientRect().width")
            check(f'burbuja de {nombre} ({"Sofía" if sofia == "true" else "provisorio"}): arriba del gatito y dentro de la pantalla',
                  th and box and th['y'] + 16 <= box['y'] + 6 and 8 <= th['y'] and 8 <= th['x'] <= w - 8, [th, box])
    s.ev("(()=>{const S=CC.S,p=S.pet;for(const k in p)p[k]=100;S.arteSofia=true;p.energia=10})()"); s.pg.wait_for_timeout(900); s.foto('burbuja-sueno')
    check('sin errores', not s.errs, str(s.errs)); s.cerrar()

@prueba
def partida_vieja(br):
    """Una partida guardada con una versión anterior (sin afinidad, sin ajustes nuevos) tiene que abrir bien."""
    s = Sesion(br).abrir(); cuidar(s)
    editar_guardado(s, "delete x.pet.afinidad;delete x.idle;delete x.tAband;delete x.arteSofia;x.last-=2*3600*1000")
    check('una partida de antes de la afinidad abre sin errores', not s.errs, str(s.errs))
    check('recibe la afinidad por defecto', s.ev('typeof CC.S.pet.afinidad') == 'number' and s.ev('CC.S.pet.afinidad') <= 40, s.ev('CC.S.pet.afinidad'))
    check('y los dibujos de Sofía activados', s.ev('CC.S.arteSofia') is True)
    check('se ve el juego (no queda en blanco)', s.ev("document.getElementById('panePet').offsetHeight") > 100 and s.ev("document.getElementById('p_afinidadB')!==null"))
    editar_guardado(s, "x.pet.energia=null;x.pet.afinidad=null;x.avatar.animo=null")
    check('un guardado con números rotos (null) se repara', s.ev('Number.isFinite(CC.S.pet.energia)&&Number.isFinite(CC.S.pet.afinidad)&&Number.isFinite(CC.S.avatar.animo)') and not s.errs, str(s.errs))
    s.pg.wait_for_timeout(1500); check('sigue sin errores un rato después', not s.errs, str(s.errs)); s.cerrar()

@prueba
def energia_y_siesta(br):
    """Cansado: se echa una siesta enseguida y la energía sube; y los efectos nuevos no rompen nada."""
    s = Sesion(br).abrir(); cuidar(s)
    s.ev("CC.S.pet.energia=10"); s.pg.wait_for_timeout(500)
    s.ev("CC.S.pet.energia=10"); e0 = 10
    s.pg.wait_for_timeout(9000); s.ev("for(const k of ['hambre','felicidad','salud','limpieza'])CC.S.pet[k]=100")
    s.pg.wait_for_timeout(4000); e1 = s.ev('CC.S.pet.energia')
    check('cansado y tranquilo: duerme la siesta y la energía sube', e1 > e0 + .2, f'{e0} -> {e1}')
    s.pg.wait_for_timeout(1500); s.foto('siesta')
    check('la barra de energía muestra que se está recuperando', s.ev("document.getElementById('p_energiaB').classList.contains('rising')"))
    s.ev("CC.S.fru+=5")
    try: s.pg.wait_for_function("document.getElementById('fruPill').classList.contains('bump')", timeout=2500); ok = True
    except Exception: ok = False
    check('el contador de frutillas rebota al ganar', ok)
    s.ev("CC.S.pet.hambre=20")
    try: s.pg.wait_for_function("document.getElementById('p_hambreB').classList.contains('dn')", timeout=2500); ok = True
    except Exception: ok = False
    check('la barra tiembla cuando baja de golpe', ok)
    s.pg.mouse.click(200, 150); s.pg.wait_for_timeout(300)
    check('tocar la escena no da errores', not s.errs, str(s.errs)); s.cerrar()

@prueba
def muerte_durante_minijuego(br):
    s = Sesion(br).abrir(); s.ev("CC.S.pet.felicidad=40")
    s.pg.click('#aPlay'); s.pg.click('[data-g=lana]'); esperar_juego(s)
    s.ev("CC.endGame('porton')")                   # se escapó por el portón en medio del juego
    s.pg.wait_for_timeout(4500)
    check('si se muere jugando, el minijuego se cierra y aparece el final',
          s.ev("document.getElementById('mg').hidden") and s.ev("!document.getElementById('final').hidden"),
          s.ev("[document.getElementById('mg').hidden,document.getElementById('final').hidden,!!CC.ending]"))
    s.cerrar()

@prueba
def ya_muerto_no_gana_premios(br):
    s = Sesion(br).abrir(); s.ev("CC.S.pet.hambre=10;CC.S.porton=true;CC.render()")
    s.ev("CC.S.last-=3600*1000")          # estuvo 1 h con el portón abierto → muere al volver
    fr = s.ev('CC.S.fru'); s.pg.click('#aFeed'); s.pg.wait_for_timeout(300)
    check('el gatito murió mientras estabas afuera', s.ev('CC.S.terminado') is True)
    check('apretar un botón justo después no te regala 🍓 ni "cuidados"', s.ev('CC.S.fru') == fr and s.ev('CC.S.cares') == 0, [fr, s.ev('CC.S.fru'), s.ev('CC.S.cares')])
    s.cerrar()

@prueba
def crecer_con_algo_abierto(br):
    s = Sesion(br).abrir(); dias(s, .9)
    s.pg.click('#shopBtn'); dias(s, .15); s.pg.wait_for_timeout(1600)
    top = s.ev("(()=>{const o=[...document.querySelectorAll('.overlay')].filter(x=>!x.hidden).map(x=>x.id);return o})()")
    check('"¡Creció!" no se esconde detrás de la tienda abierta', top == ['shop'], top)
    s.pg.click('#shopBack'); s.pg.wait_for_timeout(1600)
    check('al cerrar la tienda aparece "¡Creció!"', s.ev("!document.getElementById('grow').hidden"))
    s.cerrar()

@prueba
def reiniciar(br):
    s = Sesion(br).abrir(); s.ev("CC.S.fru=33;CC.S.own.cama=1")
    s.pg.click('#setBtn'); s.pg.click('#resetBtn'); check('pide confirmación', s.ev("!document.getElementById('resetAsk').hidden"))
    s.pg.click('#resetNo'); check('"No" cancela', s.ev("document.getElementById('resetAsk').hidden"))
    s.pg.click('#resetBtn'); s.pg.click('#resetYes'); s.pg.wait_for_timeout(300)
    check('reiniciar: pide nombre y conserva frutillas y compras', s.ev("!document.getElementById('introB').hidden") and s.ev('[CC.S.fru,!!CC.S.own.cama]') == [33, True])
    s.cerrar()

@prueba
def sonido_y_ajustes(br):
    s = Sesion(br).abrir()
    s.pg.click('#musicBtn'); a = s.ev('CC.S.music'); s.pg.click('#musicBtn'); b = s.ev('CC.S.music')
    check('el botón de música alterna', a is False and b is True)
    s.pg.click('#setBtn'); s.pg.click('#sfxSeg [data-s="0"]'); check('se puede apagar los sonidos', s.ev('CC.S.sfx') is False)
    s.pg.click('#modeSeg [data-m=prueba]'); check('cambiar a modo rápido', s.ev('CC.S.mode') == 'prueba')
    s.pg.click('#setsBack'); s.pg.click('#credBtn'); check('créditos abren', s.ev("!document.getElementById('cred').hidden"))
    s.foto('creditos'); s.pg.click('#credBack'); check('sin errores', not s.errs, str(s.errs)); s.cerrar()

TAMANOS = [('320x568 celular chico', (320, 568), True), ('360x640 Android', (360, 640), True), ('390x844 iPhone', (390, 844), True),
           ('412x915 Android grande', (412, 915), True), ('844x390 celular acostado', (844, 390), True), ('768x1024 tablet', (768, 1024), True),
           ('1280x800 compu', (1280, 800), False), ('1920x1080 compu grande', (1920, 1080), False)]
@prueba
def pantallas(br):
    for nombre, vp, movil in TAMANOS:
        s = Sesion(br, vp, movil).abrir()
        ov = s.ev('document.scrollingElement.scrollWidth-innerWidth')
        check(f'{nombre}: sin scroll horizontal', ov <= 1, ov)
        # todos los botones principales se pueden tocar (visibles al hacer scroll del panel, no tapados)
        ok = True; det = []
        for b in ['aFeed', 'aPlay', 'aBath', 'shopBtn', 'bagBtn', 'gateBtn', 'musicBtn', 'setBtn']:
            r = s.ev(f"(()=>{{const e=document.getElementById('{b}');e.scrollIntoView({{block:'nearest'}});const r=e.getBoundingClientRect();const x=r.left+r.width/2,y=r.top+r.height/2;const t=document.elementFromPoint(x,y);return [r.width>0&&r.left>=-1&&r.right<=innerWidth+1&&r.top>=-1&&r.bottom<=innerHeight+1,!!t&&(t===e||e.contains(t))]}})()")
            if not all(r): ok = False; det.append((b, r))
        check(f'{nombre}: botones dentro de la pantalla y sin nada encima', ok, det)
        # el botón del portón no tapa al gatito
        sol = s.ev("""(()=>{const g=CC.geo(),c=document.getElementById('cv').getBoundingClientRect(),b=document.getElementById('gateBtn').getBoundingClientRect();
          const gx=c.left+g.cx,gy=c.top+g.cy+g.cs*.1,gw=g.cs,gh=g.cs*.85;
          return Math.max(0,Math.min(gx+gw,b.right)-Math.max(gx,b.left))*Math.max(0,Math.min(gy+gh,b.bottom)-Math.max(gy,b.top))})()""")
        check(f'{nombre}: el botón del portón no tapa al gatito', sol < 60, round(sol))
        s.foto('pantalla-' + nombre.split()[0]); s.cerrar()

@prueba
def sin_conexion(br):
    s = Sesion(br, reloj=False).abrir(empezar=False)
    s.pg.wait_for_function('navigator.serviceWorker&&navigator.serviceWorker.controller||navigator.serviceWorker.ready.then(()=>true)', timeout=8000)
    s.pg.wait_for_timeout(2500)
    ks = s.ev("caches.keys()"); check('se crea la copia sin conexión', any(k.startswith('cuidamichis-') for k in ks), ks)
    # todos los archivos que el juego pide están en la copia
    falt = s.ev("""(async()=>{const k=(await caches.keys()).find(k=>k.startsWith('cuidamichis-'));const c=await caches.open(k);const ks=(await c.keys()).map(r=>new URL(r.url).pathname);
      const need=performance.getEntriesByType('resource').map(r=>new URL(r.name)).filter(u=>u.origin===location.origin&&!u.pathname.endsWith('sw.js')).map(u=>u.pathname);
      return need.filter(p=>!ks.includes(p))})()""")
    check('lo que carga el juego está en la copia sin conexión', not falt, falt)
    s.pg.click('.ch[data-id=sofi]'); s.pg.click('#introNext'); s.pg.fill('#nameIn', 'Offline'); s.pg.click('#introGo')
    s.ctx.set_offline(True); s.pg.reload(); s.pg.wait_for_function('window.CC', timeout=8000); s.pg.wait_for_timeout(800)
    n = s.ev('CC.S.name'); check('sin internet el juego abre y conserva la partida', n == 'Offline', n)
    img = s.ev("[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)")
    check('sin internet se ven todos los dibujos', not img, img)
    s.cerrar()

@prueba
def manifest_y_pwa(br):
    s = Sesion(br, reloj=False).abrir(empezar=False)
    m = s.ev("fetch(document.querySelector('link[rel=manifest]').href).then(r=>r.json())")
    check('manifest: tiene id y scope propios (para no pisar a los otros juegos)', m.get('id') == '/cuidamichis/' and m.get('scope') == './', m)
    ic = []
    for i in m['icons']:
        st = s.ev("fetch('%s').then(r=>r.status)" % i['src']); ic.append(st)
    check('manifest: los íconos existen', all(x == 200 for x in ic), ic)
    s.cerrar()

# =====================================================================
def main():
    t0 = time.time()
    with sync_playwright() as p:
        br = p.chromium.launch()
        for f in PRUEBAS:
            if ARGS.k and ARGS.k not in f.__name__: continue
            print(f'\n▶ {f.__name__}')
            try: f(br)
            except Exception as e:
                check(f'{f.__name__}: se ejecutó completa', False, f'{type(e).__name__}: {str(e)[:300]}')
        br.close()
    mal = [r for r in RES if not r[1]]
    print(f'\n{len(RES) - len(mal)} bien · {len(mal)} mal · {time.time() - t0:.0f} s')
    for n, _, d in mal: print('  ❌', n, '→', d)
    SRV.shutdown(); sys.exit(1 if mal else 0)
if __name__ == '__main__': main()
