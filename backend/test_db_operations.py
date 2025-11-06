"""
Script para probar operaciones de base de datos
"""
import sys
import os
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from database import Database

def test_operations():
    """Probar operaciones CRUD"""
    print("=" * 60)
    print("PRUEBA DE OPERACIONES EN BASE DE DATOS")
    print("=" * 60)
    
    db = Database()
    
    try:
        # Contar noticias
        result = db.execute_query("SELECT COUNT(*) as total FROM noticias_nul", fetch_one=True)
        print(f"\n[OK] Noticias en BD: {result['total']}")
        
        # Contar usuarios
        result = db.execute_query("SELECT COUNT(*) as total FROM usuarios_nul", fetch_one=True)
        print(f"[OK] Usuarios en BD: {result['total']}")
        
        # Listar usuarios
        usuarios = db.execute_query("SELECT idUsuario, usuario, rol FROM usuarios_nul", fetch_all=True)
        if usuarios:
            print(f"\n[INFO] Usuarios encontrados:")
            for u in usuarios:
                print(f"  - {u['usuario']} (rol: {u.get('rol', 'N/A')})")
        
        print("\n[OK] Todas las operaciones funcionaron correctamente!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        return False

if __name__ == "__main__":
    success = test_operations()
    sys.exit(0 if success else 1)

