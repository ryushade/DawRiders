class clsItemCarrito:
    def __init__(self, p_id_Item, p_id_carrito, p_id_producto, p_cantidad, p_precio_unidad, p_subtotal):
        self.idItemCarrito = p_id_Item
        self.idCarrito = p_id_carrito
        self.idProducto = p_id_producto
        self.cantidad = p_cantidad
        self.precioPorUnidad = p_precio_unidad
        self.subtotal = p_subtotal

        # Almacenando todos los atributos en un diccionario para un acceso más fácil
        self.dicItemCarrito = {
            "idItemCarrito": p_id_Item,
            "idCarrito": p_id_carrito,
            "idProducto": p_id_producto,
            "cantidad": p_cantidad,
            "precioPorUnidad": p_precio_unidad,
            "subtotal": p_subtotal
        }
