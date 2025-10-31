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
    """Obtiene los datos del usuario a partir de su username y contraseña."""
    conn = conectar_db()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
                FROM credenciales c
                JOIN usuarios u ON c.id_usuario = u.id_usuario
                WHERE c.username = %s AND c.password_hash = %s;
            """, (username, password))  # Usa crypt() para comparación segura de hash

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


if __name__ == "__main__":
    print("=== Inicio de sesión en la base de datos ===")
    user = input("Ingrese su usuario: ")
    pwd = getpass.getpass("Ingrese su contraseña: ")
    obtener_datos_usuario(user, pwd)
