from flask import Blueprint, render_template, request, redirect, url_for
from database import db_connection 

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/')
def index():
    cur = db_connection.cursor(dictionary=True)
    cur.execute("SELECT * FROM ventas")
    mis_ventas = cur.fetchall()
    cur.close()
    return render_template('Ventas/index.html', lista_ventas=mis_ventas)

@ventas_bp.route('/agregar')
def agregar_venta():
    return render_template('Ventas/agregar.html')

@ventas_bp.route('/guardar', methods=['POST'])
def guardar_venta():
    _lector = request.form['txtLector']
    _libro = request.form['txtLibro']
    _precio = request.form['txtPrecio']
    _total = request.form['txtTotal']

    cur = db_connection.cursor()
    sql = "INSERT INTO ventas (lector, libro, precio, total) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (_lector, _libro, _precio, _total))
    db_connection.commit()
    cur.close()
    return redirect(url_for('ventas.index'))

@ventas_bp.route('/eliminar/<int:id>')
def eliminar(id):
    cur = db_connection.cursor()
    cur.execute("DELETE FROM ventas WHERE id_venta = %s", (id,))
    db_connection.commit()
    cur.close()
    return redirect(url_for('ventas.index'))