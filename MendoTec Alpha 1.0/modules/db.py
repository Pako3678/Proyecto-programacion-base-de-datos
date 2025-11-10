# modules/db.py
import sqlite3
from datetime import datetime

DB_NAME = 'database.db'

def conectar_db():
    """Crea una conexión a la base de datos y activa las foreign keys."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def inicializar_tablas():
    """Crea las tablas de usuarios, productos y acciones si no existen."""
    conn = conectar_db()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'vendedor', 'invitado'))
        )
    ''')

    # Tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            precio REAL NOT NULL CHECK(precio >= 0),
            stock INTEGER NOT NULL CHECK(stock >= 0),
            descripcion TEXT,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(marca, modelo)
        )
    ''')

    # Tabla de acciones (auditoría)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS acciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            producto_id INTEGER,
            accion TEXT NOT NULL CHECK(accion IN ('agregar', 'modificar', 'eliminar')),
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            detalles TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL
        )
    ''')

    conn.commit()
    conn.close()

# Función para registrar acciones
def registrar_accion(usuario_id, producto_id, accion, detalles=""):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO acciones (usuario_id, producto_id, accion, detalles)
        VALUES (?, ?, ?, ?)
    ''', (usuario_id, producto_id, accion, detalles))
    conn.commit()
    conn.close()

# Consultas de auditoría
def obtener_acciones_por_usuario(usuario_id, limit=100):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, accion, fecha, detalles, producto_id
        FROM acciones
        WHERE usuario_id = ?
        ORDER BY fecha DESC
        LIMIT ?
    ''', (usuario_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return rows
