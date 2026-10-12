from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql
import os

# ==========================
# CARGAR VARIABLES DE ENTORNO
# ==========================

load_dotenv()

app = Flask(__name__)

CORS(app)

# ==========================
# CONEXION MYSQL
# ==========================

def obtener_conexion():

    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        cursorclass=pymysql.cursors.DictCursor
    )

# ==========================
# INICIO API
# ==========================

@app.route("/")
def inicio():

    return jsonify({
        "mensaje": "API Web Training funcionando"
    })

# ==========================
# PAGINA WEB
# ==========================

@app.route("/web")
def web():

    return render_template("index.html")

# ==========================
# TEST LOGIN
# ==========================

@app.route("/testlogin")
def testlogin():

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM usuario
        WHERE correo=%s
        AND contrasena=%s
    """,
    (
        "jonatanmat75@gmail.com",
        "123456"
    ))

    usuario = cursor.fetchone()

    conexion.close()

    return jsonify(usuario)

# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["POST"])
def login():

    datos = request.json

    print("LOGIN RECIBIDO")
    print(datos)

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_usuario,
            id_empresa,
            id_rol,
            nombres,
            apellidos,
            correo,
            estado
        FROM usuario
        WHERE correo=%s
        AND contrasena=%s
        AND estado=1
    """,
    (
        datos["correo"],
        datos["contrasena"]
    ))

    usuario = cursor.fetchone()

    conexion.close()

    if usuario:

        return jsonify({
            "success": True,
            "usuario": usuario
        })

    return jsonify({
        "success": False,
        "mensaje": "Usuario o contraseña incorrectos"
    }), 401

# ==========================
# LISTAR USUARIOS
# ==========================

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_usuario,
            id_empresa,
            id_rol,
            nombres,
            apellidos,
            documento,
            correo,
            estado
        FROM usuario
    """)

    usuarios = cursor.fetchall()

    conexion.close()

    return jsonify(usuarios)

# ==========================
# BUSCAR USUARIO
# ==========================

@app.route("/usuarios/<int:id_usuario>", methods=["GET"])
def buscar_usuario(id_usuario):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_usuario,
            id_empresa,
            id_rol,
            nombres,
            apellidos,
            documento,
            correo,
            estado
        FROM usuario
        WHERE id_usuario=%s
    """,
    (id_usuario,))

    usuario = cursor.fetchone()

    conexion.close()

    if usuario:
        return jsonify(usuario)

    return jsonify({
        "mensaje": "Usuario no encontrado"
    }), 404

# ==========================
# CREAR USUARIO
# ==========================

@app.route("/usuarios", methods=["POST"])
def crear_usuario():

    datos = request.json

    print("USUARIO RECIBIDO")
    print(datos)

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO usuario
        (
            id_empresa,
            id_rol,
            nombres,
            apellidos,
            documento,
            correo,
            contrasena,
            estado
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        datos["id_empresa"],
        datos["id_rol"],
        datos["nombres"],
        datos["apellidos"],
        datos["documento"],
        datos["correo"],
        datos["contrasena"],
        datos["estado"]
    ))

    conexion.commit()

    nuevo_id = cursor.lastrowid

    conexion.close()

    return jsonify({
        "success": True,
        "mensaje": "Usuario creado correctamente",
        "id_usuario": nuevo_id
    })

# ==========================
# ACTUALIZAR USUARIO
# ==========================

@app.route("/usuarios/<int:id_usuario>", methods=["PUT"])
def actualizar_usuario(id_usuario):

    datos = request.json

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuario
        SET
            nombres=%s,
            apellidos=%s,
            correo=%s,
            estado=%s
        WHERE id_usuario=%s
    """,
    (
        datos["nombres"],
        datos["apellidos"],
        datos["correo"],
        datos["estado"],
        id_usuario
    ))

    conexion.commit()

    conexion.close()

    return jsonify({
        "success": True,
        "mensaje": "Usuario actualizado correctamente"
    })

# ==========================
# ELIMINAR USUARIO
# ==========================

@app.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
def eliminar_usuario(id_usuario):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM usuario WHERE id_usuario=%s",
        (id_usuario,)
    )

    conexion.commit()

    conexion.close()

    return jsonify({
        "success": True,
        "mensaje": "Usuario eliminado correctamente"
    })

# ==========================
# ARRANQUE
# ==========================

if __name__ == "__main__":

    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", 5000)),
        debug=True
    )