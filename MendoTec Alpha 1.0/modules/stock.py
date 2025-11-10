# stock.py
import sqlite3
import os
import time

# DB_PATH: intenta resolver database.db en el directorio padre del módulo, soluciona error de "not modules found".
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database.db"))

def conectar_db():
    return sqlite3.connect(DB_PATH)
#Crea las tablas si no existen
def inicializar_tablas():
    """Crear tablas si no existen."""
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            marca TEXT,
            modelo TEXT,
            precio REAL,
            stock INTEGER,
            estado TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS acciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            accion TEXT,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

# Llamada a init al importar para asegurar tablas
inicializar_tablas()
# Funciones CRUD para productos
def agregar_producto(nombre, marca, modelo, precio, stock_cant, estado):
    """Agregar producto con los campos especificados. Devuelve True/False."""
    try:
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO productos (nombre, marca, modelo, precio, stock, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, marca, modelo, float(precio), int(stock_cant), estado))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️ Error al agregar producto: {e}")
        return False

def modificar_producto(id_producto, nuevo_precio=None, nuevo_stock=None):
    """Modificar precio y/o stock de un producto por su id."""
    try:
        conn = conectar_db()
        cur = conn.cursor()
        updates = []
        params = []
        if nuevo_precio is not None:
            updates.append("precio = ?")
            params.append(float(nuevo_precio))
        if nuevo_stock is not None:
            updates.append("stock = ?")
            params.append(int(nuevo_stock))
        if not updates:
            conn.close()
            return False
        params.append(id_producto)
        sql = f"UPDATE productos SET {', '.join(updates)} WHERE id = ?"
        cur.execute(sql, params)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️ Error al modificar producto: {e}")
        return False

def eliminar_producto(id_producto):
    """Eliminar producto por id."""
    try:
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️ Error al eliminar producto: {e}")
        return False

def ver_productos():
    """Devuelve lista de tuplas: (id, nombre, marca, modelo, precio, stock, estado)."""
    try:
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, marca, modelo, precio, stock, estado FROM productos ORDER BY id")
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"⚠️ Error al obtener productos: {e}")
        return []
# Funciones de control de acciones
def registrar_accion(usuario, accion):
    """Registra en tabla acciones (auditoría)."""
    try:
        conn = conectar_db()
        cur = conn.cursor()
        fecha = time.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO acciones (usuario, accion, fecha) VALUES (?, ?, ?)", (usuario, accion, fecha))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️ Error al registrar acción: {e}")
        return False

def ver_acciones():
    """Devuelve lista de acciones: (id, usuario, accion, fecha)."""
    try:
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute("SELECT id, usuario, accion, fecha FROM acciones ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"⚠️ Error al obtener acciones: {e}")
        return []
