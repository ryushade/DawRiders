from bd import obtener_conexion

def insertar_producto(descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO PRODUCTO(descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (descripcion, precio, stock, marca, modelo, color, imagen, idmoto, idaccesorio))
    conexion.commit()
    conexion.close()

def obtener_producto():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento FROM PRODUCTO")
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
        cursor.execute("select pr.*, mo.* from producto as pr inner join moto as mo on pr.idMoto = mo.idMoto")
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_moto_producto_nuevo_one(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, mo.* from producto as pr inner join moto as mo on pr.idMoto = mo.idMoto WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchone()
    conexion.close()
    return productos

def obtener_moto_producto_nuevo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, mo.* from producto as pr inner join moto as mo on pr.idMoto = mo.idMoto WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchall()
    conexion.close()
    return productos

#########################################################

def obtener_accesorio_producto():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, ac.* from producto as pr inner join accesorio as ac on pr.idAccesorio = ac.idAccesorio")
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_accesorio_producto_nuevo_one(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, ac.* from producto as pr inner join accesorio as ac on pr.idAccesorio = ac.idAccesorio WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchone()
    conexion.close()
    return productos

def obtener_accesorio_producto_nuevo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("select pr.*, ac.* from producto as pr inner join accesorio as ac on pr.idAccesorio = ac.idAccesorio WHERE pr.idProducto = %s", (id,))
        productos = cursor.fetchall()
    conexion.close()
    return productos
