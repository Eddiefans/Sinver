from Packages.Classes.accion import Accion
from Packages.Classes.utilidad import Utilidad



class Usuario:
    def __init__(self, nombreUsuario="", nombreCompleto="", edad=0, genero='', correo="", contrasena="", valorCuentaActual = 100000, cambioTotal = 0, poderAdquisitivo = 0, utilidadCompra = Utilidad("compra"), utilidadCorto = Utilidad("corto"), accionesCompra = [], accionesCorto = [], historial = []):

        # Limitacines

        # nmbreUsuario:   2 - 20 caracteres, no puede existir otro igual
        # nombreCompleto: Alfabetico 10 - 50 caracteres
        # edad:           18 - 100 años
        # genero:         Masculino: M, Femenino: F, Otro: O
        # correo:         No contener espacio, acentos, ()<>,;:[]ç%&, contener @ una vez, maximo 64 caracteres antes de
        #                 @, maximo 255 caracteres despues de @, no puede existir otro igual
        # contrasena:     8 - 30 caracteres, contener mayusculas, minisculas y numeros

        self.nombreUsuario = nombreUsuario  # String
        self.nombreCompleto = nombreCompleto  # String
        self.edad = edad  # Int
        self.genero = genero  # Char
        self.correo = correo  # String
        self.contrasena = contrasena  # String

        self.valorCuentaActual = valorCuentaActual  # Float
        self.cambioTotal = cambioTotal  # Float
        self.poderAdquisitivo = poderAdquisitivo  # Float
        self.utilidadCompra = utilidadCompra  # Object utilidad
        self.utilidadCorto = utilidadCorto  # Object utilidad
        self.accionesCompra = accionesCompra  # List( Object accion )
        self.accionesCorto = accionesCorto  # List( Object accion )
        self.historial = historial  # List( Object operacion )
