from bd import obtener_conexion

def insertar_producto(descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO PRODUCTO(descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio))
    conexion.commit()
    conexion.close()

def insertar_producto_api(descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio):
    conexion = obtener_conexion()
    id_generado = None  # Inicializa la variable para el ID generado
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO PRODUCTO(descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio))
            cursor.execute("SELECT LAST_INSERT_ID()")  # Consulta para obtener el último ID insertado
            id_generado = cursor.fetchone()[0]  # Obtiene el ID generado de la fila resultante

        conexion.commit()
    finally:
        conexion.close()
    return id_generado  # Devuelve el ID generado

def obtener_producto():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento FROM PRODUCTO")
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_producto_api():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idProducto, descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio FROM PRODUCTO")
        productos = cursor.fetchall()
    conexion.close()
    return productos

def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM PRODUCTO WHERE idProducto = %s", (id_producto,))
    conexion.commit()
    conexion.close()

def actualizar_producto(descripcion, precio, stock, marca, modelo, color, imagen, idMoto, idAccesorio, id_producto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE PRODUCTO SET descripcion = %s, precio = %s, stock = %s, marca = %s, modelo = %s, color = %s, imagen = %s, idMoto = %s, idAccesorio = %s WHERE idProducto = %s",
            (descripcion, precio, stock, marca, modelo, color, imagen, idMoto, idAccesorio, id_producto))
    conexion.commit()
    conexion.close()

def obtener_producto_por_id(id_producto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM PRODUCTO WHERE idProducto = %s", (id_producto,))
        producto = cursor.fetchone()
    conexion.close()
    return producto

#########################################################
def obtener_moto_producto():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, mo.* from PRODUCTO as pr inner join MOTO as mo on pr.idMoto = mo.idMoto")
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_moto_producto_nuevo_one(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, mo.* from PRODUCTO as pr inner join MOTO as mo on pr.idMoto = mo.idMoto WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchone()
    conexion.close()
    return productos

def obtener_moto_producto_nuevo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, mo.* from PRODUCTO as pr inner join MOTO as mo on pr.idMoto = mo.idMoto WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchall()
    conexion.close()
    return productos


def obtener_codmoto_porid_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select codMoto from PRODUCTO as pr inner join MOTO as mo on pr.idMoto = mo.idMoto WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchone()
    conexion.close()
    return productos


def obtener_codacce_porid_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select codaccesorio from PRODUCTO as pr inner join ACCESORIO as acc on pr.idAccesorio = acc.idaccesorio WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchone()
    conexion.close()
    return productos
#########################################################

def obtener_accesorio_producto():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, ac.* from PRODUCTO as pr inner join ACCESORIO as ac on pr.idAccesorio = ac.idAccesorio")
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_accesorio_producto_nuevo_one(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, ac.* from PRODUCTO as pr inner join ACCESORIO as ac on pr.idAccesorio = ac.idAccesorio WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchone()
    conexion.close()
    return productos

def obtener_accesorio_producto_nuevo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, ac.* from PRODUCTO as pr inner join ACCESORIO as ac on pr.idAccesorio = ac.idAccesorio WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchall()
    conexion.close()
    return productos
