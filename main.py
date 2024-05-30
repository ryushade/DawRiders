from flask import Flask, render_template, request, redirect, flash, jsonify, url_for, session,json  
from flask_login import login_user
import os
import controlador_pago
from bd import obtener_conexion

import urllib
import os
import controlador_cliente 
import controlador_moto
import controlador_producto
import controlador_accesorio
import controlador_carrito
app = Flask(__name__, static_folder='static')

app.secret_key = '1234' 

@app.route("/")
@app.route("/CicloRiders")
def formulario_principal():
    return render_template("index.html")

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
    return redirect("/crud_cliente")

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
            return redirect(url_for("index"))
    else:
        flash('Error al logearse. Intente nuevamente', 'error')
        return render_template("login.html")

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
            cursor.execute("INSERT INTO carrito (/* campos necesarios */) VALUES (/* valores */)")
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
    return render_template("categorias.html" , productosm=productosm)

#######

@app.route("/listar_ProductoA")
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




# Iniciar el servidor

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)