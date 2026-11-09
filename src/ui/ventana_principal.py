import customtkinter as ctk
from tkinter import messagebox, filedialog
from src.modelos.contacto import Contacto


class VentanaPrincipal(ctk.CTk):
    def __init__(self, repo_archivos, repo_indice, exportador, herramientas):
        super().__init__()
        self.repo = repo_archivos
        self.indice = repo_indice
        self.exportador = exportador
        self.herramientas = herramientas

        self.title("Agenda de Contactos - Acceso Aleatorio")
        self.geometry("750x550")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._crear_sidebar()
        self._crear_area_principal()

    def _crear_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(14, weight=1)

        ctk.CTkLabel(self.sidebar, text="Menú Principal", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0,
                                                                                                         column=0,
                                                                                                         padx=20,
                                                                                                         pady=(20, 10))

        # --- Contactos ---
        ctk.CTkLabel(self.sidebar, text="Contactos", font=ctk.CTkFont(size=14, weight="bold")).grid(row=1, column=0,
                                                                                                    padx=20,
                                                                                                    pady=(10, 0),
                                                                                                    sticky="w")
        ctk.CTkButton(self.sidebar, text="Agregar", command=self.agregar_contacto).grid(row=2, column=0, padx=20,
                                                                                        pady=5)
        ctk.CTkButton(self.sidebar, text="Buscar por ID", command=self.buscar_contacto).grid(row=3, column=0, padx=20,
                                                                                             pady=5)
        ctk.CTkButton(self.sidebar, text="Modificar", command=self.modificar_contacto).grid(row=4, column=0, padx=20,
                                                                                            pady=5)

        # --- Exportar ---
        ctk.CTkLabel(self.sidebar, text="Exportar", font=ctk.CTkFont(size=14, weight="bold")).grid(row=5, column=0,
                                                                                                   padx=20,
                                                                                                   pady=(15, 0),
                                                                                                   sticky="w")
        ctk.CTkButton(self.sidebar, text="Exportar a JSON", command=self.exportar_json).grid(row=6, column=0, padx=20,
                                                                                             pady=5)
        ctk.CTkButton(self.sidebar, text="Generar PDF", command=self.generar_pdf).grid(row=7, column=0, padx=20, pady=5)

        # --- Herramientas ---
        ctk.CTkLabel(self.sidebar, text="Herramientas", font=ctk.CTkFont(size=14, weight="bold")).grid(row=8, column=0,
                                                                                                       padx=20,
                                                                                                       pady=(15, 0),
                                                                                                       sticky="w")
        ctk.CTkButton(self.sidebar, text="Verificar Integridad", command=self.verificar_integridad).grid(row=9,
                                                                                                         column=0,
                                                                                                         padx=20,
                                                                                                         pady=5)
        ctk.CTkButton(self.sidebar, text="Crear Respaldo ZIP", command=self.crear_respaldo).grid(row=10, column=0,
                                                                                                 padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="Recuperar Respaldo", command=self.recuperar_respaldo).grid(row=11, column=0,
                                                                                                     padx=20, pady=5)
        ctk.CTkButton(self.sidebar, text="Info del Archivo", command=self.mostrar_metadatos).grid(row=12, column=0,
                                                                                                  padx=20, pady=5)

        # --- Ayuda ---
        ctk.CTkButton(self.sidebar, text="Ayuda", command=self.mostrar_ayuda, fg_color="transparent", border_width=2,
                      text_color=("gray10", "#DCE4EE")).grid(row=13, column=0, padx=20, pady=(20, 20))

    def _crear_area_principal(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.lbl_estado = ctk.CTkLabel(self.main_frame,
                                       text="Sistema de Agenda Activo\n\nUtilice el menú lateral para operar.",
                                       font=ctk.CTkFont(size=18))
        self.lbl_estado.grid(row=0, column=0)

    # --- Lógica de Contactos ---
    def agregar_contacto(self):
        try:
            id_input = ctk.CTkInputDialog(text="ID del contacto (entero):", title="Agregar Contacto").get_input()
            if not id_input: return
            id_c = int(id_input)

            if str(id_c) in self.indice.indice:
                messagebox.showerror("Error", "El ID ya existe en el índice.")
                return

            nombre = ctk.CTkInputDialog(text="Nombre:", title="Agregar Contacto").get_input() or ""
            telefono = ctk.CTkInputDialog(text="Teléfono:", title="Agregar Contacto").get_input() or ""
            correo = ctk.CTkInputDialog(text="Correo:", title="Agregar Contacto").get_input() or ""
            ciudad = ctk.CTkInputDialog(text="Ciudad:", title="Agregar Contacto").get_input() or ""

            nuevo_contacto = Contacto(id_c, nombre, telefono, correo, ciudad)

            num_registro = self.repo.agregar(nuevo_contacto)
            self.indice.registrar_id(id_c, num_registro)
            self.herramientas.calcular_y_guardar_hash()

            messagebox.showinfo("Éxito", f"Contacto guardado en el registro físico #{num_registro}.")
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al agregar: {e}")

    def buscar_contacto(self):
        try:
            id_input = ctk.CTkInputDialog(text="Ingrese el ID a buscar:", title="Buscar").get_input()
            if not id_input: return
            id_c = int(id_input)

            num_registro = self.indice.buscar_posicion(id_c)
            if num_registro is None:
                messagebox.showwarning("No encontrado", "El ID no existe en el índice.")
                return

            contacto = self.repo.leer_registro(num_registro)
            info = f"ID: {contacto.id}\nNombre: {contacto.nombre}\nTel: {contacto.telefono}\nCorreo: {contacto.correo}\nCiudad: {contacto.ciudad}"
            messagebox.showinfo(f"Registro físico #{num_registro}", info)
        except ValueError:
            messagebox.showerror("Error", "ID inválido.")

    def modificar_contacto(self):
        try:
            id_input = ctk.CTkInputDialog(text="Ingrese el ID a modificar:", title="Modificar").get_input()
            if not id_input: return
            id_c = int(id_input)

            num_registro = self.indice.buscar_posicion(id_c)
            if num_registro is None:
                messagebox.showwarning("No encontrado", "El ID no existe.")
                return

            contacto = self.repo.leer_registro(num_registro)
            nuevo_nombre = ctk.CTkInputDialog(text=f"Nuevo nombre (actual: {contacto.nombre}):",
                                              title="Modificar").get_input()

            if nuevo_nombre is not None:
                contacto.nombre = nuevo_nombre
                self.repo.modificar_registro(num_registro, contacto)
                self.herramientas.calcular_y_guardar_hash()
                messagebox.showinfo("Éxito", "Contacto sobrescrito en su posición original con seek().")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- Lógica de Exportación ---
    def exportar_json(self):
        try:
            ruta = self.exportador.exportar_a_json()
            messagebox.showinfo("Exportado", f"Datos exportados a:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generar_pdf(self):
        try:
            ruta = self.exportador.generar_reporte_pdf()
            messagebox.showinfo("PDF Generado", f"Reporte guardado en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --- Lógica de Herramientas ---
    def verificar_integridad(self):
        if self.herramientas.verificar_integridad():
            messagebox.showinfo("Integridad", "El archivo de contactos está intacto (Hash SHA-256 coincide).")
        else:
            messagebox.showwarning("Alerta", "El archivo ha sido modificado fuera de la aplicación.")

    def crear_respaldo(self):
        try:
            ruta, orig, comp = self.herramientas.crear_respaldo_zip()
            messagebox.showinfo("Respaldo ZIP",
                                f"ZIP creado en:\n{ruta}\n\nTamaño original: {orig} bytes\nComprimido: {comp} bytes")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def recuperar_respaldo(self):
        try:
            ruta_zip = filedialog.askopenfilename(
                title="Seleccione el respaldo ZIP",
                initialdir="backups",
                filetypes=[("Archivos ZIP", "*.zip")]
            )

            if not ruta_zip: return

            confirmacion = messagebox.askyesno(
                "Confirmar Recuperación",
                "Esta acción sobrescribirá los datos actuales con los del respaldo.\n¿Desea continuar?"
            )

            if confirmacion:
                self.herramientas.recuperar_respaldo_zip(ruta_zip)
                self.indice.cargar()
                messagebox.showinfo("Éxito", "Respaldo recuperado y cargado en memoria correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo recuperar el respaldo: {e}")

    def mostrar_metadatos(self):
        datos = self.herramientas.obtener_metadatos()
        if not datos:
            messagebox.showinfo("Metadatos", "El archivo de contactos aún no existe.")
            return

        info = (f"Nombre: {datos['nombre']}\n"
                f"Tamaño: {datos['tamano_bytes']} bytes\n"
                f"Modificado: {datos['ultima_modificacion']}\n"
                f"Permiso Lectura: {'Sí' if datos['lectura'] else 'No'}\n"
                f"Permiso Escritura: {'Sí' if datos['escritura'] else 'No'}")
        messagebox.showinfo("Información del Archivo", info)

    def mostrar_ayuda(self):
        messagebox.showinfo("Ayuda", "Agenda de Contactos v1.0\nProyecto de Organización Profesional")