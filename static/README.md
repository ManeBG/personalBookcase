# Personal Library

Una aplicación web para gestionar y organizar tu colección de libros personales. 

## Características

- **Autenticación de usuarios:** Regístrate e inicia sesión para gestionar tus libros.
- **Gestor de libros:** Agrega, edita y elimina libros de tu biblioteca.
- **Interfaz responsiva:** Diseñada con Bootstrap para un uso fácil en cualquier dispositivo.
- **Seguridad:** Contraseñas protegidas con hash.
- **Base de datos:** MySQL para el almacenamiento de información.

## Tecnologías utilizadas

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Bootstrap
- **Base de datos:** MySQL
- **Autenticación:** Flask-Login
- **Gestor de formularios:** Flask-WTF




## Instalación

Sigue estos pasos para instalar y ejecutar la aplicación en tu máquina local.

### Requisitos previos

- Python 3.9 o superior
- MySQL

### Pasos

1. Clona este repositorio:
   ```bash
   git clone https
   cd personalLibrary

    Crea un entorno virtual e instálalo:

python -m venv venv
source venv/bin/activate # En Windows usa `venv\Scripts\activate`
pip install -r requirements.txt

Configura la base de datos:

    Crea una base de datos llamada biblioteca en MySQL:

    CREATE DATABASE biblioteca;

    Asegúrate de que las credenciales de MySQL en app.py coincidan con tu configuración local.

Ejecuta la aplicación:

    python app.py

    Abre tu navegador y accede a: http://127.0.0.1:5000.

Uso

    Regístrate con un nuevo usuario.
    Inicia sesión para acceder al gestor de libros.
    Agrega, edita o elimina libros según sea necesario.

Estructura del proyecto

/personalLibrary/
    /static/       # Archivos estáticos como CSS e imágenes
    /templates/    # Plantillas HTML
    app.py         # Archivo principal de la aplicación Flask
    requirements.txt # Dependencias del proyecto
    README.md      # Documentación del proyecto

Futuras mejoras

    Integrar API para obtener información de libros automáticamente (como Google Books API).
    Implementar funcionalidades avanzadas como categorías o estado de lectura.
    Mejorar la interfaz con más opciones de personalización.

Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, abre un pull request o crea un issue con tus ideas.
Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.