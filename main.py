from flask import Flask, render_template, request, redirect, flash, jsonify, url_for, session, json, make_response
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
from clases.clase_itemcarrito import clsItemCarrito
from clases.clase_venta1 import clsVenta1
from clases.clase_producto import clsProducto
from clases.clase_accesorio import clsAccesorio
from clases.clase_carrito import clsCarrito
from hashlib import sha256
import random

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

@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    controlador_cliente.eliminar_cliente(request.form["id"])
    return redirect("/")

@app.route("/crud_cliente")
def crud_cliente():
    clientes = controlador_cliente.obtener_clientes()
    return render_template("crud_cliente.html", clientes=clientes)

####### LOGIN ###########

@app.route("/login")
def formulario_login_cliente():
    email = request.cookies.get('email')
    token = request.cookies.get('token')

    if email and token:
        usuario = controlador_cliente.obtener_usuario_por_email(email)

        if usuario and usuario['token'] == token:
            session['user_id'] = usuario['id']
            session['is_admin'] = usuario['is_admin']
            productosm = controlador_producto.obtener_moto_producto()
            return render_template("categoriaresp.html", productosm=productosm)

    return render_template("login.html")

@app.route("/procesar_login", methods=["POST"])
def procesar_login():
    email = request.form["email"]
    contraseña = request.form["contraseña"]

    epassword = sha256(contraseña.encode("utf-8")).hexdigest()
    usuario = controlador_cliente.obtener_usuario_por_email(email)

    if usuario and usuario['contraseña'] == epassword:
        aleatorio = str(random.randint(1, 1024))
        token = sha256(aleatorio.encode("utf-8")).hexdigest()

        session['user_id'] = usuario['id']
        session['is_admin'] = usuario['is_admin']

        resp = redirect("/crud_moto") if usuario['is_admin'] else redirect("/login")
        resp.set_cookie('email', email)
        resp.set_cookie('token', token)
        controlador_cliente.actualizar_token(email, token)

        return resp
    else:
        flash('Error al logearse. Intente nuevamente', 'error')
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    resp = make_response(redirect("/login"))
    resp.set_cookie('token', '', expires=0)
    return resp

######### REGISTRO #########
@app.route("/guardar_cliente", methods=["POST"])
def guardar_cliente():
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    contraseña = request.form["contraseña"]

    epassword = sha256(contraseña.encode("utf-8")).hexdigest()

    controlador_cliente.insertar_cliente(nombre, apellidos, email, epassword, telefono)
    return redirect("/login")


########### APIS ADMINISTRADOR ############

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

@app.route("/api_eliminar_administrador/<int:id_admin>", methods=["DELETE"])
@jwt_required()
def api_eliminar_administrador(id_admin):
    rpta = dict()
    try:
        controlador_administrador.eliminar_administrador(id_admin)
        rpta["code"] = 1
        rpta["message"] = "Administrador eliminado correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)

@app.route("/api_editar_administrador/<int:id_admin>", methods=["PUT"])
@jwt_required()
def api_actualizar_administrador(id_admin):
    rpta = dict()
    try:
        datos = request.json
        controlador_administrador.actualizar_administrador(
            datos["cliente_id"], datos["fecha_asignacion"], id_admin
        )
        rpta["code"] = 1
        rpta["message"] = "Administrador actualizado correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)

@app.route("/api_obtener_administrador_por_id/<int:id_admin>", methods=["GET"])
@jwt_required()
def api_obtener_administrador(id_admin):
    rpta = dict()
    try:
        admin = controlador_administrador.obtener_administrador_por_id(id_admin)
        if admin:
            objAdmin = clsAdministrador(admin[0], admin[1], admin[2])
            rpta["code"] = 1
            rpta["message"] = "Administrador obtenido correctamente."
            rpta["data"] = objAdmin.diccadmin
        else:
            rpta["code"] = 0
            rpta["message"] = "Administrador no encontrado."
            rpta["data"] = dict()
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
        rpta["data"] = dict()
    return jsonify(rpta)

####

##### APIS CLIENTE ####

@app.route("/api_obtener_cliente")
@jwt_required()
def api_obtener_cliente():
    rpta = dict()
    try:
        listaclientes = list()
        clientes = controlador_cliente.obtener_clientes()

        for cliente in clientes:
            objCliente = clsCliente(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], cliente[5])
            listaclientes.append(objCliente.dicctemp)

        rpta["code"] = 1
        rpta["message"] = "Listado correcto de Clientes registrados"
        rpta["data"] = listaclientes
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
        return jsonify(rpta)

