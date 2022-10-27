import math, datetime

import rich.box
from rich.console import Console
from rich.table import Table
from rich import box
from rich.theme import Theme

from Packages.Classes.operacion import Operacion
from Packages.Scripts import web_scraping, usuario_script, simulador_script
from Packages.Classes.accion import Accion

estilos = Theme({"input": "italic bold #AED6F1", "rojo": "#E74C3C", "verde": "#2ECC71", "rojob": "bold #E74C3C", "verdeb": "bold #2ECC71", "neutro": "#5D6D7E","tabla": "#CCD1D1", "tablaHeader": "bold #CCD1D1"})
nombreC = "#AEB6BF"
esp = "       "

c = Console(theme=estilos)

def rInput():
    try:
        entrada = int(c.input("[tabla]{}> ".format(esp)))
        return entrada
    except ValueError:
        return -1

def buscar_accion(acciones):
    c.print()
    c.print("  Buscar acción", style="bold #A3E4D7")
    c.print()
    long = str(len("  Ingresa el simbolo de la accion") + 2)
    accion_buscar = str(c.input("[bold white]{:<{}}>  ".format("  Ingresa el simbolo de la accion", long))).upper()
    c.clear()

    encontrado = False
    for item in acciones:
        if item['simbolo'] == accion_buscar:
            encontrado = True
            s = ""
            if item['cambioActual'] < 0:
                signo = "rojo"
            elif item['cambioActual'] > 0:
                signo = "verde"
                s = "+"
            else:
                signo = "neutro"
            definir_mercado(True)
            nombreTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE_HEAVY, style=nombreC)
            nombreTabla.add_column(item['nombre'], justify="left", style="{}".format("tabla"))
            nombreTabla.add_column("   ")
            nombreTabla.add_column("[#CCD1D1]{:,.2f}[/] [#CCD1D1]{}[/]".format(item['precioActual'], item['unidad'].upper()),justify="center", style="{}".format("#CCD1D1"))
            nombreTabla.add_column("  [{}]{}{:,.2f}  ({}{:,.2f}%)[/]".format(signo, s, item['cambioActual'], s, item['cambiopActual']),justify="center", style="{}".format("#CCD1D1"))
            nombreTabla.add_row(item['simbolo'], "", )
            c.print(nombreTabla)

            minTabla = Table(title="", header_style="{}".format(nombreC), box=box.SIMPLE, style=nombreC)
            minTabla.add_column("Precio", style="tabla", justify="left")
            minTabla.add_column("Minimo", style="tabla", justify="right")
            minTabla.add_column("Maximo", style="tabla", justify="right")
            minTabla.add_row("Día", "[bold white]{:,.2f}[/]".format(item['precioMinimo']),"[bold white]{:,.2f}[/]".format(item['precioMaximo']))
            minTabla.add_row("52 Semanas ", "[bold white]{:,.2f}[/]".format(item['precioMinimo52']),"[bold white]{:,.2f}[/]".format(item['precioMaximo52']))
            c.print(minTabla)

            estTabla = Table(title="", header_style="{}".format(nombreC), box=box.SIMPLE, style=nombreC)
            estTabla.add_column("Estadisticas", style="tabla", justify="left")
            estTabla.add_column("", style="tabla", justify="right")
            estTabla.add_row("Volumen", "[bold white]{:,.2f}[/]".format(item['volumen']))
            estTabla.add_row("Volumen 90 días", "[bold white]{:,.2f}[/]".format(item['volumen90dias']))
            estTabla.add_row("Cap. Mercado", "[bold white]{:,.2f}[/]".format(item['mercadoCap']))
            c.print(estTabla)
            c.print()
            break
    if not encontrado:
        c.print()
        c.print("      Acción no encontrada", style="rojob")


def resumen_accion(accion, valor, acciones):
    for item in acciones:
        if item[valor] == accion:
            accionOp = item
            break
    s = ""
    if item['cambioActual'] < 0:
        signo = "rojo"
    elif item['cambioActual'] > 0:
        signo = "verde"
        s = "+"
    else:
        signo = "neutro"
    nombreTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE_HEAVY, style=nombreC)
    nombreTabla.add_column(item['nombre'], justify="left", style="{}".format("tabla"))
    nombreTabla.add_column("   ")
    nombreTabla.add_column("[#CCD1D1]{:,.2f}[/] [#CCD1D1]{}[/]".format(item['precioActual'], item['unidad'].upper()),
                           justify="center", style="{}".format("#CCD1D1"))
    nombreTabla.add_column(
        "  [{}]{}{:,.2f}  ({}{:,.2f}%)[/]".format(signo, s, item['cambioActual'], s, item['cambiopActual']),
        justify="center", style="{}".format("#CCD1D1"))
    nombreTabla.add_row(item['simbolo'], "", )
    c.print(nombreTabla)


def validar_accion(accion, acciones):
    encontrado = 'o'
    for item in acciones:
        if item['nombre'].upper() == accion:
            encontrado = 'nombre'
        if item['simbolo'] == accion:
            encontrado = 'simbolo'
    return encontrado


def mostrar_acciones_cap():
    c.print()
    c.print("  Las 15 acciones con mayor capitalización de mercado actualmente: ", style="bold white", highlight=False)
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
            mercado = item["mercadoCap"] / 1000000
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
        cap_tabla.add_row("[bold #CCD1D1]{}[/]".format(item['simbolo']),
                          "[bold white]{:,.2f} {}[/]".format(item['precioActual'], item['unidad']),
                          "[{}]{:>9}{:>10}[/]".format(signo, cambioActual, cambiopActual),
                          "[white]{:,.2f} {}[/]".format(mercado, cap_uni),
                          "[white]{:,.2f} {}[/]".format(volumen, vol_uni))
    c.print(cap_tabla)
    c.print()


