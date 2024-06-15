class clsAdministrador:
    def __init__(self, p_id, p_cliente_id, p_fecha_asignacion):
        self.id = p_id
        self.cliente_id = p_cliente_id
        self.fecha_asignacion = p_fecha_asignacion

        self.diccadmin = {
            "id": p_id,
            "cliente_id": p_cliente_id,
            "fecha_asignacion": p_fecha_asignacion
        }
