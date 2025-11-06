"""
Script para probar el login directamente
"""
import sys
import os
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

from database import Database

def test_login():
    """Probar login directamente"""
    print("=" * 60)
    print("PRUEBA DE LOGIN")
    print("=" * 60)
    
    db = Database()
    
    # Simular login
    usuario = "admin"
    password = "1234"
    
    print(f"\nIntentando login con:")
    print(f"  Usuario: {usuario}")
    print(f"  Password: {password}")
    
    try:
        # Buscar usuario
        user = db.execute_query(
            "SELECT idUsuario, usuario, contrasena, nombre, rol FROM usuarios_nul WHERE usuario = %s",
            (usuario,),
            fetch_one=True
        )
        
        if user:
            print(f"\n[OK] Usuario encontrado:")
            print(f"  ID: {user['idUsuario']}")
            print(f"  Usuario: {user['usuario']}")
            print(f"  Contrasena en BD: '{user['contrasena']}'")
            print(f"  Password recibido: '{password}'")
            print(f"  Tipo contrasena: {type(user['contrasena'])}")
            print(f"  Tipo password: {type(password)}")
            print(f"  Son iguales: {user['contrasena'] == password}")
            
            if user['contrasena'] == password:
                print("\n[OK] Login exitoso!")
                return True
            else:
                print("\n[ERROR] Contrasenas no coinciden")
                return False
        else:
            print("\n[ERROR] Usuario no encontrado")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_login()
    sys.exit(0 if success else 1)

