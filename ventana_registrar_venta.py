import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
import customtkinter
import os
from ventana_recibo import VentanaRecibo

#icono imagen
file_patch = os.path.dirname(os.path.realpath(__file__))
image_1 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/agregar.png"), size=(40, 40))
image_2 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/pagar.png"), size=(40, 40))
image_3 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/exit.png"), size=(40, 40))

class VentanaRegistrarVenta:
    def __init__(self, root):
        self.root = root
        self.root.title("Registrar Venta")

        # Variables para almacenar los productos de la venta
        self.lista_productos = []

        # Frame principal
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # Configurar el grid para centrar los elementos
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Marco para campos de entrada
        self.marco_entrada = tk.Frame(self.frame)
        self.marco_entrada.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Etiquetas y campos de entrada centrados
        tk.Label(self.marco_entrada, text="Empleado:", font=('Arial', 12,"bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.empleado_combobox = ttk.Combobox(self.marco_entrada,state='readonly')
        self.empleado_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.marco_entrada, text="Cliente:", font=('Arial', 12,"bold")).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.cliente_combobox = ttk.Combobox(self.marco_entrada, width=30, state='readonly')
        self.cliente_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.marco_entrada, text="Producto:", font=('Arial', 12,"bold")).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.producto_combobox = ttk.Combobox(self.marco_entrada, width=30, state='readonly')
        self.producto_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.producto_combobox.bind("<<ComboboxSelected>>", self.cargar_precio_unitario)

        tk.Label(self.marco_entrada, text="Cantidad:", font=('Arial', 12,"bold")).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.cantidad_entry = customtkinter.CTkEntry(self.marco_entrada, font=('Arial', 14,"bold"))
        self.cantidad_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.marco_entrada, text="Precio:", font=('Arial', 12,"bold")).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.precio_entry =customtkinter.CTkEntry(self.marco_entrada,font=('Arial', 14,"bold"))
        self.precio_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Botones en una misma fila, centrados horizontalmente
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.grid(row=1, column=0, padx=10, pady=10)

        Registrar_btn = customtkinter.CTkButton(master=self.button_frame, 
            image=image_1, text="Agregar producto", command=self.agregar_producto,
            corner_radius=20, width=10, font=("Arial", 18,"bold"), border_spacing=10, fg_color="blue", hover_color="grey",text_color="black"
        )
        Registrar_btn.grid(row=2, column=0, padx=10, pady=20, sticky="ew")

        Registrar_btn = customtkinter.CTkButton(master=self.button_frame, 
            image=image_2, text="Registrar Venta", command=self.registrar_venta,
            corner_radius=20, width=10, font=("Arial", 18,"bold"), border_spacing=10, fg_color="orange", hover_color="grey",text_color="black"
        )
        Registrar_btn.grid(row=2, column=1, padx=10, pady=20, sticky="ew")

        Registrar_btn = customtkinter.CTkButton(master=self.button_frame, 
            image=image_3, text="Salir", command=self.salir,
            corner_radius=20, width=10, font=("Arial", 18,"bold"), border_spacing=10, fg_color="red", hover_color="grey",text_color="black"
        )
        Registrar_btn.grid(row=2, column=2, padx=10, pady=20, sticky="ew")
        
        # Tabla de ventas centrada
        self.ventas_tree = ttk.Treeview(self.frame, columns=("ID", "Empleado", "Cliente", "Producto", "Cantidad", "Precio", "Total"), show='headings', height=10)
        self.ventas_tree.grid(row=2, column=0, padx=10, pady=10)

        self.ventas_tree.heading("ID", text="ID")
        self.ventas_tree.heading("Empleado", text="Empleado")
        self.ventas_tree.heading("Cliente", text="Cliente")
        self.ventas_tree.heading("Producto", text="Producto")
        self.ventas_tree.heading("Cantidad", text="Cantidad")
        self.ventas_tree.heading("Precio", text="Precio")
        self.ventas_tree.heading("Total", text="Total")

        # Ajustar el ancho de las columnas de la tabla de ventas
        self.ventas_tree.column("ID", width=50, anchor=tk.CENTER)
        self.ventas_tree.column("Empleado", width=150, anchor=tk.CENTER)
        self.ventas_tree.column("Cliente", width=150, anchor=tk.CENTER)
        self.ventas_tree.column("Producto", width=200, anchor=tk.CENTER)
        self.ventas_tree.column("Cantidad", width=80, anchor=tk.CENTER)
        self.ventas_tree.column("Precio", width=100, anchor=tk.CENTER)
        self.ventas_tree.column("Total", width=100, anchor=tk.CENTER)

        # Inicializar datos
        self.cargar_comboboxes()
        self.cargar_ventas()

    def cargar_precio_unitario(self, event=None):
        producto = self.producto_combobox.get()

        if producto:
            try:
                conn = sqlite3.connect('cafeteria.db')
                cursor = conn.cursor()

                cursor.execute("SELECT precio FROM productos WHERE nombre_producto = ?", (producto,))
                precio = cursor.fetchone()

                if precio:
                    self.precio_entry.delete(0, tk.END)
                    self.precio_entry.insert(0, precio[0])

            except Exception as e:
                messagebox.showerror("Error", f"Error al obtener precio: {e}")

            finally:
                conn.close()

    def agregar_producto(self):
        producto = self.producto_combobox.get()
        cantidad = self.cantidad_entry.get()
        precio = self.precio_entry.get()

        # Validar campos obligatorios
        if not (producto and cantidad and precio):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Validar cantidad como número entero positivo
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor que cero")
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return

        # Validar precio como número positivo
        try:
            precio = float(precio)
            if precio <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor que cero")
                return
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido")
            return

        # Agregar producto a la lista de productos
        producto_data = {
            'nombre': producto,
            'cantidad': cantidad,
            'precio': precio,
            'total': cantidad * precio,
        }
        self.lista_productos.append(producto_data)

        # Limpiar campos de entrada
        self.producto_combobox.set('')
        self.cantidad_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)

        # Actualizar la tabla de ventas
        self.actualizar_tabla_ventas()

    def actualizar_tabla_ventas(self):
        # Limpiar la tabla antes de cargar los datos
        for row in self.ventas_tree.get_children():
            self.ventas_tree.delete(row)

        # Cargar los datos en la tabla
        for idx, producto in enumerate(self.lista_productos, start=1):
            self.ventas_tree.insert('', 'end', values=(idx, "", "", producto['nombre'], producto['cantidad'], producto['precio'], producto['total']))

    def registrar_venta(self):
        empleado = self.empleado_combobox.get()
        cliente = self.cliente_combobox.get()

        # Validar campos obligatorios
        if not (empleado and cliente and self.lista_productos):
            messagebox.showerror("Error", "Debe seleccionar empleado, cliente y agregar al menos un producto")
            return

        # Calcular total de la venta
        total_venta = sum(producto['total'] for producto in self.lista_productos)

        try:
            # Conectar a la base de datos y comenzar la transacción
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()

            # Registrar cada producto en la tabla 'ventas' y actualizar stock en 'productos'
            for producto in self.lista_productos:
                id_producto = self.obtener_id_producto(producto['nombre'])

                cursor.execute('''
                    INSERT INTO ventas (id_empleado, id_cliente, id_producto, cantidad, precio_producto, total)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (empleado, cliente, id_producto, producto['cantidad'], producto['precio'], producto['total']))

                # Actualizar stock en la tabla 'productos'
                cursor.execute('''
                    UPDATE productos
                    SET cantidad = cantidad - ?
                    WHERE id = ?
                ''', (producto['cantidad'], id_producto))

            conn.commit()
            messagebox.showinfo("Éxito", "Venta registrada exitosamente")

            # Generar factura PDF
            factura_filename = VentanaRecibo(empleado, cliente, self.lista_productos)
            messagebox.showinfo("Factura Generada", f"Factura generada como {factura_filename}")

            # Limpiar campos y actualizar tabla de ventas
            self.lista_productos = []
            self.actualizar_tabla_ventas()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error al registrar venta: {e}")

        finally:
            conn.close() 

    def cargar_comboboxes(self):
        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()

            # Cargar empleados
            cursor.execute("SELECT nombre || ' ' || apellidos FROM empleados")
            empleados = cursor.fetchall()
            self.empleado_combobox['values'] = [empleado[0] for empleado in empleados]

            # Cargar clientes
            cursor.execute("SELECT nombre || ' ' || apellidos FROM clientes")
            clientes = cursor.fetchall()
            self.cliente_combobox['values'] = [cliente[0] for cliente in clientes]

            # Cargar productos
            cursor.execute("SELECT nombre_producto FROM productos")
            productos = cursor.fetchall()
            self.producto_combobox['values'] = [producto[0] for producto in productos]

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {e}")

        finally:
            conn.close()

    def cargar_ventas(self):
        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ventas.id, empleados.nombre || ' ' || empleados.apellidos AS empleado, clientes.nombre || ' ' || clientes.apellidos AS cliente, productos.nombre_producto AS producto, ventas.cantidad, ventas.precio_producto, ventas.total
                FROM ventas
                JOIN empleados ON ventas.id_empleado = empleados.id
                JOIN clientes ON ventas.id_cliente = clientes.id
                JOIN productos ON ventas.id_producto = productos.id
            ''')
            ventas = cursor.fetchall()

            # Limpiar la tabla antes de cargar los datos
            for row in self.ventas_tree.get_children():
                self.ventas_tree.delete(row)

            # Cargar los datos en la tabla
            for venta in ventas:
                self.ventas_tree.insert('', 'end', values=venta)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ventas: {e}")

        finally:
            conn.close()

    def obtener_id_producto(self, nombre_producto):
        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM productos WHERE nombre_producto = ?", (nombre_producto,))
            result = cursor.fetchone()
            return result[0] if result else -1

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ID del producto: {e}")
            return -1

        finally:
            conn.close()

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaRegistrarVenta(root)
    root.mainloop()
