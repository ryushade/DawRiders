class clsItemCarrito:
    idItemCarrito = 0
    idCarrito = 0
    idProducto = 0
    cantidad = 0
    precioPorUnidad = 0.0
    subtotal = 0.0

    diccItemCarrito = dict()

    def __init__(self, p_id_Item, p_id_carrito, p_id_producto, p_cantidad, p_precio_unidad, p_subtotal):
        self.idItemCarrito = p_id_Item
        self.idCarrito = p_id_carrito
        self.idProducto = p_id_producto
        self.cantidad = p_cantidad
        self.precioPorUnidad = p_precio_unidad
        self.subtotal = p_subtotal

        self.diccItemCarrito["idItemCarrito"] = p_id_Item
        self.diccItemCarrito["idCarrito"] = p_id_carrito
        self.diccItemCarrito["idProducto"] = p_id_producto
        self.diccItemCarrito["cantidad"] = p_cantidad
        self.diccItemCarrito["precioPorUnidad"] = p_precio_unidad
        self.diccItemCarrito["subtotal"] = p_subtotal