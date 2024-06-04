from flask import Flask, render_template, request, redirect, flash, jsonify, url_for, session,json
from flask_login import login_user
from flask_jwt import JWT, jwt_required, current_identity
import controlador_pago
from bd import obtener_conexion

import urllib
import os
import controlador_cliente
import controlador_moto
import controlador_producto
import controlador_accesorio
import controlador_carrito
import controlador_administrador
import controlador_users
from clases.clase_moto import clsMoto
from clases.clase_cliente import clsCliente
from clases.clase_administrador import clsAdministrador
from clases.clase_carrito import clsItemCarrito
from clases.clase_venta1 import clsVenta1

##### SEGURIDAD - INICIO ######
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

def authenticate(username, password):
    userfrombd = controlador_users.obtener_user_por_username(username)
    user = None
    if userfrombd is not None:
        user = User(userfrombd[0], userfrombd[1], userfrombd[2])
    if user is not None and (user.password.encode('utf-8') == password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    userfrombd = controlador_users.obtener_user_por_id(user_id)
    if userfrombd is not None:
        user = User(userfrombd[0], userfrombd[1], userfrombd[2])
    return user


app = Flask(__name__, static_folder='static')
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

app.secret_key = '1234'

@app.route("/")
@app.route("/CicloRiders")
def formulario_principal():
    return render_template("indexresp.html")

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'img')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------CLIENTE------------------------
@app.route("/registroCliente")
def formulario_registrar_cliente():
    return render_template("registroCliente.html")


@app.route("/nosotros")
def formulario_nosotros():
    return render_template("nosotros.html")

@app.route("/accesorios")
def formulario_accesorios():
    return render_template("accesorios.html")

@app.route("/marcas")
def formulario_marcas():
    return render_template("marcas.html")

@app.route("/blog")
def formulario_blog():
    return render_template("blog.html")

@app.route("/administrador")
def formulario_administrador():
    return render_template("administrador.html")

@app.route("/contacto")
def formulario_contacto():
    return render_template("contacto.html")

@app.route("/login", methods=["GET"])
def formulario_login_cliente():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template('index_d.html')

@app.route("/comparar")
def formulario_comparar():
    return render_template("comparar.html")

@app.route("/carrito")
def formulario_carrito():
    items = controlador_carrito.obtener_items_carrito()
    return render_template("carritoCompra.html", items=items)





@app.route("/guardar_cliente", methods=["POST"])
def guardar_cliente():
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    contraseña = request.form["contraseña"]

    controlador_cliente.insertar_cliente(nombre, apellidos, email, contraseña, telefono)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/login")

@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    controlador_cliente.eliminar_cliente(request.form["id"])
    return redirect("/")

@app.route("/crud_cliente")
def crud_cliente():
    clientes = controlador_cliente.obtener_clientes()
    return render_template("crud_cliente.html", clientes=clientes)

@app.route("/procesar_login", methods=["POST"])
def procesar_login():
    email = request.form["email"]
    contraseña = request.form["contraseña"]
    usuario = controlador_cliente.obtener_usuario_por_email(email)

    if usuario['contraseña'] == contraseña:
        session['user_id'] = usuario['id']
        session['is_admin'] = usuario['is_admin']  # This is now coming directly from your query
        if usuario['is_admin']:
            flash('Login exitoso. Bienvenido Administrador!', 'success')
            return redirect(url_for("crud_moto"))
        else:
            flash('Login exitoso', 'success')
            return redirect("/login")
    else:
        flash('Error al logearse. Intente nuevamente', 'error')
        return render_template("login.html")

@app.route("/api_obteneradministrador")
@jwt_required()
def api_obteneradministrador():
    rpta = dict()
    try:
        listaadmin = list()
        administradores = controlador_administrador.obtener_administradores()

        for administrador in administradores:
            print(administrador)

            objAdmin = clsAdministrador(administrador[0], administrador[1], administrador[2])
            listaadmin.append(objAdmin.diccadmin)

        rpta["code"] = 1
        rpta["message"] = "Listado correcto de Administradores registrados"
        rpta["data"] = listaadmin
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
        return jsonify(rpta)


