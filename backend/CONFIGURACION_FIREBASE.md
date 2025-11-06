# 🔥 Configuración de Firebase Storage

Esta guía te ayudará a configurar Firebase Storage para subir imágenes en tu aplicación.

## 📋 Pasos para obtener las credenciales

### Paso 1: Ve a Firebase Console
1. Abre tu navegador y ve a [Firebase Console](https://console.firebase.google.com/)
2. Selecciona tu proyecto **noticiasul** (o créalo si no existe)

### Paso 2: Habilitar Firebase Storage
1. En el menú lateral, haz clic en **Storage**
2. Si no está habilitado, haz clic en **"Comenzar"** o **"Get started"**
3. Selecciona **"Modo de prueba"** (puedes cambiar las reglas después)
4. Selecciona una ubicación para tu bucket (ej: `us-central1`)
5. Haz clic en **"Listo"**

### Paso 3: Obtener credenciales de administrador
1. Ve a **Configuración del proyecto** (⚙️) en la parte superior izquierda
2. Haz clic en la pestaña **"Cuentas de servicio"**
3. Haz clic en **"Generar nueva clave privada"**
4. Se descargará un archivo JSON (ej: `noticiasul-firebase-adminsdk-xxxxx-xxxxxxxxxx.json`)

### Paso 4: Configurar el archivo de credenciales
1. **Renombra** el archivo descargado a: `firebase-credentials.json`
2. **Mueve** el archivo a la carpeta `backend/` de tu proyecto

**Ubicación final:**
```
NoticiasUL/
  └── Noticias/
      └── backend/
          └── firebase-credentials.json  ← Aquí debe estar
```

### Paso 5: Verificar el bucket
1. En Firebase Console, ve a **Storage**
2. En la parte superior verás el nombre del bucket
3. Debe ser: `noticiasul.firebasestorage.app` o similar

### Paso 6: Configurar reglas de Storage (opcional)
1. Ve a **Storage** > **Reglas**
2. Actualiza las reglas para permitir lectura pública:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /noticias/{imageId} {
      allow read: if true;  // Permitir lectura pública
      allow write: if false; // Solo escritura desde el backend con credenciales
    }
  }
}
```

3. Haz clic en **"Publicar"**

## ✅ Verificación

1. Reinicia tu servidor Flask
2. Abre en tu navegador: `http://127.0.0.1:5000/api/firebase-status`
3. Deberías ver:
```json
{
  "initialized": true,
  "credentials_path": "firebase-credentials.json",
  "credentials_exists": true,
  "bucket": "noticiasul.firebasestorage.app"
}
```

## 🔧 Solución de problemas

### Error: "Archivo de credenciales no encontrado"
- Verifica que el archivo esté en `backend/firebase-credentials.json`
- Verifica que el nombre del archivo sea exactamente `firebase-credentials.json`

### Error: "Permission denied" al subir
- Verifica que las credenciales tengan permisos de Storage Admin
- Verifica las reglas de Storage en Firebase Console

### Error: "Bucket not found"
- Verifica que el bucket existe en Firebase Console
- Verifica que el nombre del bucket en `.env` sea correcto

## 📝 Notas importantes

⚠️ **NUNCA** subas el archivo `firebase-credentials.json` a Git
- El archivo ya está en `.gitignore`
- Es información sensible que debe mantenerse privada

✅ Las imágenes se subirán automáticamente a Firebase Storage cuando:
- El archivo `firebase-credentials.json` existe
- Firebase está correctamente inicializado
- El bucket tiene permisos configurados

