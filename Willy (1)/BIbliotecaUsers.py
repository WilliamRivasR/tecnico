import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector

# Configuración de la base de datos
user = 'root'
password = ''
host = 'localhost'
database = 'biblioteca_escolar'


def ocultar_todos_frames():
    frame_buscar.pack_forget()
    frame_eliminar.pack_forget()
    frame_actualizar.pack_forget()
    frame_prestar.pack_forget()
    frame_registro.pack_forget()

def mostrar_ventana_principal():
    ventana_principal.pack(fill=tk.BOTH, expand=True)
    frame_buscar.pack_forget()
    frame_eliminar.pack_forget()
    frame_actualizar.pack_forget()
    frame_prestar.pack_forget()
    frame_login.pack_forget()

    # Actualizar el texto del título de bienvenida
    titulo_bienvenida.config(text=f"¡Bienvenido, {nombre_usuario}! ¿Qué deseas hacer?")


def mostrar_ventana_buscar():
    ventana_principal.pack_forget()
    frame_buscar.pack(fill=tk.BOTH, expand=True)

def mostrar_ventana_eliminar():
    ventana_principal.pack_forget()
    frame_eliminar.pack(fill=tk.BOTH, expand=True)

def mostrar_ventana_prestar():
    ventana_principal.pack_forget()
    frame_prestar.pack(fill=tk.BOTH, expand=True)


def mostrar_ventana_login():
    ventana_principal.pack_forget()
    frame_registro.pack_forget()
    frame_login.pack(fill=tk.BOTH, expand=True)

def mostrar_ventana_registro():
    frame_login.pack_forget()
    frame_registro.pack(fill=tk.BOTH, expand=True)