def mostrar_acciones_vol():
    c.print()
    c.print("  Las 15 acciones más comerciadas actualmente (Mayor volumen):", style="bold white", highlight=False)
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
            mercado = item["mercadoCap"] / 1000000
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
        vol_tabla.add_row("[bold #CCD1D1]{}[/]".format(item['simbolo']),
                          "[bold white]{:,.2f} {}[/]".format(item['precioActual'], item['unidad']),
                          "[{}]{:>9}{:>10}[/]".format(signo, cambioActual, cambiopActual),
                          "[white]{:,.2f} {}[/]".format(mercado, cap_uni),
                          "[white]{:,.2f} {}[/]".format(volumen, vol_uni))
    c.print(vol_tabla)
    c.print()


def actualizar_portafolio(usuario, acciones, usuarios):
    valorActualCompra = 0
    valorActualCorto = 0
    valorInicialCompra = 0
    valorInicialCorto = 0
    cambioDiaCompra = 0
    cambioDiaCorto = 0
    cambioTotalCompra = 0
    cambioTotalCorto = 0

    # Actualizar acciones que se tienen compradas
    for item in usuario.accionesCompra:
        abierto, tiempo = simulador_script.definir_mercado(False)
        accionInfo = {}
        for item2 in acciones:
            if item2['simbolo'] == item.simbolo:
                accionInfo = item2
                break
        item.precioActual = accionInfo["precioActual"]
        item.valorActual = item.precioActual * item.cantidad

        if datetime.datetime.fromisoformat(item.fecha).date() == datetime.datetime.now().date():
            dia = False
        elif (datetime.datetime.now().date() - datetime.datetime.fromisoformat(item.fecha).date()).days == 1:
            if datetime.datetime.now().isoweekday() == 6:
                dia = False
            elif abierto:
                dia = True
            elif datetime.datetime.now().time() > datetime.datetime(2022, 1, 1, 7, 30, 0, 0).time():
                dia = True
            else:
                dia = False
        elif (datetime.datetime.now().date() - datetime.datetime.fromisoformat(item.fecha).date()).days == 2 and datetime.datetime.now().isoweekday() == 7:
            dia = False
        elif (datetime.datetime.now().date() - datetime.datetime.fromisoformat(item.fecha).date()).days == 3 and datetime.datetime.now().isoweekday() == 1:
            if abierto:
                dia = True
            elif datetime.datetime.now().time() > datetime.datetime(2022, 1, 1, 7, 30, 0, 0).time():
                dia = True
            else:
                dia = False
        else:
            dia = True

        if not dia:
            item.cambioDia = (item.precioActual - item.precioInicial)*item.cantidad
            item.cambiopDia = ((item.precioActual - item.precioInicial)/item.precioInicial)*100
        else:
            item.cambioDia = accionInfo["cambioActual"]*item.cantidad
            item.cambiopDia = accionInfo["cambiopActual"]
        item.cambioTotal = (item.precioActual - item.precioInicial)*item.cantidad
        item.cambiopTotal = ((item.precioActual - item.precioInicial)/item.precioInicial)*100
        valorInicialCompra += item.valorInicial
        valorActualCompra += item.valorActual
        cambioDiaCompra += item.cambioDia
        cambioTotalCompra += item.cambioTotal

    # Actualizar acciones en corto
    for item in usuario.accionesCorto:
        abierto, tiempo = simulador_script.definir_mercado(False)
        accionInfo = {}
        for item2 in acciones:
            if item2['simbolo'] == item.simbolo:
                accionInfo = item2
                break
        item.precioActual = accionInfo["precioActual"]
        item.valorActual = item.precioActual * item.cantidad
        if datetime.datetime.fromisoformat(item.fecha).date() == datetime.datetime.now().date():
            dia = False
        elif (datetime.datetime.now().date() - datetime.datetime.fromisoformat(item.fecha).date()).days == 1:
            if datetime.datetime.now().isoweekday() == 6:
                dia = False
            elif abierto:
                dia = True
            elif datetime.datetime.now().time() > datetime.datetime(2022, 1, 1, 7, 30, 0, 0).time():
                dia = True
            else:
                dia = False
        elif (datetime.datetime.now().date() - datetime.datetime.fromisoformat(
                item.fecha).date()).days == 2 and datetime.datetime.now().isoweekday() == 7:
            dia = False
        elif (datetime.datetime.now().date() - datetime.datetime.fromisoformat(
                item.fecha).date()).days == 3 and datetime.datetime.now().isoweekday() == 1:
            if abierto:
                dia = True
            elif datetime.datetime.now().time() > datetime.datetime(2022, 1, 1, 7, 30, 0, 0).time():
                dia = True
            else:
                dia = False
        else:
            dia = True

        if not dia:
            item.cambioDia = -((item.precioActual - item.precioInicial) * item.cantidad)
            item.cambiopDia = -(((item.precioActual - item.precioInicial) / item.precioInicial) * 100)
        else:
            item.cambioDia = -(accionInfo["cambioActual"] * item.cantidad)
            item.cambiopDia = -(accionInfo["cambiopActual"])

        item.cambioTotal = -((item.precioActual - item.precioInicial)*item.cantidad)
        item.cambiopTotal = -(((item.precioActual - item.precioInicial)/item.precioInicial)*100)
        valorInicialCorto += item.valorInicial
        valorActualCorto += item.valorActual
        cambioDiaCorto += item.cambioDia
        cambioTotalCorto += item.cambioTotal

    usuario.valorCuentaActual = usuario.valorCuentaActual - usuario.utilidadCompra.cambioTotal - usuario.utilidadCorto.cambioTotal

    # Actualizar utilidad total de acciones compradas
    usuario.utilidadCompra.valorInicial = valorInicialCompra
    usuario.utilidadCompra.valorActual = valorActualCompra
    usuario.utilidadCompra.cambioDia = cambioDiaCompra
    usuario.utilidadCompra.cambioTotal = cambioTotalCompra
    if usuario.utilidadCompra.valorInicial == 0:
        usuario.utilidadCompra.cambiopDia = 0
        usuario.utilidadCompra.cambiopTotal = 0
    else:
        usuario.utilidadCompra.cambiopDia = (usuario.utilidadCompra.cambioDia / (usuario.utilidadCompra.valorActual - usuario.utilidadCompra.cambioDia)) * 100
        usuario.utilidadCompra.cambiopTotal = (usuario.utilidadCompra.cambioTotal / usuario.utilidadCompra.valorInicial) * 100

    # Actualizar utilidad total de acciones en corto
    usuario.utilidadCorto.valorInicial = valorInicialCorto
    usuario.utilidadCorto.valorActual = valorActualCorto
    usuario.utilidadCorto.cambioDia = cambioDiaCorto
    usuario.utilidadCorto.cambioTotal = cambioTotalCorto
    if usuario.utilidadCorto.valorInicial == 0:
        usuario.utilidadCorto.cambiopDia = 0
        usuario.utilidadCorto.cambiopTotal = 0
    else:
        usuario.utilidadCorto.cambiopDia = (usuario.utilidadCorto.cambioDia / (usuario.utilidadCorto.valorActual - usuario.utilidadCorto.cambioDia)) * 100
        usuario.utilidadCorto.cambiopTotal = (usuario.utilidadCorto.cambioTotal / usuario.utilidadCorto.valorInicial) * 100

    # Actualizar datos generales de cuenta
    usuario.valorCuentaActual = usuario.valorCuentaActual + usuario.utilidadCompra.cambioTotal + usuario.utilidadCorto.cambioTotal
    usuario.cambioTotal = usuario.valorCuentaActual - 100000
    usuario.poderAdquisitivo = usuario.valorCuentaActual - usuario.utilidadCompra.valorActual - usuario.utilidadCorto.valorActual
    usuarios = usuario_script.actualizar_usuario(usuario, usuarios)
    return usuario, usuarios

