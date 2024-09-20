from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time  # Importa la librería time para obtener el timestamp actual
import os

class VentanaRecibo:
    def __init__(self, empleado, cliente, productos):
        self.empleado = empleado
        self.cliente = cliente
        self.productos = productos
        self.generar_factura_pdf()

    def generar_factura_pdf(self):
        # Calcular el total de la venta sumando los totales de todos los productos
        total_venta = sum(producto['total'] for producto in self.productos)

        # Generar un nombre único para el archivo PDF usando timestamp
        timestamp = time.strftime("%Y""-""%m""-""%d""  ""%H"":""%M")
        #filename = f"reportes/venta_factura_{timestamp}.pdf"

        timestamp1 = time.strftime("%M%S")
        filename = f"reporte_venta/Factura{timestamp1}.pdf"

        # Crear el documento PDF
        c = canvas.Canvas(filename, pagesize=letter)

        # Agregar imagen del logo en la esquina superior derecha
        logo_path = os.path.join(os.path.dirname(__file__), "./logos/logo.png")
        c.drawImage(logo_path, 420, 675, width=100, height=100)  # Ajusta las coordenadas y tamaño según sea necesario

        # Títulos y detalles de la factura
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(300, 750, "FACTURA DE LA VENTA")

        # Información de la cafetería (puedes personalizar según tu cafetería)
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, "Nombre: CAFETERIA R&R")
        c.drawString(100, 705, "Dirección: La Paz, Av. cold #21")
        c.drawString(100, 690, "Teléfono: 591 73225724")
        c.drawString(100, 675, "Fecha de venta: ")
        c.drawString(195, 675, timestamp)

        # Detalles de la venta
        c.setFont("Helvetica-Bold", 13)
        c.drawString(100, 655, f"EMPLEADO: {self.empleado}")
        c.drawString(300, 655, f"CLIENTE: {self.cliente}")

        # Encabezado de la tabla
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 630, "PRODUCTO")
        c.drawString(250, 630, "CANTIDAD")
        c.drawString(345, 630, "PRECIO UNITARIO")
        c.drawString(500, 630, "TOTAL")

        # Línea debajo del encabezado de la tabla
        c.line(100, 625, 550, 625)

        # Contenido de la tabla
        c.setFont("Helvetica", 12)
        y = 600
        for producto in self.productos:
            c.drawString(120, y, producto['nombre'])
            c.drawString(265, y, str(producto['cantidad']))
            c.drawString(355, y, f"Bs {producto['precio']:.2f}")
            c.drawString(500, y, f"Bs {producto['total']:.2f}")
            y -= 20

        # Total de la venta
        c.setFont("Helvetica-Bold", 14)
        c.drawString(400, y - 40, "Total Venta:")
        c.drawString(500, y - 40, f"Bs {total_venta:.2f}")

        # Guardar el documento PDF y finalizar
        c.save()

        return filename
