import json

import bcrypt
from pwinput import pwinput
from unidecode import unidecode

import rich.box
from rich.console import Console
from rich.table import Table
from rich import box
from rich.theme import Theme

from Packages.Classes.operacion import Operacion
from Packages.Classes.usuario import Usuario
from Packages.Classes.utilidad import Utilidad
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


def cargar_usuarios():
    usuarios = []
    try:
        with open('Packages\\Files\\usuarios.json') as f:
            json_resultado = json.load(f)
        for item in json_resultado:
            usuarios.append(Usuario(**item))
            usuarios[-1].utilidadCorto = Utilidad(**item['utilidadCorto'])
            usuarios[-1].utilidadCompra = Utilidad(**item['utilidadCompra'])
            usuarios[-1].accionesCompra = []
            usuarios[-1].accionesCorto = []
            usuarios[-1].historial = []
            for item2 in item["accionesCompra"]:
                usuarios[-1].accionesCompra.append(Accion(**item2))
            for item2 in item["accionesCorto"]:
                usuarios[-1].accionesCorto.append(Accion(**item2))
            for item2 in item["historial"]:
                usuarios[-1].historial.append(Operacion(**item2))
    except IOError:
        pass
    return usuarios


def guardar_usuarios(usuarios):
    with open('Packages\\Files\\usuarios.json', 'w') as f:
        json.dump(usuarios, f, indent=2, default=lambda x: x.__dict__)


def crear_usuario(usuario, usuarios):
    usuario.nombreCompleto = validar_nombre()
    usuario.nombreUsuario = validar_nombre_usuario(usuarios)
    usuario.edad = validar_edad()
    usuario.genero = validar_genero()
    usuario.correo = validar_correo(usuarios)
    usuario.contrasena = validar_contrasena()
    c.print("      Cuenta creada con exito", style="verdeb")
    return usuario


def ver_usuario(usuario):
    c.print()
    c.print("      Ver cuenta", style="bold #A3E4D7", end="")
    usuarioTabla = Table(title="", box=box.SIMPLE, style=nombreC)
    usuarioTabla.add_column("", justify="left", style="tabla")
    usuarioTabla.add_column("", justify="right", style="bold white")
    usuarioTabla.add_row("Nombre de usuario", usuario.nombreUsuario)
    usuarioTabla.add_row("Nombre completo", usuario.nombreCompleto)
    usuarioTabla.add_row("Correo electrónico", usuario.correo)
    usuarioTabla.add_row("Edad", "{} años".format(usuario.edad))
    usuarioTabla.add_row("Genero", usuario.genero)
    c.print(usuarioTabla)
    c.print()


def eliminar_usuario(usuario, usuarios):
    for i, item in enumerate(usuarios):
        if usuario.nombreUsuario == item.nombreUsuario:
            usuarios.pop(i)
    return usuarios


def modificar_usuario(usuario, usuarios):
    usuario_viejo = usuario.nombreUsuario
    opc = 0
    while opc not in list(range(1, 5)):
        c.clear()
        c.print()
        c.print("      Modificar cuenta", style="bold #A3E4D7", end="")
        c.print()
        menu = Table(title="", show_footer=True, show_header=False, footer_style="tabla", style="bold white",
                     box=box.SIMPLE)
        menu.add_column("", justify="center", style="bold white")
        menu.add_column("", justify="left", footer="¿Qué deseas modificar?", style="bold white")
        menu.add_row("1", "Nombre de usuario")
        menu.add_row("2", "Nombre completo")
        menu.add_row("3", "Correo electrónico")
        menu.add_row("4", "Contraseña")
        c.print(menu)
        opc = rInput()
        c.clear()
    if opc == 1:
        usuario.nombreUsuario = validar_nombre_usuario(usuarios)
    elif opc == 2:
        usuario.nombreCompleto = validar_nombre()
    elif opc == 3:
        usuario.correo = validar_correo(usuarios)
    elif opc == 4:
        usuario.contrasena = validar_contrasena()
    for i, item in enumerate(usuarios):
        if item.nombreUsuario == usuario_viejo:
            usuarios[i] = usuario
    c.print("      Cuenta modificada", style="verdeb")
    return usuarios


def validar_usuario(usuarios):
    while True:
        long = str(len("  Ingresa el nombre de usuario") + 2)
        nombre_usuario = str(c.input("[bold white]{:<{}}>  ".format("  Ingresa el nombre de usuario", long)))
        c.print("[bold white]{:<{}}>  ".format("  Ingresa la contraseña", long), end="")
        contrasena = pwinput(prompt="")
        ingresado = False
        for item in usuarios:
            if item.nombreUsuario == nombre_usuario and bcrypt.checkpw(contrasena.encode('utf-8'), item.contrasena.encode('utf-8')):
                usuario_ingresado = item
                ingresado = True
                c.clear()
                c.print("")
                c.print("      Has iniciado sesión", style="verdeb", highlight=False)
        if ingresado:
            break
        c.clear()
        c.print("")
        c.print("  Datos erroneos", style="rojob", highlight=False)
        c.print("")

    return usuario_ingresado


def actualizar_usuario(usuario, usuarios):
    for i, item in enumerate(usuarios):
        if item.nombreUsuario == usuario.nombreUsuario:
            usuarios[i] = usuario
            break
    return usuarios



