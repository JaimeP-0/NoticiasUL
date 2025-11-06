"""
Módulo para manejar la conexión a MySQL
"""
import mysql.connector
from mysql.connector import Error
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    """Clase singleton para manejar la conexión a MySQL"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """Obtener o crear conexión a MySQL"""
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=Config.MYSQL_HOST,
                    port=Config.MYSQL_PORT,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DATABASE,
                    autocommit=True
                )
                logger.info(f"✅ Conexión a MySQL establecida: {Config.MYSQL_DATABASE}")
            except Error as e:
                logger.error(f"❌ Error al conectar a MySQL: {e}")
                raise
        return self._connection
    
    def close_connection(self):
        """Cerrar conexión a MySQL"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            logger.info("✅ Conexión a MySQL cerrada")
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Ejecutar una consulta SQL"""
        connection = self.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid
            
            connection.commit()
            return result
        except Error as e:
            logger.error(f"❌ Error al ejecutar consulta: {e}")
            connection.rollback()
            raise
        finally:
            cursor.close()
    
    def init_tables(self):
        """Inicializar tablas en la base de datos"""
        try:
            # Verificar si la tabla usuarios_nul existe y tiene la estructura correcta
            try:
                self.execute_query("SELECT idUsuario, usuario, contrasena FROM usuarios_nul LIMIT 1")
                logger.info("Tabla usuarios_nul ya existe")
            except:
                # Crear tabla de usuarios_nul solo si no existe
                self.execute_query("""
                    CREATE TABLE IF NOT EXISTS usuarios_nul (
                        idUsuario INT AUTO_INCREMENT PRIMARY KEY,
                        usuario VARCHAR(50) UNIQUE NOT NULL,
                        contrasena VARCHAR(255) NOT NULL,
                        nombre VARCHAR(100),
                        email VARCHAR(100),
                        rol VARCHAR(20) DEFAULT 'usuario',
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            
            # Crear tabla de noticias_nul (sin clave foránea para compatibilidad)
            try:
                self.execute_query("SELECT id FROM noticias_nul LIMIT 1")
                logger.info("Tabla noticias_nul ya existe")
            except:
                # Crear tabla de noticias_nul sin clave foránea para evitar problemas
                self.execute_query("""
                    CREATE TABLE IF NOT EXISTS noticias_nul (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        titulo VARCHAR(255) NOT NULL,
                        contenido TEXT NOT NULL,
                        autor VARCHAR(100) NOT NULL,
                        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        imagen_url VARCHAR(500),
                        usuario_id INT,
                        INDEX idx_fecha (fecha),
                        INDEX idx_autor (autor),
                        INDEX idx_titulo (titulo)
                    )
                """)
                logger.info("Tabla noticias_nul creada")
            
            # Insertar usuario admin por defecto si no existe
            try:
                existing_admin = self.execute_query(
                    "SELECT idUsuario FROM usuarios_nul WHERE usuario = %s",
                    ('admin',),
                    fetch_one=True
                )
                
                if not existing_admin:
                    # Password: '1234' (en producción usar bcrypt o similar)
                    self.execute_query("""
                        INSERT INTO usuarios_nul (usuario, contrasena, nombre, rol)
                        VALUES (%s, %s, %s, %s)
                    """, ('admin', '1234', 'Administrador', 'admin'))
                    logger.info("Usuario admin creado por defecto")
            except Exception as e:
                logger.warning(f"No se pudo crear usuario admin: {e}")
            
            logger.info("Tablas inicializadas correctamente")
            return True
        except Error as e:
            logger.error(f"Error al inicializar tablas: {e}")
            return False

