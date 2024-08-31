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


def desplazar_canvas(event):
    # Desplazar el canvas según el movimiento de la rueda del ratón
    canvas_registro.yview_scroll(int(-1*(event.delta/120)), "units")

def ocultar_todos_frames():
    frame_eliminar.pack_forget()
    frame_actualizar.pack_forget()
    frame_prestar.pack_forget()
    frame_registro.pack_forget()
    frame_agregar.pack_forget()
    frame_usuarios.pack_forget()

def mostrar_ventana_principal():
    ventana_principal.pack(fill=tk.BOTH, expand=True)
    frame_eliminar.pack_forget()
    frame_actualizar.pack_forget()
    frame_prestar.pack_forget()
    frame_login.pack_forget()
    frame_agregar.pack_forget()
    frame_usuarios.pack_forget()

    # Actualizar el texto del título de bienvenida
    titulo_bienvenida.config(text=f"¡Bienvenido, {nombre_usuario}! ¿Qué deseas hacer?")

def mostrar_ventana_prestamos():
    ventana_principal.pack_forget()
    frame_usuarios.pack(fill=tk.BOTH, expand=True)


def mostrar_ventana_agregar():
    ventana_principal.pack_forget()
    frame_agregar.pack(fill=tk.BOTH, expand=True)


def mostrar_ventana_eliminar():
    ventana_principal.pack_forget()
    frame_eliminar.pack(fill=tk.BOTH, expand=True)

def mostrar_ventana_prestar():
    ventana_principal.pack_forget()
    frame_prestar.pack(fill=tk.BOTH, expand=True)


def mostrar_ventana_login():
    ventana_principal.pack_forget()
    frame_registro.pack_forget()
    scrollbar.pack_forget()
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
    tipo_usuario = combo_tipo_usuario_login.get().strip()

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
        cursor.callproc('VerificarUsuario', [correo, contrasena, tipo_usuario])

        # Recuperar el resultado del procedimiento almacenado
        resultado = None
        for result in cursor.stored_results():
            resultado = result.fetchone()

        if resultado and resultado[0] == 1:  # Usuario válido
            # Obtener el nombre del usuario
            cursor.execute("SELECT Nombre FROM usuarios WHERE Correo_electronico = %s", (correo,))
            nombre_usuario = cursor.fetchone()[0]

            # Mostrar u ocultar botones según el tipo de usuario
            if tipo_usuario in ('docente', 'directivo'):
                btn_prestamos.pack(pady=10)  # Mostrar botón de préstamos
                btn_agregar_libro.pack(pady=10)  # Mostrar botón para agregar libro
            else:
                btn_prestamos.pack_forget()  # Ocultar botón de préstamos
                btn_agregar_libro.pack_forget()  # Ocultar botón para agregar libro

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



