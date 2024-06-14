class clsCliente:
    def __init__(self, p_id, p_nombre, p_apellidos, p_email, p_contraseña, p_telefono):
        self.id = p_id
        self.nombre = p_nombre
        self.apellidos = p_apellidos
        self.email = p_email
        self.contraseña = p_contraseña
        self.telefono = p_telefono

        self.dicctemp = {
            "id": p_id,
            "nombre": p_nombre,
            "apellidos": p_apellidos,
            "email": p_email,
            "contraseña": p_contraseña,
            "telefono": p_telefono
        }
