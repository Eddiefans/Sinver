from rich.console import Console
from rich.table import Table
from rich import box
from rich.theme import Theme
import rich

from Packages.Scripts import web_scraping

estilos = Theme({"input": "italic bold #AED6F1", "rojo": "#E74C3C", "verde": "#2ECC71", "neutro": "#5D6D7E", "tabla": "#CCD1D1", "tablaHeader": "bold #CCD1D1"})
nombreC = "#AEB6BF"

c = Console(theme=estilos)


menu = Table(title="", show_footer=True, show_header=False, footer_style="tabla", style="bold white", box=box.SIMPLE)
menu.add_column("", justify="center", style="bold white")
menu.add_column("", justify="left", footer="Elija una opción", style="bold white")
menu.add_row("1", "Iniciar sesión")
menu.add_row("2", "Crear cuenta")
menu.add_row("3", "Salir")
c.print(menu)
c.input("[tabla]       > ")


unidad = "Usd"
precioActual = 18.2444444
nombre = "Indonesia Energy Corporation Limited"
simbolo = "INDO"
cambioActual = -0.76
cambiopActual = -4
precioMinimo = 17.62
precioMaximo = 21.21
precioMinimo52 = 2.61
precioMaximo52 = 86.9922
volumen = 1300037
volumen90dias = 6308221.74444445
mercadoCap = 139485180

estilos = Theme({"input": "italic bold #AED6F1", "rojo": "#E74C3C", "verde": "#2ECC71", "neutro": "#5D6D7E", "tabla": "#CCD1D1", "tablaHeader": "bold #CCD1D1"})
nombreC = "#AEB6BF"

c = Console(theme=estilos)

nombreTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE_HEAVY, style=nombreC)
nombreTabla.add_column(nombre, justify="left", style="{}".format("tabla"))
nombreTabla.add_column("   ")
nombreTabla.add_column("[#CCD1D1]{:,.2f}[/] [#CCD1D1]{}[/]".format(precioActual, unidad.upper()), justify="center", style="{}".format("#CCD1D1"))
s = ""
if cambioActual < 0:
    signo = "rojo"
elif cambioActual > 0:
    signo = "verde"
    s = "+"
else:
    signo = "neutro"
nombreTabla.add_column("  [{}]{}{:,.2f}  ({}{:,.2f}%)[/]".format(signo, s, cambioActual, s, cambiopActual), justify="center", style="{}".format("#CCD1D1"))
nombreTabla.add_row(simbolo, "", )
c.print(nombreTabla)

minTabla = Table(title="", header_style="{}".format(nombreC), box=box.SIMPLE, style=nombreC)
minTabla.add_column(" Precio", style="tabla", justify="left")
minTabla.add_column("Minimo", style="tabla", justify="right")
minTabla.add_column("Maximo", style="tabla", justify="right")
minTabla.add_row(" Día", "[bold white]{:,.2f}[/]".format(precioMinimo), "[bold white]{:,.2f}[/]".format(precioMaximo))
minTabla.add_row(" 52 Semanas ", "[bold white]{:,.2f}[/]".format(precioMinimo52), "[bold white]{:,.2f}[/]".format(precioMaximo52))
c.print(minTabla)


estTabla = Table(title="", header_style="{}".format(nombreC), box=box.SIMPLE, style=nombreC)
estTabla.add_column("Estadisticas", style="tabla", justify="left")
estTabla.add_column("", style="tabla", justify="right")
estTabla.add_row("Volumen", "[bold white]{:,.2f}[/]".format(volumen))
estTabla.add_row("Volumen 90 días", "[bold white]{:,.2f}[/]".format(volumen90dias))
estTabla.add_row("Cap. Mercado", "[bold white]{:,.2f}[/]".format(mercadoCap))
c.print(estTabla)

