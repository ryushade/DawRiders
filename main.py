from flask import Flask, render_template, request, redirect, flash, jsonify, url_for, session, json, make_response
from flask_login import login_user
from flask_jwt import JWT, jwt_required, current_identity

from datetime import datetime, timedelta
from functools import wraps

from bd import obtener_conexion
import time

import urllib
import os
from controladores import controlador_pago
from controladores import controlador_cliente
from controladores import controlador_moto
from controladores import controlador_producto
from controladores import controlador_accesorio
from controladores import controlador_carrito
from controladores import controlador_administrador
from controladores import controlador_users
from controladores import controlador_item_carrito
from clases.clase_moto import clsMoto
from clases.clase_cliente import clsCliente
from clases.clase_administrador import clsAdministrador
from clases.clase_itemcarrito import clsItemCarrito
from clases.clase_producto import clsProducto
from clases.clase_accesorio import clsAccesorio
from clases.clase_carrito import clsCarrito
from clases.clase_venta1 import clsVenta
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

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/historial_venta")
def formulario_historial_venta():
    email = request.cookies.get('email')
    token = request.cookies.get('token')
    if not email or not token or 'user_id' not in session:
        flash('Por favor, inicie sesión para ver esta página.', 'error')
        return redirect(url_for("formulario_login_cliente"))

    id_cliente = session['user_id']
    cliente = controlador_cliente.obtener_cliente_por_id(id_cliente)
    ventas = controlador_pago.obtener_ventas_por_cliente(id_cliente)

    ventas_agrupadas = {}
    for venta in ventas:
        codigo_venta = venta[7]
        if codigo_venta not in ventas_agrupadas:
            ventas_agrupadas[codigo_venta] = {
                'fecha_venta': venta[6],
                'productos': []
            }
        ventas_agrupadas[codigo_venta]['productos'].append(venta)

    return render_template("historial_venta.html", ventas_agrupadas=ventas_agrupadas, cliente=cliente)



@app.route("/administrador")
def formulario_administrador():
    return render_template("administrador.html")

@app.route("/contacto")
def formulario_contacto():
    return render_template("contacto.html")

@app.route("/libroreclamaciones")
def formulario_libro():
    return render_template("libroreclamaciones.html")

@app.route("/terminos")
def formulario_terminos():
    return render_template("terminosGarantia.html")

@app.route("/dashboard")
def dashboard():
    return render_template('index_d.html')

@app.route("/comparar")
def formulario_comparar():
    return render_template("comparar.html")


@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    controlador_cliente.eliminar_cliente(request.form["id"])
    return redirect("/")

@app.route("/crud_cliente")
def crud_cliente():
    clientes = controlador_cliente.obtener_clientes()
    return render_template("crud_cliente.html", clientes=clientes)

@app.route("/actualizar_cliente", methods=['POST'])
def actualizar_cliente():
    id_cliente = request.form['idCliente']
    nombre = request.form['nombre']
    apellidos = request.form['apellido']
    email = request.form['email']
    telefono = request.form['telefono']
    contraseña_actual = request.form['contra']

    contraseña_actual_encrypted = sha256(contraseña_actual.encode("utf-8")).hexdigest()

    contraseña_guardada = controlador_cliente.obtener_contrasena_por_email(email)

    if contraseña_actual_encrypted == contraseña_guardada:
        controlador_cliente.actualizar_cliente(nombre, apellidos, email, contraseña_actual_encrypted, telefono, id_cliente)

        flash('La información del cliente ha sido actualizada correctamente.')
    else:
        flash('La contraseña actual no es correcta.')

    return redirect("/historial_venta")

