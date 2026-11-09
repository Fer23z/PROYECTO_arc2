import struct

FORMATO = "<i50s15s40s30s"
TAMANIO = struct.calcsize(FORMATO)


class Contacto:
    def __init__(self, id_contacto: int, nombre: str, telefono: str, correo: str, ciudad: str):
        self.id = id_contacto
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.ciudad = ciudad

    def empaquetar(self) -> bytes:
        return struct.pack(
            FORMATO,
            self.id,
            self.nombre.encode("utf-8").ljust(50, b"\x00")[:50],
            self.telefono.encode("utf-8").ljust(15, b"\x00")[:15],
            self.correo.encode("utf-8").ljust(40, b"\x00")[:40],
            self.ciudad.encode("utf-8").ljust(30, b"\x00")[:30]
        )

    @staticmethod
    def desempaquetar(datos: bytes):
        if not datos or len(datos) != TAMANIO:
            return None

        id_c, nom_b, tel_b, cor_b, ciu_b = struct.unpack(FORMATO, datos)

        return Contacto(
            id_c,
            nom_b.rstrip(b"\x00").decode("utf-8", errors="ignore"),
            tel_b.rstrip(b"\x00").decode("utf-8", errors="ignore"),
            cor_b.rstrip(b"\x00").decode("utf-8", errors="ignore"),
            ciu_b.rstrip(b"\x00").decode("utf-8", errors="ignore")
        )