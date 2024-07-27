from tkinter import *
from tkinter import ttk
import mysql.connector
from tabulate import tabulate

user = 'root'
password = '1234'
host = 'localhost'
database = 'biblioteca_escolar'

def mostrar_empleado():
    employee_id = entrada.get()

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        cursor = conexion.cursor()

        # Ejecutar una consulta de lectura
        cursor.execute("SELECT * FROM usuarios WHERE ID_usuario = %s", (employee_id,))

        # Obtener los resultados
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de las columnas

        # Limpiar el Treeview
        for row in tree.get_children():
            tree.delete(row)

        if resultados:
            # Insertar los datos en el Treeview
            for row in resultados:
                tree.insert("", "end", values=row)
        else:
            # Mostrar mensaje si no se encuentran resultados
            tree.insert("", "end", values=("No se encontró ningún usuario con ese ID.",))

    except mysql.connector.Error as error:
        print("Error al mostrar el usuario:", error)
        tree.insert("", "end", values=("Error al consultar la base de datos.",))

    finally:
        if 'conexion' in locals() or 'conexion' in globals():
            conexion.close()

ventana = Tk()  # Crear una instancia de la ventana principal
ventana.geometry("1000x600")
ventana.title("Mostrar un Usuario")

# Crear etiqueta y campo de entrada
label = Label(ventana, text="Ingrese el ID del usuario:")
label.pack(pady=10)

entrada = Entry(ventana)
entrada.pack(pady=5)

# Crear botón
button = Button(ventana, text="Mostrar Usuario", command=mostrar_empleado)
button.pack(pady=10)

# Crear Treeview para mostrar resultados
tree = ttk.Treeview(ventana, columns=("ID", "Tipo_usuario", "Nombre", "Apellidos", "Tipo_documento", "Numero_documento", "Fecha_nacimiento", "Correo_electronico", "Contraseña", "Telefono"), show='headings')

# Definir las cabeceras
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(expand=True, fill=BOTH)

# Agregar barra de desplazamiento
scrollbar = Scrollbar(ventana, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.config(yscrollcommand=scrollbar.set)

ventana.mainloop()