def validar_nombre():
    while True:
        correcto = True
        c.print()
        long = str(len("  Ingresa tu nombre completo") + 2)
        entrada = str(c.input("[bold white]{:<{}}>  ".format("  Ingresa tu nombre completo", long)))
        c.clear()
        c.print()
        if not (''.join(entrada.split(' '))).isalpha():
            correcto = False
            c.print("  Nombre debe ser alfabético", style="rojob", highlight=False)
        if len(entrada) > 50:
            correcto = False
            c.print("  No puede contener más de 50 caracteres", style="rojob", highlight=False)
        if len(entrada) < 10:
            correcto = False
            c.print("  No puede contener menos de 10 caracteres", style="rojob", highlight=False)

        if correcto:
            break
    return entrada


def validar_nombre_usuario(usuarios):
    while True:
        correcto = True
        c.print()
        long = str(len("  Ingresa tu nombre de usuario") + 2)
        entrada = str(c.input("[bold white]{:<{}}>  ".format("  Ingresa tu nombre de usuario", long)))
        c.clear()
        c.print()
        if len(entrada) > 20:
            correcto = False
            c.print("  No puede contener mas de 20 caracteres", style="rojob", highlight=False)
        for item in usuarios:
            if item.nombreUsuario == entrada:
                correcto = False
                c.print("  Nombre de usuario ya existe", style="rojob", highlight=False)
        if len(entrada) < 2:
            correcto = False
            c.print("  No puede contener menos de 2 caracteres", style="rojob", highlight=False)

        if correcto:
            break
    return entrada


def validar_edad():
    while True:
        c.print()
        correcto = True
        long = str(len("  Ingresa tu edad") + 2)
        entrada = int(c.input("[bold white]{:<{}}>  ".format("  Ingresa tu edad", long)))
        c.clear()
        c.print()
        if entrada > 100:
            correcto = False
            c.print("  Maximo 100 años de edad", style="rojob", highlight=False)
        if entrada < 18:
            correcto = False
            c.print("  Debes tener mínimo 18 años", style="rojob", highlight=False)

        if correcto:
            break
    return entrada


def validar_genero():
    while True:
        correcto = True
        menu = Table(title="", show_footer=True, show_header=False, footer_style="tabla", style="bold white",
                     box=box.SIMPLE)
        menu.add_column("", justify="center", style="bold white")
        menu.add_column("", justify="left", footer="Ingresa tu genero", style="bold white")
        menu.add_row("M", "Masculino")
        menu.add_row("F", "Femenino")
        menu.add_row("O", "Otro")
        c.print(menu)
        entrada = str(c.input("[tabla]{}> ".format(esp))).upper()
        c.clear()
        c.print()
        if entrada == "M":
            entrada = "Masculino"
        elif entrada == "F":
            entrada = "Femenino"
        elif entrada == "O":
            entrada = "Otro"
        else:
            correcto = False
            c.print("  Opción no valida", style="rojob", highlight=False)
            c.print()
        if correcto:
            break
    return entrada


def validar_correo(usuarios):
    while True:
        correcto = True
        c.print()
        long = str(len("  Ingresa tu correo electrónico") + 2)
        entrada = str(c.input("[bold white]{:<{}}>  ".format("  Ingresa tu correo electrónico", long)))
        c.clear()
        c.print()
        aux = entrada
        aux = aux.replace("ñ", "n")
        aux = aux.replace("Ñ", "N")
        if unidecode(aux) != aux:
            correcto = False
            c.print("  No se permiten acentos", style="rojob", highlight=False)
        if " " in entrada:
            correcto = False
            c.print("  No se permiten espacios", style="rojob", highlight=False)
        if ("(" or ")" or "<" or ">" or "," or ";" or ":" or "[" or "]" or "ç" or "%" or "&") in entrada:
            correcto = False
            c.print("  No se permiten los signos ()<>,;:[]ç%&", style="rojob", highlight=False)
        if entrada.count("@") != 1:
            correcto = False
            c.print("  Debe contener @ solo una vez", style="rojob", highlight=False)
        else:
            if len(entrada.split('@')[0]) > 64:
                correcto = False
                c.print("  No más de 64 caracteres a la izquierda del @", style="rojob", highlight=False)
            if len(entrada.split('@')[1]) > 255:
                correcto = False
                c.print("  No más de 255 caracteres a la derecha del @", style="rojob", highlight=False)
        for item in usuarios:
            if item.correo == entrada:
                correcto = False
                c.print("  Ya existe una cuenta con ese correo electrónico", style="rojob", highlight=False)
        if correcto:
            break
    return entrada


def validar_contrasena():
    while True:
        correcto = True
        c.print()
        long = str(len("  Confirma tu contraseña") + 2)
        c.print("[bold white]{:<{}}>  ".format("  Ingresa tu contraseña", long), end="")
        entrada = pwinput(prompt="")
        c.print("[bold white]{:<{}}>  ".format("  Confirma tu contraseña", long), end="")
        entrada2 = pwinput(prompt="")
        c.clear()
        c.print()
        hashedEntrada = bcrypt.hashpw(entrada.encode('utf-8'), bcrypt.gensalt(10))
        if len(entrada) > 30:
            correcto = False
            c.print("  No puede contener mas de 30 caracteres", style="rojob", highlight=False)
        if len(entrada) < 8:
            correcto = False
            c.print("  No puede contener menos de 8 caracteres", style="rojob", highlight=False)
        mayusculas = False
        minisculas = False
        numeros = False
        for item in entrada:
            if item.isupper():
                mayusculas = True
            if item.islower():
                minisculas = True
            if item.isdigit():
                numeros = True
        if not mayusculas or not minisculas or not numeros:
            correcto = False
            c.print("  Debe contener al menos una mayuscula, miniscula y numero", style="rojob", highlight=False)
        if entrada != entrada2:
            correcto = False
            c.print("  Las contraseñas no son iguales", style="rojob", highlight=False)
        if correcto:
            break
    return hashedEntrada.decode('utf-8')
