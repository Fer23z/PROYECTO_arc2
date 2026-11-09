import json
import os

class GestorIndice:
    def __init__(self, ruta="data/indice.json"):
        self.ruta = ruta
        self.indice = {}
        self.cargar()

    def cargar(self):
        if os.path.exists(self.ruta):
            try:
                with open(self.ruta, "r", encoding="utf-8") as f:
                    self.indice = json.load(f)
            except json.JSONDecodeError:
                self.indice = {}
        else:
            self.indice = {}

    def guardar(self):
        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)
        ruta_tmp = self.ruta + ".tmp"
        with open(ruta_tmp, "w", encoding="utf-8") as f:
            json.dump(self.indice, f, indent=4)
        os.replace(ruta_tmp, self.ruta)

    def registrar_id(self, id_contacto: int, num_registro: int):
        self.indice[str(id_contacto)] = num_registro
        self.guardar()

    def buscar_posicion(self, id_contacto: int) -> int:
        return self.indice.get(str(id_contacto))