@app.route("/actualizar_contra", methods=['POST'])
def actualizar_contra():
    email = request.form['email']
    contraseña_actual = request.form['current-password']
    nueva_contrasena = request.form['new-password']

    contraseña_actual_encrypted = sha256(contraseña_actual.encode("utf-8")).hexdigest()
    contraseña_guardada = controlador_cliente.obtener_contrasena_por_email(email)

    if contraseña_actual_encrypted == contraseña_guardada:
        nueva_contrasena_encrypted = sha256(nueva_contrasena.encode("utf-8")).hexdigest()
        controlador_cliente.actualizar_cliente_contra(email, nueva_contrasena_encrypted)

        flash('La contraseña ha sido actualizada correctamente.')
    else:
        flash('La contraseña actual no es correcta.')
    return redirect("/historial_venta")

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
        session['user_name'] = usuario['nombre']
        session['is_admin'] = usuario['is_admin']
        print("Usuario logueado:", session['user_name'])

        resp = redirect("/crud_producto") if usuario['is_admin'] else redirect("/login")
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


    if not controlador_cliente.insertar_cliente(nombre, apellidos, email, epassword, telefono):
        flash('El email o teléfono ya está registrado. Por favor, intente con otros.', 'error')
        return redirect(url_for('formulario_registro'))  # Asegúrate de redirigir al formulario de registro
    else:
        return redirect("/login")


