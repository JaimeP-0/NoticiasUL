from flask import Flask, jsonify, request
from flask_cors import CORS
from singleton_config import ConfigSingleton
from factory_noticias import NoticiaFactory
from datetime import datetime
from database import Database
from firebase_service import FirebaseService
from config import Config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=Config.CORS_ORIGINS)

# Inicializar servicios
db = Database()
firebase = FirebaseService()

# Inicializar base de datos y tablas
try:
    db.init_tables()
    logger.info("✅ Base de datos inicializada")
except Exception as e:
    logger.error(f"❌ Error al inicializar base de datos: {e}")

# Inicializar Firebase (opcional, no crítico si no está configurado)
firebase.initialize()

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint para autenticación de usuarios"""
    try:
        data = request.get_json() or {}
        usuario = data.get("usuario")
        password = data.get("password")
        
        if not usuario or not password:
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400
        
        # Buscar usuario en MySQL
        user = db.execute_query(
            "SELECT id, usuario, password, nombre, rol FROM usuarios WHERE usuario = %s",
            (usuario,),
            fetch_one=True
        )
        
        if user and user['password'] == password:  # En producción usar bcrypt
            return jsonify({
                "mensaje": "Inicio de sesión exitoso",
                "usuario": user['usuario'],
                "nombre": user.get('nombre'),
                "rol": user.get('rol')
            })
        
        return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
        logger.error(f"Error en login: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    """Obtener todas las noticias desde MySQL"""
    try:
        noticias = db.execute_query(
            "SELECT id, titulo, contenido, autor, fecha, imagen_url as imagen FROM noticias ORDER BY fecha DESC",
            fetch_all=True
        )
        
        # Convertir fecha a string para JSON
        for noticia in noticias:
            if noticia['fecha']:
                noticia['fecha'] = noticia['fecha'].strftime("%Y-%m-%d %H:%M:%S")
            if not noticia['imagen']:
                noticia['imagen'] = ""
        
        return jsonify(noticias if noticias else [])
    except Exception as e:
        logger.error(f"Error al obtener noticias: {e}")
        # Fallback a datos de ejemplo si hay error
        noticia1 = NoticiaFactory.crear("importante")
        noticia2 = NoticiaFactory.crear("evento")
        return jsonify([
            {
                "id": 1,
                "titulo": noticia1.titulo,
                "contenido": noticia1.contenido,
                "autor": "Sistema",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "imagen": ""
            }
        ])

@app.route('/api/news', methods=['POST'])
def create_news():
    """Crear una nueva noticia en MySQL"""
    try:
        data = request.get_json() or {}
        titulo = data.get("titulo")
        contenido = data.get("contenido")
        autor = data.get("autor")
        imagen_url = data.get("imagen", "")  # URL de Firebase Storage o externa
        
        if not titulo or not contenido or not autor:
            return jsonify({"error": "Faltan campos requeridos: titulo, contenido, autor"}), 400
        
        # Insertar en MySQL
        noticia_id = db.execute_query(
            "INSERT INTO noticias (titulo, contenido, autor, imagen_url) VALUES (%s, %s, %s, %s)",
            (titulo, contenido, autor, imagen_url)
        )
        
        # Obtener la noticia creada
        nueva_noticia = db.execute_query(
            "SELECT id, titulo, contenido, autor, fecha, imagen_url as imagen FROM noticias WHERE id = %s",
            (noticia_id,),
            fetch_one=True
        )
        
        if nueva_noticia and nueva_noticia['fecha']:
            nueva_noticia['fecha'] = nueva_noticia['fecha'].strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify({
            "mensaje": "Noticia creada exitosamente",
            "noticia": nueva_noticia
        }), 201
    except Exception as e:
        logger.error(f"Error al crear noticia: {e}")
        return jsonify({"error": "Error al crear la noticia"}), 500

@app.route('/api/config')
def get_config():
    config = ConfigSingleton()
    return jsonify(config.config)

if __name__ == '__main__':
    app.run(debug=True)