def mostrar_resumen(usuario):
    resumenTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE_HEAVY, style=nombreC, show_footer=True)
    resumenTabla.add_column("[bold white]{}[/]".format(usuario.nombreUsuario), justify="left", style="{}".format("tabla"), footer="[tabla]Poder adquisitivo[/]")
    resumenTabla.add_column("", justify="right", style="{}".format("tabla"), footer="[bold white]{:,.2f} USD[/]".format(usuario.poderAdquisitivo))
    resumenTabla.add_row("[tabla]Valor de cuenta[/]",
                         " [bold white]{:,.2f}[/] [bold white]USD[/]".format(usuario.valorCuentaActual))
    s = ""                                                                                                                                                                  
    if usuario.cambioTotal < 0:                                                                                                                                             
        signo = "#E74C3C"                                                                                                                                                   
    elif usuario.cambioTotal > 0:                                                                                                                                           
        signo = "#2ECC71"                                                                                                                                                   
        s = "+"                                                                                                                                                             
    else:                                                                                                                                                                   
        signo = "#5D6D7E"
    resumenTabla.add_row("[tabla]Cambio total[/]", "[bold {}]{}{:,.2f} ({}{:,.2f}%)[/]".format(signo, s, usuario.cambioTotal, s, ((usuario.cambioTotal / 100000) * 100)))   
                                                                                                                                                                            
    c.print(resumenTabla)
    c.print()


