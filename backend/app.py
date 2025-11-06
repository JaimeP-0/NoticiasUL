from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_compress import Compress
from singleton_config import ConfigSingleton
from factory_noticias import NoticiaFactory
from validators import NoticiaValidatorFactory
from role_validators import RoleValidatorFactory
from datetime import datetime
from database import Database
from firebase_service import FirebaseService
from config import Config
from permissions import require_permission, require_role, get_user_permissions, get_user_role_from_request
from cache import cache
import logging
import os
import uuid

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=Config.CORS_ORIGINS)

# Habilitar compresión gzip
Compress(app)

# Inicializar servicios
db = Database()
firebase = FirebaseService()

# Inicializar Firebase (opcional, no crítico si no está configurado)
firebase.initialize()

# Flag para inicialización lazy de tablas
_tables_initialized = False

def ensure_tables_initialized():
    """Inicializar tablas solo cuando sea necesario (lazy initialization)"""
    global _tables_initialized
    if not _tables_initialized:
        try:
            db.init_tables()
            _tables_initialized = True
        except Exception as e:
            logger.error(f"❌ Error al inicializar base de datos: {e}")

@app.route('/api/register', methods=['POST'])
def register():
    """Endpoint para registro de nuevos usuarios (solo crea usuarios con rol 'usuario')"""
    try:
        data = request.get_json() or {}
        usuario = data.get("usuario")
        password = data.get("password")
        nombre = data.get("nombre", "")
        email = data.get("email", "")
        
        logger.info(f"Intento de registro - Usuario: {usuario}")
        
        if not usuario or not password:
            logger.warning("Registro fallido: Faltan usuario o contraseña")
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400
        
        # Verificar si el usuario ya existe
        existing_user = db.execute_query(
            "SELECT idUsuario FROM usuarios_nul WHERE usuario = %s",
            (usuario,),
            fetch_one=True
        )
        
        if existing_user:
            logger.warning(f"Registro fallido: Usuario '{usuario}' ya existe")
            return jsonify({"error": "El usuario ya existe"}), 400
        
        # Crear nuevo usuario con rol 'usuario' por defecto (siempre)
        user_id = db.execute_query(
            "INSERT INTO usuarios_nul (usuario, contrasena, nombre, email, rol) VALUES (%s, %s, %s, %s, %s)",
            (usuario, password, nombre, email, 'usuario')
        )
        
        logger.info(f"Usuario registrado exitosamente: {usuario}")
        return jsonify({
            "mensaje": "Usuario registrado exitosamente",
            "usuario": usuario,
            "nombre": nombre,
            "rol": "usuario"
        }), 201
    except Exception as e:
        logger.error(f"Error en registro: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": "Error al registrar usuario"}), 500

@app.route('/api/users', methods=['GET'])
@require_permission('manage_admins')
def get_users():
    """Obtener todos los usuarios (solo superadmin) - con caché"""
    try:
        ensure_tables_initialized()
        
        # Caché para usuarios (TTL más largo: 2 minutos)
        cache_key = "users_list"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return jsonify(cached_result), 200
        
        users = db.execute_query(
            "SELECT idUsuario, usuario, nombre, email, rol, fecha_creacion FROM usuarios_nul ORDER BY fecha_creacion DESC",
            fetch_all=True
        )
        
        # Convertir fecha a string para JSON
        for user in users:
            if user.get('fecha_creacion'):
                user['fecha_creacion'] = user['fecha_creacion'].strftime("%Y-%m-%d %H:%M:%S")
            # No enviar la contraseña
            if 'contrasena' in user:
                del user['contrasena']
        
        result = users if users else []
        
        # Guardar en caché
        cache.set(cache_key, result, ttl=120)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error al obtener usuarios: {e}")
        return jsonify({"error": "Error al obtener usuarios"}), 500