def mostrar_usuarios_prestamos():
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()

        # Consulta para obtener todos los préstamos
        select_query = "SELECT * FROM prestamos"
        cursor.execute(select_query)
        resultados = cursor.fetchall()

        for row in tree_usuarios.get_children():
            tree_usuarios.delete(row)

        if resultados:
            for row in resultados:
                id_libro = row[1]  # Asume que el ID del libro está en la segunda columna
                # Consulta para obtener el nombre del libro
                cursor.execute("SELECT Titulo FROM libros WHERE ID_libro = %s", (id_libro,))
                nombre_libro = cursor.fetchone()
                if nombre_libro:
                    nombre_libro = nombre_libro[0]
                else:
                    nombre_libro = "Desconocido"
                # Inserta en el tree_usuarios el préstamo con el nombre del libro
                tree_usuarios.insert("", "end", values=(row[0], nombre_libro, row[2], row[3]))  # Ajusta los índices según la estructura de tu tabla
        else:
            tree_usuarios.insert("", "end", values=("No se encontraron préstamos en la base de datos.",))
    except mysql.connector.Error as error:
        tree_usuarios.insert("", "end", values=("Error al consultar la base de datos.",))
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def eliminar_prestamo():
    id_prestamo = entry_id_prestamo.get()
    if id_prestamo:
        try:
            conexion = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            cursor = conexion.cursor()
            delete_query = "DELETE FROM prestamos WHERE ID_prestamo = %s"
            cursor.execute(delete_query, (id_prestamo,))
            conexion.commit()
            print("Préstamo eliminado con éxito.")
            mostrar_usuarios_prestamos()  # Actualiza la lista de préstamos
        except mysql.connector.Error as error:
            print(f"Error al eliminar el préstamo: {error}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    else:
        print("Por favor, ingresa el ID del préstamo.")


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



def agregar_libro():
    Titulo = entrada_titulo_agregar.get()
    Autor = entrada_autor_agregar.get()
    Año = entrada_año_agregar.get()
    Genero = entrada_genero_agregar.get()
    Resumen = entrada_resumen_agregar.get()
    Ejemplares = entrada_ejemplares_agregar.get()
    Estado = entrada_estado_agregar.get()

    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conexion.cursor()

        # Llamar al procedimiento almacenado
        cursor.callproc('AgregarLibro', [Titulo, Autor, Año, Genero, Resumen, Ejemplares, Estado])

        conexion.commit()

        # Mostrar un mensaje de éxito
        mensaje_agregar.config(text="Libro agregado correctamente.")

        # Limpiar los campos después de agregar
        entrada_titulo_agregar.delete(0, tk.END)
        entrada_autor_agregar.delete(0, tk.END)
        entrada_año_agregar.delete(0, tk.END)
        entrada_genero_agregar.delete(0, tk.END)
        entrada_resumen_agregar.delete(0, tk.END)
        entrada_ejemplares_agregar.delete(0, tk.END)
        entrada_estado_agregar.delete(0, tk.END)

    except mysql.connector.Error as error:
        mensaje_agregar.config(text=f"Error al agregar libro: {error}")
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

# Frame con borde y título centrado para inicio de sesión
frame_login = tk.LabelFrame(ventana, text="Inicio de Sesión", font=("Arial", 14, "bold"), padx=1, pady=1, labelanchor='n')
frame_login.pack(padx=400, pady=150)

# Etiqueta y Combobox para el tipo de usuario
tk.Label(frame_login, text="Tipo de Usuario:").pack(pady=5)
opciones_tipo_usuario_login = ['estudiante', 'directivo', 'docente', 'publico_general']
combo_tipo_usuario_login = ttk.Combobox(frame_login, values=opciones_tipo_usuario_login, state='readonly')
combo_tipo_usuario_login.pack(pady=5)

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

# Crear un frame principal para contener el LabelFrame y el Scrollbar
frame_principal = tk.Frame(ventana)
frame_principal.pack(padx=200, pady=50, fill=tk.BOTH, expand=True)

# Frame con borde y título centrado para registro de usuario
frame_registro = tk.LabelFrame(frame_principal, text="Registro de Usuario", font=("Arial", 14, "bold"), padx=20, pady=20, labelanchor='n')
frame_registro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear Canvas dentro del LabelFrame
canvas_registro = tk.Canvas(frame_registro)
canvas_registro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear el Scrollbar fuera del LabelFrame pero en el mismo frame_principal
scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas_registro.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas_registro.bind_all("<MouseWheel>", desplazar_canvas)

# Configurar el Canvas para que ajuste el frame_central_registro
canvas_registro.configure(yscrollcommand=scrollbar.set)

# Crear un Frame dentro del Canvas para centrar el contenido
frame_central_registro = tk.Frame(canvas_registro)

# Asociar el evento de ajuste de tamaño para centrar el frame
canvas_registro.bind("<Configure>", centrar_frame_central)

# Configurar el Frame central para centrar los elementos
frame_central_registro.pack(padx=20, pady=20)



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
# Definir los botones globalmente
btn_actualizar_informacion = tk.Button(ventana_principal, text="Actualizar información", command=buscar_informacion_usuario, width=30)
btn_pedir_libro = tk.Button(ventana_principal, text="Pedir un libro", command=mostrar_ventana_prestar, width=30)
btn_prestamos = tk.Button(ventana_principal, text="Prestamos", command=mostrar_ventana_prestamos, width=30)
btn_agregar_libro = tk.Button(ventana_principal, text="Agregar un Libro", command=mostrar_ventana_agregar, width=30)
btn_eliminar_cuenta = tk.Button(ventana_principal, text="Eliminar cuenta", command=eliminar_empleado, width=30)

# Empaquetar los botones (excepto los que dependen del tipo de usuario)
btn_actualizar_informacion.pack(pady=10)
btn_pedir_libro.pack(pady=10)
btn_eliminar_cuenta.pack(pady=10)








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






# Frame para agregar libro
frame_agregar = tk.Frame(ventana)
frame_agregar.pack(fill=tk.BOTH, expand=True)

# Título del frame de agregar libro
titulo_agregar = tk.Label(frame_agregar, text="Agregar Libro Nuevo", font=("Arial", 16, "bold"))
titulo_agregar.pack(pady=10)

# Etiqueta y campos de entrada para agregar libro
tk.Label(frame_agregar, text="Titulo:").pack(pady=5)
entrada_titulo_agregar = tk.Entry(frame_agregar)
entrada_titulo_agregar.pack(pady=5)

tk.Label(frame_agregar, text="Autor:").pack(pady=5)
entrada_autor_agregar = tk.Entry(frame_agregar)
entrada_autor_agregar.pack(pady=5)

# Spinbox para seleccionar el año de publicación
tk.Label(frame_agregar, text="Año de Publicación:").pack(pady=5)
entrada_año_agregar = tk.Spinbox(frame_agregar, from_=1900, to=2100, format="%04.0f", width=5)
entrada_año_agregar.pack(pady=5)

tk.Label(frame_agregar, text="Género:").pack(pady=5)
entrada_genero_agregar = tk.Entry(frame_agregar)
entrada_genero_agregar.pack(pady=5)

tk.Label(frame_agregar, text="Resumen:").pack(pady=5)
entrada_resumen_agregar = tk.Entry(frame_agregar)
entrada_resumen_agregar.pack(pady=5)

tk.Label(frame_agregar, text="Ejemplares disponibles:").pack(pady=5)
entrada_ejemplares_agregar = tk.Entry(frame_agregar)
entrada_ejemplares_agregar.pack(pady=5)

tk.Label(frame_agregar, text="Estado:").pack(pady=5)
entrada_estado_agregar = tk.Entry(frame_agregar)
entrada_estado_agregar.pack(pady=5)

# Mensaje de éxito o error al agregar el libro
mensaje_agregar = tk.Label(frame_agregar, text="")
mensaje_agregar.pack(pady=10)

# Botón para agregar el libro
tk.Button(frame_agregar, text="Agregar Libro", command=agregar_libro, width=20).pack(pady=10)

# Botón para volver a la pantalla principal
tk.Button(frame_agregar, text="Volver", command=mostrar_ventana_principal, width=20).pack(pady=10)







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








# Frame para ver usuarios con préstamos
frame_usuarios = tk.Frame(ventana)
frame_usuarios.pack(fill=tk.BOTH, expand=True)

# Título del frame de buscar usuario
titulo_usuarios = tk.Label(frame_usuarios, text="Todos los usuarios con libros prestados", font=("Arial", 16, "bold"))
titulo_usuarios.pack(pady=10)

# Botón para mostrar todos los préstamos
tk.Button(frame_usuarios, text="Mostrar Usuarios", command=mostrar_usuarios_prestamos, width=25).pack(pady=10)

# Crear Treeview para mostrar resultados en el frame de préstamos
frame_tree_usuarios = tk.Frame(frame_usuarios)
frame_tree_usuarios.pack(fill=tk.BOTH, expand=True)
columns_usuarios = ("ID de Prestamo", "Nombre del Libro", "Número de Documento", "Fecha de Prestamo")
tree_usuarios = ttk.Treeview(frame_tree_usuarios, columns=columns_usuarios, show='headings')
for col in columns_usuarios:
    tree_usuarios.heading(col, text=col)
    tree_usuarios.column(col, width=120, anchor="w")
tree_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_usuarios = tk.Scrollbar(frame_tree_usuarios, orient="vertical", command=tree_usuarios.yview)
scrollbar_usuarios.pack(side="right", fill="y")
tree_usuarios.config(yscrollcommand=scrollbar_usuarios.set)

# Entrada para el ID del préstamo
tk.Label(frame_usuarios, text="ID del Préstamo a Eliminar:", font=("Arial", 12)).pack(pady=5)
entry_id_prestamo = tk.Entry(frame_usuarios, width=20)
entry_id_prestamo.pack(pady=5)

# Botón para eliminar préstamo
tk.Button(frame_usuarios, text="Eliminar Préstamo", command=eliminar_prestamo, width=25).pack(pady=10)

# Botón para volver a la pantalla principal
tk.Button(frame_usuarios, text="Volver", command=mostrar_ventana_principal, width=20).pack(pady=10)



ocultar_todos_frames()
mostrar_ventana_login()

ventana.iconbitmap(r"C:\Users\311\Downloads\tecnico-main\tecnico-main\Biblioteca\icon\Icono.ico")
ventana.mainloop()