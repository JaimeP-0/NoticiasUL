# Patrones de Diseño Implementados

Este documento explica los patrones de diseño **Singleton** y **Factory** implementados en el proyecto, su propósito práctico y cómo aportan valor a los usuarios.

---

## 📋 Tabla de Contenidos

1. [Patrón Singleton](#patrón-singleton)
2. [Patrón Factory](#patrón-factory)
3. [Beneficios para los Usuarios](#beneficios-para-los-usuarios)
4. [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🔒 Patrón Singleton

### ¿Qué es?

El patrón Singleton garantiza que una clase tenga **una única instancia** durante toda la ejecución de la aplicación y proporciona un punto de acceso global a ella.

### Implementaciones en el Proyecto

#### 1. **Database** (`database.py`)

```python
class Database:
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
```

**Propósito:**
- Gestiona el **pool de conexiones MySQL** de forma eficiente
- Evita crear múltiples pools de conexiones (costoso en recursos)
- Garantiza que todas las partes de la aplicación usen la misma conexión

**Valor para el Usuario:**
- ✅ **Mejor rendimiento**: Reutiliza conexiones existentes en lugar de crear nuevas
- ✅ **Menor consumo de recursos**: Solo mantiene un pool de conexiones
- ✅ **Mayor estabilidad**: Evita problemas de conexiones duplicadas o agotadas

**Uso:**
```python
db1 = Database()  # Primera instancia
db2 = Database()  # Misma instancia que db1
# db1 y db2 son el mismo objeto
```

---

#### 2. **FirebaseService** (`firebase_service.py`)

```python
class FirebaseService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
        return cls._instance
```

**Propósito:**
- Gestiona la **inicialización única** de Firebase Admin SDK
- Evita múltiples inicializaciones que causarían errores
- Centraliza la configuración de Firebase Storage

**Valor para el Usuario:**
- ✅ **Subida de imágenes confiable**: Una sola configuración de Firebase
- ✅ **Sin errores de inicialización**: Evita conflictos por múltiples inicializaciones
- ✅ **Mejor gestión de recursos**: No duplica servicios de Firebase

**Uso:**
```python
firebase1 = FirebaseService()
firebase2 = FirebaseService()
# firebase1 y firebase2 son el mismo objeto
firebase1.initialize()  # Se inicializa una sola vez
```

---

#### 3. **ConfigSingleton** (`singleton_config.py`)

```python
class ConfigSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigSingleton, cls).__new__(cls)
            cls._instance.config = {...}
        return cls._instance
```

**Propósito:**
- Almacena configuración de la aplicación de forma centralizada
- Garantiza acceso consistente a la configuración

**Valor para el Usuario:**
- ✅ **Configuración consistente**: Todos los módulos ven la misma configuración
- ✅ **Fácil mantenimiento**: Un solo lugar para cambiar configuraciones

---

## 🏭 Patrón Factory

### ¿Qué es?

El patrón Factory proporciona una **interfaz para crear objetos** sin especificar la clase exacta del objeto que se creará. Permite crear objetos según parámetros o condiciones.

### Implementaciones en el Proyecto

#### 1. **NoticiaFactory** (`factory_noticias.py`)

**Propósito:**
Crea objetos `Noticia` especializados según el tipo de noticia (general, importante, evento, anuncio).

**Valor para el Usuario:**
- ✅ **Validación automática**: Cada tipo de noticia tiene reglas específicas
- ✅ **Estructura consistente**: Todas las noticias siguen el mismo formato
- ✅ **Extensibilidad**: Fácil agregar nuevos tipos de noticias

**Tipos de Noticias Disponibles:**

| Tipo | Características |
|------|----------------|
| `general` | Noticia estándar sin restricciones especiales |
| `importante` | Requiere imagen y palabras clave de importancia |
| `evento` | Debe incluir fecha/hora del evento y imagen |
| `anuncio` | Contenido corto y conciso (máx. 500 caracteres) |

**Ejemplo de Uso:**
```python
# Crear una noticia importante
noticia = NoticiaFactory.crear(
    tipo='importante',
    titulo='Anuncio Importante: Cambio de Horario',
    contenido='Se informa que...',
    autor='admin',
    imagen_url='https://...'
)
```

---

#### 2. **NoticiaValidatorFactory** (`validators.py`)

**Propósito:**
Crea validadores específicos según el tipo de noticia. Cada validador tiene reglas de validación diferentes.

**Valor para el Usuario:**
- ✅ **Validación inteligente**: Reglas diferentes según el tipo de noticia
- ✅ **Mensajes de error claros**: Indica exactamente qué falta o está mal
- ✅ **Calidad de contenido**: Asegura que las noticias cumplan estándares mínimos

**Ejemplo de Validación:**

```python
# Validar una noticia importante
validator = NoticiaValidatorFactory.create_validator('importante')
es_valido, error = validator.validate(
    titulo='Anuncio Importante',
    contenido='Contenido de la noticia...',
    autor='admin',
    imagen_url='https://...'
)

if not es_valido:
    print(f"Error: {error}")  # Ej: "Las noticias importantes deben incluir una imagen"
```

**Reglas por Tipo:**

| Tipo | Reglas Especiales |
|------|------------------|
| `general` | Mínimo 50 caracteres de contenido |
| `importante` | Mínimo 100 caracteres, requiere imagen, palabras clave en título |
| `evento` | Debe incluir fecha/hora, requiere imagen |
| `anuncio` | Máximo 500 caracteres, más permisivo |

---

#### 3. **RoleValidatorFactory** (`role_validators.py`)

**Propósito:**
Crea validadores de permisos según el rol del usuario. Cada rol tiene diferentes capacidades y reglas de validación.

**Valor para el Usuario:**
- ✅ **Seguridad mejorada**: Control granular de permisos por rol
- ✅ **Experiencia personalizada**: Cada rol ve y puede hacer cosas diferentes
- ✅ **Prevención de errores**: Valida permisos antes de realizar acciones

**Roles y Permisos:**

| Rol | Crear | Editar | Eliminar | Reglas Especiales |
|-----|-------|--------|----------|-------------------|
| `superadmin` | ✅ | ✅ (todas) | ✅ (todas) | Validación más permisiva |
| `admin` | ✅ | ✅ (todas) | ✅ (todas) | Validación estándar |
| `maestro` | ✅ | ✅ (solo propias) | ✅ (solo propias) | Requiere más contenido |
| `usuario` | ❌ | ❌ | ❌ | Solo lectura |

**Ejemplo de Uso:**

```python
# Obtener validador según el rol del usuario actual
validator = RoleValidatorFactory.create_validator('maestro')

# Verificar si puede editar una noticia específica
puede_editar = validator.can_edit_news(
    user_role='maestro',
    news_author='maestro1',
    current_user='maestro1'  # Solo puede editar sus propias noticias
)

# Obtener reglas de validación específicas del rol
reglas = validator.get_validation_rules('maestro')
# {'min_titulo_length': 5, 'min_contenido_length': 30, ...}
```

---

## 🎯 Beneficios para los Usuarios

### Rendimiento
- **Singleton**: Reduce el consumo de recursos al reutilizar conexiones y servicios
- **Factory**: Optimiza la creación de objetos según el contexto

### Seguridad
- **RoleValidatorFactory**: Control granular de permisos previene accesos no autorizados
- **NoticiaValidatorFactory**: Valida que el contenido cumpla estándares de calidad

### Experiencia de Usuario
- **Validaciones claras**: Mensajes de error específicos ayudan a corregir problemas
- **Funcionalidad diferenciada**: Cada rol tiene capacidades apropiadas a su función

### Mantenibilidad
- **Código organizado**: Patrones claros facilitan el mantenimiento
- **Extensibilidad**: Fácil agregar nuevos tipos de noticias o roles

---

## 📝 Ejemplos de Uso Completo

### Crear una Noticia con Validación

```python
# En el endpoint POST /api/news
data = request.get_json()
tipo_noticia = data.get("tipo", "general")

# 1. Obtener validador según el tipo
validator = NoticiaValidatorFactory.create_validator(tipo_noticia)

# 2. Validar los datos
es_valido, error = validator.validate(
    titulo=data.get("titulo"),
    contenido=data.get("contenido"),
    autor=data.get("autor"),
    imagen_url=data.get("imagen")
)

if not es_valido:
    return jsonify({"error": error}), 400

# 3. Crear objeto Noticia usando Factory
noticia = NoticiaFactory.crear(
    tipo=tipo_noticia,
    titulo=data.get("titulo"),
    contenido=data.get("contenido"),
    autor=data.get("autor"),
    imagen_url=data.get("imagen")
)

# 4. Guardar en base de datos
# ...
```

### Verificar Permisos por Rol

```python
# Obtener rol del usuario actual
user_role = get_user_role_from_request()

# Crear validador según el rol
role_validator = RoleValidatorFactory.create_validator(user_role)

# Verificar si puede realizar una acción
if not role_validator.can_edit_news(user_role, news_author, current_user):
    return jsonify({"error": "No tienes permisos para editar esta noticia"}), 403

# Obtener reglas de validación específicas del rol
reglas = role_validator.get_validation_rules(user_role)
min_length = reglas['min_contenido_length']
```

---

## 🔧 Extensibilidad

### Agregar un Nuevo Tipo de Noticia

```python
# 1. Crear clase de noticia
class NoticiaUrgente(Noticia):
    def __init__(self, titulo, contenido, autor, imagen_url=None):
        super().__init__(titulo, contenido, autor, tipo='urgente', imagen_url=imagen_url)
        self.prioridad = 'critica'

# 2. Crear validador
class NoticiaUrgenteValidator(NoticiaValidator):
    def validate(self, titulo, contenido, autor, imagen_url=None):
        # Reglas específicas para noticias urgentes
        ...

# 3. Registrar en el Factory
NoticiaValidatorFactory.register_validator('urgente', NoticiaUrgenteValidator)
```

### Agregar un Nuevo Rol

```python
# 1. Crear validador de rol
class EditorValidator(RoleBasedValidator):
    def can_create_news(self, user_role):
        return True
    # ...

# 2. Registrar en el Factory
RoleValidatorFactory.register_validator('editor', EditorValidator)
```

---

## 📚 Referencias

- [Singleton Pattern - Refactoring Guru](https://refactoring.guru/design-patterns/singleton)
- [Factory Pattern - Refactoring Guru](https://refactoring.guru/design-patterns/factory-method)
- [Python Design Patterns](https://python-patterns.guide/)

---

**Última actualización**: 2024

