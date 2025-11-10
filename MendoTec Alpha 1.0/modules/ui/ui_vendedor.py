import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import stock

class VendedorPanel:
    def __init__(self, master, usuario):
        self.master = master
        self.usuario = usuario
        self.master.configure(bg="#f8f8f8")

        header = tk.Frame(self.master, bg="#5a189a", height=60)
        header.pack(fill="x")

        tk.Label(
            header, 
            text=f"🧾 MendoTec - Panel del Vendedor ({self.usuario})",
            bg="#5a189a", 
            fg="white", 
            font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=20)

        tk.Button(
            header, 
            text="Cerrar sesión", 
            bg="#9d4edd", 
            fg="white",
            font=("Segoe UI", 10, "bold"), 
            relief="flat",
            command=self.cerrar_sesion
        ).pack(side="right", padx=20, pady=10)

        container = tk.Frame(self.master, bg="#f8f8f8", padx=15, pady=15)
        container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            container,
            columns=("id", "nombre", "marca", "modelo", "precio", "stock", "estado"),
            show="headings", height=18
        )
        for col, title in zip(self.tree["columns"], 
            ["ID", "Nombre", "Marca", "Modelo", "Precio", "Stock", "Estado"]):
            self.tree.heading(col, text=title)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True)

        # Botonera
        btn_frame = tk.Frame(container, bg="#f8f8f8")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Actualizar stock", bg="#7b2cbf", fg="white",
                  width=14, font=("Segoe UI", 10, "bold"), relief="flat",
                  command=self.modificar_stock).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Registrar venta", bg="#5a189a", fg="white",
                  width=14, font=("Segoe UI", 10, "bold"), relief="flat",
                  command=self.registrar_venta).grid(row=0, column=1, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        productos = stock.ver_productos()
        for p in productos:
            self.tree.insert("", "end", values=p)

    def modificar_stock(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto.")
            return
        item = self.tree.item(seleccion)
        id_producto = item["values"][0]
        nuevo_stock = simpledialog.askinteger("Modificar stock", "Nuevo stock:")
        if nuevo_stock is None:
            return
        stock.modificar_producto(id_producto, None, nuevo_stock)
        stock.registrar_accion(self.usuario, f"Modificó stock de producto ID {id_producto}")
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Stock actualizado correctamente.")
#Registra una venta y actualiza el stock
    def registrar_venta(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto para vender.")
            return

        item = self.tree.item(seleccion)
        id_producto, nombre, precio, stock_actual = item["values"][0], item["values"][1], item["values"][4], item["values"][5]

        cantidad = simpledialog.askinteger("Venta", f"Ingrese cantidad de '{nombre}' a vender:")
        if cantidad is None or cantidad <= 0:
            return
        if cantidad > stock_actual:
            messagebox.showerror("Error", "Cantidad superior al stock disponible.")
            return

        metodo_pago = simpledialog.askstring("Venta", "Método de pago (efectivo / tarjeta / transferencia):")
        if not metodo_pago:
            return

        nuevo_stock = stock_actual - cantidad
        stock.modificar_producto(id_producto, None, nuevo_stock)
        stock.registrar_accion(self.usuario, f"Vendió {cantidad}x '{nombre}' ({metodo_pago})")
        self.cargar_datos()
        messagebox.showinfo("Venta registrada", f"Venta de {cantidad}x '{nombre}' registrada correctamente.")

    def cerrar_sesion(self):
        self.master.destroy()
