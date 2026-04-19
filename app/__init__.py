from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # Importamos los Blueprints aquí adentro
    from app.routes.ventas import ventas_bp
    from app.routes.inventario import inventario_bp

    # Registramos con sus prefijos
    app.register_blueprint(ventas_bp, url_prefix='/ventas')
    app.register_blueprint(inventario_bp, url_prefix='/inventario')

    @app.route('/')
    def index():
        # Ya no regresamos el "¡Hola!", regresamos el archivo real
        return render_template('index.html')

    return app