import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ventana_registrar_producto import VentanaRegistrarProducto
from ventana_registrar_empleado import VentanaRegistrarEmpleado
from ventana_registrar_cliente import VentanaRegistrarCliente
from ventana_registrar_venta import VentanaRegistrarVenta
from ventana_reportes import VentanaReportes
from ventana_inicio import VentanaInicio

class VentanaMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafetería - Menú Principal")
        self.root.geometry("750x499")

        # Cargar la imagen de fondo
        self.fondo_image = Image.open("./fondos/M_FONDO.png")
        self.fondo_photo = ImageTk.PhotoImage(self.fondo_image)

        # Crear un canvas para poner la imagen de fondo
        self.canvas = tk.Canvas(self.root, width=self.fondo_photo.width(), height=self.fondo_photo.height())
        self.canvas.pack(fill="both", expand=True)

        # Añadir la imagen al canvas
        self.canvas.create_image(0, 0, image=self.fondo_photo, anchor="nw")

        # Crear la barra de menús
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú de Productos
        productos_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Productos", menu=productos_menu)
        productos_menu.add_command(label="Registrar Producto", command=self.abrir_productos)

        # Menú de Empleados
        empleados_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Empleados", menu=empleados_menu)
        empleados_menu.add_command(label="Registrar Empleado", command=self.abrir_empleados)

        # Menú de Clientes
        clientes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Clientes", menu=clientes_menu)
        clientes_menu.add_command(label="Registrar Cliente", command=self.abrir_clientes)

        # Menú de Ventas
        ventas_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ventas", menu=ventas_menu)
        ventas_menu.add_command(label="Registrar Venta", command=self.abrir_ventas)

        # Menú de Reportes
        reportes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reportes", menu=reportes_menu)
        reportes_menu.add_command(label="Generar Reportes", command=self.abrir_reportes)

        # Menú Ayuda
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        ayuda_menu.add_command(label="Acerca de coffe Software", command=self.mostrar_acerca_de)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)

        #Menu de salir
        salir_menu = tk.Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Salir",menu=salir_menu)
        salir_menu.add_command(label="Salir del programa",command=self.salir_programa)
        
    def abrir_productos(self):
        VentanaRegistrarProducto(self.root)

    def abrir_empleados(self):
        VentanaRegistrarEmpleado(self.root)

    def abrir_clientes(self):
        VentanaRegistrarCliente(self.root)

    def abrir_ventas(self):
        ventana_venta = tk.Toplevel(self.root)
        app = VentanaRegistrarVenta(ventana_venta)
        
    def abrir_reportes(self):
        ventana_venta = tk.Toplevel(self.root)
        app = VentanaReportes(ventana_venta)
    
    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de coffe Software", "Coffe Software - sistema cafeteria\nVersión 1.0\nDesarrollado por jhon-coffe\nhttps://wa.me/qr/64D3KOU4Q5UPN1")
        
    def salir_programa(self):
        self.root.quit()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaMenu(root)
    root.mainloop()