@app.route('/api/users', methods=['POST'])
@require_permission('manage_admins')
def create_user():
    """Endpoint para crear usuarios con roles específicos (solo superadmin)"""
    try:
        data = request.get_json() or {}
        usuario = data.get("usuario")
        password = data.get("password")
        nombre = data.get("nombre", "")
        email = data.get("email", "")
        rol = data.get("rol", "usuario")
        
        # Validar que el rol sea válido
        valid_roles = ['superadmin', 'admin', 'maestro', 'usuario']
        if rol not in valid_roles:
            return jsonify({"error": f"Rol inválido. Roles permitidos: {valid_roles}"}), 400
        
        logger.info(f"Superadmin creando usuario - Usuario: {usuario}, Rol: {rol}")
        
        if not usuario or not password:
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400
        
        # Verificar si el usuario ya existe
        existing_user = db.execute_query(
            "SELECT idUsuario FROM usuarios_nul WHERE usuario = %s",
            (usuario,),
            fetch_one=True
        )
        
        if existing_user:
            return jsonify({"error": "El usuario ya existe"}), 400
        
        # Crear usuario con el rol especificado
        user_id = db.execute_query(
            "INSERT INTO usuarios_nul (usuario, contrasena, nombre, email, rol) VALUES (%s, %s, %s, %s, %s)",
            (usuario, password, nombre, email, rol)
        )
        
        # Limpiar caché de usuarios
        cache.delete("users_list")
        
        logger.info(f"Usuario creado por superadmin: {usuario} con rol {rol}")
        return jsonify({
            "mensaje": "Usuario creado exitosamente",
            "usuario": usuario,
            "nombre": nombre,
            "rol": rol
        }), 201
    except Exception as e:
        logger.error(f"Error al crear usuario: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": "Error al crear usuario"}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@require_permission('manage_admins')