@app.route("/guardar_clienteC", methods=["POST"])
def guardar_clienteC():
    nombre = request.form["nombre"]
    apellidos = request.form["apellidos"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    contraseña = request.form["contraseña"]

    # Cifrado de contraseña
    epassword = sha256(contraseña.encode("utf-8")).hexdigest()
    # Intentar insertar el cliente nuevo
    if not controlador_cliente.insertar_cliente(nombre, apellidos, email, epassword, telefono):
        flash('El teléfono ya está registrado. Por favor, intente con otro.', 'error')
        return redirect("/crud_cliente")

    flash('Cliente agregado exitosamente!', 'success')
    return redirect("/crud_cliente")


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
        return jsonify(rpta)


@app.route("/api_guardaradministrador", methods=["POST"])
@jwt_required()
def api_guardaradministrador():
    rpta = dict()
    try:
        cliente_id = request.json["cliente_id"]
        fecha_asignacion = request.json["fecha_asignacion"]

        idgenerado = controlador_administrador.insertar_administrador_api(cliente_id, fecha_asignacion)

        rpta["code"] = 1
        rpta["message"] = "Administrador registrado correctamente. "
        rpta["data"] = {"idgenerado" : idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
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
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
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
        idgenerado = controlador_cliente.insertar_cliente_api(nombre, apellidos, email, contraseña, telefono)

        rpta["code"] = 1
        rpta["message"] = "Cliente registrado correctamente."
        rpta["data"] = {"idgenerado": idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
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
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
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
        idgenerado = controlador_moto.insertar_moto_api(codmoto, tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento)

        rpta["code"] = 1
        rpta["message"] = "Moto registrado correctamente. "
        rpta["data"] = {"idgenerado" : idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
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
            datos["tipo"], datos["posicionManejo"], datos["numAsientos"],
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
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)


######

@app.route("/crud_producto")
def crud_producto():
    if 'user_id' in session and session['is_admin']:
        productosm = controlador_producto.obtener_moto_producto()
        return render_template("crud_producto.html", productosm=productosm)
    else:
        flash("Acceso denegado. Debe ser administrador para acceder a esta página.", "error")
        return redirect(url_for("formulario_login_cliente"))



# -----------Accesorio-----------------

@app.route("/registrarAccesorio")
def formulario_registrar_accesorio():
    return render_template("registrarAccesorio.html")

@app.route("/guardar_accesorio", methods=["POST"])
def guardar_accesorio():
    try:
        codaccesorio = request.form["codAccesorio"]
        tipo = request.form["tipo"]
        material = request.form["material"]
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

        controlador_accesorio.insertar_accesorio(codaccesorio, tipo, material)

        idAccesorio = controlador_accesorio.obtener_cod_accesorio(codaccesorio)

        controlador_producto.insertar_producto(descripcion, precio, stock, marca, modelo, color, imagen_codificada, None, idAccesorio)

        return redirect("/crud_accesorio")

    except Exception as e:
        error_message = f"Error al guardar el accesorio: {str(e)}"
        return error_message

@app.route("/crud_accesorio")
def crud_accesorio():
    accesorios = controlador_producto.obtener_accesorio_producto()
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
        return jsonify(rpta)

@app.route("/api_guardaraccesorio", methods=["POST"])
@jwt_required()
def api_guardaraccesorio():
    rpta = dict()
    try:
        codaccesorio = request.json["codaccesorio"]
        tipo = request.json["tipo"]
        material = request.json["material"]

        idgenerado = controlador_accesorio.insertar_accesorio_api(codaccesorio, tipo, material)

        rpta["code"] = 1
        rpta["message"] = "Accesorio registrado correctamente. "
        rpta["data"] = {"idgenerado" : idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return rpta


@app.route("/api_eliminar_accesorio/<int:id_accesorio>", methods=["DELETE"])
@jwt_required()
def api_eliminar_accesorio(id_accesorio):
    rpta = dict()
    try:
        controlador_accesorio.eliminar_accesorio_api(id_accesorio)
        rpta["code"] = 1
        rpta["message"] = "Accesorio eliminado correctamente."
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
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
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: " + repr(e)
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
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
    return jsonify(rpta)

#############


# -----------Producto-----------------


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
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Ocurrió un problema: {str(e)}"
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

@app.route("/carrito")
def formulario_carrito():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para ver tu carrito.", "error")
        return redirect(url_for("formulario_login_cliente"))

    id_cliente = session['user_id']
    carrito = controlador_carrito.obtener_carrito_por_cliente_id(id_cliente)
    if not carrito:
        id_carrito = controlador_carrito.crear_carrito_para_cliente(id_cliente)
    else:
        id_carrito = carrito[0]

    items = controlador_carrito.obtener_items_carrito_por_id_carrito(id_carrito)
    return render_template("carritoCompra.html", items=items)


@app.route("/agregar_carrito", methods=["POST"])
def agregar_carrito():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para agregar productos al carrito.", "error")
        return redirect(url_for("formulario_login_cliente"))

    product_id = request.form.get('product_id', type=int)
    cantidad = request.form.get('quantity', type=int)
    precio = float(request.form.get('precio'))
    nombre = request.form.get('nombre')
    imagen = request.form.get('imagen')

    if cantidad < 1:
        flash("La cantidad debe ser al menos uno.", "error")
        return redirect(url_for("detalle_producto_moto", id=product_id))

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT stock FROM PRODUCTO WHERE idProducto = %s", (product_id,))
            stock = cursor.fetchone()[0]
            if cantidad > stock:
                flash("No hay suficiente stock para la cantidad solicitada.", "error")
                return redirect(url_for("detalle_producto_moto", id=product_id))

            id_cliente = session['user_id']
            cursor.execute("SELECT idCarrito FROM CARRITO WHERE idCliente = %s", (id_cliente,))
            carrito = cursor.fetchone()
            if carrito:
                idCarrito = carrito[0]
            else:
                cursor.execute("INSERT INTO CARRITO (idCliente, fechaCreacion) VALUES (%s, NOW())", (id_cliente,))
                idCarrito = cursor.lastrowid

            # Verificar si el producto ya está en el carrito
            cursor.execute("SELECT cantidad FROM ITEM_CARRITO WHERE idCarrito = %s AND idProducto = %s", (idCarrito, product_id))
            item = cursor.fetchone()
            if item:
                nueva_cantidad = item[0] + cantidad
                nuevo_subtotal = nueva_cantidad * precio
                cursor.execute("UPDATE ITEM_CARRITO SET cantidad = %s, subtotal = %s WHERE idCarrito = %s AND idProducto = %s",
                               (nueva_cantidad, nuevo_subtotal, idCarrito, product_id))
            else:
                cursor.execute("INSERT INTO ITEM_CARRITO (idCarrito, idProducto, cantidad, precioPorUnidad, subtotal) VALUES (%s, %s, %s, %s, %s)",
                               (idCarrito, product_id, cantidad, precio, cantidad * precio))

            conexion.commit()
            flash("Producto agregado al carrito exitosamente!", "success")
    except Exception as e:
        print(f"Exception: {e}")
        flash("Error al agregar al carrito: {}".format(e), "error")
    finally:
        conexion.close()
        return redirect(url_for("detalle_producto_moto", id=product_id))


@app.route("/agregar_carrito_accesorio", methods=["POST"])
def agregar_carrito_accesorio():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para agregar productos al carrito.", "error")
        return redirect(url_for("formulario_login_cliente"))

    product_id = request.form.get('product_id', type=int)
    cantidad = request.form.get('quantity', type=int)
    precio = float(request.form.get('precio'))
    nombre = request.form.get('nombre')
    imagen = request.form.get('imagen')

    if cantidad < 1:
        flash("La cantidad debe ser al menos uno.", "error")
        return redirect(url_for("detalle_producto_moto", id=product_id))

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT stock FROM PRODUCTO WHERE idProducto = %s", (product_id,))
            stock = cursor.fetchone()[0]
            if cantidad > stock:
                flash("No hay suficiente stock para la cantidad solicitada.", "error")
                return redirect(url_for("detalle_producto_accesorio", id=product_id))

            id_cliente = session['user_id']
            cursor.execute("SELECT idCarrito FROM CARRITO WHERE idCliente = %s", (id_cliente,))
            carrito = cursor.fetchone()
            if carrito:
                idCarrito = carrito[0]
            else:
                cursor.execute("INSERT INTO CARRITO (idCliente, fechaCreacion) VALUES (%s, NOW())", (id_cliente,))
                idCarrito = cursor.lastrowid


            cursor.execute("INSERT INTO ITEM_CARRITO (idCarrito, idProducto, cantidad, precioPorUnidad, subtotal) VALUES (%s, %s, %s, %s, %s)",
                           (idCarrito, product_id, cantidad, precio, cantidad * precio))
            conexion.commit()
            flash("Producto agregado al carrito exitosamente!", "success")
    except Exception as e:
        print(f"Exception: {e}")
        flash("Error al agregar al carrito: {}".format(e), "error")
    finally:
        conexion.close()
        return redirect(url_for("detalle_producto_accesorio", id=product_id))



@app.route("/eliminar_item_carrito/<int:id_item>", methods=["POST"])
def eliminar_item_carrito(id_item):
    if 'user_id' not in session:
        return jsonify({"error": "No has iniciado sesión"}), 401

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM ITEM_CARRITO WHERE idItemCarrito = %s", (id_item,))
            if cursor.rowcount == 0:
                return jsonify({"error": "No se encontró el ítem a eliminar"}), 404
            conexion.commit()
            return jsonify({"success": "Producto eliminado correctamente del carrito."}), 200
    except Exception as e:
        conexion.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conexion.close()


@app.route("/detalle_producto_categoria")
def formulario_detalle_categoria():
    productosm = controlador_producto.obtener_moto_producto()
    return render_template("categoriaresp.html" , productosm=productosm)

@app.route("/detalle_producto_accesorio")
def formulario_detalle_accesorio():
    productosacc = controlador_producto.obtener_accesorio_producto()
    return render_template("categoriaAccesorio.html" , productosacc=productosacc)

########   APIS ITEM CARRITO   ##############

@app.route("/api_obtener_items_carrito")
@jwt_required()
def api_obtener_items_carrito():
    respuesta = dict()
    try:
        lista_items = []
        items_carrito = controlador_item_carrito.obtener_items_carrito()

        for item in items_carrito:
            objItem = clsItemCarrito(item[0], item[1], item[2], item[3], item[4], item[5])
            lista_items.append(objItem.dicItemCarrito)

        respuesta["code"] = 1
        respuesta["message"] = "Listado correcto de ítems en el carrito"
        respuesta["data"] = lista_items
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Problemas en el servicio web: {str(e)}"
        respuesta["data"] = dict()
        return jsonify(respuesta)

@app.route("/api_guardar_item_carrito", methods=["POST"])
@jwt_required()
def api_guardar_item_carrito():
    respuesta = dict()
    try:
        nuevo_item = clsItemCarrito(**request.json)
        id_generado = controlador_item_carrito.insertar_item_carrito(nuevo_item)

        respuesta["code"] = 1
        respuesta["message"] = "Ítem registrado correctamente."
        respuesta["data"] = {"idGenerado": id_generado}
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Ocurrió un problema: {repr(e)}"
        respuesta["data"] = dict()
        return jsonify(respuesta)

@app.route("/api_eliminar_item_carrito/<int:id_item>", methods=["DELETE"])
@jwt_required()
def api_eliminar_item_carrito(id_item):
    respuesta = dict()
    try:
        controlador_item_carrito.eliminar_item_carrito(id_item)
        respuesta["code"] = 1
        respuesta["message"] = "Ítem eliminado correctamente."
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Ocurrió un problema: {str(e)}"
        return jsonify(respuesta)

@app.route("/api_actualizar_item_carrito/<int:id_item>", methods=["PUT"])
@jwt_required()
def api_actualizar_item_carrito(id_item):
    respuesta = dict()
    try:
        datos = request.json
        controlador_item_carrito.editar_item_carrito(id_item, **datos)
        respuesta["code"] = 1
        respuesta["message"] = "Ítem actualizado correctamente."
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Ocurrió un problema: {str(e)}"
        return jsonify(respuesta)

@app.route("/api_obtener_item_carrito_por_id/<int:id_item>", methods=["GET"])
@jwt_required()
def api_obtener_item_carrito_por_id(id_item):
    respuesta = dict()
    try:
        item = controlador_item_carrito.obtener_item_carrito_por_id(id_item)
        if item:
            objItem = clsItemCarrito(item[0], item[1], item[2], item[3], item[4], item[5])
            respuesta["code"] = 1
            respuesta["message"] = "Ítem obtenido correctamente."
            respuesta["data"] = objItem.dicItemCarrito
        else:
            respuesta["code"] = 0
            respuesta["message"] = "Ítem no encontrado."
            respuesta["data"] = dict()
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Ocurrió un problema: {str(e)}"
        respuesta["data"] = dict()
        return jsonify(respuesta)


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
        idgenerado = controlador_producto.insertar_producto_api(descripcion, precio, stock, marca, modelo, color, imagen, idMoto, idAccesorio)

        rpta["code"] = 1
        rpta["message"] = "Producto registrado correctamente."
        rpta["data"] = {"idgenerado": idgenerado}

    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
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
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {str(e)}"
    return jsonify(rpta)


###

@app.route("/listarProductoA")
@jwt_required()
def listar_productosA():
    productosa = controlador_producto.obtener_accesorio_producto()
    return render_template("listaProductoA.html", productosa=productosa)

@app.route("/eliminar_productoM", methods=["POST"])
def eliminar_productoM():
    try:
        producto_id = request.form.get('id')
        if not producto_id:
            raise ValueError("ID de producto no proporcionado")

        codMoto = controlador_producto.obtener_codmoto_porid_producto(producto_id)
        if not codMoto:
            raise ValueError("Código de moto no encontrado para el ID de producto dado")

        controlador_pago.eliminar_venta_pr(producto_id)
        controlador_producto.eliminar_producto(producto_id)
        controlador_moto.eliminar_moto_por_cod(codMoto)

        return redirect(url_for('crud_producto'))
    except Exception as e:
        print(f"Error al eliminar el producto: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/eliminar_productoA", methods=["POST"])
def eliminar_productoA():
    try:
        producto_id = request.form.get('id')
        print(f"Producto ID recibido: {producto_id}")

        if not producto_id:
            raise ValueError("ID de Producto-Accesorio no proporcionado")

        codAccesorio = controlador_producto.obtener_codacce_porid_producto(producto_id)
        if not codAccesorio:
            raise ValueError("Código de Accesorio no encontrado para el ID de producto dado")

        controlador_pago.eliminar_venta_pr(producto_id)
        controlador_producto.eliminar_producto(producto_id)
        controlador_accesorio.eliminar_accesorio_por_cod(codAccesorio)

        print("Producto eliminado correctamente.")
        return redirect(url_for('crud_accesorio'))
    except Exception as e:
        print(f"Error al eliminar el accesorio: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/pago")
def formulario_pago():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para proceder al pago.", "error")
        return redirect(url_for("formulario_login_cliente"))

    id_cliente = session['user_id']
    conexion = obtener_conexion()
    items = []
    try:
        with conexion.cursor() as cursor:
            # Obtener el idCarrito del cliente
            cursor.execute("SELECT idCarrito FROM CARRITO WHERE idCliente = %s", (id_cliente,))
            carrito = cursor.fetchone()
            if carrito:
                idCarrito = carrito[0]
                items = controlador_carrito.obtener_items_carrito_por_id_carrito(idCarrito)
            else:
                flash("No hay carrito disponible para el pago.", "error")
                return redirect(url_for("formulario_principal"))

        return render_template("pago.html", items=items)
    finally:
        conexion.close()


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

    idMoto = controlador_moto.obtener_cod_moto(codmoto)

    controlador_moto.actualizar_moto(tipo, posicionManejo, numAsientos, numPasajeros, largo, ancho, alto, tipoMotor, combustible, numCilindros, capacidadTanque, rendimiento, idMoto)
    controlador_producto.actualizar_producto(descripcion, precio, stock, marca, modelo, color, imagen, idMoto, None, idProducto)
    return redirect("/crud_producto")

@app.route("/actualizar_productoAcc", methods=["POST"])
def actualizar_productoAcc():
    idProducto = request.form["idProducto"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]
    marca = request.form["marca"]
    modelo = request.form["modelo"]
    color = request.form["color"]
    imagen = request.form["imagen"]
    codaccesorio = request.form["codaccesorio"]
    tipo = request.form["tipo"]
    material = request.form["material"]

    idAccesorio = controlador_accesorio.obtener_cod_accesorio(codaccesorio)

    controlador_accesorio.actualizar_accesorio(codaccesorio, tipo, material, idAccesorio)
    controlador_producto.actualizar_producto(descripcion, precio, stock, marca, modelo, color, imagen, None, idAccesorio, idProducto)
    return redirect("/crud_accesorio")


@app.route("/formulario_editar_productoM/<int:id>")
def editar_productoM(id):
    producto = controlador_producto.obtener_moto_producto_nuevo_one(id)
    return render_template("crud_producto.html", producto=producto)

@app.route("/formulario_editar_accesorio/<int:id>")
def editar_productoA(id):
    producto = controlador_producto.obtener_accesorio_producto_nuevo_one(id)
    return render_template("crud_accesorio.html", producto=producto)


@app.route("/formulario_detalle_producto_moto/<int:id>")
def detalle_producto_moto(id):
    productomoto = controlador_producto.obtener_moto_producto_nuevo(id)
    usuario_logueado = 'user_id' in session
    producto_en_carrito = False

    if usuario_logueado:
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                # Obtener el ID del carrito del usuario logueado
                cursor.execute("SELECT idCarrito FROM CARRITO WHERE idCliente = %s", (session['user_id'],))
                carrito = cursor.fetchone()
                if carrito:
                    idCarrito = carrito[0]
                    # Verificar si el producto ya está en el carrito
                    cursor.execute("SELECT * FROM ITEM_CARRITO WHERE idCarrito = %s AND idProducto = %s", (idCarrito, id))
                    if cursor.fetchone():
                        producto_en_carrito = True
        finally:
            conexion.close()

    return render_template("detalleProductoMoto.html", productomoto=productomoto, usuario_logueado=usuario_logueado, en_carrito=producto_en_carrito)



@app.route("/formulario_detalle_producto_accesorio/<int:id>")
def detalle_producto_accesorio(id):
    productoaccesorio = controlador_producto.obtener_accesorio_producto_nuevo(id)
    return render_template("detalleProductoAccesorio.html", productoaccesorio=productoaccesorio)

@app.route("/compra_exitosa")
def compra_exitosa():
    email = request.cookies.get('email')
    token = request.cookies.get('token')
    if not email or not token or not session.get('user_id'):
        flash("Debes iniciar sesión para proceder al pago.", "error")
        return redirect(url_for("formulario_login_cliente"))

    id_cliente = session['user_id']
    if not venta_reciente(id_cliente):
        flash("No se ha detectado una compra reciente.", "error")
        return redirect(url_for("formulario_principal"))

    return render_template("compraexitosa.html")


def venta_reciente(id_cliente):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            print(f"Checando ventas recientes para el cliente ID: {id_cliente}")
            cursor.execute("""
                SELECT fechaVenta FROM VENTA1
                WHERE idCliente = %s AND fechaVenta >= %s
                ORDER BY fechaVenta DESC LIMIT 1
            """, (id_cliente, datetime.now() - timedelta(minutes=10)))
            venta = cursor.fetchone()
            tiene_venta_reciente = venta is not None
            print(f"Resultado de venta reciente: {tiene_venta_reciente}")
            return tiene_venta_reciente
    finally:
        conexion.close()

# ---------------Venta------------------------
@app.route("/guardar_venta", methods=["POST"])
def guardar_venta():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para realizar esta acción.", "error")
        return redirect(url_for("formulario_login_cliente"))

    num_venta = int(time.time())

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
    id_cliente = session['user_id']
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT idCarrito FROM CARRITO WHERE idCliente = %s", (id_cliente,))
            carrito = cursor.fetchone()
            if not carrito:
                flash("No hay carrito asociado a esta venta.", "error")
                return redirect(url_for("formulario_principal"))

            idCarrito = carrito[0]
            cursor.execute("SELECT idProducto, subtotal, cantidad FROM ITEM_CARRITO WHERE idCarrito = %s", (idCarrito,))
            productos = cursor.fetchall()

            for producto in productos:
                idProducto, monto_final, cantidad = producto
                controlador_pago.insertar_venta(nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, año, cvv, numtarjeta, idProducto, monto_final, num_venta, id_cliente, cantidad)

                cursor.execute("UPDATE PRODUCTO SET stock = stock - %s WHERE idProducto = %s", (cantidad, idProducto))

            cursor.execute("DELETE FROM ITEM_CARRITO WHERE idCarrito = %s", (idCarrito,))
            conexion.commit()
            return redirect("/compra_exitosa")

    except Exception as e:
        conexion.rollback()
        flash("Error al procesar la venta: {}".format(e), "error")
        return redirect(url_for("formulario_pago"))
    finally:
        conexion.close()

##### APIS

@app.route("/api_obtener_ventas", methods=["GET"])
@jwt_required()
def api_obtener_ventas():
    respuesta = dict()
    try:
        lista_ventas = []
        ventas = controlador_pago.api_obtener_ventas()

        for venta in ventas:
            objVenta = clsVenta(*venta)
            lista_ventas.append(objVenta.diccVenta)

        respuesta["code"] = 1
        respuesta["message"] = "Listado correcto de ventas registradas"
        respuesta["data"] = lista_ventas
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Problemas en el servicio web: {str(e)}"
        respuesta["data"] = dict()
        return jsonify(respuesta)

@app.route("/api_guardar_venta", methods=["POST"])
@jwt_required()
def api_guardar_venta():
    respuesta = dict()
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
        anio = request.json["anio"]
        cvv = request.json["cvv"]
        numtarjeta = request.json["numtarjeta"]
        idProducto = request.json["idProducto"]
        monto_final = request.json["monto_final"]
        num_venta = request.json["num_venta"]
        idCliente = request.json["idCliente"]
        cantidad = request.json["cantidad"]

        id_generado = controlador_pago.api_insertar_venta(
            nombre, apellidos, pais, direccion, region, localidad, telefono, correo, mes, anio, cvv, numtarjeta, idProducto, monto_final, num_venta, idCliente, cantidad
        )

        respuesta["code"] = 1
        respuesta["message"] = "Venta registrada correctamente."
        respuesta["data"] = {"idGenerado": id_generado}
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Ocurrió un problema: {repr(e)}"
        return jsonify(respuesta)


@app.route("/api_eliminar_venta/<int:id_venta>", methods=["DELETE"])
@jwt_required()
def api_eliminar_venta(id_venta):
    respuesta = dict()
    try:
        controlador_pago.api_eliminar_venta(id_venta)
        respuesta["code"] = 1
        respuesta["message"] = "Venta eliminada correctamente."
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Ocurrió un problema: {str(e)}"
        return jsonify(respuesta)

@app.route("/api_editar_venta/<int:id_venta>", methods=["PUT"])
@jwt_required()
def api_actualizar_venta(id_venta):
    respuesta = dict()
    try:
        datos = request.json
        controlador_pago.api_editar_venta(id_venta, **datos)
        respuesta["code"] = 1
        respuesta["message"] = "Venta actualizada correctamente."
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Ocurrió un problema: {str(e)}"
        return jsonify(respuesta)

@app.route("/api_obtener_venta_por_id/<int:id_venta>", methods=["GET"])
@jwt_required()
def api_obtener_venta_por_id(id_venta):
    respuesta = dict()
    try:
        venta = controlador_pago.api_obtener_venta_por_id(id_venta)
        if venta:
            objVenta = clsVenta(*venta)
            respuesta["code"] = 1
            respuesta["message"] = "Venta obtenida correctamente."
            respuesta["data"] = objVenta.diccVenta
        else:
            respuesta["code"] = 0
            respuesta["message"] = "Venta no encontrada."
            respuesta["data"] = dict()
        return jsonify(respuesta)
    except Exception as e:
        respuesta["code"] = 0
        respuesta["message"] = f"Ocurrió un problema: {str(e)}"
        return jsonify(respuesta)




# Iniciar el servidor

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)