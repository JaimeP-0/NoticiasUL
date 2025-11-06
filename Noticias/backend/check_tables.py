"""
Script para verificar la estructura de las tablas
"""
import sys
import os
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from database import Database

def check_tables():
    """Verificar estructura de tablas"""
    db = Database()
    connection = db.get_connection()
    cursor = connection.cursor()
    
    print("=" * 60)
    print("ESTRUCTURA DE TABLAS")
    print("=" * 60)
    
    # Verificar tabla usuarios_nul
    print("\n[INFO] Tabla: usuarios_nul")
    try:
        cursor.execute("DESCRIBE usuarios_nul")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Verificar tabla noticias_nul
    print("\n[INFO] Tabla: noticias_nul")
    try:
        cursor.execute("DESCRIBE noticias_nul")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    cursor.close()
    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_tables()