c.print("  Las 25 acciones con mayor capitalización de mercado actualmente: ", style="bold white", highlight=False)
acciones = web_scraping.scrap_acciones_cap()
cap_tabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE, style=nombreC)
cap_tabla.add_column("Nombre", style="tabla", justify="left")
cap_tabla.add_column("Precio", style="tabla", justify="right")
cap_tabla.add_column("Cambio", style="tabla", justify="right")
cap_tabla.add_column("Cap. Mercado", style="tabla", justify="right")
cap_tabla.add_column("Volumen", style="tabla", justify="right")
for item in acciones:
    s = ""
    if item["cambioActual"] < 0:
        signo = "rojo"
    elif item["cambioActual"] > 0:
        signo = "verde"
        s = "+"
    else:
        signo = "neutro"
    cambioActual = s + "{:,.2f}".format(item["cambioActual"])
    cambiopActual = "({}{:,.2f}%)".format(s, item["cambiopActual"])
    if 1000000 <= item["mercadoCap"] < 1000000000000:
        mercado = item["mercadoCap"]/1000000
        cap_uni = "M"
    elif item["mercadoCap"] >= 1000000000000:
        mercado = item["mercadoCap"] / 1000000000000
        cap_uni = "B"
    else:
        mercado = item["mercadoCap"]
        cap_uni = " "
    if 1000000 <= item["volumen"] < 1000000000000:
        volumen = item["volumen"] / 1000000
        vol_uni = "M"
    elif item["mercadoCap"] >= 1000000000000:
        volumen = item["volumen"] / 1000000000000
        vol_uni = "B"
    else:
        volumen = item["volumen"]
        vol_uni = " "
    cap_tabla.add_row("[bold #CCD1D1]{}[/]".format(item['simbolo']), "[bold white]{:,.2f} {}[/]".format(item['precioActual'], item['unidad']), "[{}]{:>9}{:>10}[/]".format(signo, cambioActual, cambiopActual), "[white]{:,.2f} {}[/]".format(mercado, cap_uni), "[white]{:,.2f} {}[/]".format(volumen, vol_uni))
c.print(cap_tabla)

c.print("  Las 25 acciones más comerciadas actualmente (Mayor volumen):", style="bold white", highlight=False)
acciones = web_scraping.scrap_acciones_activas()
vol_tabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE, style=nombreC)
vol_tabla.add_column("Nombre", style="tabla", justify="left")
vol_tabla.add_column("Precio", style="tabla", justify="right")
vol_tabla.add_column("Cambio", style="tabla", justify="right")
vol_tabla.add_column("Cap. Mercado", style="tabla", justify="right")
vol_tabla.add_column("Volumen", style="tabla", justify="right")
for item in acciones:
    s = ""
    if item["cambioActual"] < 0:
        signo = "rojo"
    elif item["cambioActual"] > 0:
        signo = "verde"
        s = "+"
    else:
        signo = "neutro"
    cambioActual = s + "{:,.2f}".format(item["cambioActual"])
    cambiopActual = "({}{:,.2f}%)".format(s, item["cambiopActual"])
    if 1000000 <= item["mercadoCap"] < 1000000000000:
        mercado = item["mercadoCap"]/1000000
        cap_uni = "M"
    elif item["mercadoCap"] >= 1000000000000:
        mercado = item["mercadoCap"] / 1000000000000
        cap_uni = "B"
    else:
        mercado = item["mercadoCap"]
        cap_uni = " "
    if 1000000 <= item["volumen"] < 1000000000000:
        volumen = item["volumen"] / 1000000
        vol_uni = "M"
    elif item["mercadoCap"] >= 1000000000000:
        volumen = item["volumen"] / 1000000000000
        vol_uni = "B"
    else:
        volumen = item["volumen"]
        vol_uni = " "
    vol_tabla.add_row("[bold #CCD1D1]{}[/]".format(item['simbolo']), "[bold white]{:,.2f} {}[/]".format(item['precioActual'], item['unidad']), "[{}]{:>9}{:>10}[/]".format(signo, cambioActual, cambiopActual), "[white]{:,.2f} {}[/]".format(mercado, cap_uni), "[white]{:,.2f} {}[/]".format(volumen, vol_uni))
c.print(vol_tabla)

