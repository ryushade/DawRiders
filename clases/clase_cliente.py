class clsCliente:
	id = 0
	nombre = ""
	apellidos = ""
	email = ""
	contraseña = ""
	telefono = ""

	def __init__(self, p_id, p_nombre, p_apellidos, p_email, p_contraseña, p_telefono,):
		self.id = p_id
		self.nombre = p_nombre
		self.apellidos = p_apellidos
		self.email = p_email
		self.contraseña = p_contraseña
		self.telefono = p_telefono

	def obtenerObjetoSerializable(self):
		dicctemp = dict()
		###debemos pasarle la información del objeto
		dicctemp["id"] = self.id
		dicctemp["nombre"] = self.nombre
		dicctemp["apellidos"] = self.apellidos
		dicctemp["email"] = self.email
		dicctemp["contraseña"] = self.contraseña
		dicctemp["telefono"] = self.telefono
		return dicctemp

