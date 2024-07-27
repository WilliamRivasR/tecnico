from tkinter import *
from tkinter import messagebox
import mysql.connector
from tabulate import tabulate

user = 'root'
password = '1234'
host = 'localhost'
database = 'biblioteca_escolar'


def mostrar_empleado():
    employee_id = entrada.get()

    # Confirmar la eliminación
    confirmacion = messagebox.askyesno("Confirmar Eliminación",
                                       f"¿Estás seguro de que deseas eliminar el usuario con ID {employee_id}?")

    if not confirmacion:
        return  # Si el usuario elige "No", no hacer nada

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        cursor = conexion.cursor()

        # Ejecutar la consulta de eliminación
        cursor.execute("CALL BorrarUsuario(%s)", (employee_id,))
        conexion.commit()  # Confirmar los cambios

        # Mostrar mensaje de éxito
        if cursor.rowcount > 0:
            empleado.config(text=f"Usuario con ID {employee_id} eliminado correctamente.")
        else:
            empleado.config(text=f"No se encontró ningún usuario con el ID {employee_id}.")

    except mysql.connector.Error as error:
        print("Error al eliminar el usuario:", error)
        empleado.config(text="Error al eliminar el usuario.")

    finally:
        if 'conexion' in locals() or 'conexion' in globals():
            conexion.close()


ventana = Tk()  # Crear una instancia de la ventana principal
ventana.geometry("1000x400")
ventana.title("Eliminar Usuario")

# Crear etiqueta y campo de entrada
label = Label(ventana, text="Ingrese el documento del usuario que desea eliminar:")
label.pack(pady=10)

entrada = Entry(ventana)
entrada.pack(pady=5)

# Crear botón
button = Button(ventana, text="Eliminar Usuario", command=mostrar_empleado)
button.pack(pady=10)

# Crear etiqueta para mostrar mensajes
empleado = Label(ventana, text="")
empleado.pack(pady=10)

ventana.mainloop()

