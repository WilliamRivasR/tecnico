from tkinter import *
import mysql.connector
from tabulate import tabulate

user = 'root'
password = ''
host = 'localhost'
database = 'biblioteca_escolar'

def insertar_empleado():
    Tipo_usuario = entrada1.get()
    Nombre = entrada2.get()
    Apellidos = entrada3.get()
    Fecha_nacimiento = entrada4.get()
    Tipo_documento = entrada5.get()
    Numero_documento = entrada6.get()
    Correo_electronico = entrada7.get()
    Contraseña = entrada8.get()
    Telefono = entrada9.get()

    try:
        # Establecer conexión con la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()

        # Preparar consulta SQL para insertar usuario
        insert_query = """
                INSERT INTO usuarios (Tipo_usuario, Nombre, Apellidos, Tipo_documento, Numero_documento, Fecha_nacimiento, Correo_electronico, Contraseña, Telefono)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

        # Preparar datos para la consulta
        empleado_data = (
        Tipo_usuario, Nombre, Apellidos, Tipo_documento, Numero_documento, Fecha_nacimiento, Correo_electronico,
        Contraseña, Telefono)

        # Ejecutar la consulta
        cursor.execute(insert_query, empleado_data)
        conexion.commit()  # Confirmar los cambios

        # Mostrar mensaje de éxito
        empleado.config(text="Usuario insertado correctamente!")

    except mysql.connector.Error as error:
        # Manejar errores de la base de datos
        print(f"Error al insertar usuario: {error}")
        empleado.config(text=f"Error: {error}")

    finally:
        # Cerrar la conexión a la base de datos
        if conexion.is_connected():
            conexion.close()



ventana = Tk()  # Crear una instancia de la ventana principal
ventana.geometry("1000x400")
ventana.title("Insertar Usuario")


label = Label(ventana, text="Ingrese el tipo de usuario:")
label.pack()


entrada1 = Entry(ventana)
entrada1.pack()


empleado = Label(ventana, text="")
empleado.pack()




label = Label(ventana, text="Ingrese el nombre:")
label.pack()


entrada2 = Entry(ventana)
entrada2.pack()


empleado = Label(ventana, text="")
empleado.pack()




label = Label(ventana, text="Ingrese el apellido:")
label.pack()


entrada3 = Entry(ventana)
entrada3.pack()


empleado = Label(ventana, text="")
empleado.pack()





label = Label(ventana, text="Ingrese la fecha de nacimiento:")
label.pack()


entrada4 = Entry(ventana)
entrada4.pack()


empleado = Label(ventana, text="")
empleado.pack()





label = Label(ventana, text="Ingrese el tipo de documento:")
label.pack()


entrada5 = Entry(ventana)
entrada5.pack()


empleado = Label(ventana, text="")
empleado.pack()




label = Label(ventana, text="Ingrese el número de documento:")
label.pack()


entrada6 = Entry(ventana)
entrada6.pack()


empleado = Label(ventana, text="")
empleado.pack()



label = Label(ventana, text="Ingrese el correo electronico:")
label.pack()


entrada7 = Entry(ventana)
entrada7.pack()


empleado = Label(ventana, text="")
empleado.pack()



label = Label(ventana, text="Ingrese la contraseña:")
label.pack()


entrada8 = Entry(ventana)
entrada8.pack()


empleado = Label(ventana, text="")
empleado.pack()



label = Label(ventana, text="Ingrese el telefono:")
label.pack()


entrada9 = Entry(ventana)
entrada9.pack()


empleado = Label(ventana, text="")
empleado.pack()





button = Button(ventana, text="Insertar Usuario", command=insertar_empleado)
button.pack()

ventana.mainloop()