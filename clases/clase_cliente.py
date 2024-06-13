class clsCliente:
    id = 0
    nombre = ""
    apellidos = ""
    email = ""
    contraseña = ""
    telefono = ""

    dicctemp = dict()

    def __init__(self, p_id, p_nombre, p_apellidos, p_email, p_contraseña, p_telefono):
        self.id = p_id
        self.nombre = p_nombre
        self.apellidos = p_apellidos
        self.email = p_email
        self.contraseña = p_contraseña
        self.telefono = p_telefono

        self.dicctemp["id"] = p_id
        self.dicctemp["nombre"] = p_nombre
        self.dicctemp["apellidos"] = p_apellidos
        self.dicctemp["email"] = p_email
        self.dicctemp["contraseña"] = p_contraseña
        self.dicctemp["telefono"] = p_telefono