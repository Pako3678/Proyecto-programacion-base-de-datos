import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
import stock
# Panel de Invitado - Solo vista de productos
class GuestPanel:
    def __init__(self, master, usuario):
        self.master = master
        self.usuario = usuario
        self.master.configure(bg="#f8f8f8")

        header = tk.Frame(self.master, bg="#9d4edd", height=60)
        header.pack(fill="x")

        tk.Label(
            header, 
            text=f"👁️ MendoTec - Vista de Invitado ({self.usuario})",
            bg="#9d4edd", 
            fg="white", 
            font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=20)

        tk.Button(
            header, 
            text="Cerrar sesión", 
            bg="#7b2cbf", 
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

        self.cargar_datos()

    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        productos = stock.ver_productos()
        for p in productos:
            self.tree.insert("", "end", values=p)

    def cerrar_sesion(self):
        self.master.destroy()
