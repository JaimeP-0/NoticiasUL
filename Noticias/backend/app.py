from flask import Flask, jsonify, request
from flask_cors import CORS
from singleton_config import ConfigSingleton
from factory_noticias import NoticiaFactory
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Datos simulados
usuarios = {"admin": "1234"}
# Simulación de base de datos MySQL - lista de noticias almacenadas
noticias_db = []

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    usuario = data.get("usuario")
    password = data.get("password")
    if usuario in usuarios and usuarios[usuario] == password:
        return jsonify({"mensaje": "Inicio de sesión exitoso", "usuario": usuario})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/api/news', methods=['GET'])
def get_news():
    # Obtener noticias desde MySQL (simulado con lista)
    # Si no hay noticias en la DB, usar las del factory como ejemplo
    if len(noticias_db) == 0:
        noticia1 = NoticiaFactory.crear("importante")
        noticia2 = NoticiaFactory.crear("evento")
        return jsonify([
            {
                "id": 1,
                "titulo": noticia1.titulo,
                "contenido": noticia1.contenido,
                "autor": "Sistema",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "imagen": ""  # URL de Firebase Storage simulada
            },
            {
                "id": 2,
                "titulo": noticia2.titulo,
                "contenido": noticia2.contenido,
                "autor": "Sistema",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "imagen": ""
            }
        ])
    return jsonify(noticias_db)

@app.route('/api/news', methods=['POST'])
def create_news():
    # Endpoint para crear nueva noticia (requiere permisos)
    data = request.get_json() or {}
    titulo = data.get("titulo")
    contenido = data.get("contenido")
    autor = data.get("autor")
    imagen_url = data.get("imagen", "")  # URL de Firebase Storage
    
    if not titulo or not contenido or not autor:
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    # Crear nueva noticia (simulando inserción en MySQL)
    nueva_noticia = {
        "id": len(noticias_db) + 1,
        "titulo": titulo,
        "contenido": contenido,
        "autor": autor,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "imagen": imagen_url
    }
    noticias_db.append(nueva_noticia)
    
    return jsonify({"mensaje": "Noticia creada exitosamente", "noticia": nueva_noticia}), 201

@app.route('/api/config')
def get_config():
    config = ConfigSingleton()
    return jsonify(config.config)

if __name__ == '__main__':
    app.run(debug=True)
