import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector

# Configuración de la base de datos
user = 'root'
password = '1234'
host = 'localhost'
database = 'biblioteca_escolar'

def insertar_empleado():
    Tipo_usuario = combo_tipo_usuario.get()
    Nombre = entrada_nombre.get()
    Apellidos = entrada_apellido.get()
    Fecha_nacimiento = entrada_fecha_nacimiento.get_date()  # Obtener la fecha seleccionada
    Tipo_documento = combo_tipo_documento.get()
    Numero_documento = entrada_numero_documento.get()
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

        # Preparar consulta SQL para insertar usuario
        insert_query = """
            CALL InsertarUsuario(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        empleado_data = (Tipo_usuario, Nombre, Apellidos, Tipo_documento, Numero_documento, Fecha_nacimiento, Correo_electronico, Contraseña, Telefono)

        # Ejecutar la consulta
        cursor.execute(insert_query, empleado_data)
        conexion.commit()  # Confirmar los cambios

        # Mostrar mensaje de éxito
        mensaje.config(text="Usuario insertado correctamente!")

    except mysql.connector.Error as error:
        # Manejar errores de la base de datos
        mensaje.config(text=f"Error al insertar usuario: {error}")

    finally:
        # Cerrar la conexión a la base de datos
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def mostrar_empleado():
    Numero_documento = entrada_buscar.get()

    try:
        # Establecer conexión con la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()

        # Preparar consulta SQL para mostrar usuario
        select_query = """
            SELECT * FROM usuarios WHERE Numero_documento = %s
        """
        cursor.execute(select_query, (Numero_documento,))

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
            tree.insert("", "end", values=("No se encontró ningún usuario con ese número de documento.",))

    except mysql.connector.Error as error:
        # Manejar errores de la base de datos
        tree.insert("", "end", values=("Error al consultar la base de datos.",))

    finally:
        # Cerrar la conexión a la base de datos
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def mostrar_todos_usuarios():
    try:
        # Establecer conexión con la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()

        # Preparar consulta SQL para mostrar todos los usuarios
        select_query = """
            SELECT * FROM usuarios
        """
        cursor.execute(select_query)

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
            tree.insert("", "end", values=("No se encontraron usuarios en la base de datos.",))

    except mysql.connector.Error as error:
        # Manejar errores de la base de datos
        tree.insert("", "end", values=("Error al consultar la base de datos.",))

    finally:
        # Cerrar la conexión a la base de datos
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def eliminar_empleado():
    Numero_documento = entrada_eliminar.get()

    # Confirmar la eliminación
    confirmacion = messagebox.askyesno("Confirmar Eliminación",
                                       f"¿Estás seguro de que deseas eliminar el usuario con el número de documento {Numero_documento}?")

    if not confirmacion:
        return  # Si el usuario elige "No", no hacer nada

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()

        # Ejecutar la consulta de eliminación
        cursor.execute("CALL BorrarUsuario(%s)", (Numero_documento,))
        conexion.commit()  # Confirmar los cambios

        # Mostrar mensaje de éxito
        if cursor.rowcount > 0:
            mensaje_eliminar.config(text=f"Usuario con número de documento {Numero_documento} eliminado correctamente.")
        else:
            mensaje_eliminar.config(text=f"No se encontró ningún usuario con el número de documento {Numero_documento}.")

    except mysql.connector.Error as error:
        mensaje_eliminar.config(text=f"Error al eliminar el usuario: {error}")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("1200x700")
ventana.title("Gestión de Usuarios")

# Frame principal para contener los frames de insertar y mostrar usuarios
frame_principal = tk.Frame(ventana)
frame_principal.pack(fill=tk.BOTH, expand=True)

# Frame para insertar usuario
frame_insertar = tk.Frame(frame_principal, padx=10, pady=10)
frame_insertar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Título del frame de insertar usuario
titulo_insertar = tk.Label(frame_insertar, text="Insertar Usuario", font=("Arial", 16, "bold"))
titulo_insertar.grid(row=0, column=0, columnspan=2, pady=10)

# Etiqueta y Combobox para el tipo de usuario
tk.Label(frame_insertar, text="Tipo de Usuario:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
opciones_tipo_usuario = ['estudiante', 'directivo', 'docente', 'publico_general']
combo_tipo_usuario = ttk.Combobox(frame_insertar, values=opciones_tipo_usuario, state='readonly')
combo_tipo_usuario.grid(row=1, column=1, padx=5, pady=5)

# Crear el campo de entrada para el nombre
tk.Label(frame_insertar, text="Nombre:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entrada_nombre = tk.Entry(frame_insertar)
entrada_nombre.grid(row=2, column=1, padx=5, pady=5)

# Crear el campo de entrada para el apellido
tk.Label(frame_insertar, text="Apellidos:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
entrada_apellido = tk.Entry(frame_insertar)
entrada_apellido.grid(row=3, column=1, padx=5, pady=5)

# Crear el campo de entrada para la fecha de nacimiento usando DateEntry
tk.Label(frame_insertar, text="Fecha de Nacimiento:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
entrada_fecha_nacimiento = DateEntry(frame_insertar, date_pattern='yyyy-mm-dd')
entrada_fecha_nacimiento.grid(row=4, column=1, padx=5, pady=5)

# Etiqueta y Combobox para el tipo de documento
tk.Label(frame_insertar, text="Tipo de Documento:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
opciones_tipo_documento = ['CC', 'CE', 'PA', 'TI', 'PPT', 'PEP']
combo_tipo_documento = ttk.Combobox(frame_insertar, values=opciones_tipo_documento, state='readonly')
combo_tipo_documento.grid(row=5, column=1, padx=5, pady=5)

# Crear el campo de entrada para el número de documento
tk.Label(frame_insertar, text="Número de Documento:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
entrada_numero_documento = tk.Entry(frame_insertar)
entrada_numero_documento.grid(row=6, column=1, padx=5, pady=5)

# Crear el campo de entrada para el correo electrónico
tk.Label(frame_insertar, text="Correo Electrónico:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
entrada_correo = tk.Entry(frame_insertar)
entrada_correo.grid(row=7, column=1, padx=5, pady=5)

# Crear el campo de entrada para la contraseña
tk.Label(frame_insertar, text="Contraseña:").grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
entrada_contrasena = tk.Entry(frame_insertar, show='*')
entrada_contrasena.grid(row=8, column=1, padx=5, pady=5)

# Crear el campo de entrada para el teléfono
tk.Label(frame_insertar, text="Teléfono:").grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
entrada_telefono = tk.Entry(frame_insertar)
entrada_telefono.grid(row=9, column=1, padx=5, pady=5)

# Mensaje de éxito o error
mensaje = tk.Label(frame_insertar, text="")
mensaje.grid(row=10, column=0, columnspan=2, pady=10)

# Botón para insertar usuario
tk.Button(frame_insertar, text="Insertar Usuario", command=insertar_empleado, width=20).grid(row=11, column=0, columnspan=2, pady=10)

# Frame para eliminar usuario
frame_eliminar = tk.Frame(frame_principal, padx=10, pady=10)
frame_eliminar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Título del frame de eliminar usuario
titulo_eliminar = tk.Label(frame_eliminar, text="Eliminar Usuario", font=("Arial", 16, "bold"))
titulo_eliminar.pack(pady=10)

# Etiqueta y campo de entrada para eliminar usuario
tk.Label(frame_eliminar, text="Número de Documento a Eliminar:").pack(pady=5)
entrada_eliminar = tk.Entry(frame_eliminar)
entrada_eliminar.pack(pady=5)

# Botón para eliminar usuario
tk.Button(frame_eliminar, text="Eliminar Usuario", command=eliminar_empleado).pack(pady=10)

# Mensaje de éxito o error para eliminación
mensaje_eliminar = tk.Label(frame_eliminar, text="")
mensaje_eliminar.pack(pady=10)

# Frame para mostrar usuario
frame_mostrar = tk.Frame(frame_principal, padx=10, pady=10)
frame_mostrar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Título del frame de mostrar usuario
titulo_mostrar = tk.Label(frame_mostrar, text="Mostrar Usuario", font=("Arial", 16, "bold"))
titulo_mostrar.pack(pady=10)

# Frame para botones de búsqueda
frame_botones = tk.Frame(frame_mostrar)
frame_botones.pack(pady=10)

# Etiqueta y campo de entrada para buscar usuario
tk.Label(frame_botones, text="Número de Documento a Buscar:").pack(side=tk.LEFT, padx=5)
entrada_buscar = tk.Entry(frame_botones)
entrada_buscar.pack(side=tk.LEFT, padx=5)

# Botones para mostrar usuario y mostrar todos los usuarios
button_mostrar = tk.Button(frame_botones, text="Mostrar Usuario", command=mostrar_empleado, width=20)
button_mostrar.pack(side=tk.LEFT, padx=5)

button_mostrar_todos = tk.Button(frame_botones, text="Mostrar Todos los Usuarios", command=mostrar_todos_usuarios, width=25)
button_mostrar_todos.pack(side=tk.LEFT, padx=5)

# Frame para el Treeview
frame_tree = tk.Frame(frame_mostrar)
frame_tree.pack(fill=tk.BOTH, expand=True)

# Crear Treeview para mostrar resultados
tree = ttk.Treeview(frame_tree, columns=("Tipo_usuario", "Nombre", "Apellidos", "Tipo_documento", "Numero_documento", "Fecha_nacimiento", "Correo_electronico", "Contraseña", "Telefono"), show='headings')

# Definir las cabeceras
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="w")

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Agregar barra de desplazamiento vertical
scrollbar = tk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.config(yscrollcommand=scrollbar.set)

ventana.mainloop()
