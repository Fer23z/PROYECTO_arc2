import json
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from src.repositorios.archivo_fijo import ArchivoFijo


class Exportador:
    def __init__(self, repo_archivos: ArchivoFijo):
        self.repo = repo_archivos

    def exportar_a_json(self, ruta_destino="reports/exportacion_contactos.json"):
        os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
        contactos = self.repo.leer_todos()

        lista_diccionarios = [
            {"id": c.id, "nombre": c.nombre, "telefono": c.telefono, "correo": c.correo, "ciudad": c.ciudad}
            for c in contactos
        ]

        with open(ruta_destino, "w", encoding="utf-8") as f:
            json.dump(lista_diccionarios, f, indent=4)

        return ruta_destino

    def generar_reporte_pdf(self, ruta_json="reports/exportacion_contactos.json",
                            ruta_pdf="reports/reporte_contactos.pdf"):
        if not os.path.exists(ruta_json):
            self.exportar_a_json(ruta_json)

        with open(ruta_json, "r", encoding="utf-8") as f:
            contactos_json = json.load(f)

        pdf = canvas.Canvas(ruta_pdf)
        pdf.drawString(100, 780, f"REPORTE DE CONTACTOS - {datetime.now().strftime('%d/%m/%Y')}")

        y = 740
        for contacto in contactos_json:
            if y < 50:
                pdf.showPage()
                y = 780

            texto = f"ID: {contacto['id']} | Nombre: {contacto['nombre']} | Tel: {contacto['telefono']}"
            pdf.drawString(60, y, texto)

            y -= 20
            texto2 = f"    Correo: {contacto['correo']} | Ciudad: {contacto['ciudad']}"
            pdf.drawString(60, y, texto2)

            y -= 25  # Separación entre registros

        pdf.save()
        return ruta_pdf