def mostrar_compra(usuario):
    s = ""
    if usuario.utilidadCompra.cambioDia < 0:
        signo = "#E74C3C"
    elif usuario.utilidadCompra.cambioDia > 0:
        signo = "#2ECC71"
        s = "+"
    else:
        signo = "#5D6D7E"
    st = ""
    if usuario.utilidadCompra.cambioTotal < 0:
        signot = "#E74C3C"
    elif usuario.utilidadCompra.cambiopTotal > 0:
        signot = "#2ECC71"
        st = "+"
    else:
        signot = "#5D6D7E"
    c.print("Acciones compradas", style="bold white", highlight=False, justify="right", width=70)
    cambioDiaUtilidad = s + "{:,.2f}".format(usuario.utilidadCompra.cambioDia)
    cambiopDiaUtilidad = "({}{:,.2f}%)".format(s, usuario.utilidadCompra.cambiopDia)
    cambioTotalUtilidad = st + "{:,.2f}".format(usuario.utilidadCompra.cambioTotal)
    cambiopTotalUtilidad = "({}{:,.2f}%)".format(st, usuario.utilidadCompra.cambiopTotal)
    accionesTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE, style=nombreC,
                          show_footer=True)
    accionesTabla.add_column("Simbolo", style="tabla", justify="left")
    accionesTabla.add_column("Cantidad", style="tabla", justify="right")
    accionesTabla.add_column("Precio inicial", style="tabla", justify="right")
    accionesTabla.add_column("Precio actual", style="tabla", justify="right")
    accionesTabla.add_column("Valor inicial", style="tabla", justify="right",
                             footer="[bold #CCD1D1]{:,.2f} USD[/]".format(usuario.utilidadCompra.valorInicial))
    accionesTabla.add_column("Valor actual", style="tabla", justify="right",
                             footer="[bold white]{:,.2f} USD[/]".format(usuario.utilidadCompra.valorActual))
    accionesTabla.add_column("Cambio del día", style="tabla", justify="right",
                             footer="[{}]{:>10}{:>10}[/]".format(signo, cambioDiaUtilidad, cambiopDiaUtilidad))
    accionesTabla.add_column("Cambio total", style="tabla", justify="right",
                             footer="[{}]{:>10}{:>10}[/]".format(signot, cambioTotalUtilidad, cambiopTotalUtilidad))

    if len(usuario.accionesCompra) == 0:
        c.print("  No tienes ninguna acción comprada", style="rojo", highlight=False)
        c.print()
        c.print()
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
                                  "[bold #CCD1D1]{:,}[/]".format(item.cantidad),
                                  "[bold #CCD1D1]{:,.2f} USD[/]".format(item.precioInicial),
                                  "[bold white]{:,.2f} USD[/]".format(item.precioActual),
                                  "[bold #CCD1D1]{:,.2f} USD[/]".format(item.valorInicial),
                                  "[bold white]{:,.2f} USD[/]".format(item.valorActual),
                                  "[{}]{:>10}{:>10}[/]".format(signo, cambioDia, cambiopDia),
                                  "[{}]{:>10}{:>10}[/]".format(signot, cambioTotal, cambiopTotal))
    c.print(accionesTabla)
    c.print()

def mostrar_corto(usuario):
    s = ""
    if usuario.utilidadCorto.cambioDia < 0:
        signo = "#E74C3C"
    elif usuario.utilidadCorto.cambioDia > 0:
        signo = "#2ECC71"
        s = "+"
    else:
        signo = "#5D6D7E"
    st = ""
    if usuario.utilidadCorto.cambioTotal < 0:
        signot = "#E74C3C"
    elif usuario.utilidadCorto.cambiopTotal > 0:
        signot = "#2ECC71"
        st = "+"
    else:
        signot = "#5D6D7E"
    c.print("Acciones en corto", style="bold white", highlight=False, justify="right", width=70)
    cambioDiaUtilidad = s + "{:,.2f}".format(usuario.utilidadCorto.cambioDia)
    cambiopDiaUtilidad = "({}{:,.2f}%)".format(s, usuario.utilidadCorto.cambiopDia)
    cambioTotalUtilidad = st + "{:,.2f}".format(usuario.utilidadCorto.cambioTotal)
    cambiopTotalUtilidad = "({}{:,.2f}%)".format(st, usuario.utilidadCorto.cambiopTotal)
    cortosTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE, style=nombreC,
                          show_footer=True)
    cortosTabla.add_column("Simbolo", style="tabla", justify="left")
    cortosTabla.add_column("Cantidad", style="tabla", justify="right")
    cortosTabla.add_column("Precio inicial", style="tabla", justify="right")
    cortosTabla.add_column("Precio actual", style="tabla", justify="right")
    cortosTabla.add_column("Valor inicial", style="tabla", justify="right",
                             footer="[bold #CCD1D1]{:,.2f} USD[/]".format(usuario.utilidadCorto.valorInicial))
    cortosTabla.add_column("Valor actual", style="tabla", justify="right",
                             footer="[bold white]{:,.2f} USD[/]".format(usuario.utilidadCorto.valorActual))
    cortosTabla.add_column("Cambio del día", style="tabla", justify="right",
                             footer="[{}]{:>10}{:>10}[/]".format(signo, cambioDiaUtilidad, cambiopDiaUtilidad))
    cortosTabla.add_column("Cambio total", style="tabla", justify="right",
                             footer="[{}]{:>10}{:>10}[/]".format(signot, cambioTotalUtilidad, cambiopTotalUtilidad))

    if len(usuario.accionesCorto) == 0:
        cortosTabla.show_footer = False
        c.print(cortosTabla)
        c.print("  No tienes ninguna acción en corto", style="rojo", highlight=False)
        c.print()
        c.print()
    else:
        for item in usuario.accionesCorto:
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
            cortosTabla.add_row("[bold #CCD1D1]{}[/]".format(item.simbolo),
                                  "[bold #CCD1D1]{:,}[/]".format(item.cantidad),
                                  "[bold #CCD1D1]{:,.2f} USD[/]".format(item.precioInicial),
                                  "[bold white]{:,.2f} USD[/]".format(item.precioActual),
                                  "[bold #CCD1D1]{:,.2f} USD[/]".format(item.valorInicial),
                                  "[bold white]{:,.2f} USD[/]".format(item.valorActual),
                                  "[{}]{:>10}{:>10}[/]".format(signo, cambioDia, cambiopDia),
                                  "[{}]{:>10}{:>10}[/]".format(signot, cambioTotal, cambiopTotal))
        c.print(cortosTabla)
        c.print()


