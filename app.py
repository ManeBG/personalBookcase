from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# Inicialización de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'  # Cambia esto por una clave secreta en producción

# Configuración de la base de datos
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Usa tu usuario de MySQL
        password='myLocal.140999',  # Usa tu contraseña de MySQL
        database='biblioteca'  # Nombre de tu base de datos
    )
    return conn

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Clase UserMixin para el login (este es un ejemplo de un modelo básico de usuario)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Cargar usuario desde la base de datos (si existiera una tabla de usuarios)
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(id=user['id'])
    return None

# Ruta principal para mostrar todos los libros
@app.route("/")
@login_required  # Solo los usuarios autenticados pueden ver esta página
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros WHERE user_id = %s", (current_user.id,))
    libros = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", libros=libros)

# Ruta para agregar un libro
@app.route("/agregar", methods=["GET", "POST"])
@login_required
def agregar():
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        genero = request.form["genero"]
        estanteria = request.form["estanteria"]
        anio_publicacion = request.form["anio_publicacion"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO libros (titulo, autor, genero, estanteria, anio_publicacion, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (titulo, autor, genero, estanteria, anio_publicacion, current_user.id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Libro añadido correctamente', 'success')
        return redirect(url_for("index"))

    return render_template("agregar.html")

# Ruta para editar un libro
@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros WHERE id = %s AND user_id = %s", (id, current_user.id))
    libro = cursor.fetchone()

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        genero = request.form["genero"]
        estanteria = request.form["estanteria"]
        anio_publicacion = request.form["anio_publicacion"]

        cursor.execute("""
            UPDATE libros SET titulo = %s, autor = %s, genero = %s, estanteria = %s, anio_publicacion = %s
            WHERE id = %s
        """, (titulo, autor, genero, estanteria, anio_publicacion, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Libro actualizado correctamente', 'success')
        return redirect(url_for("index"))

    cursor.close()
    conn.close()
    return render_template("editar.html", libro=libro)

# Ruta para eliminar un libro
@app.route("/eliminar/<int:id>")
@login_required
def eliminar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libros WHERE id = %s AND user_id = %s", (id, current_user.id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Libro eliminado correctamente', 'success')
    return redirect(url_for("index"))

# Ruta de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # Al verificar la contraseña al hacer login
        is_correct = check_password_hash(hashed_password, password)  # Verifica si la contraseña coincide con el hash

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario registrado correctamente', 'success')
        return redirect(url_for("login"))

    return render_template("register.html")

# Ruta de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            user_obj = User(id=user['id'])
            login_user(user_obj)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for("index"))
        else:
            flash('Credenciales incorrectas, intente de nuevo', 'danger')

    return render_template("login.html")

# Ruta para cerrar sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for("login"))

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
