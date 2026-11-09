import os
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox


RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

os.chdir(RAIZ_PROYECTO)

from src.repositorios.archivo_fijo import ArchivoFijo
from src.repositorios.gestor_indice import GestorIndice
from src.servicios.exportador import Exportador
from src.servicios.herramientas_archivos import HerramientasArchivos
from src.ui.ventana_principal import VentanaPrincipal


def main():
    herramientas = HerramientasArchivos()
    repo_contactos = ArchivoFijo()
    repo_indice = GestorIndice()
    exportador = Exportador(repo_contactos)

    ctk.set_appearance_mode("System")

    app = VentanaPrincipal(repo_contactos, repo_indice, exportador, herramientas)

    if not herramientas.verificar_integridad():
        app.withdraw()

        messagebox.showwarning(
            "Advertencia de Integridad",
            "El archivo de contactos fue alterado manualmente o fuera de la aplicación.\nEl hash SHA-256 no coincide."
        )

        app.deiconify()

    app.mainloop()


if __name__ == "__main__":
    main()