@app.route("/api_guardar_cliente", methods=["POST"])
@jwt_required()
def api_guardar_cliente():
    rpta = dict()
    try:
        nombre = request.json["nombre"]
        apellidos = request.json["apellidos"]
        email = request.json["email"]
        contraseña = request.json["contraseña"]
        telefono = request.json["telefono"]
        idgenerado = controlador_cliente.insertar_cliente(nombre, apellidos, email, contraseña, telefono)

        rpta["code"] = 1
        rpta["message"] = "Cliente registrado correctamente."
        rpta["data"] = {"idgenerado": idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return jsonify(rpta)

@app.route("/api_eliminar_cliente/<int:id_cliente>", methods=["DELETE"])
@jwt_required()
def api_eliminar_cliente(id_cliente):
    rpta = dict()
    try:
        controlador_cliente.eliminar_cliente(id_cliente)
        rpta["code"] = 1
        rpta["message"] = "Cliente eliminado correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)

@app.route("/api_editar_cliente/<int:id_cliente>", methods=["PUT"])
@jwt_required()
def api_editar_cliente(id_cliente):
    rpta = dict()
    try:
        datos = request.json
        controlador_cliente.actualizar_cliente(
            datos["nombre"], datos["apellidos"], datos["email"], datos["contraseña"], datos["telefono"], id_cliente
        )
        rpta["code"] = 1
        rpta["message"] = "Cliente actualizado correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)

@app.route("/api_obtener_cliente_por_id/<int:id_cliente>", methods=["GET"])
@jwt_required()
def api_obtener_cliente_por_id(id_cliente):
    rpta = dict()
    try:
        cliente = controlador_cliente.obtener_cliente_por_id(id_cliente)
        if cliente:
            objCliente = clsCliente(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], cliente[5])
            rpta["code"] = 1
            rpta["message"] = "Cliente obtenido correctamente."
            rpta["data"] = objCliente.dicctemp
        else:
            rpta["code"] = 0
            rpta["message"] = "Cliente no encontrado."
            rpta["data"] = dict()
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
        rpta["data"] = dict()
    return jsonify(rpta)

#######



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

######### APIS MOTO #################

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

@app.route("/api_eliminar_moto/<int:id_moto>", methods=["DELETE"])
@jwt_required()
def api_eliminar_moto(id_moto):
    rpta = dict()
    try:
        controlador_moto.eliminar_moto(id_moto)
        rpta["code"] = 1
        rpta["message"] = f"Moto eliminada correctamente. ID: {id_moto}"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)

@app.route("/api_editar_moto/<int:id_moto>", methods=["PUT"])
@jwt_required()
def api_editar_moto(id_moto):
    rpta = dict()
    try:
        datos = request.json
        controlador_moto.actualizar_moto(
            datos["codmoto"], datos["tipo"], datos["posicionManejo"], datos["numAsientos"],
            datos["numPasajeros"], datos["largo"], datos["ancho"], datos["alto"],
            datos["tipoMotor"], datos["combustible"], datos["numCilindros"],
            datos["capacidadTanque"], datos["rendimiento"], id_moto
        )
        rpta["code"] = 1
        rpta["message"] = "Moto actualizada correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)

@app.route("/api_obtener_moto_por_id/<int:id_moto>", methods=["GET"])
@jwt_required()
def api_obtener_moto_por_id(id_moto):
    rpta = dict()
    try:
        moto = controlador_moto.obtener_moto_por_id(id_moto)
        if moto:
            objMoto = clsMoto(
                moto[0], moto[1], moto[2], moto[3], moto[4], moto[5],
                moto[6], moto[7], moto[8], moto[9], moto[10], moto[11],
                moto[12], moto[13]
            )
            rpta["code"] = 1
            rpta["message"] = "Moto obtenida correctamente."
            rpta["data"] = objMoto.diccmoto
        else:
            rpta["code"] = 0
            rpta["message"] = "Moto no encontrada."
            rpta["data"] = dict()
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
        rpta["data"] = dict()
    return jsonify(rpta)


######

@app.route("/crud_moto")
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

######## APIS ACCESORIOS ##############

@app.route("/api_obtener_accesorios")
@jwt_required()
def api_obtener_accesorios():
    rpta = dict()
    try:
        listaaccesorios = list()
        accesorios = controlador_accesorio.obtener_accesorios_api()

        for accesorio in accesorios:

            objAccesorio = clsAccesorio(accesorio[0], accesorio[1], accesorio[2],
                              accesorio[3])
            listaaccesorios.append(objAccesorio.diccaccesorio)

        rpta["code"] = 1
        rpta["message"] = "Listado correcto de Accesorios registradas"
        rpta["data"] = listaaccesorios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
        return jsonify(rpta)