def update_user(user_id):
    """Actualizar rol de un usuario (solo superadmin) - NO permite cambiar contraseñas"""
    try:
        data = request.get_json() or {}
        nuevo_rol = data.get("rol")
        
        # Verificar que el usuario existe
        user_existente = db.execute_query(
            "SELECT idUsuario, usuario, rol FROM usuarios_nul WHERE idUsuario = %s",
            (user_id,),
            fetch_one=True
        )
        
        if not user_existente:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # Validar que el rol sea válido si se proporciona
        if nuevo_rol:
            valid_roles = ['superadmin', 'admin', 'maestro', 'usuario']
            if nuevo_rol not in valid_roles:
                return jsonify({"error": f"Rol inválido. Roles permitidos: {valid_roles}"}), 400
        
        # Solo actualizar el rol
        if nuevo_rol is None:
            return jsonify({"error": "Debe proporcionar un rol para actualizar"}), 400
        
        db.execute_query(
            "UPDATE usuarios_nul SET rol = %s WHERE idUsuario = %s",
            (nuevo_rol, user_id)
        )
        
        # Obtener el usuario actualizado
        usuario_actualizado = db.execute_query(
            "SELECT idUsuario, usuario, nombre, email, rol, fecha_creacion FROM usuarios_nul WHERE idUsuario = %s",
            (user_id,),
            fetch_one=True
        )
        
        if usuario_actualizado and usuario_actualizado.get('fecha_creacion'):
            usuario_actualizado['fecha_creacion'] = usuario_actualizado['fecha_creacion'].strftime("%Y-%m-%d %H:%M:%S")
        
        # Limpiar caché de usuarios
        cache.delete("users_list")
        
        logger.info(f"Rol de usuario {user_existente['usuario']} actualizado a {nuevo_rol} por superadmin")
        return jsonify({
            "mensaje": "Rol actualizado exitosamente",
            "usuario": usuario_actualizado
        }), 200
    except Exception as e:
        logger.error(f"Error al actualizar usuario: {e}")
        return jsonify({"error": "Error al actualizar usuario"}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@require_permission('manage_admins')
def delete_user(user_id):
    """Eliminar un usuario (solo superadmin)"""
    try:
        # Verificar que el usuario existe
        user_existente = db.execute_query(
            "SELECT idUsuario, usuario, rol FROM usuarios_nul WHERE idUsuario = %s",
            (user_id,),
            fetch_one=True
        )
        
        if not user_existente:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # No permitir eliminar al último superadmin
        if user_existente['rol'] == 'superadmin':
            superadmin_count = db.execute_query(
                "SELECT COUNT(*) as total FROM usuarios_nul WHERE rol = 'superadmin'",
                fetch_one=True
            )
            if superadmin_count and superadmin_count.get('total', 0) <= 1:
                return jsonify({"error": "No se puede eliminar el último superadmin del sistema"}), 400
        
        # Eliminar usuario
        db.execute_query(
            "DELETE FROM usuarios_nul WHERE idUsuario = %s",
            (user_id,)
        )
        
        # Limpiar caché de usuarios
        cache.delete("users_list")
        
        logger.info(f"Usuario {user_existente['usuario']} eliminado por superadmin")
        return jsonify({
            "mensaje": "Usuario eliminado exitosamente"
        }), 200
    except Exception as e:
        logger.error(f"Error al eliminar usuario: {e}")
        return jsonify({"error": "Error al eliminar usuario"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint para autenticación de usuarios"""
    try:
        data = request.get_json() or {}
        usuario = data.get("usuario")
        password = data.get("password")
        
        logger.info(f"Intento de login - Usuario: {usuario}")
        
        if not usuario or not password:
            logger.warning("Login fallido: Faltan usuario o contraseña")
            return jsonify({"error": "Usuario y contraseña requeridos"}), 400
        
        # Buscar usuario en MySQL
        user = db.execute_query(
            "SELECT idUsuario, usuario, contrasena, nombre, rol FROM usuarios_nul WHERE usuario = %s",
            (usuario,),
            fetch_one=True
        )
        
        if not user:
            logger.warning(f"Login fallido: Usuario '{usuario}' no encontrado")
            return jsonify({"error": "Credenciales incorrectas"}), 401
        
        logger.info(f"Usuario encontrado: {user['usuario']}")
        
        if user['contrasena'] == password:  # En producción usar bcrypt
            rol = user.get('rol') or 'usuario'  # Asegurar que siempre haya un rol
            logger.info(f"Login exitoso para usuario: {usuario}")
            return jsonify({
                "mensaje": "Inicio de sesión exitoso",
                "usuario": user['usuario'],
                "nombre": user.get('nombre'),
                "rol": rol
            })
        else:
            logger.warning(f"Login fallido: Contraseña incorrecta para usuario '{usuario}'")
            return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
        logger.error(f"Error en login: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    """Obtener noticias desde MySQL (optimizado con caché)"""
    try:
        ensure_tables_initialized()
        
        # Obtener parámetros de paginación
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)
        
        # Clave de caché basada en parámetros
        cache_key = f"news_{limit}_{offset}"
        
        # Intentar obtener del caché
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return jsonify(cached_result)
        
        # Query optimizada con JOIN para obtener el nombre del usuario y contenido (para búsqueda)
        noticias = db.execute_query(
            """SELECT n.id, n.titulo, n.contenido, n.autor, n.fecha, n.imagen_url as imagen,
                      COALESCE(u.nombre, n.autor) as nombre_autor
               FROM noticias_nul n
               LEFT JOIN usuarios_nul u ON n.autor = u.usuario
               ORDER BY n.fecha DESC LIMIT %s OFFSET %s""",
            (limit, offset),
            fetch_all=True
        )
        
        # Convertir fecha a string para JSON
        for noticia in noticias:
            if noticia.get('fecha'):
                noticia['fecha'] = noticia['fecha'].strftime("%Y-%m-%d %H:%M:%S")
            if not noticia.get('imagen'):
                noticia['imagen'] = ""
        
        result = noticias if noticias else []
        
        # Guardar en caché (TTL de 30 segundos)
        cache.set(cache_key, result, ttl=30)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error al obtener noticias: {e}")
        return jsonify({"error": "Error al obtener noticias"}), 500

@app.route('/api/news/<int:news_id>', methods=['GET'])
def get_news_by_id(news_id):
    """Obtener una noticia específica por ID desde MySQL (con caché)"""
    try:
        ensure_tables_initialized()
        
        # Intentar obtener del caché
        cache_key = f"news_detail_{news_id}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return jsonify(cached_result)
        
        noticia = db.execute_query(
            """SELECT n.id, n.titulo, n.contenido, n.autor, n.fecha, n.imagen_url as imagen,
                      COALESCE(u.nombre, n.autor) as nombre_autor
               FROM noticias_nul n
               LEFT JOIN usuarios_nul u ON n.autor = u.usuario
               WHERE n.id = %s""",
            (news_id,),
            fetch_one=True
        )
        
        if not noticia:
            return jsonify({"error": "Noticia no encontrada"}), 404
        
        # Convertir fecha a string para JSON
        if noticia.get('fecha'):
            noticia['fecha'] = noticia['fecha'].strftime("%Y-%m-%d %H:%M:%S")
        if not noticia.get('imagen'):
            noticia['imagen'] = ""
        
        # Guardar en caché (TTL de 60 segundos para detalles)
        cache.set(cache_key, noticia, ttl=60)
        
        return jsonify(noticia)
    except Exception as e:
        logger.error(f"Error al obtener noticia: {e}")
        return jsonify({"error": "Error al obtener la noticia"}), 500

@app.route('/api/news', methods=['POST'])
@require_permission('create')
def create_news():
    """Crear una nueva noticia en MySQL (requiere permiso 'create': admin o maestro)"""
    try:
        ensure_tables_initialized()
        
        data = request.get_json() or {}
        titulo = data.get("titulo")
        contenido = data.get("contenido")
        autor = data.get("autor")
        imagen_url = data.get("imagen", "")  # URL de Firebase Storage o externa
        tipo_noticia = data.get("tipo", "general")  # Tipo de noticia (general, importante, evento, anuncio)
        
        # Validación básica de campos requeridos
        if not titulo or not contenido or not autor:
            return jsonify({"error": "Faltan campos requeridos: titulo, contenido, autor"}), 400
        
        # Usar Factory Pattern para obtener el validador según el tipo de noticia
        validator = NoticiaValidatorFactory.create_validator(tipo_noticia)
        es_valido, error = validator.validate(titulo, contenido, autor, imagen_url)
        
        if not es_valido:
            return jsonify({"error": error}), 400
        
        # Usar Factory Pattern para crear el objeto Noticia según su tipo
        # (aunque finalmente guardamos en BD, el factory nos da estructura y validación)
        noticia_obj = NoticiaFactory.crear(tipo_noticia, titulo, contenido, autor, imagen_url)
        
        # Insertar en MySQL
        noticia_id = db.execute_query(
            "INSERT INTO noticias_nul (titulo, contenido, autor, imagen_url) VALUES (%s, %s, %s, %s)",
            (titulo, contenido, autor, imagen_url)
        )
        
        # Limpiar caché de lista de noticias
        cache.delete("news_50_0")  # Limpiar la primera página
        
        # Obtener la noticia creada con nombre del autor
        nueva_noticia = db.execute_query(
            """SELECT n.id, n.titulo, n.contenido, n.autor, n.fecha, n.imagen_url as imagen,
                      COALESCE(u.nombre, n.autor) as nombre_autor
               FROM noticias_nul n
               LEFT JOIN usuarios_nul u ON n.autor = u.usuario
               WHERE n.id = %s""",
            (noticia_id,),
            fetch_one=True
        )
        
        if nueva_noticia and nueva_noticia.get('fecha'):
            nueva_noticia['fecha'] = nueva_noticia['fecha'].strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify({
            "mensaje": "Noticia creada exitosamente",
            "noticia": nueva_noticia
        }), 201
    except Exception as e:
        logger.error(f"Error al crear noticia: {e}")
        return jsonify({"error": "Error al crear la noticia"}), 500

@app.route('/api/news/<int:news_id>', methods=['PUT'])
@require_permission('edit')
def update_news(news_id):
    """Actualizar una noticia existente (requiere permiso 'edit': solo admin)"""
    try:
        data = request.get_json() or {}
        titulo = data.get("titulo")
        contenido = data.get("contenido")
        imagen_url = data.get("imagen")
        
        # Verificar que la noticia existe
        noticia_existente = db.execute_query(
            "SELECT id FROM noticias_nul WHERE id = %s",
            (news_id,),
            fetch_one=True
        )
        
        if not noticia_existente:
            return jsonify({"error": "Noticia no encontrada"}), 404
        
        # Construir query de actualización dinámicamente
        updates = []
        params = []
        
        if titulo is not None:
            updates.append("titulo = %s")
            params.append(titulo)
        if contenido is not None:
            updates.append("contenido = %s")
            params.append(contenido)
        if imagen_url is not None:
            updates.append("imagen_url = %s")
            params.append(imagen_url)
        
        if not updates:
            return jsonify({"error": "No se proporcionaron campos para actualizar"}), 400
        
        params.append(news_id)
        query = f"UPDATE noticias_nul SET {', '.join(updates)} WHERE id = %s"
        
        db.execute_query(query, tuple(params))
        
        # Obtener la noticia actualizada con nombre del autor
        noticia_actualizada = db.execute_query(
            """SELECT n.id, n.titulo, n.contenido, n.autor, n.fecha, n.imagen_url as imagen,
                      COALESCE(u.nombre, n.autor) as nombre_autor
               FROM noticias_nul n
               LEFT JOIN usuarios_nul u ON n.autor = u.usuario
               WHERE n.id = %s""",
            (news_id,),
            fetch_one=True
        )
        
        if noticia_actualizada and noticia_actualizada['fecha']:
            noticia_actualizada['fecha'] = noticia_actualizada['fecha'].strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify({
            "mensaje": "Noticia actualizada exitosamente",
            "noticia": noticia_actualizada
        }), 200
    except Exception as e:
        logger.error(f"Error al actualizar noticia: {e}")
        return jsonify({"error": "Error al actualizar la noticia"}), 500

@app.route('/api/news/<int:news_id>', methods=['DELETE'])
@require_permission('delete')
def delete_news(news_id):
    """Eliminar una noticia (requiere permiso 'delete': solo admin)"""
    try:
        # Verificar que la noticia existe
        noticia_existente = db.execute_query(
            "SELECT id, imagen_url FROM noticias_nul WHERE id = %s",
            (news_id,),
            fetch_one=True
        )
        
        if not noticia_existente:
            return jsonify({"error": "Noticia no encontrada"}), 404
        
        # Eliminar imagen de Firebase si existe
        if noticia_existente.get('imagen_url') and firebase._initialized:
            try:
                # Extraer el path de Firebase desde la URL
                imagen_url = noticia_existente['imagen_url']
                if 'firebasestorage' in imagen_url or 'storage.googleapis.com' in imagen_url:
                    # Intentar extraer el path del blob
                    # Formato: https://firebasestorage.googleapis.com/v0/b/bucket/o/path%2Ffile.jpg
                    import urllib.parse
                    if '/o/' in imagen_url:
                        path_part = imagen_url.split('/o/')[1].split('?')[0]
                        blob_path = urllib.parse.unquote(path_part)
                        firebase.delete_image(blob_path)
            except Exception as e:
                logger.warning(f"No se pudo eliminar imagen de Firebase: {e}")
        
        # Eliminar de MySQL
        db.execute_query(
            "DELETE FROM noticias_nul WHERE id = %s",
            (news_id,)
        )
        
        # Limpiar caché de lista de noticias
        cache.delete("news_50_0")  # Limpiar la primera página
        
        return jsonify({
            "mensaje": "Noticia eliminada exitosamente"
        }), 200
    except Exception as e:
        logger.error(f"Error al eliminar noticia: {e}")
        return jsonify({"error": "Error al eliminar la noticia"}), 500

@app.route('/api/upload', methods=['POST'])
@require_permission('create')
def upload_image():
    """Endpoint para subir imágenes a Firebase Storage"""
    try:
        # Verificar que Firebase esté inicializado
        if not firebase._initialized:
            logger.error("❌ Firebase no está inicializado")
            logger.error(f"Archivo de credenciales: {Config.FIREBASE_CREDENTIALS_PATH}")
            logger.error(f"¿Existe el archivo? {os.path.exists(Config.FIREBASE_CREDENTIALS_PATH)}")
            return jsonify({
                "error": "Firebase Storage no está configurado. Verifica que el archivo firebase-credentials.json exista en la carpeta backend/."
            }), 500
        
        if 'imagen' not in request.files:
            return jsonify({"error": "No se proporcionó ningún archivo"}), 400
        
        file = request.files['imagen']
        
        if file.filename == '':
            return jsonify({"error": "No se seleccionó ningún archivo"}), 400
        
        # Validar tipo de archivo
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({"error": "Tipo de archivo no permitido. Solo se aceptan PNG, JPG, JPEG, GIF y WEBP."}), 400
        
        # Validar tamaño (máximo 10MB)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Resetear posición
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            return jsonify({"error": "El archivo es demasiado grande. Máximo permitido: 10MB."}), 400
        
        # Generar nombre único para el archivo
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        destination_path = f"noticias/{unique_filename}"
        
        logger.info(f"Intentando subir imagen: {destination_path}")
        logger.info(f"Bucket configurado: {Config.FIREBASE_STORAGE_BUCKET}")
        
        # Subir a Firebase Storage
        image_url = firebase.upload_image_from_file_storage(file, destination_path)
        
        if not image_url:
            logger.error("❌ Error: Firebase Storage no está disponible o hubo un error al subir")
            logger.error(f"Firebase inicializado: {firebase._initialized}")
            logger.error(f"Bucket configurado: {Config.FIREBASE_STORAGE_BUCKET}")
            return jsonify({
                "error": "Error al subir la imagen a Firebase Storage. Verifica los logs del servidor para más detalles."
            }), 500
        
        logger.info(f"✅ Imagen subida exitosamente: {image_url}")
        return jsonify({"url": image_url}), 200
        
    except Exception as e:
        logger.error(f"❌ Error al subir imagen: {e}")
        import traceback
        error_traceback = traceback.format_exc()
        logger.error(error_traceback)
        return jsonify({
            "error": f"Error interno al subir la imagen: {str(e)}",
            "details": error_traceback if Config.DEBUG else "Habilita DEBUG para ver más detalles"
        }), 500

@app.route('/api/config')
def get_config():
    config = ConfigSingleton()
    return jsonify(config.config)

@app.route('/api/firebase-status', methods=['GET'])
def firebase_status():
    """Endpoint para verificar el estado de Firebase"""
    try:
        creds_path = Config.FIREBASE_CREDENTIALS_PATH
        creds_exists = os.path.exists(creds_path)
        
        status = {
            "initialized": firebase._initialized,
            "credentials_path": creds_path,
            "credentials_exists": creds_exists,
            "bucket": Config.FIREBASE_STORAGE_BUCKET,
        }
        
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error al verificar estado de Firebase: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/permissions', methods=['GET'])
def get_permissions():
    """Obtener permisos del usuario actual basado en su rol"""
    try:
        user_role = request.headers.get('X-User-Role', 'usuario')
        permissions = get_user_permissions(user_role)
        
        return jsonify({
            "role": user_role,
            "permissions": permissions
        }), 200
    except Exception as e:
        logger.error(f"Error al obtener permisos: {e}")
        return jsonify({"error": "Error al obtener permisos"}), 500

if __name__ == '__main__':
    app.run(debug=True)
