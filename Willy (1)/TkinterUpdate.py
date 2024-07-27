import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error

# Configuración de la base de datos
user = 'root'
password = '1234'
host = 'localhost'
database = 'biblioteca_escolar'

def actualizar_usuario():
    Numero_documento = entrada_numero_documento.get()  # Obtener el número de documento para identificar el usuario
    Tipo_usuario = combo_tipo_usuario.get()
    Nombre = entrada_nombre.get()
    Apellidos = entrada_apellido.get()
    Fecha_nacimiento = entrada_fecha_nacimiento.get()
    Tipo_documento = combo_tipo_documento.get()
    Correo_electronico = entrada_correo.get()
    Contraseña = entrada_contrasena.get()
    Telefono = entrada_telefono.get()

    try:
        # Establecer conexión con la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()

        # Preparar consulta SQL para llamar al procedimiento almacenado
        update_query = """
            CALL ActualizarUsuario(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Preparar datos para la consulta
        usuario_data = (Numero_documento, Tipo_usuario, Nombre, Apellidos, Tipo_documento, Fecha_nacimiento, Correo_electronico, Contraseña, Telefono)

        # Ejecutar la consulta
        cursor.callproc('ActualizarUsuario', usuario_data)
        conexion.commit()  # Confirmar los cambios

        # Mostrar mensaje de éxito
        mensaje.config(text="Usuario actualizado correctamente!")

    except mysql.connector.Error as error:
        # Manejar errores de la base de datos
        print(f"Error al actualizar usuario: {error}")
        mensaje.config(text=f"Error: {error}")

    finally:
        # Cerrar la conexión a la base de datos
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("1000x600")
ventana.title("Actualizar Usuario")

# Crear el campo de entrada para el número de documento
label_numero_documento = tk.Label(ventana, text="Ingrese el número de documento del usuario a actualizar:")
label_numero_documento.pack()
entrada_numero_documento = tk.Entry(ventana)
entrada_numero_documento.pack()

# Etiqueta y Combobox para el tipo de usuario
label_tipo_usuario = tk.Label(ventana, text="Seleccione el tipo de usuario:")
label_tipo_usuario.pack()
opciones_tipo_usuario = ['estudiante', 'directivo', 'docente', 'publico_general']  # Ajusta según tus necesidades
combo_tipo_usuario = ttk.Combobox(ventana, values=opciones_tipo_usuario, state='readonly')
combo_tipo_usuario.pack()

# Crear el campo de entrada para el nombre
label_nombre = tk.Label(ventana, text="Ingrese el nombre:")
label_nombre.pack()
entrada_nombre = tk.Entry(ventana)
entrada_nombre.pack()

# Crear el campo de entrada para el apellido
label_apellido = tk.Label(ventana, text="Ingrese el/los apellido/s:")
label_apellido.pack()
entrada_apellido = tk.Entry(ventana)
entrada_apellido.pack()

# Crear el campo de entrada para la fecha de nacimiento usando DateEntry
label_fecha_nacimiento = tk.Label(ventana, text="Ingrese la fecha de nacimiento:")
label_fecha_nacimiento.pack()
entrada_fecha_nacimiento = DateEntry(ventana, date_pattern='yyyy-mm-dd')  # Define el patrón de fecha
entrada_fecha_nacimiento.pack()

# Etiqueta y Combobox para el tipo de documento
label_tipo_documento = tk.Label(ventana, text="Seleccione el tipo de documento:")
label_tipo_documento.pack()
opciones_tipo_documento = ['CC', 'CE', 'PA', 'TI', 'PPT', 'PEP']  # Ajusta según tus necesidades
combo_tipo_documento = ttk.Combobox(ventana, values=opciones_tipo_documento, state='readonly')
combo_tipo_documento.pack()

# Crear el campo de entrada para el correo electrónico
label_correo = tk.Label(ventana, text="Ingrese el correo electrónico:")
label_correo.pack()
entrada_correo = tk.Entry(ventana)
entrada_correo.pack()

# Crear el campo de entrada para la contraseña
label_contrasena = tk.Label(ventana, text="Ingrese la contraseña:")
label_contrasena.pack()
entrada_contrasena = tk.Entry(ventana, show='*')
entrada_contrasena.pack()

# Crear el campo de entrada para el teléfono
label_telefono = tk.Label(ventana, text="Ingrese el teléfono:")
label_telefono.pack()
entrada_telefono = tk.Entry(ventana)
entrada_telefono.pack()

mensaje = tk.Label(ventana, text="")
mensaje.pack()

button = tk.Button(ventana, text="Actualizar Usuario", command=actualizar_usuario)
button.pack()

ventana.mainloop()