@app.route("/api_guardaradministrador", methods=["POST"])
@jwt_required()
def api_guardaradministrador():
    rpta = dict()
    try:
        cliente_id = request.json["cliente_id"]
        fecha_asignacion = request.json["fecha_asignacion"]

        idgenerado = controlador_administrador.insertar_administrador(cliente_id, fecha_asignacion)

        rpta["code"] = 1
        rpta["message"] = "Administrador registrado correctamente. "
        rpta["data"] = {"idgenerado" : idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return rpta

 ####APIS CLIENTE ####

@app.route("/api_obtener_cliente")
@jwt_required()
def api_obtener_cliente():
    response = dict()
    try:
        datos = []
        clientes = controlador_cliente.obtener_clientes()
        for cliente in clientes:
            if len(cliente) != 6:
                raise ValueError(f"Esperaba 6 elementos, pero recibí {len(cliente)} elementos: {cliente}")

            miobjcli = clsCliente(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], cliente[5])
            datos.append(miobjcli.obtenerObjetoSerializable())

        response["data"] = datos
        response["status"] = 1
        response["message"] = "Correcto listado de cliente"
    except Exception as e:
        response["data"] = []
        response["status"] = 0
        response["message"] = f"Problemas en el servicio web: {str(e)}"
    return jsonify(response)


@app.route("/api_guardar_cliente", methods=["POST"])
@jwt_required()
def api_guardar_cliente():
	try:
		nombre, apellidos, email, contraseña, telefono = (
			request.json["nombre"],
			request.json["apellidos"],
			request.json["email"],
			request.json["contraseña"],
			request.json["telefono"],
		)

		controlador_cliente.insertar_cliente(nombre, apellidos, email, contraseña, telefono)
		datos = []
		return jsonify({"data": datos, "code": 1, "message": "Cliente registrado correctamente"})
	except Exception as e:
		return jsonify({"data": None, "code": 0, "message": f"Error al registrar el vendedor: {str(e)}"}), 500









# ---------------MOTO------------------------
@app.route("/registrarMoto")
def formulario_registrar_moto():
    return render_template("registrarMoto.html")




@app.route("/guardar_moto", methods=["POST"])
def guardar_moto():
    try:
        codmoto = request.form["codmoto"]
        tipo = request.form["tipo"]
        posicionManejo = request.form["posicionManejo"]
        numAsientos = request.form["numAsientos"]
        numPasajeros = request.form["numPasajeros"]
        largo = request.form["largo"]
        ancho = request.form["ancho"]
        alto = request.form["alto"]
        tipoMotor = request.form["tipoMotor"]
        combustible = request.form["combustible"]
        numCilindros = request.form["numCilindros"]
        capacidadTanque = request.form["capacidadTanque"]
        rendimiento = request.form["rendimiento"]

        descripcion = request.form["descripcion"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        color = request.form["color"]
        imagen = request.files["uploadedFile"]
        imagen_codificada = urllib.parse.quote(imagen.filename)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], imagen_codificada)
        imagen.save(filepath)

        controlador_moto.insertar_moto(codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento)

        idMoto = controlador_moto.obtener_cod_moto(codmoto)

        controlador_producto.insertar_producto(descripcion, precio, stock, marca, modelo, color, imagen_codificada, idMoto, None)

        return redirect("/crud_producto")

    except Exception as e:
        error_message = f"Error al guardar la moto: {str(e)}"
        return error_message


@app.route("/api_obtenermotos")
@jwt_required()
def api_obtenermotos():
    rpta = dict()
    try:
        listamotos = list()
        motos = controlador_moto.obtener_motos_api()

        for moto in motos:
            print(moto)

            if len(moto) != 14:
                raise ValueError(f"Esperaba 14 elementos, pero recibí {len(moto)} elementos: {moto}")

            objMoto = clsMoto(moto[0], moto[1], moto[2],
                              moto[3], moto[4], moto[5],
                              moto[6], moto[7], moto[8],
                              moto[9], moto[10], moto[11],
                              moto[12], moto[13])
            listamotos.append(objMoto.diccmoto)

        rpta["code"] = 1
        rpta["message"] = "Listado correcto de Motos registradas"
        rpta["data"] = listamotos
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
        return jsonify(rpta)