@app.route("/api_guardaraccesorio", methods=["POST"])
@jwt_required()
def api_guardaraccesorio():
    rpta = dict()
    try:
        codaccesorio = request.json["codaccesorio"]
        tipo = request.json["tipo"]
        material = request.json["material"]

        idgenerado = controlador_accesorio.insertar_accesorio(codaccesorio, tipo, material)

        rpta["code"] = 1
        rpta["message"] = "Accesorio registrado correctamente. "
        rpta["data"] = {"idgenerado" : idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return rpta


@app.route("/api_eliminar_accesorio/<int:id_accesorio>", methods=["DELETE"])
@jwt_required()
def api_eliminar_accesorio(id_accesorio):
    rpta = dict()
    try:
        controlador_accesorio.eliminar_accesorio_api(id_accesorio)
        rpta["code"] = 1
        rpta["message"] = "Accesorio eliminado correctamente."
        rpta["data"] = dict()
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
        rpta["data"] = dict()
    return jsonify(rpta)


@app.route("/api_editar_accesorio/<int:id_accesorio>", methods=["PUT"])
@jwt_required()
def api_editar_accesorio(id_accesorio):
    rpta = dict()
    try:
        codaccesorio = request.json["codaccesorio"]
        tipo = request.json["tipo"]
        material = request.json["material"]

        controlador_accesorio.actualizar_accesorio(codaccesorio, tipo, material, id_accesorio)

        rpta["code"] = 1
        rpta["message"] = "Accesorio actualizado correctamente."
        rpta["data"] = dict()
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return jsonify(rpta)

@app.route("/api_obtener_accesorio_por_id/<int:id_accesorio>", methods=["GET"])
@jwt_required()
def api_obtener_accesorio_por_id(id_accesorio):
    rpta = dict()
    try:
        accesorio = controlador_accesorio.obtener_accesorio_por_id(id_accesorio)
        if accesorio:
            objAccesorio = clsAccesorio(
                accesorio[0], accesorio[1], accesorio[2], accesorio[3]
            )
            rpta["code"] = 1
            rpta["message"] = "Accesorio obtenido correctamente."
            rpta["data"] = objAccesorio.diccaccesorio
        else:
            rpta["code"] = 0
            rpta["message"] = "Accesorio no encontrado."
            rpta["data"] = dict()
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
        rpta["data"] = dict()
    return jsonify(rpta)

#############


# -----------Producto-----------------

@app.route("/crud_producto")
def crud_producto():
    productosm = controlador_producto.obtener_moto_producto()
    return render_template("crud_producto.html", productosm=productosm)



@app.route("/detalle_producto_moto")
def formulario_detalle_producto():
    productosm = controlador_producto.obtener_moto_producto()
    return render_template("detalleProductoMoto.html" , productosm=productosm)

############## API CARRITO #############

@app.route("/api_obtener_carrito")
@jwt_required()
def api_obtener_carrito():
    rpta = dict()
    try:
        listacarrito = list()
        carritos = controlador_carrito.obtener_carrito_api_an()

        for carrito in carritos:

            objCarrito = clsCarrito(carrito[0], carrito[1], carrito[2])
            listacarrito.append(objCarrito.dicccarrito)

        rpta["code"] = 1
        rpta["message"] = "Listado correcto de detalle del carrito registradas"
        rpta["data"] = listacarrito
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
        return jsonify(rpta)


@app.route("/api_guardar_carrito", methods=["POST"])
@jwt_required()
def api_guardar_carrito():
    rpta = dict()
    try:
        idCliente = request.json["idCliente"]
        fechaCreacion = request.json["fechaCreacion"]

        idgenerado = controlador_carrito.insertar_carrito_api(idCliente, fechaCreacion)

        rpta["code"] = 1
        rpta["message"] = "Carrito registrado correctamente. "
        rpta["data"] = {"idgenerado" : idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return rpta

@app.route("/api_eliminar_carrito/<int:id_carrito>", methods=["DELETE"])
@jwt_required()
def api_eliminar_carrito(id_carrito):
    rpta = dict()
    try:
        controlador_carrito.eliminar_carrito(id_carrito)
        rpta["code"] = 1
        rpta["message"] = "Carrito eliminado correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)

@app.route("/api_obtener_carrito_id/<int:id_carrito>", methods=["GET"])
@jwt_required()
def api_obtener_carrito_id(id_carrito):
    rpta = dict()
    try:
        carrito = controlador_carrito.obtener_carrito_id(id_carrito)
        if carrito:
            objCarrito = clsCarrito(
                carrito[0], carrito[1], carrito[2]
            )
            rpta["code"] = 1
            rpta["message"] = "Carrito obtenido correctamente."
            rpta["data"] = objCarrito.dicccarrito
        else:
            rpta["code"] = 0
            rpta["message"] = "Carrito no encontrado."
            rpta["data"] = dict()
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
        rpta["data"] = dict()
    return jsonify(rpta)


@app.route("/api_editar_carrito/<int:id_carrito>", methods=["PUT"])
@jwt_required()
def api_editar_carrito(id_carrito):
    rpta = dict()
    try:
        datos = request.json
        controlador_carrito.modificar_carrito(id_carrito, datos["idCliente"], datos["fechaCreacion"])
        rpta["code"] = 1
        rpta["message"] = "Carrito modificado correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)


######


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
    return render_template("categoriaresp.html" , productosm=productosm)

########   APIS ITEM CARRITO   ##############

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


########   PRODUCTO   ##############

@app.route("/api_obtenerproductos")
@jwt_required()
def api_obtenerproductos():
    rpta = dict()
    try:
        listaproductos = list()
        productos = controlador_producto.obtener_producto_api()

        for producto in productos:

            objProducto = clsProducto(producto[0], producto[1], producto[2],
                              producto[3], producto[4], producto[5],
                              producto[6], producto[7], producto[8],
                              producto[9])
            listaproductos.append(objProducto.dicctemp)

        rpta["code"] = 1
        rpta["message"] = "Listado correcto de Productos registradas"
        rpta["data"] = listaproductos
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
        return jsonify(rpta)

@app.route("/api_guardar_producto", methods=["POST"])
@jwt_required()
def api_guardar_producto():
    rpta = dict()
    try:
        descripcion = request.json["descripcion"]
        precio = request.json["precio"]
        stock = request.json["stock"]
        marca = request.json["marca"]
        modelo = request.json["modelo"]
        color = request.json["color"]
        imagen = request.json["imagen"]
        idMoto = request.json["idMoto"]
        idAccesorio = request.json["idAccesorio"]
        idgenerado = controlador_producto.insertar_producto(descripcion, precio, stock, marca, modelo, color, imagen, idMoto, idAccesorio)

        rpta["code"] = 1
        rpta["message"] = "Producto registrado correctamente."
        rpta["data"] = {"idgenerado": idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return jsonify(rpta)

@app.route("/api_eliminar_producto/<int:id_producto>", methods=["DELETE"])
@jwt_required()
def api_eliminar_producto(id_producto):
    rpta = dict()
    try:
        controlador_producto.eliminar_producto(id_producto)
        rpta["code"] = 1
        rpta["message"] = "Producto eliminado correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
    return jsonify(rpta)

@app.route("/api_editar_producto/<int:id_producto>", methods=["PUT"])
@jwt_required()
def api_editar_producto(id_producto):
    rpta = dict()
    try:
        descripcion = request.json["descripcion"]
        precio = request.json["precio"]
        stock = request.json["stock"]
        marca = request.json["marca"]
        modelo = request.json["modelo"]
        color = request.json["color"]
        imagen = request.json["imagen"]
        idMoto = request.json["idMoto"]
        idAccesorio = request.json["idAccesorio"]

        controlador_producto.actualizar_producto(descripcion, precio, stock, marca, modelo, color, imagen, idMoto, idAccesorio, id_producto)

        rpta["code"] = 1
        rpta["message"] = "Producto actualizado correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
        rpta["data"] = dict()
    return jsonify(rpta)

@app.route("/api_obtener_producto_por_id/<int:id_producto>", methods=["GET"])
@jwt_required()
def api_obtener_producto_por_id(id_producto):
    rpta = dict()
    try:
        producto = controlador_producto.obtener_producto_por_id(id_producto)
        if producto:
            objProducto = clsProducto(producto[0], producto[1], producto[2], producto[3], producto[4], producto[5], producto[6], producto[7], producto[8], producto[9])
            rpta["code"] = 1
            rpta["message"] = "Producto encontrado correctamente."
            rpta["data"] = objProducto.dicctemp
        else:
            rpta["code"] = 0
            rpta["message"] = "Producto no encontrado."
            rpta["data"] = dict()
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
        rpta["data"] = dict()
    return jsonify(rpta)


###

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