def comprar_accion(accion, valor, acciones, usuario, usuarios):
    while True:
        correcto = True
        for item in acciones:
            if item[valor] == accion:
                accionOp = item
                break

        maximo = math.trunc(usuario.poderAdquisitivo / accionOp['precioActual'])
        if maximo == 0:
            c.print()
            c.print("      No tienes el poder adquisitvo suficiente", style="rojob")
            break
        c.print()
        menu = Table(title="", show_footer=True, show_header=False,
                     footer_style="tabla",
                     style="bold white",
                     box=box.SIMPLE)
        menu.add_column("", justify="left", style="bold white")
        menu.add_column("", justify="left", footer="Ingresa cantidad a comprar",
                        style="bold white")
        menu.add_row("Precio", "{:,.2f} USD".format(accionOp['precioActual']))
        menu.add_row("Cantidad", "1 a {:,} acciones".format(maximo))
        c.print(menu)
        cantidad = rInput()
        c.clear()
        acciones = web_scraping.scrap_todas_acciones()
        usuario, usuarios = simulador_script.actualizar_portafolio(usuario, acciones, usuarios)
        if cantidad < 1:
            c.print()
            c.print("  Cantidad erronea", style="rojob")
            correcto = False
        else:
            maximo = math.trunc(usuario.poderAdquisitivo / accionOp['precioActual'])
            if cantidad > maximo:
                c.print()
                c.print("  Cantidad no puede superar el maximo", style="rojob")
                correcto = False
            else:
                existe = False
                for i, item in enumerate(usuario.accionesCompra):
                    if item.simbolo == accionOp['simbolo']:
                        existe = True
                        indice = i
                usuario.historial.append(Operacion(datetime.datetime.now().isoformat(), "Compra de accion", accionOp['simbolo'], cantidad, accionOp['precioActual'], cantidad*accionOp['precioActual']))
                if existe:
                    nuevoPrecio = ((usuario.accionesCompra[indice].cantidad * usuario.accionesCompra[indice].precioInicial) + (cantidad * accionOp['precioActual'])) / (cantidad + usuario.accionesCompra[indice].cantidad)
                    usuario.accionesCompra[indice].cantidad += cantidad
                    usuario.accionesCompra[indice].precioInicial = nuevoPrecio
                    usuario.accionesCompra[indice].valorInicial = usuario.accionesCompra[indice].precioInicial * usuario.accionesCompra[indice].cantidad
                    usuario.accionesCompra[indice].valorActual = usuario.accionesCompra[indice].precioActual * usuario.accionesCompra[indice].cantidad
                    usuario.accionesCompra[indice].fecha = datetime.datetime.now().isoformat()
                else:
                    usuario.accionesCompra.append(Accion("compra", datetime.datetime.now().isoformat(), accionOp['simbolo'], cantidad, accionOp['precioActual'], cantidad*accionOp['precioActual'], accionOp['precioActual'], cantidad*accionOp['precioActual']))
                c.print()
                c.print("  Compra de acción realizada con éxito", style="verdeb")
                opTabla = Table(title="", box=box.SIMPLE_HEAVY, style=nombreC)
                opTabla.add_column("", justify="left", style="tabla")
                opTabla.add_column("", justify="right", style="tabla")
                opTabla.add_row("Cantidad", "{:,}{}".format(cantidad, "    "))
                opTabla.add_row("Precio", "{:,.2f} USD".format(accionOp['precioActual']))
                opTabla.add_row("[bold white]{:<14}".format("Monto pagado"), "[bold white]{:,.2f} USD".format(cantidad*accionOp['precioActual']))
                c.print(opTabla)
                c.print()
                acciones = web_scraping.scrap_todas_acciones()
                usuario, usuarios = simulador_script.actualizar_portafolio(usuario, acciones, usuarios)
        if correcto:
            break
    return usuario, usuarios, acciones


def vender_accion(accion, valor, acciones, usuario, usuarios):
    while True:
        correcto = True
        for item in acciones:
            if item[valor] == accion:
                accionOp = item
                break
        encontrado = False
        for i, item in enumerate(usuario.accionesCompra):
            if item.simbolo == accionOp['simbolo']:
                encontrado = True
                accionVender = item
                indice = i
        if not encontrado:
            c.print()
            c.print("      No tienes titulos comprados de esta acción", style="rojob")
            break
        if (((datetime.datetime.now() - datetime.datetime.fromisoformat(accionVender.fecha)).total_seconds()) / 60) < 15:
            c.print()
            c.print("      No han pasado 15 minutos de haber comprado la acción", style="rojob", highlight="False")
            break
        maximo = accionVender.cantidad
        c.print()
        menu = Table(title="", show_footer=True, show_header=False,
                     footer_style="tabla",
                     style="bold white",
                     box=box.SIMPLE)
        menu.add_column("", justify="left", style="bold white")
        menu.add_column("", justify="left", footer="Ingresa cantidad a vender",
                        style="bold white")
        menu.add_row("Precio", "{:,.2f} USD".format(accionOp['precioActual']))
        menu.add_row("Cantidad", "1 a {:,} acciones".format(maximo))
        c.print(menu)
        cantidad = rInput()
        c.clear()
        if cantidad < 1:
            c.print()
            c.print("  Cantidad erronea", style="rojob")
            correcto = False
        if cantidad > maximo:
            c.print()
            c.print("  Cantidad no puede superar el maximo", style="rojob")
            correcto = False
        if correcto:
            acciones = web_scraping.scrap_todas_acciones()
            usuario, usuarios = simulador_script.actualizar_portafolio(usuario, acciones, usuarios)
            for item in acciones:
                if item[valor] == accion:
                    accionOp = item
                    break
            usuario.historial.append(Operacion(datetime.datetime.now().isoformat(), "Venta de accion", usuario.accionesCompra[indice].simbolo, cantidad, usuario.accionesCompra[indice].precioActual, usuario.accionesCompra[indice].precioActual*cantidad))
            if cantidad == maximo:
                usuario.valorCuentaActual += usuario.accionesCompra[indice].cambioTotal
                usuario.accionesCompra.pop(indice)
            else:
                usuario.valorCuentaActual += ((usuario.accionesCompra[indice].cambioTotal/usuario.accionesCompra[indice].cantidad)*cantidad)
                usuario.accionesCompra[indice].cantidad -= cantidad
                usuario.accionesCompra[indice].valorInicial = usuario.accionesCompra[indice].cantidad * usuario.accionesCompra[indice].precioInicial
                usuario.accionesCompra[indice].valorActual = usuario.accionesCompra[indice].cantidad * usuario.accionesCompra[indice].precioActual
            c.print()
            c.print("  Venta de acción realizada con éxito", style="verdeb")
            opTabla = Table(title="", box=box.SIMPLE_HEAVY, style=nombreC)
            opTabla.add_column("", justify="left", style="tabla")
            opTabla.add_column("", justify="right", style="tabla")
            opTabla.add_row("Cantidad", "{:,}{}".format(cantidad, "    "))
            opTabla.add_row("Precio", "{:,.2f} USD".format(accionOp['precioActual']))
            opTabla.add_row("[bold white]{:<14}".format("Monto cobrado"),
                            "[bold white]{:,.2f} USD".format(cantidad * accionOp['precioActual']))
            c.print(opTabla)
            c.print()
            acciones = web_scraping.scrap_todas_acciones()
            usuario, usuarios = simulador_script.actualizar_portafolio(usuario, acciones, usuarios)
            break
    return usuario, usuarios, acciones


