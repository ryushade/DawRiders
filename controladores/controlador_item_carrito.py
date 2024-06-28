from bd import obtener_conexion

def insertar_item_carrito(id_carrito, id_producto, cantidad, precio_unidad, subtotal):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO ITEM_CARRITO(idCarrito, idProducto, cantidad, precioPorUnidad, subtotal) VALUES (%s, %s, %s, %s, %s)",
            (id_carrito, id_producto, cantidad, precio_unidad, subtotal))
    conexion.commit()
    conexion.close()

def editar_item_carrito(id_item, id_carrito, id_producto, cantidad, precio_unidad, subtotal):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE ITEM_CARRITO SET idCarrito = %s, idProducto = %s, cantidad = %s, precioPorUnidad = %s, subtotal = %s WHERE idItemCarrito = %s",
            (id_carrito, id_producto, cantidad, precio_unidad, subtotal, id_item))
    conexion.commit()
    conexion.close()

def eliminar_item_carrito(id_item):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM ITEM_CARRITO WHERE idItemCarrito = %s", (id_item,))
    conexion.commit()
    conexion.close()

def obtener_items_carrito():
    conexion = obtener_conexion()
    items_carrito = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idItemCarrito, idCarrito, idProducto, cantidad, precioPorUnidad, subtotal FROM ITEM_CARRITO")
        items_carrito = cursor.fetchall()
    conexion.close()
    return items_carrito

def obtener_item_carrito_por_id(id_item):
    conexion = obtener_conexion()
    item = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT idItemCarrito, idCarrito, idProducto, cantidad, precioPorUnidad, subtotal FROM ITEM_CARRITO WHERE idItemCarrito = %s", (id_item,))
        item = cursor.fetchone()
    conexion.close()
    return item

