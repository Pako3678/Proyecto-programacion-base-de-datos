import tkinter as tk
from tkinter import messagebox
# Funciones de ayuda para UI
def alerta_info(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)

def alerta_error(titulo, mensaje):
    messagebox.showerror(titulo, mensaje)

def alerta_warning(titulo, mensaje):
    messagebox.showwarning(titulo, mensaje)

def crear_boton(parent, texto, comando, color="#7b2cbf"):
    return tk.Button(
        parent, 
        text=texto, 
        bg=color, 
        fg="white",
        font=("Segoe UI", 10, "bold"), 
        relief="flat",
        command=comando
    )
