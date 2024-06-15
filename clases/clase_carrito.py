class clsCarrito:
    def __init__(self, p_id, p_idCliente, p_fechaCreacion):
        self.id = p_id
        self.idCliente = p_idCliente
        self.fechaCreacion = p_fechaCreacion

        self.dicccarrito = {
            "id": p_id,
            "idCliente": p_idCliente,
            "fechaCreacion": p_fechaCreacion
        }
