import os
import psycopg2
import getpass

# Configuración de la base de datos (usa variables de entorno cuando sea posible)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "credenciales")
DB_USER = os.getenv("DB_USER", "Admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "p4ssw0rdDB")


def conectar_db():
    """Conecta a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None


def obtener_datos_usuario(username, password):
    """
    Obtiene los datos del usuario a partir de su username y contraseña.
    Soporta:
      - contraseñas hasheadas con pgcrypto (crypt)
      - contraseñas en texto plano (modo de compatibilidad temporal)
    """
    conn = conectar_db()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            # Intentamos validar primero contra un hash (crypt).
            # Si el registro tiene password en texto plano, también lo aceptamos
            # (esto es temporal; se recomienda migrar todos los registros a hash).
            cursor.execute("""
                SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
                FROM credenciales c
                JOIN usuarios u ON c.id_usuario = u.id_usuario
                WHERE c.username = %s
                  AND (
                    c.password_hash = crypt(%s, c.password_hash)
                    OR c.password_hash = %s
                  );
            """, (username, password, password))

            usuario = cursor.fetchone()

            if usuario:
                print("\n✅ Usuario encontrado:")
                print(f"ID: {usuario[0]}")
                print(f"Nombre: {usuario[1]}")
                print(f"Correo: {usuario[2]}")
                print(f"Teléfono: {usuario[3]}")
                print(f"Fecha de nacimiento: {usuario[4]}")
            else:
                print("\n⚠️ Usuario o contraseña incorrectos.")

    except Exception as e:
        print("❌ Error al consultar la base de datos:", e)

    finally:
        conn.close()


def registrar_usuario():
    """Permite registrar un nuevo usuario en la base de datos."""
    conn = conectar_db()
    if not conn:
        return

    try:
        nombre = input("Nombre completo: ")
        correo = input("Correo electrónico: ")
        telefono = input("Teléfono: ")
        fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
        username = input("Nombre de usuario: ")
        password = getpass.getpass("Contraseña: ")

        with conn.cursor() as cursor:
            # Insertar en usuarios
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento)
                VALUES (%s, %s, %s, %s)
                RETURNING id_usuario;
            """, (nombre, correo, telefono, fecha_nacimiento))
            id_usuario = cursor.fetchone()[0]

            # Insertar en credenciales con hash de contraseña (bcrypt via pgcrypto)
            cursor.execute("""
                INSERT INTO credenciales (id_usuario, username, password_hash)
                VALUES (%s, %s, crypt(%s, gen_salt('bf')));
            """, (id_usuario, username, password))

            conn.commit()
            print("\n✅ Usuario registrado exitosamente.")

    except Exception as e:
        print("❌ Error al registrar el usuario:", e)
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    print("=== Sistema de acceso a la base de datos ===")
    print("1. Iniciar sesión")
    print("2. Registrar nuevo usuario")
    opcion = input("Seleccione una opción (1/2): ")

    if opcion == "1":
        user = input("Ingrese su usuario: ")
        pwd = getpass.getpass("Ingrese su contraseña: ")
        obtener_datos_usuario(user, pwd)
    elif opcion == "2":
        registrar_usuario()
    else:
        print("Opción no válida.")