def vender_corto(accion, valor, acciones, usuario, usuarios):
    while True:
        correcto = True
        for item in acciones:
            if item[valor] == accion:
                accionOp = item
                break
        maximo = math.trunc(usuario.poderAdquisitivo / accionOp['precioActual'])
        if maximo == 0:
            c.print()
            c.print("      No tienes el poder adquisitvo suficiente", style="rojob")
            break
        c.print()
        menu = Table(title="", show_footer=True, show_header=False,
                     footer_style="tabla",
                     style="bold white",
                     box=box.SIMPLE)
        menu.add_column("", justify="left", style="bold white")
        menu.add_column("", justify="left", footer="Ingresa cantidad a vender en corto",
                        style="bold white")
        menu.add_row("Precio", "{:,.2f} USD".format(accionOp['precioActual']))
        menu.add_row("Cantidad", "1 a {:,} acciones".format(maximo))
        c.print(menu)
        cantidad = rInput()
        c.clear()
        acciones = web_scraping.scrap_todas_acciones()
        usuario, usuarios = simulador_script.actualizar_portafolio(usuario, acciones, usuarios)
        for item in acciones:
            if item[valor] == accion:
                accionOp = item
                break
        if cantidad < 1:
            c.print()
            c.print("  Cantidad erronea", style="rojob")
            correcto = False
        else:
            maximo = math.trunc(usuario.poderAdquisitivo / accionOp['precioActual'])
            if cantidad > maximo:
                c.print()
                c.print("  Cantidad no puede superar el maximo", style="rojob")
                correcto = False
            else:
                existe = False
                for i, item in enumerate(usuario.accionesCorto):
                    if item.simbolo == accionOp['simbolo']:
                        existe = True
                        indice = i
                usuario.historial.append(Operacion(datetime.datetime.now().isoformat(), "Venta en corto", accionOp['simbolo'], cantidad, accionOp['precioActual'], cantidad * accionOp['precioActual']))
                if existe:
                    nuevoPrecio = ((usuario.accionesCorto[indice].cantidad * usuario.accionesCorto[indice].precioInicial) + (cantidad*accionOp['precioActual'])) / (cantidad+usuario.accionesCorto[indice].cantidad)
                    usuario.accionesCorto[indice].cantidad += cantidad
                    usuario.accionesCorto[indice].precioInicial = nuevoPrecio
                    usuario.accionesCorto[indice].valorInicial = usuario.accionesCorto[indice].precioInicial * usuario.accionesCorto[indice].cantidad
                    usuario.accionesCorto[indice].valorActual = usuario.accionesCorto[indice].precioActual * usuario.accionesCorto[indice].cantidad
                    usuario.accionesCorto[indice].fecha = datetime.datetime.now().isoformat()
                else:
                    usuario.accionesCorto.append(Accion("corto", datetime.datetime.now().isoformat(), accionOp['simbolo'], cantidad, accionOp['precioActual'], cantidad * accionOp['precioActual'], accionOp['precioActual'], cantidad * accionOp['precioActual']))
                c.print()
                c.print("  Venta en corto realizada con éxito", style="verdeb")
                opTabla = Table(title="", box=box.SIMPLE_HEAVY, style=nombreC)
                opTabla.add_column("", justify="left", style="tabla")
                opTabla.add_column("", justify="right", style="tabla")
                opTabla.add_row("Cantidad", "{:,}{}".format(cantidad, "    "))
                opTabla.add_row("Precio", "{:,.2f} USD".format(accionOp['precioActual']))
                opTabla.add_row("[bold white]{:<14}".format("Monto pagado"),
                                "[bold white]{:,.2f} USD".format(cantidad * accionOp['precioActual']))
                c.print(opTabla)
                c.print()
                acciones = web_scraping.scrap_todas_acciones()
                usuario, usuarios = simulador_script.actualizar_portafolio(usuario, acciones, usuarios)
        if correcto:
            break
    return usuario, usuarios, acciones


