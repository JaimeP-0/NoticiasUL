# 🔧 Guía de Configuración - MySQL y Firebase

Esta guía explica cómo configurar MySQL y Firebase Storage para el proyecto Noticias Universitarias.

## 📋 Índice

1. [Configuración de MySQL](#mysql)
2. [Configuración de Firebase](#firebase)
3. [Instalación de Dependencias](#instalacion)
4. [Configuración de Variables de Entorno](#variables)
5. [Inicialización de la Base de Datos](#inicializacion)
6. [Verificación](#verificacion)

---

## 🗄️ MySQL

### Paso 1: Instalar MySQL

**Windows:**
1. Descarga MySQL desde: https://dev.mysql.com/downloads/installer/
2. Ejecuta el instalador y sigue las instrucciones
3. Anota la contraseña del usuario `root` que configures

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### Paso 2: Crear la Base de Datos

Abre una terminal y ejecuta:

```bash
mysql -u root -p
```

Luego ejecuta:

```sql
CREATE DATABASE noticias_ul CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Paso 3: Inicializar las Tablas

Ejecuta el script SQL de inicialización:

```bash
cd backend
mysql -u root -p noticias_ul < init_database.sql
```

O manualmente desde MySQL:

```bash
mysql -u root -p
USE noticias_ul;
SOURCE init_database.sql;
```

---

## 🔥 Firebase Storage

### Paso 1: Crear Proyecto en Firebase

1. Ve a https://console.firebase.google.com/
2. Haz clic en "Agregar proyecto"
3. Ingresa un nombre para tu proyecto (ej: `noticias-universitarias`)
4. Sigue los pasos del asistente

### Paso 2: Habilitar Firebase Storage

1. En la consola de Firebase, ve a **Storage** en el menú lateral
2. Haz clic en "Comenzar"
3. Selecciona el modo de seguridad (puedes usar "Modo de prueba" para desarrollo)
4. Selecciona la ubicación del bucket (ej: `us-central1`)
5. Haz clic en "Listo"

### Paso 3: Obtener Credenciales de Administrador

1. Ve a **Configuración del proyecto** (⚙️) > **Cuentas de servicio**
2. Haz clic en "Generar nueva clave privada"
3. Se descargará un archivo JSON con las credenciales
4. **Renombra** este archivo a `firebase-credentials.json`
5. **Mueve** el archivo a la carpeta `backend/`

### Paso 4: Obtener el Nombre del Bucket

1. Ve a **Storage** en Firebase Console
2. En la parte superior verás el nombre del bucket (ej: `tu-proyecto.appspot.com`)
3. Anota este nombre, lo necesitarás para la configuración

---

## 📦 Instalación de Dependencias

### Paso 1: Activar el Entorno Virtual

**Windows (PowerShell):**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
cd backend
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
cd backend
source venv/bin/activate
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- `mysql-connector-python` - Para conectar a MySQL
- `firebase-admin` - Para Firebase Storage
- `python-dotenv` - Para variables de entorno

---

## 🔐 Variables de Entorno

### Paso 1: Crear Archivo .env

Crea un archivo `.env` en la carpeta `backend/` (copia de `.env.example`):

**Windows:**
```powershell
copy .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

### Paso 2: Configurar Variables

Abre el archivo `.env` y configura las siguientes variables:

```env
# ============================================
# CONFIGURACIÓN DE MYSQL
# ============================================
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tu_password_mysql_aqui
MYSQL_DATABASE=noticias_ul

# ============================================
# CONFIGURACIÓN DE FIREBASE
# ============================================
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
FIREBASE_STORAGE_BUCKET=tu-proyecto.appspot.com

# ============================================
# CONFIGURACIÓN DE FLASK
# ============================================
SECRET_KEY=dev-secret-key-change-in-production
FLASK_DEBUG=True
CORS_ORIGINS=http://localhost:4321
```

**⚠️ IMPORTANTE:**
- Reemplaza `tu_password_mysql_aqui` con tu contraseña de MySQL
- Reemplaza `tu-proyecto.appspot.com` con el nombre de tu bucket de Firebase
- En producción, cambia `SECRET_KEY` por una clave secreta fuerte

---

## 🚀 Inicialización

### Paso 1: Verificar Archivos

Asegúrate de tener estos archivos en `backend/`:
- ✅ `.env` (configurado)
- ✅ `firebase-credentials.json` (si usas Firebase)
- ✅ `init_database.sql`

### Paso 2: Ejecutar el Backend

**Windows:**
```powershell
.\run.ps1
```

**Linux/macOS:**
```bash
python app.py
```

Si todo está bien configurado, deberías ver:
```
✅ Base de datos inicializada
✅ Firebase Storage inicializado: tu-proyecto.appspot.com
 * Running on http://127.0.0.1:5000
```

---

## ✅ Verificación

### Verificar MySQL

1. Abre una terminal de MySQL:
```bash
mysql -u root -p noticias_ul
```

2. Verifica que las tablas existan:
```sql
SHOW TABLES;
-- Deberías ver: usuarios, noticias

SELECT * FROM usuarios;
-- Deberías ver el usuario 'admin'
```

### Verificar Firebase

1. Intenta subir una imagen desde el código (esto se implementará en el frontend)
2. Verifica en Firebase Console > Storage que los archivos se suban correctamente

### Verificar Backend

1. Abre http://127.0.0.1:5000/api/news en tu navegador
2. Deberías ver un JSON con las noticias (vacío o con datos de ejemplo)

---

## 🔧 Solución de Problemas

### Error: "Can't connect to MySQL server"

**Solución:**
- Verifica que MySQL esté ejecutándose
- Verifica las credenciales en `.env`
- Verifica que el puerto sea correcto (3306 por defecto)

### Error: "Access denied for user"

**Solución:**
- Verifica el usuario y contraseña en `.env`
- Asegúrate de que el usuario tenga permisos para acceder a la base de datos:
```sql
GRANT ALL PRIVILEGES ON noticias_ul.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### Error: "Firebase credentials not found"

**Solución:**
- Verifica que `firebase-credentials.json` esté en la carpeta `backend/`
- Verifica que `FIREBASE_CREDENTIALS_PATH` en `.env` apunte al archivo correcto
- ⚠️ Si no quieres usar Firebase, la aplicación funcionará sin él (solo no se subirán imágenes)

### Error: "Database not found"

**Solución:**
- Crea la base de datos manualmente:
```sql
CREATE DATABASE noticias_ul CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
- Luego ejecuta `init_database.sql`

---

## 📝 Notas Importantes

1. **Seguridad:**
   - ⚠️ En producción, usa `bcrypt` para hashear contraseñas
   - ⚠️ No subas el archivo `.env` a Git (agrégalo a `.gitignore`)
   - ⚠️ No subas `firebase-credentials.json` a Git

2. **Firebase es Opcional:**
   - Si no configuras Firebase, la aplicación funcionará normalmente
   - Solo las imágenes no se subirán automáticamente a Firebase Storage
   - Puedes usar URLs de imágenes externas directamente

3. **Backup:**
   - Haz backups regulares de tu base de datos MySQL
   - Usa `mysqldump` para crear backups:
```bash
mysqldump -u root -p noticias_ul > backup.sql
```

---

## 📚 Recursos Adicionales

- [Documentación de MySQL](https://dev.mysql.com/doc/)
- [Documentación de Firebase Storage](https://firebase.google.com/docs/storage)
- [Documentación de mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
- [Documentación de firebase-admin](https://firebase.google.com/docs/admin/setup)

