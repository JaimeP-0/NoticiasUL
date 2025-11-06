# Guía de Configuración - Noticias Universitarias

## 📋 Configuración de Disqus

### Ubicación del archivo:
`NoticiasUL/Noticias/frontend/src/pages/noticias.astro`

### Cambios necesarios:

1. **Línea 223** - En la función `cargarDisqus()`:
   ```javascript
   const DISQUS_SHORTNAME = 'TU-DISQUS-SHORTNAME';
   ```
   **Cambiar por:** Tu identificador de Disqus real (ejemplo: `'tudominio-ejemplo'`)

2. **Línea 243** - En el script inline:
   ```javascript
   s.src = 'https://TU-DISQUS-SHORTNAME.disqus.com/embed.js';
   ```
   **Cambiar por:** `'https://tudominio-ejemplo.disqus.com/embed.js'`

### Cómo obtener tu identificador de Disqus:
1. Ve a https://disqus.com/admin/ y crea una cuenta o inicia sesión
2. Crea un nuevo sitio/web
3. Copia el "Shortname" que te asignan
4. Reemplázalo en los dos lugares mencionados arriba

---

## 🔐 Configuración del Login

### Ubicación del archivo:
`NoticiasUL/Noticias/backend/app.py`

### Cambios necesarios:

**Línea 11** - Para agregar/modificar usuarios:
```python
usuarios = {"admin": "1234"}
```

**Ejemplos:**
- Agregar más usuarios:
  ```python
  usuarios = {
      "admin": "1234",
      "editor": "password123",
      "usuario1": "clave456"
  }
  ```

- Cambiar contraseña del admin:
  ```python
  usuarios = {"admin": "nueva_password"}
  ```

### ⚠️ IMPORTANTE:
- Las credenciales actuales son: **usuario: `admin`**, **password: `1234`**
- El frontend ya está configurado correctamente (usa `username` pero lo convierte a `usuario` para el backend)
- No necesitas cambiar nada en el frontend para modificar usuarios

---

## 📝 Resumen de Archivos a Modificar

### Para Disqus:
1. `src/pages/noticias.astro` - Línea 223 y 243

### Para Login:
1. `backend/app.py` - Línea 11 (para agregar/modificar usuarios)

---

## ✅ Verificación

**Disqus:**
- Después de cambiar el shortname, recarga la página de noticias
- Deberías ver el widget de Disqus aparecer debajo de los comentarios propios

**Login:**
- Las credenciales funcionan inmediatamente después de modificar `app.py`
- No necesitas reiniciar el servidor (si está en modo debug)

---

## 🗄️ Configuración de MySQL y Firebase

Para configurar MySQL y Firebase Storage, consulta la guía completa:

**📄 Ver:** `backend/CONFIGURACION_BD.md`

### Resumen rápido:

1. **Instalar MySQL** y crear la base de datos `noticias_ul`
2. **Configurar Firebase** y obtener `firebase-credentials.json`
3. **Instalar dependencias:** `pip install -r requirements.txt`
4. **Configurar `.env`** con tus credenciales
5. **Inicializar tablas:** Ejecutar `init_database.sql`

Para más detalles, lee el archivo `CONFIGURACION_BD.md` en la carpeta `backend/`.

