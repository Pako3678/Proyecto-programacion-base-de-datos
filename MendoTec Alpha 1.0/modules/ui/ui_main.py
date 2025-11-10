import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
import modules.auth as auth
from ui.ui_admin import AdminPanel
from ui.ui_vendedor import VendedorPanel
from ui.ui_guest import GuestPanel


class LoginUI:
    def __init__(self, master):
        self.master = master
        self.master.title("MendoTec - Sistema de Inventario y Ventas")
        self.master.geometry("420x400")
        self.master.configure(bg="#ece9f1")
        self.master.resizable(False, False)

        self.logo_label = tk.Label(
            self.master,
            text="📦 MendoTec",
            font=("Segoe UI", 20, "bold"),
            bg="#ece9f1",
            fg="#5a189a"
        )
        self.logo_label.pack(pady=(40, 10))

        tk.Label(self.master, text="Usuario:", bg="#ece9f1", fg="#3b3b3b", font=("Segoe UI", 11)).pack(pady=(10, 0))
        self.username_entry = tk.Entry(self.master, width=30, font=("Segoe UI", 11))
        self.username_entry.pack(pady=5)

        tk.Label(self.master, text="Contraseña:", bg="#ece9f1", fg="#3b3b3b", font=("Segoe UI", 11)).pack(pady=(10, 0))
        self.password_entry = tk.Entry(self.master, show="*", width=30, font=("Segoe UI", 11))
        self.password_entry.pack(pady=5)

        # Boton de inicio de sesión
        self.login_button = tk.Button(
            self.master,
            text="Iniciar sesión",
            bg="#7b2cbf",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            width=18,
            command=self.login
        )
        self.login_button.pack(pady=15)

        # Boton de registro
        self.register_button = tk.Button(
            self.master,
            text="Registrar nuevo usuario",
            bg="#c77dff",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=20,
            command=self.open_register_window
        )
        self.register_button.pack(pady=(0, 20))

        self.master.bind("<Return>", lambda e: self.login())

    # Login 
    def login(self):
        usuario = self.username_entry.get()
        contrasena = self.password_entry.get()

        if not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
            return

        rol = auth.login(usuario, contrasena)
        if rol:
            messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso como {rol}.")
            self.open_dashboard(rol, usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    # Panel principal (segun rol elegido)
    def open_dashboard(self, rol, usuario):
        self.master.withdraw()
        dashboard = tk.Toplevel()
        dashboard.title(f"MendoTec - Panel {rol.capitalize()}")
        dashboard.geometry("1100x650")
        dashboard.configure(bg="#f8f8f8")

        if rol == "admin":
            AdminPanel(dashboard, usuario)
        elif rol == "vendedor":
            VendedorPanel(dashboard, usuario)
        else:
            GuestPanel(dashboard, usuario)

        def volver_login():
            dashboard.destroy()
            self.master.deiconify()

        dashboard.protocol("WM_DELETE_WINDOW", volver_login)

    # Registro de nuevo usuario
    def open_register_window(self):
        reg_win = tk.Toplevel(self.master)
        reg_win.title("Registrar nuevo usuario")
        reg_win.geometry("400x400")
        reg_win.configure(bg="#ece9f1")

        tk.Label(reg_win, text="Nuevo Usuario", bg="#ece9f1", fg="#5a189a", font=("Segoe UI", 16, "bold")).pack(pady=10)

        tk.Label(reg_win, text="Nombre de usuario:", bg="#ece9f1").pack(pady=(10, 0))
        username = tk.Entry(reg_win, width=30)
        username.pack()

        tk.Label(reg_win, text="Contraseña:", bg="#ece9f1").pack(pady=(10, 0))
        password = tk.Entry(reg_win, show="*", width=30)
        password.pack()

        tk.Label(reg_win, text="Confirmar contraseña:", bg="#ece9f1").pack(pady=(10, 0))
        confirm = tk.Entry(reg_win, show="*", width=30)
        confirm.pack()

        tk.Label(reg_win, text="Rol:", bg="#ece9f1").pack(pady=(10, 0))
        rol_var = tk.StringVar()
        rol_box = ttk.Combobox(reg_win, textvariable=rol_var, state="readonly", width=27)
        rol_box["values"] = ["admin", "vendedor", "invitado"]
        rol_box.pack(pady=5)

        def registrar():
            user = username.get()
            pw = password.get()
            conf = confirm.get()
            rol = rol_var.get()

            if not all([user, pw, conf, rol]):
                messagebox.showwarning("Campos vacíos", "Debe completar todos los campos.")
                return
            if pw != conf:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return

            ok, msg = auth.registrar_usuario(user, pw, rol)
            if ok:
                messagebox.showinfo("Éxito", msg)
                reg_win.destroy()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(
            reg_win,
            text="Registrar",
            bg="#7b2cbf",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            command=registrar
        ).pack(pady=20)


# Launcher de MendoTec
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginUI(root)
    root.mainloop()
