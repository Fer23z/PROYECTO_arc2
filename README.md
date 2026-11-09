# Agenda de Contactos con Acceso Aleatorio

Aplicación de escritorio desarrollada en Python que administra una agenda de contactos utilizando archivos de registros de tamaño fijo. Este proyecto aplica los principios de organización profesional del software, separando el código fuente por capas (Modelos, Repositorios, Servicios y UI).

## Características Principales
* **Manejo de Archivos Binarios:** Lectura y escritura en posiciones de memoria exactas utilizando los métodos `seek()` y `tell()` (Modificación en el lugar).
* **Índice Primario:** Búsquedas optimizadas $O(1)$ mediante un índice en memoria respaldado en JSON.
* **Seguridad:** Verificación de integridad en cada arranque utilizando el algoritmo de encriptación SHA-256.
* **Respaldo y Recuperación:** Compresión del archivo de datos e índice utilizando ZIP.
* **Exportación:** Generación de reportes PDF y exportación completa a formato JSON.

## Estructura del Proyecto
```text
agenda_contactos/
├── src/                    # Código fuente del sistema
│   ├── modelos/            # Entidades y estructuras (struct)
│   ├── repositorios/       # Acceso a datos físicos y JSON
│   ├── servicios/          # Compresión, hash, reportes y utilidades
│   ├── ui/                 # Interfaz gráfica con CustomTkinter
│   └── main.py             # Punto de entrada de la aplicación
├── data/                   # Archivos vivos (.dat, .json, .sha256)
├── backups/                # Respaldos comprimidos (.zip)
├── reports/                # Reportes generados (.pdf, .json)
├── README.md               # Documentación inicial
└── requirements.txt        # Dependencias de Python
```

## Requisitos
* Python 3.10 o superior.
* Instalar las dependencias ejecutando:
  ```bash
  pip install -r requirements.txt
  ```

## Ejecución
Para iniciar el sistema, asegúrate de estar en la carpeta raíz del proyecto y ejecuta:
```bash
python src/main.py
```