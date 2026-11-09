import os
from src.modelos.contacto import Contacto, TAMANIO

class ArchivoFijo:
    def __init__(self, ruta="data/contactos.dat"):
        self.ruta = ruta
        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)
        if not os.path.exists(self.ruta):
            with open(self.ruta, "wb") as f:
                pass

    def agregar(self, contacto: Contacto) -> int:
        with open(self.ruta, "ab") as archivo:
            posicion_byte = archivo.tell()
            archivo.write(contacto.empaquetar())
            num_registro = posicion_byte // TAMANIO
            return int(num_registro)

    def leer_registro(self, num_registro: int) -> Contacto:
        with open(self.ruta, "rb") as archivo:
            posicion_byte = num_registro * TAMANIO
            archivo.seek(posicion_byte)
            datos = archivo.read(TAMANIO)
            return Contacto.desempaquetar(datos)

    def modificar_registro(self, num_registro: int, contacto: Contacto):
        with open(self.ruta, "r+b") as archivo:
            posicion_byte = num_registro * TAMANIO
            archivo.seek(posicion_byte)
            archivo.write(contacto.empaquetar())

    def leer_todos(self) -> list[Contacto]:
        contactos = []
        with open(self.ruta, "rb") as archivo:
            while True:
                datos = archivo.read(TAMANIO)
                if not datos:
                    break
                contacto = Contacto.desempaquetar(datos)
                if contacto:
                    contactos.append(contacto)
        return contactos