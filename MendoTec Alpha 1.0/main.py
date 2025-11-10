import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ui.ui_main import LoginUI
# Launcher de MendoTec, ejecutar main.py
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginUI(root)
    root.mainloop()