def comprar_corto(accion, valor, acciones, usuario, usuarios):
    while True:
        correcto = True
        for item in acciones:
            if item[valor] == accion:
                accionOp = item
                break
        encontrado = False
        for i, item in enumerate(usuario.accionesCorto):
            if item.simbolo == accionOp['simbolo']:
                encontrado = True
                accionVender = item
                indice = i
        if not encontrado:
            c.print()
            c.print("      No tienes titulos en corto de esta acción", style="rojob")
            break
        if (((datetime.datetime.now() - datetime.datetime.fromisoformat(accionVender.fecha)).total_seconds()) / 60) < 15:
            c.print()
            c.print("      No han pasado 15 minutos de haber vendido la acción en corto", style="rojob", highlight="False")
            break
        maximo = accionVender.cantidad
        c.print()
        menu = Table(title="", show_footer=True, show_header=False,
                     footer_style="tabla",
                     style="bold white",
                     box=box.SIMPLE)
        menu.add_column("", justify="left", style="bold white")
        menu.add_column("", justify="left", footer="Ingresa cantidad a comprar para cubrir",
                        style="bold white")
        menu.add_row("Precio", "{:,.2f} USD".format(accionOp['precioActual']))
        menu.add_row("Cantidad", "1 a {:,} acciones".format(maximo))
        c.print(menu)
        cantidad = rInput()
        c.clear()
        if cantidad < 1:
            c.print()
            c.print("  Cantidad erronea", style="rojob")
            correcto = False
        if cantidad > maximo:
            c.print()
            c.print("  Cantidad no puede superar el maximo", style="rojob")
            correcto = False
        if correcto:
            acciones = web_scraping.scrap_todas_acciones()
            usuario, usuarios = simulador_script.actualizar_portafolio(usuario, acciones, usuarios)
            for item in acciones:
                if item[valor] == accion:
                    accionOp = item
                    break
            usuario.historial.append(Operacion(datetime.datetime.now().isoformat(), "Compra para cubrir", usuario.accionesCorto[indice].simbolo, cantidad, usuario.accionesCorto[indice].precioActual, usuario.accionesCorto[indice].precioActual * cantidad))
            if cantidad == maximo:
                usuario.valorCuentaActual += usuario.accionesCorto[indice].cambioTotal
                usuario.accionesCorto.pop(indice)
            else:
                usuario.valorCuentaActual += ((usuario.accionesCorto[indice].cambioTotal / usuario.accionesCorto[indice].cantidad) * cantidad)
                usuario.accionesCorto[indice].cantidad -= cantidad
                usuario.accionesCorto[indice].valorInicial = usuario.accionesCorto[indice].cantidad * usuario.accionesCorto[indice].precioInicial
                usuario.accionesCorto[indice].valorActual = usuario.accionesCorto[indice].cantidad * usuario.accionesCorto[indice].precioActual

            c.print()
            c.print("  Compra para cubrir realizada con éxito", style="verdeb")
            opTabla = Table(title="", box=box.SIMPLE_HEAVY, style=nombreC)
            opTabla.add_column("", justify="left", style="tabla")
            opTabla.add_column("", justify="right", style="tabla")
            opTabla.add_row("Cantidad", "{:,}{}".format(cantidad, "    "))
            opTabla.add_row("Precio", "{:,.2f} USD".format(accionOp['precioActual']))
            opTabla.add_row("[bold white]{:<14}".format("Monto cobrado"),
                            "[bold white]{:,.2f} USD".format(cantidad * accionOp['precioActual']))
            c.print(opTabla)
            c.print()
            acciones = web_scraping.scrap_todas_acciones()
            usuario, usuarios = simulador_script.actualizar_portafolio(usuario, acciones, usuarios)
            break
    return usuario, usuarios, acciones


def mostrar_competencia(usuario, usuarios):
    capitales = []
    ranking = []
    usuariosaux = [item for item in usuarios]
    for item in usuarios:
        capitales.append(item.valorCuentaActual)
    capitales.sort()
    capitales = capitales[::-1]
    for cap in capitales:
        for i, u in enumerate(usuariosaux):
            if u.valorCuentaActual == cap:
                ranking.append(u)
                usuariosaux.pop(i)
                break
    for i, item in enumerate(ranking):
        if usuario.nombreUsuario == item.nombreUsuario:
            rankingusuario = i+1
    compeTabla = Table(title="", box=rich.box.SIMPLE_HEAVY, style=nombreC)
    compeTabla.add_column("")
    compeTabla.add_column("[bold white]{}[/]".format(usuario.nombreUsuario), justify="left")
    compeTabla.add_column("", justify="right")
    compeTabla.add_row("", "[tabla]Participantes[/]", "[tabla]{}".format(len(usuarios)))
    compeTabla.add_row("", "[bold white]Lugar[/]", "[bold white]{}".format(rankingusuario))
    c.print(compeTabla)
    compe2Tabla = Table(title="", box=box.SIMPLE, style=nombreC)
    compe2Tabla.add_column("", justify="right", style="tabla")
    compe2Tabla.add_column("Tabla", justify="left", style="tabla")
    compe2Tabla.add_column("", justify="right", style="tabla")
    compe2Tabla.add_column("", justify="right", style="tabla")
    compe2Tabla.add_column("", justify="right", style="tabla")
    for i, item in enumerate(ranking):
        s = ""
        if item.cambioTotal < 0:
            signo = "#E74C3C"
        elif item.cambioTotal > 0:
            signo = "#2ECC71"
            s = "+"
        else:
            signo = "#5D6D7E"
        if usuario.nombreUsuario == item.nombreUsuario:
            compe2Tabla.add_row("[bold white]{}[/]".format(i+1), "[bold white]{}[/]".format(item.nombreUsuario), "[bold white]{:,.2f} USD[/]".format(item.valorCuentaActual), "[bold {}]{}{:,.2f}[/]".format(signo, s, item.cambioTotal), "[bold {}]({}{:,.2f}%)[/]".format(signo, s, (item.cambioTotal / 100000) * 100))
        else:
            compe2Tabla.add_row("{}".format(i+1), "{}".format(item.nombreUsuario), "{:,.2f} USD".format(item.valorCuentaActual), "[{}]{}{:,.2f}[/]".format(signo, s, item.cambioTotal), "[{}]({}{:,.2f}%)[/]".format(signo, s, (item.cambioTotal / 100000) * 100))
    c.print(compe2Tabla)


