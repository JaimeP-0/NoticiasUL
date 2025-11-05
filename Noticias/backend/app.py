from flask import Flask, jsonify, request
from flask_cors import CORS
from singleton_config import ConfigSingleton
from factory_noticias import NoticiaFactory

app = Flask(__name__)
CORS(app)

# Datos simulados
usuarios = {"admin": "1234"}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")
    if usuario in usuarios and usuarios[usuario] == password:
        return jsonify({"mensaje": "Inicio de sesión exitoso"})
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/api/news')
def get_news():
    noticia1 = NoticiaFactory.crear("importante")
    noticia2 = NoticiaFactory.crear("evento")
    return jsonify([
        {"titulo": noticia1.titulo, "contenido": noticia1.contenido},
        {"titulo": noticia2.titulo, "contenido": noticia2.contenido}
    ])

@app.route('/api/config')
def get_config():
    config = ConfigSingleton()
    return jsonify(config.config)

if __name__ == '__main__':
    app.run(debug=True)