@app.route("/api_guardarmoto", methods=["POST"])
@jwt_required()
def api_guardarmoto():
    rpta = dict()
    try:
        codmoto = request.json["codmoto"]
        tipo = request.json["tipo"]
        posicionManejo = request.json["posicionManejo"]
        numAsientos = request.json["numAsientos"]
        numPasajeros = request.json["numPasajeros"]
        largo = request.json["largo"]
        ancho = request.json["ancho"]
        alto = request.json["alto"]
        tipoMotor = request.json["tipoMotor"]
        combustible = request.json["combustible"]
        numCilindros = request.json["numCilindros"]
        capacidadTanque = request.json["capacidadTanque"]
        rendimiento = request.json["rendimiento"]
        idgenerado = controlador_moto.insertar_moto(codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento)

        rpta["code"] = 1
        rpta["message"] = "Moto registrado correctamente. "
        rpta["data"] = {"idgenerado" : idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return rpta


@app.route("/crud_moto")
@jwt_required()
def crud_moto():
    moto = controlador_moto.obtener_motos()
    return render_template("crud_moto.html", moto=moto)

@app.route("/formulario_editar_Moto/<int:id>")
def editar_moto(id):
    moto = controlador_moto.obtener_moto_por_id(id)
    return render_template("editar_moto.html", moto=moto)

@app.route("/eliminar_moto", methods=["POST"])
def eliminar_moto():
    controlador_moto.eliminar_moto(request.form["codmoto"])
    return redirect("/crud_moto.html")

# -----------Accesorio-----------------

@app.route("/registrarAccesorio")
def formulario_registrar_accesorio():
    return render_template("registrarAccesorio.html")

@app.route("/guardar_accesorio", methods=["POST"])
def guardar_accesorio():
    try:
        codaccesorio = request.form["codaccesorio"]
        tipo = request.form["tipo"]
        material = request.form["material"]
        descripcion = request.form["descripcion"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        color = request.form["color"]
        imagen = request.form["imagen"]

        controlador_accesorio.insertar_accesorio(codaccesorio, tipo, material)

        idAccesorio = controlador_accesorio.obtener_cod_accesorio(codaccesorio)

        controlador_producto.insertar_producto(descripcion, precio, stock, marca, modelo, color, imagen, None, idAccesorio)

        return redirect("/")

    except Exception as e:
        error_message = f"Error al guardar el accesorio: {str(e)}"
        return error_message

@app.route("/crud_accesorio")
def crud_accesorio():
    accesorios = controlador_accesorio.obtener_accesorios()
    return render_template("crud_accesorio.html", accesorios=accesorios)

@app.route("/eliminar_accesorio", methods=["POST"])
def eliminar_accesorio():
    controlador_accesorio.eliminar_accesorio(request.form["codaccesorio"])
    return redirect("/listar_Accesorio")

# -----------Producto-----------------

@app.route("/crud_producto")
def crud_producto():
    productosm = controlador_producto.obtener_moto_producto()
    return render_template("crud_producto.html", productosm=productosm)



@app.route("/detalle_producto_moto")
def formulario_detalle_producto():
    productosm = controlador_producto.obtener_moto_producto()
    return render_template("detalleProductoMoto.html" , productosm=productosm)

@app.route("/agregar_carrito", methods=["POST"])
def agregar_carrito():
    product_id = request.form.get('product_id', type=int)
    print(f"Product ID: {product_id}")  # Debug print
    cantidad = request.form.get('quantity', type=int)
    print(f"Quantity: {cantidad}")  # Debug print
    precio = float(request.form.get('precio'))
    print(f"Price: {precio}")  # Debug print
    nombre = request.form.get('nombre')
    print(f"Name: {nombre}")  # Debug print
    imagen = request.form.get('imagen')
    print(f"Image: {imagen}")  # Debug print

    if cantidad < 1:
        flash("La cantidad debe ser al menos uno.", "error")
        return redirect(url_for("detalle_producto_moto", id_producto=product_id))

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Primero, crea un nuevo carrito y obtén su ID
            cursor.execute("INSERT INTO CARRITO (/* campos necesarios */) VALUES (/* valores */)")
            idCarrito = cursor.lastrowid

            # Luego, inserta el ítem en el carrito
            cursor.execute("INSERT INTO ITEM_CARRITO (idCarrito, idProducto, cantidad, precioPorUnidad, subtotal) VALUES (%s, %s, %s, %s, %s)",
                           (idCarrito, product_id, cantidad, precio, cantidad * precio))
            conexion.commit()
            # flash("Producto agregado al carrito exitosamente!", "success")
    except Exception as e:
        print(f"Exception: {e}")  # Debug print
        flash("Error al agregar al carrito: {}".format(e), "error")
    finally:
        conexion.close()
        return redirect(url_for("detalle_producto_moto", id=product_id))

@app.route("/detalle_producto_categoria")
def formulario_detalle_categoria():
    productosm = controlador_producto.obtener_moto_producto()
    return render_template("categoriasresp.html" , productosm=productosm)



@app.route("/api_obteneritemcarrito")
@jwt_required()
def api_obteneritemcarrito():
    rpta = dict()
    try:
        listaitemcarrito = list()
        itemcarrito = controlador_carrito.obtener_carrito_api()

        if len(itemcarrito) == 0:
            rpta["code"] = 1
            rpta["message"] = "El carrito está vacío"
            rpta["data"] = listaitemcarrito
            return jsonify(rpta)

        for carrito in itemcarrito:
            objCarrito = clsItemCarrito(carrito[0], carrito[1], carrito[2],
                              carrito[3], carrito[4], carrito[5])
            listaitemcarrito.append(objCarrito.diccItemCarrito)

        rpta["code"] = 1
        rpta["message"] = "Listado correcto de items carrito"
        rpta["data"] = listaitemcarrito
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
        return jsonify(rpta)

@app.route("/api_guardarcarrito", methods=["POST"])
@jwt_required()
def api_guardarcarrito():
    rpta = dict()
    try:
        idCarrito = request.json["idCarrito"]
        idProducto = request.json["idProducto"]
        cantidad = request.json["cantidad"]
        precioPorUnidad = request.json["precioPorUnidad"]
        subtotal = request.json["subtotal"]
        idgenerado = controlador_carrito.insertar_carrito(idCarrito, idProducto, cantidad, precioPorUnidad, subtotal)

        rpta["code"] = 1
        rpta["message"] = "Item carrito registrado correctamente. "
        rpta["data"] = {"idgenerado" : idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return rpta




@app.route("/api_obtenerproductos")
@jwt_required()
def api_obtenerproductos():
    try:
        productos = controlador_producto.obtener_moto()
        # Convertir las tuplas a diccionarios directamente
        productos_lista = [{
            "idProducto": prod[0],
            "descripcion": prod[1],
            "precio": prod[2],
            "stock": prod[3],
            "marca": prod[4],
            "modelo": prod[5],
            "color": prod[6],
            "imagen": prod[7],
            "idMoto": prod[8],
            "idAccesorio": prod[9]
        } for prod in productos]
        return jsonify({
            "code": 200,
            "message": "Productos cargados exitosamente",
            "data": productos_lista
        })
    except Exception as e:
        return jsonify({
            "code": 404,
            "message": f"Error interno del servidor: {str(e)}",
            "data": []
        }), 404


@app.route("/listarProductoA")
@jwt_required()
def listar_productosA():
    productosa = controlador_producto.obtener_accesorio_producto()
    return render_template("listaProductoA.html", productosa=productosa)

@app.route("/eliminar_productoM", methods=["POST"])
def eliminar_productoM():
    controlador_producto.eliminar_producto(request.form["id"])
    return redirect("/crud_producto")

@app.route("/eliminar_productoA", methods=["POST"])
def eliminar_productoA():
    controlador_producto.eliminar_producto(request.form["id"])
    return redirect("/listar_ProductoA")



@app.route("/pago")
def formulario_pago():
    items = controlador_carrito.obtener_items_carrito()

    return render_template("pago.html", items=items)

@app.route("/actualizar_productoM", methods=["POST"])
def actualizar_productoM():
    idProducto = request.form["idProducto"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    color = request.form["color"]
    imagen = request.form["imagen"]
    codmoto = request.form["codmoto"]#10
    tipo = request.form["tipo"]
    posicionManejo = request.form["posicionManejo"]
    numAsientos = request.form["numAsientos"]
    numPasajeros = request.form["numPasajeros"]
    largo = request.form["largo"]
    ancho = request.form["ancho"]
    alto = request.form["alto"]
    tipoMotor = request.form["tipoMotor"]
    combustible = request.form["combustible"]
    numCilindros = request.form["numCilindros"]
    capacidadTanque = request.form["capacidadTanque"]
    rendimiento = request.form["rendimiento"]

    idMoto = controlador_moto.obtener_cod_moto(codmoto)
    idProducto = controlador_moto.obtener_cod_moto(codmoto)

    controlador_moto.actualizar_moto(codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento, idMoto)
    controlador_producto.actualizar_producto(descripcion, precio, stock, marca, modelo, color, imagen, idMoto, None, idProducto)
    return redirect("/crud_producto")

@app.route("/formulario_editar_productoM/<int:id>")
def editar_productoM(id):
    producto = controlador_producto.obtener_moto_producto_nuevo_one(id)
    return render_template("crud_producto.html", producto=producto)

@app.route("/actualizar_productoA", methods=["POST"])
def actualizar_productoA():
    idProducto = request.form["idProducto"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    color = request.form["color"]
    imagen = request.form["imagen"]
    codaccesorio = request.form["codaccesorio"]#8
    tipo = request.form["tipo"]
    material = request.form["material"]

    idAccesorio = controlador_accesorio.obtener_cod_accesorio(codaccesorio)
    idProducto = controlador_accesorio.obtener_cod_accesorio(codaccesorio)

    controlador_accesorio.actualizar_accesorio(tipo, material, codaccesorio,idAccesorio)
    controlador_producto.actualizar_producto(descripcion, precio, stock, marca, modelo, color, imagen, None, idAccesorio, idProducto)
    return redirect("/listar_ProductoA")

@app.route("/formulario_editar_productoA/<int:id>")
def editar_productoA(id):
    producto = controlador_producto.obtener_accesorio_producto_nuevo_one(id)
    return render_template("editarAccesorio.html", producto=producto)


@app.route("/formulario_detalle_producto_moto/<int:id>")
def detalle_producto_moto(id):
    productomoto = controlador_producto.obtener_moto_producto_nuevo(id)
    return render_template("detalleProductoMoto.html", productomoto=productomoto)

@app.route("/formulario_detalle_producto_accesorio/<int:id>")
def detalle_producto_accesorio(id):
    productoaccesorio = controlador_producto.obtener_accesorio_producto_nuevo(id)
    return render_template("detalleProductoAccesorio.html", productoaccesorio=productoaccesorio)

@app.route("/compra_exitosa")
def compra_exitosa():
    return render_template("compraexitosa.html")
# ---------------Venta------------------------
@app.route("/guardar_venta", methods=["POST"])
def guardar_venta():
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        pais = request.form["pais"]
        direccion = request.form["direccion"]
        region = request.form["departamento"]
        localidad = request.form["localidad"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        mes = request.form["mes"]
        año = request.form["año"]
        cvv = request.form["cvv"]
        numtarjeta = request.form["num_tarjeta"]
        idProducto = request.form["idProducto"]
        monto_final = request.form["monto_final"]

        controlador_pago.insertar_venta(nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final)

        return redirect("/compra_exitosa")


@app.route("/api_obtenerventa1")
@jwt_required()
def api_obtenerventa1():
    rpta = dict()
    try:
        listaventa1 = list()
        venta1 = controlador_pago.obtener_venta_por_id_api()

        if venta1 is None:
            venta1 = []

        if len(venta1) == 0:
            rpta["code"] = 1
            rpta["message"] = "No hay datos de venta disponibles"
            rpta["data"] = listaventa1
            return jsonify(rpta)

        for index, venta in enumerate(venta1):
            try:
                print(f"Procesando venta #{index}: {venta}")
                objVenta1 = clsItemCarrito(venta[0], venta[1], venta[2],
                              venta[3], venta[4], venta[5], venta[6], venta[7], venta[8],
                              venta[9], venta[10], venta[11], venta[12], venta[13], venta[14])
                listaventa1.append(objVenta1.diccVenta1)
            except Exception as e:
                print(f"Error procesando venta #{index}: {e}")
                raise e

        rpta["code"] = 1
        rpta["message"] = "Listado correcto de la venta"
        rpta["data"] = listaventa1
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
        return jsonify(rpta)

@app.route("/api_guardarventa", methods=["POST"])
@jwt_required()
def api_guardarventa():
    rpta = dict()
    try:
        nombre = request.json["nombre"]
        apellidos = request.json["apellidos"]
        pais = request.json["pais"]
        direccion = request.json["direccion"]
        region = request.json["region"]
        localidad = request.json["localidad"]
        telefono = request.json["telefono"]
        correo = request.json["correo"]
        mes = request.json["mes"]
        año = request.json["año"]
        cvv = request.json["cvv"]
        numtarjeta = request.json["numtarjeta"]
        idProducto = request.json["idProducto"]
        monto_final = request.json["monto_final"]
        idgenerado = controlador_pago.insertar_venta(nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final)

        rpta["code"] = 1
        rpta["message"] = "Venta1 registrada correctamente. "
        rpta["data"] = {"idgenerado" : idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return rpta




# Iniciar el servidor

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)