# Mostrar el frame de registro con desplazamiento
    canvas_registro.pack(fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def centrar_frame_central(event):
    # Obtener el tamaño del Canvas y del frame_central_registro
    canvas_width = canvas_registro.winfo_width()
    canvas_height = canvas_registro.winfo_height()
    frame_central_width = frame_central_registro.winfo_reqwidth()
    frame_central_height = frame_central_registro.winfo_reqheight()

    # Calcular la posición central
    x = (canvas_width - frame_central_width) // 2
    y = (canvas_height - frame_central_height) // 2

    # Colocar el frame_central_registro en el Canvas
    canvas_registro.create_window((x, y), window=frame_central_registro, anchor="nw")

    # Ajustar el scrollregion del Canvas
    canvas_registro.config(scrollregion=canvas_registro.bbox("all"))

# Función para iniciar sesión
def iniciar_sesion():
    global nombre_usuario
    correo = entrada_correo_login.get().strip()
    contrasena = entrada_contrasena_login.get().strip()

    if not correo or not contrasena:
        mensaje_login.config(text="Por favor, ingrese correo electrónico y contraseña.")
        return

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()
        cursor.callproc('VerificarUsuario', [correo, contrasena])

        # Recuperar el resultado del procedimiento almacenado
        resultado = None
        for result in cursor.stored_results():
            resultado = result.fetchone()

        if resultado and resultado[0] == 1:  # Asumimos que el procedimiento devuelve 1 si el usuario es válido
            # Obtener el nombre del usuario
            cursor.execute("SELECT Nombre FROM usuarios WHERE Correo_electronico = %s", (correo,))
            nombre_usuario = cursor.fetchone()[0]

            mensaje_login.config(text="Inicio de sesión exitoso.")
            mostrar_ventana_principal()
        else:
            mensaje_login.config(text="Correo electrónico o contraseña incorrectos.")

    except mysql.connector.Error as error:
        mensaje_login.config(text=f"Error al iniciar sesión: {error}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def registrar_usuario():
    Tipo_usuario = combo_tipo_usuario_registro.get().strip()
    Nombre = entrada_nombre_registro.get().strip()
    Apellidos = entrada_apellido_registro.get().strip()
    Fecha_nacimiento = entrada_fecha_nacimiento_registro.get_date()
    Tipo_documento = combo_tipo_documento_registro.get().strip()
    Numero_documento = entrada_numero_documento_registro.get().strip()
    Correo_electronico = entrada_correo_registro.get().strip()
    Contraseña = entrada_contrasena_registro.get().strip()
    Telefono = entrada_telefono_registro.get().strip()

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
        mensaje_registro.config(text="Usuario registrado correctamente! Ahora puedes inciar sesión")
    except mysql.connector.Error as error:
        mensaje_registro.config(text=f"Error al registrar usuario: {error}")
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
        for row in tree_buscar.get_children():
            tree_buscar.delete(row)
        if resultados:
            for row in resultados:
                tree_buscar.insert("", "end", values=row)
        else:
            tree_buscar.insert("", "end", values=("No se encontró ningún usuario con ese número de documento.",))
    except mysql.connector.Error as error:
        tree_buscar.insert("", "end", values=("Error al consultar la base de datos.",))
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()



def mostrar_todos_usuarios():
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()
        select_query = "SELECT * FROM usuarios"
        cursor.execute(select_query)
        resultados = cursor.fetchall()

        for row in tree_buscar.get_children():
            tree_buscar.delete(row)

        if resultados:
            for row in resultados:
                tree_buscar.insert("", "end", values=row)
        else:
            tree_buscar.insert("", "end", values=("No se encontraron usuarios en la base de datos.",))
    except mysql.connector.Error as error:
        tree_buscar.insert("", "end", values=("Error al consultar la base de datos.",))
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def mostrar_libros_disponibles():
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()
        select_query = "SELECT * FROM libros WHERE Ejemplares_disponibles >= 1"
        cursor.execute(select_query)
        resultados = cursor.fetchall()

        for row in tree_prestar.get_children():
            tree_prestar.delete(row)

        if resultados:
            for row in resultados:
                tree_prestar.insert("", "end", values=row)
        else:
            tree_prestar.insert("", "end", values=("No se encontraron libros en la base de datos.",))
    except mysql.connector.Error as error:
        tree_prestar.insert("", "end", values=("Error al consultar la base de datos.",))
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def prestar_libro():
    ID_libro = entrada_prestar.get().strip()
    fecha = entrada_prestar_fecha.get().strip()
    correo_electronico = entrada_correo_login.get().strip()
    contrasena = entrada_contrasena_login.get().strip()

    if not ID_libro:
        messagebox.showwarning("Entrada Inválida", "Por favor, ingrese el ID del libro.")
        return

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()

        # Obtener el número de documento del usuario
        select_query = """
                    SELECT Numero_documento
                    FROM usuarios 
                    WHERE Correo_electronico = %s AND Contraseña = %s
                """
        cursor.execute(select_query, (correo_electronico, contrasena))
        resultado = cursor.fetchone()

        if resultado:
            numero_documento = resultado[0]  # Desempaqueta el número de documento

            # Obtener los libros prestados actuales
            cursor.callproc('AgregarLibroPrestado', (numero_documento, ID_libro, fecha))
            conexion.commit()

            messagebox.showinfo("Éxito", "Libro prestado correctamente.")


    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Error al prestar el libro: {error}")
        print(f"Error al prestar el libro: {error}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


def eliminar_empleado():
    correo_electronico = entrada_correo_login.get().strip()
    contrasena = entrada_contrasena_login.get().strip()

    confirmacion = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar tu cuenta? Tendrás que volver a registrarte")
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

        # Obtener el número de documento del usuario
        select_query = """
            SELECT Numero_documento
            FROM usuarios 
            WHERE Correo_electronico = %s AND Contraseña = %s
        """
        cursor.execute(select_query, (correo_electronico, contrasena))
        resultado = cursor.fetchone()

        if resultado:
            Numero_documento = resultado[0]  # Desempaqueta el número de documento

            # Llamar al procedimiento almacenado para eliminar el usuario
            cursor.callproc('BorrarUsuario', (Numero_documento,))
            conexion.commit()

            # Verificar si se eliminó algún registro
            if cursor.rowcount > 0:
                mensaje_eliminar.config(text="Cuenta eliminada correctamente.")
            else:
                mensaje_eliminar.config(text=f"No se encontró ningún usuario con el número de documento {Numero_documento}.")
        else:
            mensaje_eliminar.config(text="No se encontró ningún usuario con ese correo electrónico y contraseña.")

    except mysql.connector.Error as error:
        mensaje_eliminar.config(text=f"Error al eliminar el usuario: {error}")
        print(f"Error al eliminar el usuario: {error}")
    finally:
        if conexion.is_connected():
            ocultar_todos_frames()
            mostrar_ventana_login()
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


def buscar_informacion_usuario():
    correo_electronico = entrada_correo_login.get().strip()
    contrasena = entrada_contrasena_login.get().strip()

    if not correo_electronico or not contrasena:
        mensaje_actualizar.config(text="Por favor, ingrese correo electrónico y contraseña.")
        return

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()
        select_query = """
            SELECT Numero_documento, Nombre, Apellidos, Fecha_nacimiento, Correo_electronico, Telefono, Contraseña 
            FROM usuarios 
            WHERE Correo_electronico = %s AND Contraseña = %s
        """
        cursor.execute(select_query, (correo_electronico, contrasena))
        resultado = cursor.fetchone()

        if resultado:
            entrada_numero_documento_actualizar.delete(0, tk.END)
            entrada_numero_documento_actualizar.insert(0, resultado[0])

            entrada_nombre_actualizar.delete(0, tk.END)
            entrada_nombre_actualizar.insert(0, resultado[1])

            entrada_apellido_actualizar.delete(0, tk.END)
            entrada_apellido_actualizar.insert(0, resultado[2])

            entrada_fecha_nacimiento_actualizar.set_date(resultado[3])

            entrada_correo_actualizar.delete(0, tk.END)
            entrada_correo_actualizar.insert(0, resultado[4])

            entrada_telefono_actualizar.delete(0, tk.END)
            entrada_telefono_actualizar.insert(0, resultado[5])

            entrada_contrasena_actualizar.delete(0, tk.END)
            entrada_contrasena_actualizar.insert(0, resultado[6])

            mensaje_actualizar.config(text="Información del usuario cargada correctamente.")
            ventana_principal.pack_forget()
            frame_actualizar.pack(fill=tk.BOTH, expand=True)
        else:
            mensaje_actualizar.config(text="No se encontró ningún usuario con ese correo electrónico y contraseña.")

    except mysql.connector.Error as error:
        mensaje_actualizar.config(text=f"Error al buscar usuario: {error}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()




# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("1200x700")
ventana.title("Gestión de Usuarios")


# Frame para inicio de sesión
frame_login = tk.Frame(ventana)

# Título del frame de inicio de sesión
titulo_login = tk.Label(frame_login, text="Iniciar Sesión", font=("Arial", 16, "bold"))
titulo_login.pack(pady=10)

# Etiqueta y campo de entrada para el correo electrónico
tk.Label(frame_login, text="Correo Electrónico:").pack(pady=5)
entrada_correo_login = tk.Entry(frame_login)
entrada_correo_login.pack(pady=5)

# Etiqueta y campo de entrada para la contraseña
tk.Label(frame_login, text="Contraseña:").pack(pady=5)
entrada_contrasena_login = tk.Entry(frame_login, show='*')
entrada_contrasena_login.pack(pady=5)

# Mensaje de error para inicio de sesión
mensaje_login = tk.Label(frame_login, text="")
mensaje_login.pack(pady=10)
tk.Button(frame_login, text="Iniciar Sesión", command=iniciar_sesion, width=20).pack(pady=10)
tk.Button(frame_login, text="Registrarse", command=mostrar_ventana_registro, width=20).pack(pady=10)

# Frame para registro de usuario
frame_registro = tk.Frame(ventana)
frame_registro.pack(fill=tk.BOTH, expand=True)

# Crear Canvas y Scrollbar para el frame de registro
canvas_registro = tk.Canvas(frame_registro)
scrollbar = tk.Scrollbar(frame_registro, orient="vertical", command=canvas_registro.yview)
canvas_registro.configure(yscrollcommand=scrollbar.set)

# Colocar el Canvas y el Scrollbar en el frame_registro
canvas_registro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Crear un Frame dentro del Canvas para centrar el contenido
frame_central_registro = tk.Frame(canvas_registro)

# Configurar el Canvas para que ajuste el frame_central_registro
canvas_registro.create_window((0, 0), window=frame_central_registro, anchor="nw")

# Asociar el evento de ajuste de tamaño para centrar el frame
canvas_registro.bind("<Configure>", centrar_frame_central)

# Título del frame de registro de usuario
titulo_registro = tk.Label(frame_central_registro, text="Registrar Usuario", font=("Arial", 16, "bold"))
titulo_registro.pack(pady=10)

# Etiqueta y Combobox para el tipo de usuario
tk.Label(frame_central_registro, text="Tipo de Usuario:").pack(pady=5)
opciones_tipo_usuario_registro = ['estudiante', 'directivo', 'docente', 'publico_general']
combo_tipo_usuario_registro = ttk.Combobox(frame_central_registro, values=opciones_tipo_usuario_registro, state='readonly')
combo_tipo_usuario_registro.pack(pady=5)

# Campos de entrada
tk.Label(frame_central_registro, text="Nombre:").pack(pady=5)
entrada_nombre_registro = tk.Entry(frame_central_registro)
entrada_nombre_registro.pack(pady=5)

tk.Label(frame_central_registro, text="Apellidos:").pack(pady=5)
entrada_apellido_registro = tk.Entry(frame_central_registro)
entrada_apellido_registro.pack(pady=5)

tk.Label(frame_central_registro, text="Fecha de Nacimiento:").pack(pady=5)
entrada_fecha_nacimiento_registro = DateEntry(frame_central_registro, date_pattern='yyyy-mm-dd')
entrada_fecha_nacimiento_registro.pack(pady=5)

tk.Label(frame_central_registro, text="Tipo de Documento:").pack(pady=5)
opciones_tipo_documento_registro = ['CC', 'CE', 'PA', 'TI', 'PPT', 'PEP']
combo_tipo_documento_registro = ttk.Combobox(frame_central_registro, values=opciones_tipo_documento_registro, state='readonly')
combo_tipo_documento_registro.pack(pady=5)

tk.Label(frame_central_registro, text="Número de Documento:").pack(pady=5)
entrada_numero_documento_registro = tk.Entry(frame_central_registro)
entrada_numero_documento_registro.pack(pady=5)

tk.Label(frame_central_registro, text="Correo Electrónico:").pack(pady=5)
entrada_correo_registro = tk.Entry(frame_central_registro)
entrada_correo_registro.pack(pady=5)

tk.Label(frame_central_registro, text="Contraseña:").pack(pady=5)
entrada_contrasena_registro = tk.Entry(frame_central_registro, show='*')
entrada_contrasena_registro.pack(pady=5)

tk.Label(frame_central_registro, text="Teléfono:").pack(pady=5)
entrada_telefono_registro = tk.Entry(frame_central_registro)
entrada_telefono_registro.pack(pady=5)

# Mensaje de éxito o error para registro
mensaje_registro = tk.Label(frame_central_registro, text="")
mensaje_registro.pack(pady=10)

# Botón para registrar usuario
tk.Button(frame_central_registro, text="Registrar", command=registrar_usuario, width=20).pack(pady=10)

# Botón para volver
tk.Button(frame_central_registro, text="Volver", command=mostrar_ventana_login, width=20).pack(pady=10)


# Frame de bienvenida
ventana_principal = tk.Frame(ventana)
ventana_principal.pack(fill=tk.BOTH, expand=True)

#titulo de bienvenida
titulo_bienvenida = tk.Label(ventana_principal, text="", font=("Arial", 20, "bold"))
titulo_bienvenida.pack(pady=20)

# Botones de bienvenida
tk.Button(ventana_principal, text="Buscar un usuario ya existente", command=mostrar_ventana_buscar, width=30).pack(pady=10)
tk.Button(ventana_principal, text="Actualizar información", command=buscar_informacion_usuario, width=30).pack(pady=10)
tk.Button(ventana_principal, text="Pedir un libro", command=mostrar_ventana_prestar, width=30).pack(pady=10)
tk.Button(ventana_principal, text="Eliminar cuenta", command=eliminar_empleado, width=30).pack(pady=10)





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

# Crear Treeview para mostrar resultados en el frame de buscar usuario
frame_tree_buscar = tk.Frame(frame_buscar)
frame_tree_buscar.pack(fill=tk.BOTH, expand=True)
columns_buscar = ("ID_usuario", "Tipo_usuario", "Nombre", "Apellidos", "Tipo_documento", "Numero_documento", "Fecha_nacimiento", "Correo_electronico", "Contraseña", "Telefono")
tree_buscar = ttk.Treeview(frame_tree_buscar, columns=columns_buscar, show='headings')
for col in columns_buscar:
    tree_buscar.heading(col, text=col)
    tree_buscar.column(col, width=120, anchor="w")
tree_buscar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_buscar = tk.Scrollbar(frame_tree_buscar, orient="vertical", command=tree_buscar.yview)
scrollbar_buscar.pack(side="right", fill="y")
tree_buscar.config(yscrollcommand=scrollbar_buscar.set)

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







# Frame para pedir libro
frame_prestar = tk.Frame(ventana)
frame_prestar.pack(fill=tk.BOTH, expand=True)

# Título del frame de buscar usuario
titulo_prestar = tk.Label(frame_prestar, text="Pedir Libro", font=("Arial", 16, "bold"))
titulo_prestar.pack(pady=10)

# Etiqueta y campo de entrada para pedir libro
tk.Label(frame_prestar, text="ID del Libro a Pedir:").pack(pady=5)
entrada_prestar = tk.Entry(frame_prestar)
entrada_prestar.pack(pady=5)

# Etiqueta y campo de usuario a pedir libro
tk.Label(frame_prestar, text="Número de documento:").pack(pady=5)
entrada_prestar_documento = tk.Entry(frame_prestar)
entrada_prestar_documento.pack(pady=5)

tk.Label(frame_prestar, text="Fecha:").pack(pady=5)
entrada_prestar_fecha = DateEntry(frame_prestar, date_pattern='yyyy-mm-dd')
entrada_prestar_fecha.pack(pady=5)

# Botón para pedir libro
tk.Button(frame_prestar, text="Pedir Libro", command=prestar_libro, width=20).pack(pady=10)

# Botón para mostrar todos los libros disponibles
tk.Button(frame_prestar, text="Mostrar Libros Disponibles", command=mostrar_libros_disponibles, width=25).pack(pady=10)

# Crear Treeview para mostrar resultados en el frame de pedir libro
frame_tree_prestar = tk.Frame(frame_prestar)
frame_tree_prestar.pack(fill=tk.BOTH, expand=True)
columns_prestar = ("ID_libro", "Titulo", "Autor", "Año de Publicación", "Género", "Resumen", "Ejemplares Disponibles", "Estado")
tree_prestar = ttk.Treeview(frame_tree_prestar, columns=columns_prestar, show='headings')
for col in columns_prestar:
    tree_prestar.heading(col, text=col)
    tree_prestar.column(col, width=120, anchor="w")
tree_prestar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_prestar = tk.Scrollbar(frame_tree_prestar, orient="vertical", command=tree_prestar.yview)
scrollbar_prestar.pack(side="right", fill="y")
tree_prestar.config(yscrollcommand=scrollbar_prestar.set)

# Botón para volver a la pantalla principal
tk.Button(frame_prestar, text="Volver", command=mostrar_ventana_principal, width=20).pack(pady=10)
ocultar_todos_frames()
mostrar_ventana_login()

ventana.mainloop()