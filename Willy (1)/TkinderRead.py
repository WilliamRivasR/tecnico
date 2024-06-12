from tkinter import *
import mysql.connector
from tabulate import tabulate

user = 'root'
password = ''
host = 'localhost'
database = 'biblioteca_escolar'

def mostrar_empleado():
    employee_id = entrada.get()

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            passwd="",
            database=database
        )
        cursor = conexion.cursor()

        # Ejecutar una consulta de lectura
        cursor.execute("SELECT * FROM usuarios WHERE ID_usuario = %s", (employee_id,))

        # Obtener los resultados
        resultados = cursor.fetchall()

        if resultados:
            empleado.config(text=tabulate(resultados))
        else:
            empleado.config(text="No se encontró ningún usuario con ese ID.")

    except mysql.connector.Error as error:
        print("Error al mostrar el usuario:", error)

    finally:
        if 'conexion' in locals() or 'conexion' in globals():
            conexion.close()



ventana = Tk()  # Crear una instancia de la ventana principal
ventana.geometry("1000x400")
ventana.title("Mostrar un usuario")


label = Label(ventana, text="Ingrese el ID del usuario:")
label.pack()


entrada = Entry(ventana)
entrada.pack()


button = Button(ventana, text="Mostrar Usuario", command=mostrar_empleado)
button.pack()


empleado = Label(ventana, text="")
empleado.pack()


ventana.mainloop()
