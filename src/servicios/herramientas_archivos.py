import os
import hashlib
import zipfile
from datetime import datetime
from pathlib import Path


class HerramientasArchivos:
    def __init__(self, ruta_dat="data/contactos.dat", ruta_indice="data/indice.json",
                 ruta_hash="data/contactos.sha256"):
        self.ruta_dat = ruta_dat
        self.ruta_indice = ruta_indice
        self.ruta_hash = ruta_hash

    def calcular_y_guardar_hash(self):
        if not os.path.exists(self.ruta_dat):
            return None

        sha256 = hashlib.sha256()
        with open(self.ruta_dat, "rb") as f:
            while bloque := f.read(4096):
                sha256.update(bloque)

        hash_actual = sha256.hexdigest()

        os.makedirs(os.path.dirname(self.ruta_hash), exist_ok=True)
        with open(self.ruta_hash, "w", encoding="utf-8") as f:
            f.write(hash_actual)

        return hash_actual

    def verificar_integridad(self) -> bool:
        if not os.path.exists(self.ruta_dat) or not os.path.exists(self.ruta_hash):
            return True

        sha256 = hashlib.sha256()
        with open(self.ruta_dat, "rb") as f:
            while bloque := f.read(4096):
                sha256.update(bloque)
        hash_calculado = sha256.hexdigest()

        with open(self.ruta_hash, "r", encoding="utf-8") as f:
            hash_guardado = f.read().strip()

        return hash_calculado == hash_guardado

    def crear_respaldo_zip(self, directorio_respaldos="backups") -> tuple[str, int, int]:
        os.makedirs(directorio_respaldos, exist_ok=True)
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_zip = f"{directorio_respaldos}/respaldo_{fecha}.zip"

        tamano_original = 0
        archivos_a_respaldar = [self.ruta_dat, self.ruta_indice]

        with zipfile.ZipFile(nombre_zip, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for archivo in archivos_a_respaldar:
                if os.path.exists(archivo):
                    tamano_original += os.path.getsize(archivo)
                    zipf.write(archivo, arcname=os.path.basename(archivo))

        tamano_comprimido = os.path.getsize(nombre_zip)
        return nombre_zip, tamano_original, tamano_comprimido

    def recuperar_respaldo_zip(self, ruta_zip: str, directorio_destino="data"):
        if not os.path.exists(ruta_zip):
            raise FileNotFoundError("El archivo ZIP no existe.")

        with zipfile.ZipFile(ruta_zip, "r") as zipf:
            zipf.extractall(directorio_destino)

        self.calcular_y_guardar_hash()

    def obtener_metadatos(self) -> dict:
        ruta = Path(self.ruta_dat)
        if not ruta.exists():
            return {}

        datos_stat = ruta.stat()
        return {
            "nombre": ruta.name,
            "tamano_bytes": datos_stat.st_size,
            "ultima_modificacion": datetime.fromtimestamp(datos_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "lectura": os.access(ruta, os.R_OK),
            "escritura": os.access(ruta, os.W_OK)
        }