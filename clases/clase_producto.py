class clsProducto:
    def __init__(self, p_id, p_descripcion, p_precio, p_stock, p_marca, p_modelo, p_color, p_imagen, p_idMoto, p_idAccesorio):
        self.id = p_id
        self.descripcion = p_descripcion
        self.precio = p_precio
        self.stock = p_stock
        self.marca = p_marca
        self.modelo = p_modelo
        self.color = p_color
        self.imagen = p_imagen
        self.idMoto = p_idMoto
        self.idAccesorio = p_idAccesorio

        self.dicctemp = {
            "id": p_id,
            "descripcion": p_descripcion,
            "precio": p_precio,
            "stock": p_stock,
            "marca": p_marca,
            "modelo": p_modelo,
            "color": p_color,
            "imagen": p_imagen,
            "idMoto": p_idMoto,
            "idAccesorio": p_idAccesorio
        }
