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

def mostrar_ventana_principal():
    ventana_principal.pack(fill=tk.BOTH, expand=True)
    frame_insertar.pack_forget()
    frame_buscar.pack_forget()
    frame_eliminar.pack_forget()
    frame_actualizar.pack_forget()

def mostrar_ventana_insertar():
    ventana_principal.pack_forget()
    frame_insertar.pack(fill=tk.BOTH, expand=True)

def mostrar_ventana_buscar():
    ventana_principal.pack_forget()
    frame_buscar.pack(fill=tk.BOTH, expand=True)

def mostrar_ventana_eliminar():
    ventana_principal.pack_forget()
    frame_eliminar.pack(fill=tk.BOTH, expand=True)

def mostrar_ventana_actualizar():
    ventana_principal.pack_forget()
    frame_actualizar.pack(fill=tk.BOTH, expand=True)

def insertar_empleado():
    Tipo_usuario = combo_tipo_usuario.get().strip()
    Nombre = entrada_nombre.get().strip()
    Apellidos = entrada_apellido.get().strip()
    Fecha_nacimiento = entrada_fecha_nacimiento.get_date()
    Tipo_documento = combo_tipo_documento.get().strip()
    Numero_documento = entrada_numero_documento.get().strip()
    Correo_electronico = entrada_correo.get().strip()
    Contraseña = entrada_contrasena.get().strip()
    Telefono = entrada_telefono.get().strip()

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()
        cursor.callproc('InsertarUsuario', (Tipo_usuario, Nombre, Apellidos, Tipo_documento, Numero_documento, Fecha_nacimiento, Correo_electronico, Contraseña, Telefono))
        conexion.commit()
        mensaje.config(text="Usuario insertado correctamente!")
    except mysql.connector.Error as error:
        mensaje.config(text=f"Error al insertar usuario: {error}")
        print(f"Error al insertar usuario: {error}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def mostrar_empleado():
    Numero_documento = entrada_buscar.get()
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()
        select_query = """
            SELECT * FROM usuarios WHERE Numero_documento = %s
        """
        cursor.execute(select_query, (Numero_documento,))
        resultados = cursor.fetchall()
        for row in tree.get_children():
            tree.delete(row)
        if resultados:
            for row in resultados:
                tree.insert("", "end", values=row)
        else:
            tree.insert("", "end", values=("No se encontró ningún usuario con ese número de documento.",))
    except mysql.connector.Error as error:
        tree.insert("", "end", values=("Error al consultar la base de datos.",))
    finally:
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
    Numero_documento = entrada_eliminar.get().strip()

    # Verificar que el campo necesario está completo
    if not Numero_documento:
        mensaje_eliminar.config(text="Por favor, ingrese el número de documento.")
        return

    confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar el usuario con el número de documento {Numero_documento}?")
    if not confirmacion:
        return

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()
        cursor.callproc('BorrarUsuario', (Numero_documento,))
        conexion.commit()

        # Verificar si se eliminó algún registro
        if cursor.rowcount > 0:
            mensaje_eliminar.config(text=f"Usuario con número de documento {Numero_documento} eliminado correctamente.")
        else:
            mensaje_eliminar.config(text=f"No se encontró ningún usuario con el número de documento {Numero_documento}.")
    except mysql.connector.Error as error:
        mensaje_eliminar.config(text=f"Error al eliminar el usuario: {error}")
        print(f"Error al eliminar el usuario: {error}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def actualizar_empleado():
    Numero_documento = entrada_numero_documento_actualizar.get()
    Nombre = entrada_nombre_actualizar.get()
    Apellidos = entrada_apellido_actualizar.get()
    Fecha_nacimiento = entrada_fecha_nacimiento_actualizar.get_date()
    Correo_electronico = entrada_correo_actualizar.get()
    Contraseña = entrada_contrasena_actualizar.get()
    Telefono = entrada_telefono_actualizar.get()

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()
        # Llamar al procedimiento almacenado
        cursor.callproc('ActualizarUsuario', [
            Numero_documento if Numero_documento else None,
            Nombre if Nombre else None,
            Apellidos if Apellidos else None,
            Fecha_nacimiento if Fecha_nacimiento else None,
            Correo_electronico if Correo_electronico else None,
            Contraseña if Contraseña else None,
            Telefono if Telefono else None
        ])

        # Obtener el resultado del procedimiento almacenado
        for result in cursor.stored_results():
            mensaje = result.fetchone()[0]
            mensaje_actualizar.config(text=mensaje)

        conexion.commit()
    except mysql.connector.Error as error:
        mensaje_actualizar.config(text=f"Error al actualizar usuario: {error}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("1200x700")
ventana.title("Gestión de Usuarios")

# Frame de bienvenida
ventana_principal = tk.Frame(ventana)
ventana_principal.pack(fill=tk.BOTH, expand=True)

# Título del frame de bienvenida
titulo_bienvenida = tk.Label(ventana_principal, text="¡Bienvenido! ¿Qué deseas hacer?", font=("Arial", 20, "bold"))
titulo_bienvenida.pack(pady=20)

# Botones de bienvenida
tk.Button(ventana_principal, text="Agregar un nuevo usuario", command=mostrar_ventana_insertar, width=30).pack(pady=10)
tk.Button(ventana_principal, text="Buscar un usuario ya existente", command=mostrar_ventana_buscar, width=30).pack(pady=10)
tk.Button(ventana_principal, text="Eliminar un usuario", command=mostrar_ventana_eliminar, width=30).pack(pady=10)
tk.Button(ventana_principal, text="Actualizar un usuario", command=mostrar_ventana_actualizar, width=30).pack(pady=10)

# Frame para insertar usuario
frame_insertar = tk.Frame(ventana)
frame_insertar.pack(fill=tk.BOTH, expand=True)

# Crear un subframe para centrar el contenido
subframe_insertar = tk.Frame(frame_insertar)
subframe_insertar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Título del frame de insertar usuario
titulo_insertar = tk.Label(subframe_insertar, text="Insertar Usuario", font=("Arial", 16, "bold"))
titulo_insertar.grid(row=0, column=0, columnspan=2, pady=10)

# Etiqueta y Combobox para el tipo de usuario
tk.Label(subframe_insertar, text="Tipo de Usuario:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
opciones_tipo_usuario = ['estudiante', 'directivo', 'docente', 'publico_general']
combo_tipo_usuario = ttk.Combobox(subframe_insertar, values=opciones_tipo_usuario, state='readonly')
combo_tipo_usuario.grid(row=1, column=1, padx=5, pady=5)

# Campos de entrada
tk.Label(subframe_insertar, text="Nombre:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entrada_nombre = tk.Entry(subframe_insertar)
entrada_nombre.grid(row=2, column=1, padx=5, pady=5)

tk.Label(subframe_insertar, text="Apellidos:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
entrada_apellido = tk.Entry(subframe_insertar)
entrada_apellido.grid(row=3, column=1, padx=5, pady=5)

tk.Label(subframe_insertar, text="Fecha de Nacimiento:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
entrada_fecha_nacimiento = DateEntry(subframe_insertar, date_pattern='yyyy-mm-dd')
entrada_fecha_nacimiento.grid(row=4, column=1, padx=5, pady=5)

tk.Label(subframe_insertar, text="Tipo de Documento:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
opciones_tipo_documento = ['CC', 'CE', 'PA', 'TI', 'PPT', 'PEP']
combo_tipo_documento = ttk.Combobox(subframe_insertar, values=opciones_tipo_documento, state='readonly')
combo_tipo_documento.grid(row=5, column=1, padx=5, pady=5)

tk.Label(subframe_insertar, text="Número de Documento:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
entrada_numero_documento = tk.Entry(subframe_insertar)
entrada_numero_documento.grid(row=6, column=1, padx=5, pady=5)

tk.Label(subframe_insertar, text="Correo Electrónico:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
entrada_correo = tk.Entry(subframe_insertar)
entrada_correo.grid(row=7, column=1, padx=5, pady=5)

tk.Label(subframe_insertar, text="Contraseña:").grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
entrada_contrasena = tk.Entry(subframe_insertar, show='*')
entrada_contrasena.grid(row=8, column=1, padx=5, pady=5)

tk.Label(subframe_insertar, text="Teléfono:").grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
entrada_telefono = tk.Entry(subframe_insertar)
entrada_telefono.grid(row=9, column=1, padx=5, pady=5)

# Mensaje de éxito o error
mensaje = tk.Label(subframe_insertar, text="")
mensaje.grid(row=10, column=0, columnspan=2, pady=10)

# Botón para insertar usuario
tk.Button(subframe_insertar, text="Insertar Usuario", command=insertar_empleado, width=20).grid(row=11, column=0, columnspan=2, pady=10)

# Botón para volver a la pantalla principal
tk.Button(subframe_insertar, text="Volver", command=mostrar_ventana_principal, width=20).grid(row=12, column=0, columnspan=2, pady=10)

# Frame para buscar usuario
frame_buscar = tk.Frame(ventana)
frame_buscar.pack(fill=tk.BOTH, expand=True)

# Título del frame de buscar usuario
titulo_buscar = tk.Label(frame_buscar, text="Buscar Usuario", font=("Arial", 16, "bold"))
titulo_buscar.pack(pady=10)

# Etiqueta y campo de entrada para buscar usuario
tk.Label(frame_buscar, text="Número de Documento a Buscar:").pack(pady=5)
entrada_buscar = tk.Entry(frame_buscar)
entrada_buscar.pack(pady=5)

# Botón para mostrar usuario
tk.Button(frame_buscar, text="Mostrar Usuario", command=mostrar_empleado, width=20).pack(pady=10)

# Botón para mostrar todos los usuarios
tk.Button(frame_buscar, text="Mostrar Todos los Usuarios", command=mostrar_todos_usuarios, width=25).pack(pady=10)

# Frame para el Treeview
frame_tree = tk.Frame(frame_buscar)
frame_tree.pack(fill=tk.BOTH, expand=True)

# Crear Treeview para mostrar resultados con la nueva columna "ID del usuario"
columns = ("ID_usuario", "Tipo_usuario", "Nombre", "Apellidos", "Tipo_documento", "Numero_documento", "Fecha_nacimiento", "Correo_electronico", "Contraseña", "Telefono")
tree = ttk.Treeview(frame_tree, columns=columns, show='headings')

# Definir las cabeceras
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="w")

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Agregar barra de desplazamiento vertical
scrollbar = tk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.config(yscrollcommand=scrollbar.set)

# Botón para volver a la pantalla principal
tk.Button(frame_buscar, text="Volver", command=mostrar_ventana_principal, width=20).pack(pady=10)

# Frame para eliminar usuario
frame_eliminar = tk.Frame(ventana)
frame_eliminar.pack(fill=tk.BOTH, expand=True)

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

# Botón para volver a la pantalla principal
tk.Button(frame_eliminar, text="Volver", command=mostrar_ventana_principal, width=20).pack(pady=10)

# Frame para actualizar usuario
frame_actualizar = tk.Frame(ventana)
frame_actualizar.pack(fill=tk.BOTH, expand=True)

# Título del frame de actualizar usuario
titulo_actualizar = tk.Label(frame_actualizar, text="Actualizar Usuario", font=("Arial", 16, "bold"))
titulo_actualizar.pack(pady=10)

# Etiqueta y campos de entrada para actualizar usuario
tk.Label(frame_actualizar, text="Número de Documento:").pack(pady=5)
entrada_numero_documento_actualizar = tk.Entry(frame_actualizar)
entrada_numero_documento_actualizar.pack(pady=5)

tk.Label(frame_actualizar, text="Nombre:").pack(pady=5)
entrada_nombre_actualizar = tk.Entry(frame_actualizar)
entrada_nombre_actualizar.pack(pady=5)

tk.Label(frame_actualizar, text="Apellidos:").pack(pady=5)
entrada_apellido_actualizar = tk.Entry(frame_actualizar)
entrada_apellido_actualizar.pack(pady=5)

tk.Label(frame_actualizar, text="Fecha de Nacimiento:").pack(pady=5)
entrada_fecha_nacimiento_actualizar = DateEntry(frame_actualizar, date_pattern='yyyy-mm-dd')
entrada_fecha_nacimiento_actualizar.pack(pady=5)

tk.Label(frame_actualizar, text="Correo Electrónico:").pack(pady=5)
entrada_correo_actualizar = tk.Entry(frame_actualizar)
entrada_correo_actualizar.pack(pady=5)

tk.Label(frame_actualizar, text="Teléfono:").pack(pady=5)
entrada_telefono_actualizar = tk.Entry(frame_actualizar)
entrada_telefono_actualizar.pack(pady=5)

tk.Label(frame_actualizar, text="Contraseña:").pack(pady=5)
entrada_contrasena_actualizar = tk.Entry(frame_actualizar)
entrada_contrasena_actualizar.pack(pady=5)

# Mensaje de éxito o error para actualización
mensaje_actualizar = tk.Label(frame_actualizar, text="")
mensaje_actualizar.pack(pady=10)

# Botón para actualizar usuario
tk.Button(frame_actualizar, text="Actualizar Usuario", command=actualizar_empleado, width=20).pack(pady=10)

# Botón para volver a la pantalla principal
tk.Button(frame_actualizar, text="Volver", command=mostrar_ventana_principal, width=20).pack(pady=10)

# Mostrar la ventana principal inicialmente
mostrar_ventana_principal()

ventana.mainloop()


