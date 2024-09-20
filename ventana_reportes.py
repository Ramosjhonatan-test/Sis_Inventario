import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
import customtkinter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
#icono imagen
file_patch = os.path.dirname(os.path.realpath(__file__))
image_2 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/impime.png"), size=(40, 40))
image_3 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/exit.png"), size=(40, 40))
class VentanaReportes:
    def __init__(self, root):
        self.root = root
        self.root.title("Generar Reportes en PDF")
        
        # Frame principal
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Marco para seleccionar tipo de reporte
        self.marco_tipo_reporte = tk.LabelFrame(self.frame, text="Seleccionar Tipo de Reporte")
        self.marco_tipo_reporte.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Radio buttons para seleccionar tipo de reporte
        self.tipo_reporte = tk.StringVar()
        self.tipo_reporte.set("productos")  # Valor por defecto

        ttk.Radiobutton(self.marco_tipo_reporte, text="Productos", value="productos", variable=self.tipo_reporte).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.marco_tipo_reporte, text="Clientes", value="clientes", variable=self.tipo_reporte).grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.marco_tipo_reporte, text="Empleados", value="empleados", variable=self.tipo_reporte).grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        # Botones
        self.generar_button = customtkinter.CTkButton(self.frame,image=image_2,text="Generar Reporte PDF", command=self.generar_reporte_pdf
                                                      , font=("Arial", 14,"bold"),text_color="black", hover_color="orange")
        self.generar_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.salir_button = customtkinter.CTkButton(self.frame, image=image_3,text="Salir", command=self.salir
                                                    , fg_color="red", hover_color="orange", font=("Arial", 14,"bold"),text_color="black")
        self.salir_button.pack(side=tk.LEFT, padx=10, pady=10)

    def generar_reporte_pdf(self):
        tipo_reporte = self.tipo_reporte.get()

        if tipo_reporte == "productos":
            self.generar_reporte_productos()
        elif tipo_reporte == "clientes":
            self.generar_reporte_clientes()
        elif tipo_reporte == "empleados":
            self.generar_reporte_empleados()

    def agregar_encabezado(self, c, titulo):
        # Márgenes
        margen_izquierdo = 50
        margen_superior = 750

        # Agregar imagen del logo en la esquina superior derecha
        logo_path = os.path.join(os.path.dirname(__file__), "./logos/logo.png")
        c.drawImage(logo_path, 420, margen_superior - 75, width=100, height=100)

        # Encabezado del reporte
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(300, margen_superior, titulo)

        # Información de la cafetería
        c.setFont("Helvetica", 12)
        c.drawString(margen_izquierdo, margen_superior - 20, "Cafetería R&R")
        c.drawString(margen_izquierdo, margen_superior - 35, "Dirección: La Paz")
        c.drawString(margen_izquierdo, margen_superior - 50, "Teléfono: 591 73225724")

    def agregar_pie_pagina(self, c):
        c.setFont("Helvetica", 10)
        c.drawCentredString(300, 30, "Reporte generado por Cafetería R&R")

    def generar_reporte_productos(self):
        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()

            # Obtener todos los productos
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            # Generar el documento PDF
            filename = os.path.join('reportes', 'reporte_productos.pdf')
            c = canvas.Canvas(filename, pagesize=letter)

            # Encabezado del reporte
            self.agregar_encabezado(c, "REPORTE DE PRODUCTOS")

            # Cabecera de la tabla
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 667, "ID")
            c.drawString(100, 667, "NOMBRE")
            c.drawString(250, 667, "CATEGORIA")
            c.drawString(350, 667, "CANTIDAD")
            c.drawString(450, 667, "PRECIO")

            # Contenido de la tabla
            c.setFont("Helvetica", 12)
            y = 650
            for producto in productos:
                c.drawString(50, y, str(producto[0]))
                c.drawString(100, y, producto[1])
                c.drawString(250, y, producto[2])
                c.drawString(350, y, str(producto[3]))
                c.drawString(450, y, f"Bs {producto[4]:.2f}")
                y -= 20

            # Pie de página
            self.agregar_pie_pagina(c)

            # Guardar el PDF y finalizar
            c.save()

            messagebox.showinfo("Reporte Generado", f"Reporte de Productos generado como '{filename}'")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte de productos: {e}")

        finally:
            conn.close()

    def generar_reporte_clientes(self):
        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()

            # Obtener todos los clientes
            cursor.execute("SELECT * FROM clientes")
            clientes = cursor.fetchall()

            # Generar el documento PDF
            filename = os.path.join('reportes', 'reporte_clientes.pdf')
            c = canvas.Canvas(filename, pagesize=letter)

            # Encabezado del reporte
            self.agregar_encabezado(c, "REPORTE DE CLIENTES")

            # Cabecera de la tabla
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 667, "ID")
            c.drawString(100, 667, "NOMBRE")
            c.drawString(250, 667, "APELLIDO")
            c.drawString(350, 667, "DIRECCION")
            c.drawString(450, 667, "TELEFONO")

            # Contenido de la tabla
            c.setFont("Helvetica", 12)
            y = 650
            for cliente in clientes:
                c.drawString(50, y, str(cliente[0]))
                c.drawString(100, y, cliente[1])
                c.drawString(250, y, cliente[2])
                c.drawString(350, y, cliente[3])
                c.drawString(450, y, cliente[4])
                y -= 20

            # Pie de página
            self.agregar_pie_pagina(c)

            # Guardar el PDF y finalizar
            c.save()

            messagebox.showinfo("Reporte Generado", f"Reporte de Clientes generado como '{filename}'")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte de clientes: {e}")

        finally:
            conn.close()

    def generar_reporte_empleados(self):
        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()

            # Obtener todos los empleados
            cursor.execute("SELECT * FROM empleados")
            empleados = cursor.fetchall()

            # Generar el documento PDF
            filename = os.path.join('reportes', 'reporte_empleados.pdf')
            c = canvas.Canvas(filename, pagesize=letter)

            # Encabezado del reporte
            self.agregar_encabezado(c, "REPORTE DE EMPLEADOS")

            # Cabecera de la tabla
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 667, "ID")
            c.drawString(100, 667, "NOMBRE")
            c.drawString(250, 667, "APELLIDO")
            c.drawString(350, 667, "DIRECCION")
            c.drawString(450, 667, "TELEFONO")

            # Contenido de la tabla
            c.setFont("Helvetica", 12)
            y = 650
            for empleado in empleados:
                c.drawString(50, y, str(empleado[0]))
                c.drawString(100, y, empleado[1])
                c.drawString(250, y, empleado[2])
                c.drawString(350, y, empleado[3])
                c.drawString(450, y, empleado[4])
                y -= 20

            # Pie de página
            self.agregar_pie_pagina(c)

            # Guardar el PDF y finalizar
            c.save()

            messagebox.showinfo("Reporte Generado", f"Reporte de Empleados generado como '{filename}'")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte de empleados: {e}")

        finally:
            conn.close()

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaReportes(root)
    root.mainloop()
