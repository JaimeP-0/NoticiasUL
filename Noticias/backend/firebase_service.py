"""
Servicio para manejar Firebase Storage
"""
import os
import firebase_admin
from firebase_admin import credentials, storage
from config import Config
import logging

logger = logging.getLogger(__name__)

class FirebaseService:
    """Clase singleton para manejar Firebase Storage"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
        return cls._instance
    
    def initialize(self):
        """Inicializar Firebase Admin SDK"""
        if self._initialized:
            return True
        
        try:
            # Verificar si existe el archivo de credenciales
            if not os.path.exists(Config.FIREBASE_CREDENTIALS_PATH):
                logger.warning(f"⚠️ Archivo de credenciales de Firebase no encontrado: {Config.FIREBASE_CREDENTIALS_PATH}")
                logger.warning("⚠️ Firebase Storage no estará disponible. Usa URLs de imágenes externas.")
                return False
            
            # Inicializar Firebase Admin
            cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred, {
                'storageBucket': Config.FIREBASE_STORAGE_BUCKET
            })
            
            self._initialized = True
            logger.info(f"✅ Firebase Storage inicializado: {Config.FIREBASE_STORAGE_BUCKET}")
            return True
        except Exception as e:
            logger.error(f"❌ Error al inicializar Firebase: {e}")
            return False
    
    def upload_image(self, file_path, destination_path):
        """
        Subir una imagen a Firebase Storage
        
        Args:
            file_path: Ruta local del archivo
            destination_path: Ruta en Firebase Storage (ej: 'noticias/imagen1.jpg')
        
        Returns:
            URL pública de la imagen o None si hay error
        """
        if not self._initialized:
            logger.warning("⚠️ Firebase no está inicializado")
            return None
        
        try:
            bucket = storage.bucket()
            blob = bucket.blob(destination_path)
            
            # Subir archivo
            blob.upload_from_filename(file_path)
            
            # Hacer público el archivo
            blob.make_public()
            
            # Obtener URL pública
            url = blob.public_url
            logger.info(f"✅ Imagen subida: {url}")
            return url
        except Exception as e:
            logger.error(f"❌ Error al subir imagen a Firebase: {e}")
            return None
    
    def delete_image(self, destination_path):
        """
        Eliminar una imagen de Firebase Storage
        
        Args:
            destination_path: Ruta en Firebase Storage
        """
        if not self._initialized:
            return False
        
        try:
            bucket = storage.bucket()
            blob = bucket.blob(destination_path)
            blob.delete()
            logger.info(f"✅ Imagen eliminada: {destination_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Error al eliminar imagen: {e}")
            return False
    
    def get_image_url(self, destination_path):
        """
        Obtener URL pública de una imagen
        
        Args:
            destination_path: Ruta en Firebase Storage
        
        Returns:
            URL pública o None si no existe
        """
        if not self._initialized:
            return None
        
        try:
            bucket = storage.bucket()
            blob = bucket.blob(destination_path)
            
            if blob.exists():
                blob.make_public()
                return blob.public_url
            return None
        except Exception as e:
            logger.error(f"❌ Error al obtener URL: {e}")
            return None

