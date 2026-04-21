from flask import Blueprint, render_template, request, redirect, url_for
from database import db_connection 

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/')
def index():
    termino = request.args.get('buscar', '')
    cur = db_connection.cursor(dictionary=True)
    
    if termino:
        sql = "SELECT * FROM productos WHERE nombre LIKE %s OR descripcion LIKE %s"
        cur.execute(sql, (f"%{termino}%", f"%{termino}%"))
    else:
        cur.execute("SELECT * FROM productos")
    
    mis_libros = cur.fetchall()
    cur.close()
    return render_template('Inventario/index.html', libros=mis_libros)

@inventario_bp.route('/agregar')
def agregar_libro():
    return render_template('Inventario/agregar.html')

@inventario_bp.route('/guardar', methods=['POST'])
def guardar_libro():
    # Usar .get('') evita el error de la pantalla blanca si un campo falta
    _codigo = request.form.get('txtCodigo', '')
    _nombre = request.form.get('txtNombre', '')
    _desc = request.form.get('txtDescripcion', '')
    _precio = request.form.get('txtPrecio', '0')
    _stock = request.form.get('txtStock', '0')

    cur = db_connection.cursor()
    sql = "INSERT INTO productos (codigo, nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, (_codigo, _nombre, _desc, _precio, _stock))
    db_connection.commit()
    cur.close()
    return redirect(url_for('inventario.index'))

# --- ESTO ES LO QUE TE FALTABA PARA QUITAR EL ERROR ---
@inventario_bp.route('/biblioteca')
def biblioteca():
    cur = db_connection.cursor(dictionary=True)
    cur.execute("SELECT * FROM productos")
    mis_libros = cur.fetchall()
    cur.close()
    return render_template('Biblioteca/index.html', libros=mis_libros)