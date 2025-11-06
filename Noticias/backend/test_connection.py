"""
Script para probar la conexión a MySQL
"""
import sys
import os
# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from database import Database
from config import Config

def test_connection():
    """Probar conexión a MySQL"""
    print("=" * 50)
    print("PRUEBA DE CONEXIÓN A MYSQL")
    print("=" * 50)
    print(f"Host: {Config.MYSQL_HOST}")
    print(f"Puerto: {Config.MYSQL_PORT}")
    print(f"Base de datos: {Config.MYSQL_DATABASE}")
    print(f"Usuario: {Config.MYSQL_USER}")
    print("=" * 50)
    
    try:
        db = Database()
        connection = db.get_connection()
        
        if connection.is_connected():
            print("[OK] Conexion exitosa a MySQL!")
            
            # Probar consulta simple
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"[OK] Version de MySQL: {version[0]}")
            
            # Verificar si las tablas existen
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"\n[OK] Tablas encontradas: {len(tables)}")
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("\n[INFO] No se encontraron tablas. Se crearan automaticamente.")
                print("   Ejecutando inicializacion de tablas...")
                if db.init_tables():
                    print("[OK] Tablas creadas exitosamente")
                else:
                    print("[ERROR] Error al crear tablas")
            
            cursor.close()
            return True
        else:
            print("[ERROR] No se pudo conectar a MySQL")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error al conectar: {e}")
        print("\n[INFO] Verifica:")
        print("   1. Que el servidor MySQL este accesible")
        print("   2. Que las credenciales en .env sean correctas")
        print("   3. Que tu IP este permitida en el servidor remoto")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

