from bd import obtener_conexion

def agregar_producto_al_carrito(id_carrito, id_producto, cantidad, precio):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM ITEM_CARRITO WHERE idCarrito = %s AND idProducto = %s", (id_carrito, id_producto))
            item = cursor.fetchone()
            if item:
                nueva_cantidad = item['cantidad'] + cantidad
                subtotal = nueva_cantidad * precio
                cursor.execute("UPDATE ITEM_CARRITO SET cantidad = %s, subtotal = %s WHERE idItemCarrito = %s", (nueva_cantidad, subtotal, item['idItemCarrito']))
            else:
                cursor.execute("INSERT INTO ITEM_CARRITO (idCarrito, idProducto, cantidad, precioPorUnidad, subtotal) VALUES (%s, %s, %s, %s, %s)",
                               (id_carrito, id_producto, cantidad, precio, cantidad * precio))
        conexion.commit()
    finally:
        conexion.close()

def eliminar_producto_del_carrito(id_item_carrito):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM ITEM_CARRITO WHERE idItemCarrito = %s", (id_item_carrito,))
        conexion.commit()
    finally:
        conexion.close()


def actualizar_cantidad_producto_carrito(id_item_carrito, nueva_cantidad):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT precioPorUnidad FROM ITEM_CARRITO WHERE idItemCarrito = %s", (id_item_carrito,))
            precio = cursor.fetchone()['precioPorUnidad']
            subtotal = nueva_cantidad * precio
            cursor.execute("UPDATE ITEM_CARRITO SET cantidad = %s, subtotal = %s WHERE idItemCarrito = %s", (nueva_cantidad, subtotal, id_item_carrito))
        conexion.commit()
    finally:
        conexion.close()

def obtener_items_carrito():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT p.idProducto, p.imagen, CONCAT(p.marca, ' ', p.modelo) AS modelo, p.precio, ic.cantidad, ic.subtotal FROM ITEM_CARRITO ic INNER JOIN PRODUCTO p ON ic.idProducto = p.idProducto")
            items = cursor.fetchall()
            return items
    finally:
        conexion.close()


def obtener_carrito(id_carrito):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM ITEM_CARRITO WHERE idCarrito = %s", (id_carrito,))
            items = cursor.fetchall()
        return items
    finally:
        conexion.close()


def obtener_carrito_api():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM ITEM_CARRITO")
            items = cursor.fetchall()
        return items
    finally:
        conexion.close()

def obtener_carrito_api_an():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT idCarrito, idCliente, fechaCreacion FROM CARRITO")
            items = cursor.fetchall()
        return items
    finally:
        conexion.close()

def insertar_item_carrito(idCarrito, idProducto, cantidad, precioPorUnidad, subtotal):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO ITEM_CARRITO(idCarrito, idProducto, cantidad, precioPorUnidad, subtotal) VALUES (%s, %s, %s, %s, %s)",
            (idCarrito, idProducto, cantidad, precioPorUnidad, subtotal))
    conexion.commit()
    conexion.close()


###APIS

def insertar_carrito_api(idCliente, fechaCreacion):
    conexion = obtener_conexion()
    id_generado = None
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO CARRITO(idCliente, fechaCreacion) VALUES (%s, %s)",
                (idCliente, fechaCreacion))
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_generado = cursor.fetchone()[0]

        conexion.commit()
    finally:
        conexion.close()
    return id_generado  # Devuelve el ID generado


def eliminar_carrito(id_carrito):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM CARRITO WHERE idCarrito = %s", (id_carrito,))
        conexion.commit()
    finally:
        conexion.close()

def obtener_carrito_id(id_carrito):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM CARRITO WHERE idCarrito = %s", (id_carrito,))
            carrito = cursor.fetchone()
        return carrito
    finally:
        conexion.close()

def modificar_carrito(id_carrito, id_cliente, fecha_creacion):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE CARRITO SET idCliente = %s, fechaCreacion = %s WHERE idCarrito = %s", (id_cliente, fecha_creacion, id_carrito))
        conexion.commit()
    finally:
        conexion.close()


def obtener_carrito_por_cliente_id(id_cliente):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM CARRITO WHERE idCliente = %s", (id_cliente,))
            carrito = cursor.fetchone()
            return carrito
    finally:
        conexion.close()

def crear_carrito_para_cliente(id_cliente):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO CARRITO (idCliente, fechaCreacion) VALUES (%s, NOW())", (id_cliente,))
            conexion.commit()
            return cursor.lastrowid
    finally:
        conexion.close()

def obtener_items_carrito_por_id_carrito(id_carrito):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT p.idProducto, p.imagen, CONCAT(p.marca, ' ', p.modelo) AS modelo, p.precio, ic.cantidad, ic.subtotal, ic.idItemCarrito FROM ITEM_CARRITO ic INNER JOIN PRODUCTO p ON ic.idProducto = p.idProducto WHERE ic.idCarrito = %s", (id_carrito,))
            items = cursor.fetchall()
            return items
    finally:
        conexion.close()
