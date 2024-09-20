import tkinter as tk
from ventana_inicio import VentanaInicio

def abrir_menu_principal(root):
    from ventana_menu import VentanaMenu
    VentanaMenu(root)

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaInicio(root, abrir_menu_principal)
    root.mainloop()
