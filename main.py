from Packages.Classes.usuario import Usuario
from Packages.Scripts import web_scraping, usuario_script, simulador_script

import rich.box
from rich.console import Console
from rich.table import Table
from rich import box
from rich.theme import Theme

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

if __name__ == "__main__":
    acciones = web_scraping.scrap_todas_acciones()
    usuarios = usuario_script.cargar_usuarios()

    while True:
        c.print()
        c.print("      Ingresar al sistema", style="bold #A3E4D7")
        usuarioEliminado = False
        menu = Table(title="", show_footer=True, show_header=False, footer_style="tabla", style="bold white",
                     box=box.SIMPLE)
        menu.add_column("", justify="center", style="bold white")
        menu.add_column("", justify="left", footer="Elija una opción", style="bold white")
        menu.add_row("1", "Iniciar sesión")
        menu.add_row("2", "Crear cuenta")
        menu.add_row("3", "Salir")
        c.print(menu)
        opcInicio = rInput()
        c.clear()
        if opcInicio in list(range(1, 3)):
            if opcInicio == 1:
                c.print()
                c.print("  Iniciar sesión", style="bold #A3E4D7")
                c.print()
                usuarioActual = usuario_script.validar_usuario(usuarios)


                # Inicio del sistema una vez ingresado
                acciones = web_scraping.scrap_todas_acciones()
                usuarioActual, usuarios = simulador_script.actualizar_portafolio(usuarioActual, acciones, usuarios)
                while True:
                    c.print()
                    c.print("      Bienvenido a SINVER", style="bold #A3E4D7")
                    menu = Table(title="", show_footer=True, show_header=False, footer_style="tabla",
                                 style="bold white",
                                 box=box.SIMPLE)
                    menu.add_column("", justify="center", style="bold white")
                    menu.add_column("", justify="left", footer="Elija una opción", style="bold white")
                    menu.add_row("1", "Simulador")
                    menu.add_row("2", "Cuenta")
                    menu.add_row("3", "Ayuda")
                    menu.add_row("4", "Salir")
                    c.print(menu)
                    opcModulos = rInput()
                    c.clear()
                    if opcModulos in list(range(1, 4)):
                        if opcModulos == 1:


                            # Inicio del simulador
                            while True:
                                c.print()
                                c.print("      Simulador", style="bold #A3E4D7")
                                menu = Table(title="", show_footer=True, show_header=False, footer_style="tabla",
                                             style="bold white",
                                             box=box.SIMPLE)
                                menu.add_column("", justify="center", style="bold white")
                                menu.add_column("", justify="left", footer="Elija una opción", style="bold white")
                                menu.add_row("1", "Portafolio")
                                menu.add_row("2", "Comerciar")
                                menu.add_row("3", "Investigar")
                                menu.add_row("4", "Competencia")
                                menu.add_row("5", "Salir")
                                c.print(menu)
                                opcSimulador = rInput()
                                c.clear()
                                if opcSimulador in list(range(1, 5)):
                                    if opcSimulador == 1:


                                        # Portafolio
                                        while True:
                                            c.print()
                                            c.print("      Portafolio", style="bold #A3E4D7")
                                            menu = Table(title="", show_footer=True, show_header=False,
                                                         footer_style="tabla",
                                                         style="bold white",
                                                         box=box.SIMPLE)
                                            menu.add_column("", justify="center", style="bold white")
                                            menu.add_column("", justify="left", footer="Elija una opción",
                                                            style="bold white")
                                            menu.add_row("1", "Mostrar resumen de cuenta")
                                            menu.add_row("2", "Mostrar acciones compradas")
                                            menu.add_row("3", "Mostrar acciones vendidas en corto")
                                            menu.add_row("4", "Mostrar historial de operaciones")
                                            menu.add_row("5", "Salir")
                                            c.print(menu)
                                            opcPortafolio = rInput()
                                            c.clear()
                                            if opcPortafolio in list(range(1, 5)):
                                                simulador_script.definir_mercado(True)
                                                if opcPortafolio == 1:
                                                    acciones = web_scraping.scrap_todas_acciones()
                                                    usuarioActual, usuarios = simulador_script.actualizar_portafolio(usuarioActual, acciones, usuarios)
                                                    simulador_script.mostrar_resumen(usuarioActual)
                                                elif opcPortafolio == 2:
                                                    acciones = web_scraping.scrap_todas_acciones()
                                                    usuarioActual, usuarios = simulador_script.actualizar_portafolio(usuarioActual, acciones, usuarios)
                                                    simulador_script.mostrar_compra(usuarioActual)
                                                elif opcPortafolio == 3:
                                                    acciones = web_scraping.scrap_todas_acciones()
                                                    usuarioActual, usuarios = simulador_script.actualizar_portafolio(usuarioActual, acciones, usuarios)
                                                    simulador_script.mostrar_corto(usuarioActual)
                                                else:
                                                    acciones = web_scraping.scrap_todas_acciones()
                                                    usuarioActual, usuarios = simulador_script.actualizar_portafolio(usuarioActual, acciones, usuarios)
                                                    simulador_script.mostrar_historial(usuarioActual)
                                            elif opcPortafolio == 5:
                                                break
                                            else:
                                                c.clear()


                                    elif opcSimulador == 2:


                                        # Comerciar
                                        abierto, tiempo = simulador_script.definir_mercado(True)
                                        if abierto:
                                            while True:
                                                c.print()
                                                c.print("  Comerciar", style="bold #A3E4D7")
                                                c.print()
                                                long = str(len("  Ingresa el simbolo de acción o nombre de empresa") + 2)
                                                accion = str(c.input("[bold white]{:<{}}>  ".format("  Ingresa el simbolo de acción o nombre de empresa", long))).upper()
                                                c.clear()
                                                encontrado = simulador_script.validar_accion(accion, acciones)
                                                if encontrado != 'o':
                                                    break
                                                else:
                                                    simulador_script.definir_mercado(True)
                                                    c.print()
                                                    c.print("  Accion no existente", style="rojob")
                                            acciones = web_scraping.scrap_todas_acciones()
                                            simulador_script.definir_mercado(True)
                                            c.print()
                                            simulador_script.resumen_accion(accion, encontrado, acciones)
                                            salirComercio = False
                                            while not salirComercio:

                                                menu = Table(title="", show_footer=True, show_header=False,
                                                             footer_style="tabla",
                                                             style="bold white",
                                                             box=box.SIMPLE)
                                                menu.add_column("", justify="center", style="bold white")
                                                menu.add_column("", justify="left", footer="Operación a realizar",
                                                                style="bold white")
                                                menu.add_row("", "Acciones compradas")
                                                menu.add_row("1", "Comprar")
                                                menu.add_row("2", "Vender")
                                                menu.add_row("", "")
                                                menu.add_row("", "Acciones en corto")
                                                menu.add_row("3", "Vender en corto")
                                                menu.add_row("4", "Comprar para cubrir")
                                                menu.add_row("", "")
                                                menu.add_row("5", "Cancelar")
                                                c.print(menu)
                                                opcComercio = rInput()
                                                c.clear()
                                                if opcComercio in list(range(1, 5)):
                                                    salirComercio = True
                                                    acciones = web_scraping.scrap_todas_acciones()
                                                    usuarioActual, usuarios = simulador_script.actualizar_portafolio(usuarioActual, acciones, usuarios)
                                                    if opcComercio == 1:
                                                        usuarioActual, usuarios, acciones = simulador_script.comprar_accion(accion, encontrado, acciones, usuarioActual, usuarios)
                                                    elif opcComercio == 2:
                                                        usuarioActual, usuarios, acciones = simulador_script.vender_accion(accion, encontrado, acciones, usuarioActual, usuarios)
                                                    elif opcComercio == 3:
                                                        usuarioActual, usuarios, acciones = simulador_script.vender_corto(accion, encontrado, acciones, usuarioActual, usuarios)
                                                    else:
                                                        usuarioActual, usuarios, acciones = simulador_script.comprar_corto(accion, encontrado, acciones, usuarioActual, usuarios)
                                                elif opcComercio == 5:
                                                    salirComercio = True
                                                else:
                                                    c.clear()


                                    elif opcSimulador == 3:


                                        # Investigar
                                        while True:
                                            c.print()
                                            c.print("      Investigar", style="bold #A3E4D7")
                                            menu = Table(title="", show_footer=True, show_header=False,
                                                         footer_style="tabla",
                                                         style="bold white",
                                                         box=box.SIMPLE)
                                            menu.add_column("", justify="center", style="bold white")
                                            menu.add_column("", justify="left", footer="Elija una opción",
                                                            style="bold white")
                                            menu.add_row("1", "Buscar acción")
                                            menu.add_row("2", "Mostrar acciones con mayor capitalización")
                                            menu.add_row("3", "Mostrar acciones más comerciadas")
                                            menu.add_row("4", "Salir")
                                            c.print(menu)
                                            opcInvestigar = rInput()
                                            c.clear()
                                            if opcInvestigar in list(range(1, 4)):
                                                simulador_script.definir_mercado(True)
                                                if opcInvestigar == 1:
                                                    acciones = web_scraping.scrap_todas_acciones()
                                                    simulador_script.buscar_accion(acciones)
                                                elif opcInvestigar == 2:
                                                    simulador_script.mostrar_acciones_cap()
                                                else:
                                                    simulador_script.mostrar_acciones_vol()
                                            elif opcInvestigar == 4:
                                                break
                                            else:
                                                c.clear()


                                    else:


                                        # Competencia
                                        simulador_script.definir_mercado(True)
                                        acciones = web_scraping.scrap_todas_acciones()
                                        usuarioActual, usuarios = simulador_script.actualizar_portafolio(usuarioActual, acciones, usuarios)
                                        for us in usuarios:
                                            us, usuarios = simulador_script.actualizar_portafolio(us, acciones, usuarios)
                                        simulador_script.mostrar_competencia(usuarioActual, usuarios)


                                elif opcSimulador == 5:
                                    break
                                else:
                                    c.clear()


                        elif opcModulos == 2:


                            # Modulo de cuenta
                            while True:
                                c.print()
                                c.print("      Cuenta", style="bold #A3E4D7")
                                menu = Table(title="", show_footer=True, show_header=False, footer_style="tabla",
                                             style="bold white",
                                             box=box.SIMPLE)
                                menu.add_column("", justify="center", style="bold white")
                                menu.add_column("", justify="left", footer="Elija una opción", style="bold white")
                                menu.add_row("1", "Ver cuenta")
                                menu.add_row("2", "Modificar cuenta")
                                menu.add_row("3", "Eliminar cuenta")
                                menu.add_row("4", "Salir")
                                c.print(menu)
                                opcCuenta = rInput()
                                c.clear()
                                if opcCuenta in list(range(1, 4)):
                                    if opcCuenta == 1:
                                        usuario_script.ver_usuario(usuarioActual)
                                    elif opcCuenta == 2:
                                        usuarios = usuario_script.modificar_usuario(usuarioActual, usuarios)
                                    else:
                                        usuarios = usuario_script.eliminar_usuario(usuarioActual, usuarios)
                                        usuarioEliminado = True
                                        c.print()
                                        c.print("      Cuenta eliminada", style="rojob")
                                        break
                                elif opcCuenta == 4:
                                    break
                                else:
                                    c.clear()
                            if usuarioEliminado:
                                break


                        else:


                            # Modulo de ayuda
                            c.print()
                            c.print("SINVER", style="bold #A3E4D7")
                            c.print("Sinver es un simulador de compra y venta de acciones (bolsa de valores), su función es asemejarse lo más posible a una aplicación de bolsa real, esto para brindar práctica a cualquier persona interesada en invertir en la bolsa de valores", style="bold white", width=150)
                            c.print()
                            c.print("CUENTA", style="bold #A3E4D7")
                            c.print("Para poder ingresar al sistema, seguramente cresate una cuenta en algún momento, dicha cuenta tiene información personal la cual puede ser manejada. Dentro de este módulo, podrás ver, modificar y eliminar tu cuenta o cualquier dato de la misma", style="bold white", width=150)
                            c.print()
                            c.print("MODULOS", style="bold #A3E4D7")
                            c.print()
                            c.print("Portafolio", style="bold #A3E4D7")
                            c.print("Un portafolio resume las ganacias, perdidas y acciones que tienes o has tenido. Dentro de este módulo, podrás encontrar:", style="bold white", width=150)
                            c.print()
                            c.print("  - Resumen de cuenta. Muestra la ganancia o perdida de la cuenta, así como su valor actual", style="bold white", width=150)
                            c.print("  - Acciones compradas. Lista de acciones que tienes compradas y sus ganancias/perdidas", style="bold white", width=150)
                            c.print("  - Acciones vendidas en corto. Lista de acciones que tienes en corto y sus ganancias/perdidas", style="bold white", width=150)
                            c.print("  - Historial de operaciones. Lista de todas las operaciones realizadas", style="bold white", width=150)
                            c.print()
                            c.print("Investigar", style="bold #A3E4D7")
                            c.print("Una parte muy importante al invertir en la bolsa de valores, es el analizar la información y datos de las acciones; en este módulo puedes indagar más acerca de todas las acciones del mercado sin necesidad de realizar una operación. Dentro de este modulo, podrás encontrar:", style="bold white", width=150)
                            c.print()
                            c.print("  - Busqueda de acción. Muestra información muy compleat acerca de la acción especificada", style="bold white", width=150)
                            c.print("  - Acciones con mayor capitalización. Las 15 acciones con mayor capitalización del mercado", style="bold white", width=150, highlight=False)
                            c.print("  - Acciones más comerciadas. Las 15 acciones más comerciadas del momento (Mayor volumen)", style="bold white", width=150, highlight=False)
                            c.print("  - Historial de operaciones. Lista de todas las operaciones realizadas", style="bold white", width=150)
                            c.print()
                            c.print("Competencia", style="bold #A3E4D7")
                            c.print("El sistema está diseñado para competir con demás usuarios y comparar las ganancias que cada uno tiene. Por esta razón, dentro de este módulo, podrás ver tu rendimiento comparado con todos los usuarios dentro del sistema", style="bold white", width=150)
                            c.print()




                    elif opcModulos == 4:
                        break
                    else:
                        c.clear()


            else:
                usuarios.append(usuario_script.crear_usuario(Usuario(), usuarios))
        elif opcInicio == 3:
            break
        else:
            c.clear()
    usuario_script.guardar_usuarios(usuarios)
