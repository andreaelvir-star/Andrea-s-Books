from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de tu base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ujcv-books" 
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventario')
def inventario():
    # 1. Atrapamos lo que el usuario escribió en el input "buscar"
    termino = request.args.get('buscar', '')
    
    cur = conn.cursor(dictionary=True)
    
    if termino:
        # 2. Si hay búsqueda, usamos "LIKE" para buscar nombres que se parezcan
        # El % permite buscar cualquier coincidencia antes o después
        sql = "SELECT * FROM productos WHERE nombre LIKE %s OR descripcion LIKE %s"
        cur.execute(sql, (f"%{termino}%", f"%{termino}%"))
    else:
        # 3. Si no hay búsqueda, traemos todo como antes
        cur.execute("SELECT * FROM productos")
    
    mis_libros = cur.fetchall()
    cur.close()
    
    return render_template('Inventario/index.html', libros=mis_libros)

# --- MÓDULO VENTAS ---
@app.route('/ventas')
def ventas():
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM ventas")
    mis_ventas = cur.fetchall()
    cur.close()
    return render_template('Ventas/index.html', lista_ventas=mis_ventas)

# --- NUEVAS RUTAS (Movidas arriba del __main__) ---
@app.route('/ventas/agregar')
def agregar_venta():
    return render_template('Ventas/agregar.html')

@app.route('/ventas/guardar', methods=['POST'])
def guardar_venta():
    _lector = request.form['txtLector']
    _libro = request.form['txtLibro']
    _precio = request.form['txtPrecio']
    _total = request.form['txtTotal']

    cur = conn.cursor()
    sql = "INSERT INTO ventas (lector, libro, precio, total) VALUES (%s, %s, %s, %s)"
    valores = (_lector, _libro, _precio, _total)
    
    cur.execute(sql, valores)
    conn.commit()
    cur.close()
    
    return redirect(url_for('ventas'))
@app.route('/ventas/eliminar/<int:id>')
def eliminar_venta(id):
    cur = conn.cursor()
    # Borra de la tabla ventas donde el id coincida
    sql = "DELETE FROM ventas WHERE id_venta = %s"
    cur.execute(sql, (id,))
    conn.commit()
    cur.close()
    return redirect(url_for('ventas'))
@app.route('/inventario/agregar')
def agregar_libro():
    return render_template('Inventario/agregar.html')

@app.route('/inventario/guardar', methods=['POST'])
def guardar_libro():
    _codigo = request.form['txtCodigo']
    _nombre = request.form['txtNombre']
    _desc = request.form['txtDescripcion']
    _precio = request.form['txtPrecio']
    _stock = request.form['txtStock']

    cur = conn.cursor()
    sql = "INSERT INTO productos (codigo, nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, (_codigo, _nombre, _desc, _precio, _stock))
    conn.commit()
    cur.close()
    return redirect(url_for('inventario'))

# ESTO SIEMPRE AL FINAL
if __name__ == "__main__":
    app.run(debug=True, port=5001)