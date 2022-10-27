import datetime


class Accion:
    def __init__(self, tipo, fecha, simbolo="", cantidad=0, precioInicial=0, valorInicial=0, precioActual=0, valorActual=0, cambioDia=0, cambiopDia=0, cambioTotal=0, cambiopTotal=0):
        self.tipo = tipo  # String (corto o compra)
        self.simbolo = simbolo  # String
        self.cantidad = cantidad  # Int
        self.precioInicial = precioInicial  # Float
        self.valorInicial = valorInicial  # Float
        self.precioActual = precioActual  # Float
        self.valorActual = valorActual  # Float
        self.cambioDia = cambioDia  # Float
        self.cambiopDia = cambiopDia  # Float
        self.cambioTotal = cambioTotal  # Float
        self.cambiopTotal = cambiopTotal  # Float
        self.fecha = fecha  # String (Iso format of datetime)