def definir_mercado(imprimir):

    hora = datetime.datetime.now().hour
    minuto = datetime.datetime.now().minute
    minutosTotales = (hora*60) + minuto
    minutosAbrir = (8*60) + 30
    minutosCerrar = 15*60
    dia = datetime.datetime.now().isoweekday()
    if dia == 6 or dia == 7:
        abierto = False
        tiempo = (24*60) - minutosTotales + minutosAbrir
        hora = math.trunc(tiempo / 60)
        minuto = tiempo - (hora * 60)
        if dia == 7:
            tiempo = "Abre en {} hrs, {} mins".format(hora, minuto)
        else:
            tiempo = "Abre en 1 día, {} hrs, {} mins".format(hora, minuto)
    else:
        if minutosAbrir <= minutosTotales < minutosCerrar:
            abierto = True
            tiempo = minutosCerrar - minutosTotales
            hora = math.trunc(tiempo / 60)
            minuto = tiempo - (hora*60)
            tiempo = "Cierra en {} hrs, {} mins".format(hora, minuto)
        else:
            abierto = False
            if minutosTotales >= minutosCerrar:
                tiempo = (24 * 60) - minutosTotales + minutosAbrir
            else:
                tiempo = minutosAbrir - minutosTotales
            hora = math.trunc(tiempo / 60)
            minuto = tiempo - (hora * 60)
            if dia == 5 and minutosTotales >= minutosCerrar:
                tiempo = "Abre en 2 días, {} hrs, {} mins".format(hora, minuto)
            else:
                tiempo = "Abre en {} hrs, {} mins".format(hora, minuto)
    if imprimir:
        c.print()
        if abierto:
            c.print("[verdeb]  Mercado abierto")
        else:
            c.print("[rojob]  Mercado cerrado")
        c.print("[bold white]  {}".format(tiempo))
        c.print("")
    return abierto, tiempo

def mostrar_historial(usuario):
    c.print()
    c.print("Historial de operaciones", style="bold white", highlight=False, justify="right", width=55)
    if len(usuario.historial) == 0:
        c.print("  No tienes historial de operaciones", style="rojob", highlight=False, justify="left")
        c.print()
        c.print()
    else:
        historialTabla = Table(title="", header_style="bold {}".format(nombreC), box=box.SIMPLE, style=nombreC)
        historialTabla.add_column("Fecha", style="tabla", justify="right")
        historialTabla.add_column("Tipo", style="tabla", justify="left")
        historialTabla.add_column("Acción", style="tabla", justify="left")
        historialTabla.add_column("Cantidad", style="tabla", justify="right")
        historialTabla.add_column("Precio", style="tabla", justify="right")
        historialTabla.add_column("Valor total", style="tabla", justify="right")
        for i, item in enumerate(usuario.historial):
            if (i+1)%2 == 0:
                estilo = "tabla"
            else:
                estilo = "bold white"
                if datetime.datetime.fromisoformat(item.fecha).day < 10:
                    dia = "0"
                else:
                    dia = ""
                if datetime.datetime.fromisoformat(item.fecha).month < 10:
                    mes = "0"
                else:
                    mes = ""
                if datetime.datetime.fromisoformat(item.fecha).hour < 10:
                    hora = "0"
                else:
                    hora = ""
                if datetime.datetime.fromisoformat(item.fecha).minute < 10:
                    minuto = "0"
                else:
                    minuto = ""
            historialTabla.add_row("[{}]{}-{}-{}  {}:{}[/]".format(estilo, dia+str(datetime.datetime.fromisoformat(item.fecha).day),
                                                                        mes+str(datetime.datetime.fromisoformat(item.fecha).month),
                                                                        datetime.datetime.fromisoformat(item.fecha).year,
                                                                        hora+str(datetime.datetime.fromisoformat(item.fecha).hour),
                                                                        minuto+str(datetime.datetime.fromisoformat(item.fecha).minute)),
                                   "[{}]{}[/]".format(estilo, item.descripcion), "[{}]{}[/]".format(estilo, item.simbolo), "[{}]{:,}[/]".format(estilo, item.cantidad), "[{}]{:,.2f} USD[/]".format(estilo, item.precio), "[{}]{:,.2f} USD[/]".format(estilo, item.valorTotal))

        c.print(historialTabla)
        c.print()