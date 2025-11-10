import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../database.db")

def conectar_db():
    return sqlite3.connect(DB_PATH)

def registrar_usuario(username, password, role):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        # Asegura que la tabla exista
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # Verifica si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, f"El usuario '{username}' ya existe."

        # Inserta el nuevo usuario
        cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)",
                       (username, password, role))
        conn.commit()
        conn.close()
        return True, f"Usuario '{username}' registrado correctamente."

    except Exception as e:
        return False, f"Error al registrar usuario: {e}"

def login(username, password):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM usuarios WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        return None
    except Exception as e:
        print(f"⚠️ Error en login: {e}")
        return None
#Borra usuario duplicado en base de datos, de nada chicos
def eliminar_usuario(username):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return True, f"Usuario '{username}' eliminado correctamente."
    except Exception as e:
        return False, f"Error al eliminar usuario: {e}"
