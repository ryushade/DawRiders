from bd import obtener_conexion

def agregar_producto_al_carrito(id_carrito, id_producto, cantidad, precio):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar si el producto ya está en el carrito
            cursor.execute("SELECT * FROM ITEM_CARRITO WHERE idCarrito = %s AND idProducto = %s", (id_carrito, id_producto))
            item = cursor.fetchone()
            if item:
                # Actualizar cantidad y subtotal si el producto ya está en el carrito
                nueva_cantidad = item['cantidad'] + cantidad
                subtotal = nueva_cantidad * precio
                cursor.execute("UPDATE ITEM_CARRITO SET cantidad = %s, subtotal = %s WHERE idItemCarrito = %s", (nueva_cantidad, subtotal, item['idItemCarrito']))
            else:
                # Insertar nuevo ítem en el carrito
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

def insertar_item_carrito(idCarrito, idProducto, cantidad, precioPorUnidad, subtotal):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO ITEM_CARRITO(idCarrito, idProducto, cantidad, precioPorUnidad, subtotal) VALUES (%s, %s, %s, %s, %s)",
            (idCarrito, idProducto, cantidad, precioPorUnidad, subtotal))
    conexion.commit()
    conexion.close()