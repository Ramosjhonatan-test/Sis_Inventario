import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import customtkinter
import os

customtkinter.set_appearance_mode("Light")  # O "Light" o "Dark" según prefieras
customtkinter.set_default_color_theme("green")  # Puedes cambiar "blue" por otros colores disponibles

file_patch = os.path.dirname(os.path.realpath(__file__))
image_1 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/acep.png"), size=(30, 30))
image_2 = customtkinter.CTkImage(Image.open(file_patch + "/iconos/reg.png"), size=(30, 30))

class VentanaRegistrarEmpleado:
    def __init__(self, root):
        self.root = root
        self.toplevel = tk.Toplevel(self.root)
        self.toplevel.title("Registrar Empleado")
        self.toplevel.geometry("850x650")

        # Marco para la parte superior (campos de entrada y botones)
        self.marco_superior = tk.Frame(self.toplevel, bd=4, relief=tk.SOLID)
        self.marco_superior.pack(fill=tk.BOTH, padx=10, pady=10)

        # Títulos y campos de entrada
        tk.Label(self.marco_superior, text="Nombre:", font=('Arial', 12,"bold")).grid(row=0, column=4, padx=10, pady=10, sticky="e")
        self.nombre_entry = customtkinter.CTkEntry(self.marco_superior, font=('Courier New', 14,"bold"))
        self.nombre_entry.grid(row=0, column=5, padx=10, pady=10)

        tk.Label(self.marco_superior, text="Apellidos:", font=('Arial', 12,"bold")).grid(row=1, column=4, padx=10, pady=10, sticky="e")
        self.apellidos_entry = customtkinter.CTkEntry(self.marco_superior, font=('Courier New', 14,"bold"))
        self.apellidos_entry.grid(row=1, column=5, padx=10, pady=10)

        tk.Label(self.marco_superior, text="Teléfono:", font=('Arial', 12,"bold")).grid(row=2, column=4, padx=10, pady=10, sticky="e")
        self.telefono_entry = customtkinter.CTkEntry(self.marco_superior, font=('Courier New', 14,"bold"))
        self.telefono_entry.grid(row=2, column=5, padx=10, pady=10)

        tk.Label(self.marco_superior, text="Correo:", font=('Arial', 12,"bold")).grid(row=3, column=4, padx=10, pady=10, sticky="e")
        self.correo_entry = customtkinter.CTkEntry(self.marco_superior, font=('Courier New', 14,"bold"))
        self.correo_entry.grid(row=3, column=5, padx=10, pady=10)

        tk.Label(self.marco_superior, text="Puesto:", font=('Arial', 12,"bold")).grid(row=4, column=4, padx=10, pady=10, sticky="e")
        self.puesto_entry = customtkinter.CTkEntry(self.marco_superior, font=('Courier New', 14,"bold"))
        self.puesto_entry.grid(row=4, column=5, padx=10, pady=10)

        tk.Label(self.marco_superior, text="Salario:", font=('Arial', 12,"bold")).grid(row=5, column=4, padx=10, pady=10, sticky="e")
        self.salario_entry = customtkinter.CTkEntry(self.marco_superior, font=('Courier New', 14,"bold"))
        self.salario_entry.grid(row=5, column=5, padx=10, pady=10)

        # Botones
        self.marco_botones = tk.Frame(self.toplevel)
        self.marco_botones.pack(pady=10)

        Registrar_btn = customtkinter.CTkButton(master=self.marco_botones, 
            image=image_2, text="Registrar", command=self.registrar_empleado,
            corner_radius=20, width=10, font=("Courier New", 16,"bold"), border_spacing=10, fg_color="brown", hover_color="grey",text_color="black"
        )
        Registrar_btn.grid(row=2, column=0, padx=10, pady=20, sticky="ew")

        Modificar_btn = customtkinter.CTkButton(master=self.marco_botones, 
            image=image_1, text="Modificar", command=self.modificar_empleado,
            corner_radius=20, width=10, font=("Courier New", 16,"bold"), border_spacing=10, fg_color="violet", hover_color="grey",text_color="black"
        )
        Modificar_btn.grid(row=2, column=1, padx=10, pady=20, sticky="ew")

        Eliminar_btn = customtkinter.CTkButton(master=self.marco_botones, 
            image=image_2, text="Eliminar", command=self.eliminar_empleado,
            corner_radius=20, width=10, font=("Courier New", 16,"bold"), border_spacing=10, fg_color="orange", hover_color="grey",text_color="black" 
        )
        Eliminar_btn.grid(row=2, column=2, padx=10, pady=20, sticky="ew")

        Salir_btn = customtkinter.CTkButton(master=self.marco_botones, 
            image=image_1, text="Salir", command=self.cerrar_ventana,
            corner_radius=20, width=10, font=("Courier New", 16,"bold"), border_spacing=10, fg_color="red", hover_color="grey",text_color="black"
        )
        Salir_btn.grid(row=2, column=3, padx=10, pady=20, sticky="ew")

        # Marco para la parte inferior (tabla)
        self.marco_inferior = tk.Frame(self.toplevel, bd=4, relief=tk.SOLID)
        self.marco_inferior.pack(fill=tk.BOTH,padx=10, pady=10)

        # Crear tabla para mostrar empleados
        self.empleados_tree = ttk.Treeview(self.marco_inferior, columns=("ID", "Nombre", "Apellidos", "Teléfono", "Correo", "Puesto", "Salario"), show='headings', height=15)
        self.empleados_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.empleados_tree.heading("Nombre", text="Nombre", anchor=tk.CENTER)
        self.empleados_tree.heading("Apellidos", text="Apellidos", anchor=tk.CENTER)
        self.empleados_tree.heading("Teléfono", text="Teléfono", anchor=tk.CENTER)
        self.empleados_tree.heading("Correo", text="Correo", anchor=tk.CENTER)
        self.empleados_tree.heading("Puesto", text="Puesto", anchor=tk.CENTER)
        self.empleados_tree.heading("Salario", text="Salario", anchor=tk.CENTER)

        # Ajustar el ancho de las columnas
        self.empleados_tree.column("ID", width=50, anchor=tk.CENTER)
        self.empleados_tree.column("Nombre", width=150, anchor=tk.CENTER)
        self.empleados_tree.column("Apellidos", width=150, anchor=tk.CENTER)
        self.empleados_tree.column("Teléfono", width=100, anchor=tk.CENTER)
        self.empleados_tree.column("Correo", width=150, anchor=tk.CENTER)
        self.empleados_tree.column("Puesto", width=100, anchor=tk.CENTER)
        self.empleados_tree.column("Salario", width=100, anchor=tk.CENTER)

        # Alinear contenido al centro en todas las columnas
        for col in ("ID", "Nombre", "Apellidos", "Teléfono", "Correo", "Puesto", "Salario"):
            self.empleados_tree.column(col, anchor=tk.CENTER)

        # Configurar scrollbar para la tabla
        scrollbar = ttk.Scrollbar(self.marco_inferior, orient=tk.VERTICAL, command=self.empleados_tree.yview)
        self.empleados_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.empleados_tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Configurar evento de selección en la tabla
        self.empleados_tree.bind("<ButtonRelease-1>", self.cargar_datos_seleccionados)

        # Obtener y mostrar empleados al iniciar
        self.cargar_empleados()

    def cargar_empleados(self):
        # Limpiar la tabla antes de cargar nuevos datos
        registros = self.empleados_tree.get_children()
        for registro in registros:
            self.empleados_tree.delete(registro)

        # Conectar a la base de datos y obtener empleados
        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM empleados")
            empleados = cursor.fetchall()
            conn.close()

            # Insertar empleados en la tabla
            for empleado in empleados:
                self.empleados_tree.insert("", "end", values=empleado)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleados: {e}")

    def cargar_datos_seleccionados(self, event):
        # Limpiar campos de entrada
        self.limpiar_campos()

        # Obtener el item seleccionado en la tabla
        seleccionado = self.empleados_tree.focus()
        valores = self.empleados_tree.item(seleccionado, "values")

        # Si hay un item seleccionado, cargar los datos en los campos de entrada
        if valores:
            self.id_empleado = valores[0]
            self.nombre_entry.insert(0, valores[1])
            self.apellidos_entry.insert(0, valores[2])
            self.telefono_entry.insert(0, valores[3])
            self.correo_entry.insert(0, valores[4])
            self.puesto_entry.insert(0, valores[5])
            self.salario_entry.insert(0, valores[6])

    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.apellidos_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)
        self.correo_entry.delete(0, tk.END)
        self.puesto_entry.delete(0, tk.END)
        self.salario_entry.delete(0, tk.END)

    def registrar_empleado(self):
        nombre = self.nombre_entry.get()
        apellidos = self.apellidos_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        puesto = self.puesto_entry.get()
        salario = self.salario_entry.get()

        if not nombre or not apellidos or not telefono or not correo or not puesto or not salario:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO empleados (nombre, apellidos, telefono, correo, puesto, salario) VALUES (?, ?, ?, ?, ?, ?)", 
                           (nombre, apellidos, telefono, correo, puesto, salario))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Empleado registrado exitosamente.")
            self.cargar_empleados()
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar empleado: {e}")

    def modificar_empleado(self):
        try:
            nombre = self.nombre_entry.get()
            apellidos = self.apellidos_entry.get()
            telefono = self.telefono_entry.get()
            correo = self.correo_entry.get()
            puesto = self.puesto_entry.get()
            salario = self.salario_entry.get()

            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute("""UPDATE empleados SET nombre = ?, apellidos = ?, telefono = ?, correo = ?, puesto = ?, salario = ?
                              WHERE id = ?""", (nombre, apellidos, telefono, correo, puesto, salario, self.id_empleado))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Empleado modificado exitosamente.")
            self.cargar_empleados()
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar empleado: {e}")

    def eliminar_empleado(self):
        try:
            conn = sqlite3.connect('cafeteria.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM empleados WHERE id = ?", (self.id_empleado,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Empleado eliminado exitosamente.")
            self.cargar_empleados()
            self.limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar empleado: {e}")

    def cerrar_ventana(self):
        self.toplevel.destroy()

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaRegistrarEmpleado(root)
    root.mainloop()
