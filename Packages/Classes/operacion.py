import datetime


class Operacion:
    def __init__(self, fecha, descripcion="", simbolo="", cantidad=0, precio=0, valorTotal=0):
        self.descripcion = descripcion  # String
        self.simbolo = simbolo  # String
        self.cantidad = cantidad  # Int
        self.precio = precio  # Float
        self.valorTotal = valorTotal  # Float
        self.fecha = fecha  # String (Iso format of datetime)
