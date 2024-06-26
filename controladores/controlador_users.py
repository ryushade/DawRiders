from bd import obtener_conexion

def obtener_user_por_username(username):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, email, password FROM users WHERE email = %s", (username,))
        user = cursor.fetchone()
    conexion.close()
    return user


def obtener_user_por_id(id):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, email, password FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
    conexion.close()
    return user

