from app import create_app  # Esto busca la función dentro de app/__init__.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)