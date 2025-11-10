# ui_admin.py
import os, sys
# Ajusta la ruta para que pueda importar stock desde la carpeta padre
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk, messagebox
import stock

class AdminPanel:
    def __init__(self, master, usuario):
        self.master = master
        self.usuario = usuario
        self.master.configure(bg="#f8f8f8")

        header = tk.Frame(self.master, bg="#7b2cbf", height=60)
        header.pack(fill="x")

        tk.Label(header, text="📦 MendoTec - Panel de Administración", bg="#7b2cbf", fg="white",
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=20)

        tk.Button(header, text="Cerrar sesión", bg="#9d4edd", fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  command=self.cerrar_sesion).pack(side="right", padx=20, pady=10)

        container = tk.Frame(self.master, bg="#f8f8f8", padx=15, pady=15)
        container.pack(fill="both", expand=True)

        # Tabla
        self.tree = ttk.Treeview(container,
            columns=("id", "nombre", "marca", "modelo", "precio", "stock", "estado"),
            show="headings", height=18)
        for col, title in zip(self.tree["columns"], ["ID", "Nombre", "Marca", "Modelo", "Precio", "Stock", "Estado"]):
            self.tree.heading(col, text=title)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True)

        # Botonera
        btn_frame = tk.Frame(container, bg="#f8f8f8")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="➕ Agregar", bg="#7b2cbf", fg="white", width=12,
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  command=self.agregar_producto).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="✏️ Modificar", bg="#9d4edd", fg="white", width=12,
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  command=self.modificar_producto).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#c9184a", fg="white", width=12,
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  command=self.eliminar_producto).grid(row=0, column=2, padx=5)

        tk.Button(btn_frame, text="📜 Historial", bg="#5a189a", fg="white", width=12,
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  command=self.ver_historial).grid(row=0, column=3, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        """Carga productos desde stock.ver_productos()"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        productos = stock.ver_productos()
        for p in productos:
            # p ya es una tupla (id, nombre, marca, modelo, precio, stock, estado)
            self.tree.insert("", "end", values=p)
# Agrega un nuevo producto mediante un formulario de pieza modal (un bloque)
    def agregar_producto(self):
        """Formulario modal único para añadir producto"""
        win = tk.Toplevel(self.master)
        win.title("Agregar nuevo producto")
        win.geometry("420x480")
        win.configure(bg="#f8f8f8")
        win.transient(self.master)
        win.grab_set()

        tk.Label(win, text="Agregar nuevo producto", bg="#f8f8f8", fg="#5a189a",
                 font=("Segoe UI", 14, "bold")).pack(pady=10)

        frame = tk.Frame(win, bg="#f8f8f8")
        frame.pack(padx=12, pady=6, fill="x")

        tk.Label(frame, text="Nombre:", bg="#f8f8f8", anchor="w").pack(fill="x")
        e_nombre = tk.Entry(frame); e_nombre.pack(fill="x", pady=4)

        tk.Label(frame, text="Marca:", bg="#f8f8f8", anchor="w").pack(fill="x")
        e_marca = tk.Entry(frame); e_marca.pack(fill="x", pady=4)

        tk.Label(frame, text="Modelo:", bg="#f8f8f8", anchor="w").pack(fill="x")
        e_modelo = tk.Entry(frame); e_modelo.pack(fill="x", pady=4)

        tk.Label(frame, text="Precio:", bg="#f8f8f8", anchor="w").pack(fill="x")
        e_precio = tk.Entry(frame); e_precio.pack(fill="x", pady=4)

        tk.Label(frame, text="Stock:", bg="#f8f8f8", anchor="w").pack(fill="x")
        e_stock = tk.Entry(frame); e_stock.pack(fill="x", pady=4)

        tk.Label(frame, text="Estado (nuevo/usado):", bg="#f8f8f8", anchor="w").pack(fill="x")
        e_estado = tk.Entry(frame); e_estado.pack(fill="x", pady=4)

        def guardar():
            nombre = e_nombre.get().strip()
            marca = e_marca.get().strip()
            modelo = e_modelo.get().strip()
            precio = e_precio.get().strip()
            stock_cant = e_stock.get().strip()
            estado = e_estado.get().strip() or "nuevo"

            if not all([nombre, marca, modelo, precio, stock_cant]):
                messagebox.showwarning("Campos vacíos", "Debe completar todos los campos obligatorios.")
                return

            try:
                precio_f = float(precio)
                stock_i = int(stock_cant)
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores numéricos válidos para precio y stock.")
                return

            ok = stock.agregar_producto(nombre, marca, modelo, precio_f, stock_i, estado)
            if ok:
                stock.registrar_accion(self.usuario, f"Agregó producto '{nombre}'")
                self.cargar_datos()
                win.destroy()
                messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto. Revisa la consola para más detalles.")

        tk.Button(win, text="Guardar", bg="#7b2cbf", fg="white", width=15,
                  font=("Segoe UI", 10, "bold"), relief="flat", command=guardar).pack(pady=14)

    def modificar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto para modificar.")
            return
        item = self.tree.item(seleccion)
        id_producto = item["values"][0]

        # Modal para editar precio y/o stock
        win = tk.Toplevel(self.master)
        win.title("Modificar producto")
        win.geometry("360x260")
        win.configure(bg="#f8f8f8")
        win.transient(self.master)
        win.grab_set()

        tk.Label(win, text="Modificar producto", bg="#f8f8f8", fg="#5a189a",
                 font=("Segoe UI", 13, "bold")).pack(pady=8)

        frame = tk.Frame(win, bg="#f8f8f8"); frame.pack(padx=12, pady=8, fill="x")
        tk.Label(frame, text="Nuevo precio (vacío = sin cambio):", bg="#f8f8f8", anchor="w").pack(fill="x")
        e_precio = tk.Entry(frame); e_precio.pack(fill="x", pady=4)
        tk.Label(frame, text="Nuevo stock (vacío = sin cambio):", bg="#f8f8f8", anchor="w").pack(fill="x")
        e_stock = tk.Entry(frame); e_stock.pack(fill="x", pady=4)

        def guardar_cambios():
            np = e_precio.get().strip()
            ns = e_stock.get().strip()
            np_val = None
            ns_val = None
            if np != "":
                try:
                    np_val = float(np)
                except ValueError:
                    messagebox.showerror("Error", "Precio inválido."); return
            if ns != "":
                try:
                    ns_val = int(ns)
                except ValueError:
                    messagebox.showerror("Error", "Stock inválido."); return
            ok = stock.modificar_producto(id_producto, nuevo_precio=np_val, nuevo_stock=ns_val)
            if ok:
                stock.registrar_accion(self.usuario, f"Modificó producto ID {id_producto}")
                self.cargar_datos()
                win.destroy()
                messagebox.showinfo("Actualizado", "Producto modificado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo modificar el producto.")

        tk.Button(win, text="Guardar cambios", bg="#7b2cbf", fg="white", width=16,
                  font=("Segoe UI", 10, "bold"), relief="flat", command=guardar_cambios).pack(pady=10)

    def eliminar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar.")
            return
        item = self.tree.item(seleccion)
        id_producto = item["values"][0]
        nombre = item["values"][1]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar el producto '{nombre}'?")
        if confirm:
            ok = stock.eliminar_producto(id_producto)
            if ok:
                stock.registrar_accion(self.usuario, f"Eliminó producto '{nombre}'")
                self.cargar_datos()
                messagebox.showinfo("Eliminado", f"Producto '{nombre}' eliminado.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto.")

    def ver_historial(self):
        acciones = stock.ver_acciones()
        if not acciones:
            messagebox.showinfo("Historial vacío", "No hay acciones registradas.")
            return
        top = tk.Toplevel(self.master)
        top.title("Historial de acciones")
        top.geometry("700x420")
        tree_hist = ttk.Treeview(top, columns=("id", "usuario", "accion", "fecha"), show="headings")
        for col, title in zip(tree_hist["columns"], ["ID", "Usuario", "Acción", "Fecha"]):
            tree_hist.heading(col, text=title)
            tree_hist.column(col, anchor="center", width=160)
        tree_hist.pack(fill="both", expand=True)
        for a in acciones:
            tree_hist.insert("", "end", values=a)

    def cerrar_sesion(self):
        self.master.destroy()