"""
resumenTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE_HEAVY, style=nombreC)
resumenTabla.add_column("", style="{}".format("tabla"))
resumenTabla.add_column(usuario.nombreUsuario, justify="right", style="{}".format("tabla"))
resumenTabla.add_row("[tabla]Valor de cuenta[/]", "[#CCD1D1]{:,.2f}[/] [#CCD1D1]USD[/]".format(usuario.valorCuentaActual))
s = ""
if usuario.cambioTotal < 0:
    signo = "rojo"
elif usuario.cambioTotal > 0:
    signo = "verde"
    s = "+"
else:
    signo = "neutro"
resumenTabla.add_row("[tabla]Cambio total[/]", "[{}]{}{:,.2f}  ({}{:,.2f}%)[/]".format(signo, s, usuario.cambioTotal, s, (usuario.cambioTotal/100000)*100)))
c.print(resumenTabla)
"""

"""
c.print("Acciones compradas", style="bold white", highlight=False)
resumenAccionTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE_HEAVY, style=nombreC)
resumenAccionTabla.add_column("", justify="left", style="{}".format("tabla"))
resumenAccionTabla.add_column("Cambio del día", justify="right", style="{}".format("tabla"))
resumenAccionTabla.add_column("Valor inicial", justify="right", style="{}".format("tabla"))
resumenAccionTabla.add_column("Valor actual", justify="right", style="{}".format("tabla"))
resumenAccionTabla.add_column("Cambio total", justify="right", style="{}".format("tabla"))
s = ""
if usuario.utilidadCompra.cambioDia < 0:
    signo = "#E74C3C"
elif usuario.utilidadCompra.cambioDia > 0:
    signo = "#2ECC71"
    s = "+"
else:
    signo = "neutro"
st = ""
if usuario.utilidadCompra.cambioTotal < 0:
    signot = "#E74C3C"
elif usuario.utilidadCompra.cambiopTotal > 0:
    signot = "#2ECC71"
    st = "+"
else:
    signot = "neutro"
resumenAccionTabla.add_row("[tabla]Resumen de acciones[/]", "[bold {}]{}{:,.2f} ({}{:,.2f}%)[/]".format(signo, s, usuario.utilidadCompra.cambioDia, s, usuario.utilidadCompra.cambiopDia), "[bold white]{:,.2f} USD[/]".format(usuario.utilidadCompra.valorInicial), "[bold white]{:,.2f} USD[/]".format(usuario.utilidadCompra.valorActual, "[bold {}]{}{:,.2f} ({}{:,.2f}%)[/]".format(signot, st, usuario.utilidadCompra.cambioTotal, st, usuario.utilidadCompra.cambiopTotal)))
c.print(resumenAccionTabla)














accionesTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE, style=nombreC)
accionesTabla.add_column("Simbolo", style="tabla", justify="left")
accionesTabla.add_column("Cantidad", style="tabla", justify="right")
accionesTabla.add_column("Precio inicial", style="tabla", justify="right")
accionesTabla.add_column("Precio actual", style="tabla", justify="right")
accionesTabla.add_column("Valor inicial", style="tabla", justify="right")
accionesTabla.add_column("Valor actual", style="tabla", justify="right")
accionesTabla.add_column("Cambio del día", style="tabla", justify="right")
accionesTabla.add_column("Cambio total", style="tabla", justify="right")

if len(usuario.accionesCompra) == 0:
    c.print("", style="rojo", highlight=False)
else:
    for item in usuario.accionesCompra:
        s = ""
        if item.cambioDia < 0:
            signo = "rojo"
        elif item.cambioDia > 0:
            signo = "verde"
            s = "+"
        else:
            signo = "neutro"
        st = ""
        if item.cambioTotal < 0:
            signot = "rojo"
        elif item.cambioTotal > 0:
            signot = "verde"
            st = "+"
        else:
            signot = "neutro"
        cambioDia = s + "{:,.2f}".format(item.cambioDia)
        cambiopDia = "({}{:,.2f}%)".format(s, item.cambiopDia)
        cambioTotal = st + "{:,.2f}".format(item.cambioTotal)
        cambiopTotal = "({}{:,.2f}%)".format(st, item.cambiopTotal)
        accionesTabla.add_row("[bold #CCD1D1]{}[/]".format(item.simbolo),
                              "[bold #CCD1D1]{}[/]".format(item.cantidad),
                              "[bold #CCD1D1]{}[/]".format(item.precioInicial),
                              "[bold white]{:,.2f} USD[/]".format(item.precioActual),
                              "[bold #CCD1D1]{}[/]".format(item.valorInicial),
                              "[bold white]{:,.2f} USD[/]".format(item.valorActual),
                              "[{}]{:>10}{:>10}[/]".format(signo, cambioDia, cambiopDia),
                              "[{}]{:>10}{:>10}[/]".format(signot, cambioTotal, cambiopTotal))
c.print(accionesTabla)







c.print("Acciones compradas", style="bold white", highlight=False, justify="right", width=75)
s = ""
if usuario.utilidadCompra.cambioDia < 0:
    signo = "#E74C3C"
elif usuario.utilidadCompra.cambioDia > 0:
    signo = "#2ECC71"
    s = "+"
else:
    signo = "neutro"
st = ""
if usuario.utilidadCompra.cambioTotal < 0:
    signot = "#E74C3C"
elif usuario.utilidadCompra.cambiopTotal > 0:
    signot = "#2ECC71"
    st = "+"
else:
    signot = "neutro"
cambioDiaUtilidad = s + "{:,.2f}".format(usuario.utilidadCompra.cambioDia)
cambiopDiaUtilidad = "({}{:,.2f}%)".format(s, usuario.utilidadCompra.cambiopDia)
cambioTotalUtilidad = st + "{:,.2f}".format(usuario.utilidadCompra.cambioTotal)
cambiopTotalUtilidad = "({}{:,.2f}%)".format(st, usuario.utilidadCompra.cambiopTotal)
accionesTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE, style=nombreC, show_footer=True)
accionesTabla.add_column("Simbolo", style="tabla", justify="left")
accionesTabla.add_column("Cantidad", style="tabla", justify="right")
accionesTabla.add_column("Precio inicial", style="tabla", justify="right")
accionesTabla.add_column("Precio actual", style="tabla", justify="right")
accionesTabla.add_column("Valor inicial", style="tabla", justify="right", footer="[bold #CCD1D1]{}[/]".format(usuario.utilidadCompra.valorInicial))
accionesTabla.add_column("Valor actual", style="tabla", justify="right", footer="[bold white]{:,.2f} USD[/]".format(usuario.utilidadCompra.valorActual))
accionesTabla.add_column("Cambio del día", style="tabla", justify="right", footer="[{}]{:>10}{:>10}[/]".format(signo, cambioDiaUtilidad, cambiopDiaUtilidad))
accionesTabla.add_column("Cambio total", style="tabla", justify="right", footer="[{}]{:>10}{:>10}[/]".format(signot, cambioTotalUtilidad, cambiopTotalUtilidad))

if len(usuario.accionesCompra) == 0:
    c.print("", style="rojo", highlight=False)
    accionesTabla.show_footer = False
else:
    for item in usuario.accionesCompra:
        s = ""
        if item.cambioDia < 0:
            signo = "rojo"
        elif item.cambioDia > 0:
            signo = "verde"
            s = "+"
        else:
            signo = "neutro"
        st = ""
        if item.cambioTotal < 0:
            signot = "rojo"
        elif item.cambioTotal > 0:
            signot = "verde"
            st = "+"
        else:
            signot = "neutro"
        cambioDia = s + "{:,.2f}".format(item.cambioDia)
        cambiopDia = "({}{:,.2f}%)".format(s, item.cambiopDia)
        cambioTotal = st + "{:,.2f}".format(item.cambioTotal)
        cambiopTotal = "({}{:,.2f}%)".format(st, item.cambiopTotal)
        accionesTabla.add_row("[bold #CCD1D1]{}[/]".format(item.simbolo),
                              "[bold #CCD1D1]{}[/]".format(item.cantidad),
                              "[bold #CCD1D1]{}[/]".format(item.precioInicial),
                              "[bold white]{:,.2f} USD[/]".format(item.precioActual),
                              "[bold #CCD1D1]{}[/]".format(item.valorInicial),
                              "[bold white]{:,.2f} USD[/]".format(item.valorActual),
                              "[{}]{:>10}{:>10}[/]".format(signo, cambioDia, cambiopDia),
                              "[{}]{:>10}{:>10}[/]".format(signot, cambioTotal, cambiopTotal))
c.print(accionesTabla)
"""