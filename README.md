# Sistema de Gestión de Tiendas

Sistema integral de gestión empresarial para administración de múltiples tiendas, inventario, ventas, servicios y finanzas. Desarrollado con Django REST Framework para proporcionar un backend robusto y escalable.

## 📋 Descripción del Proyecto

Este sistema permite la gestión completa de negocios con múltiples tiendas, diseñado específicamente para:

- **Gestión de Tiendas**: Administración de múltiples sedes con inventarios independientes
- **Control de Inventario**: Sistema de lotes (FIFO) con trazabilidad completa de productos
- **Ventas y Facturación**: Registro de ventas con boletas, gestión de créditos y métodos de pago
- **Servicios**: Facturación de servicios con seguimiento de deudas
- **Finanzas**: Control de gastos fijos y variables, cierre de caja diario
- **Recursos Humanos**: Gestión de trabajadores, salarios y horas trabajadas
- **Reportes**: Visualización de ganancias diarias, semanales y mensuales

## 🎯 Características Principales

### Roles de Usuario
- **Dueño**: Acceso completo, creación de tiendas, visualización de reportes consolidados
- **Administrador de Tienda**: Gestión completa de una tienda específica
- **Trabajador**: Registro de ventas, servicios y cierre de caja

### Módulos del Sistema

#### 1. **Gestión de Tiendas** (`apps/tiendas`)
- Creación y administración de múltiples sedes
- Asignación de trabajadores por tienda
- Información personal y salarial de empleados
- Control de horas trabajadas (con descuento de almuerzo)

#### 2. **Inventario** (`apps/inventario`)
- **Sistema de Lotes (FIFO)**: El producto más antiguo sale primero
- Cada lote incluye:
  - ID único del lote
  - Fecha de llegada
  - Productos con cantidad
  - Costo de operación
  - Costo de transporte
- **Productos**: Nombre, ID, precio de compra, precio de venta

#### 3. **Ventas** (`apps/ventas`)
- **Boletas de Venta** con:
  - Fecha de venta
  - Datos del cliente (nombre, número, dirección - opcionales)
  - Productos vendidos (FIFO automático)
  - Precio de venta ajustable (con validación de margen de ganancia)
  - Método de pago
- **Sistema de Créditos**:
  - Gestión de saldo y deuda
  - Historial de deudas por cliente
  - Datos obligatorios del cliente para créditos

#### 4. **Servicios** (`apps/servicios`)
- Registro de servicios prestados
- Descripción del servicio
- Responsable del servicio
- Fecha o rango de fechas
- Costo del servicio
- Opción de crédito

#### 5. **Finanzas** (`apps/finanzas`)
- **Gastos Mensuales**:
  - Gastos fijos (programables en calendario)
  - Gastos variables (registro diario)
- **Cierre de Caja**:
  - Conteo de efectivo
  - Comparación con ventas del día
  - Deducción de gastos
  - Registro de faltantes con responsable
  - Estado: Correcto/Pendiente

#### 6. **Usuarios** (`apps/users`)
- Sistema de autenticación y autorización
- Gestión de roles y permisos
- Perfil de usuario

### Visualizaciones y Reportes
- 📊 Ganancias diarias, semanales y mensuales
- 💰 Deudas pendientes
- 📅 Calendario de gastos fijos programados
- 👥 Organigrama de la empresa
- ⏰ Registro de horas trabajadas (actual y histórico)
- 🔍 Filtros avanzados en ventas y productos

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 6.0.2
- **API**: Django REST Framework 3.16.1
- **Autenticación**: JWT (djangorestframework_simplejwt 5.5.1)
- **Base de Datos**: PostgreSQL (psycopg2-binary 2.9.11)
- **Filtros**: django-filter 25.2
- **Variables de Entorno**: python-dotenv 1.2.1

## 📦 Requisitos Previos

### Para Windows y Linux:
- Python 3.13.3
- PostgreSQL 15 
- Docker Desktop (Windows) o Docker Engine (Linux)
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### Windows

#### 1. Instalar Python
1. Descargar Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, marcar "Add Python to PATH"
3. Verificar instalación:
```cmd
python --version
pip --version   
```

#### 2. Instalar Docker
1. Descargar e instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Iniciar Docker Desktop y asegurar que esté corriendo

#### 3. Clonar o Descargar el Proyecto
```cmd
https://github.com/GiomarMC/EXPENSE-MANAGEMENT-SYSTEM.git
```

#### 4. Crear Entorno Virtual
```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### 5. Instalar Dependencias
```cmd
cd core
pip install -r requirements.txt
```

#### 6. Configurar Variables de Entorno
Crear archivo `.env` en la carpeta `core/` (necesario para Docker y Django):
```env
# Base de Datos
POSTGRES_DB=gestion_tiendas
POSTGRES_USER=gestion_user
POSTGRES_PASSWORD=tu_contraseña_segura
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Django
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET_KEY=otra-clave-secreta-para-jwt
```

#### 7. Levantar Base de Datos (Docker)
Ejecutar desde la raíz del proyecto (donde está `compose.yml`):
```cmd
docker compose up -d
```
Esto levantará el contenedor de PostgreSQL configurado automáticamente.

#### 8. Ejecutar Migraciones
```cmd
python manage.py makemigrations
python manage.py migrate
```

#### 9. Crear Superusuario
```cmd
python manage.py createsuperuser
```

#### 10. Ejecutar el Servidor
```cmd
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

---

### Linux (Ubuntu/Debian)

#### 1. Actualizar Sistema
```bash
sudo apt update
sudo apt upgrade -y
```

#### 2. Instalar Python y pip
```bash
sudo apt install python3 python3-pip python3-venv -y
python3 --version
pip3 --version
```

#### 3. Instalar Docker
```bash
# Instalar Docker y Docker Compose
sudo apt install docker.io docker-compose-v2 -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
# (Cerrar sesión e iniciar de nuevo para aplicar cambios de grupo)
```

#### 4. Clonar o Navegar al Proyecto
```bash
cd ~/Projects/Gestion_gastos/Gestion_gastos
```

#### 5. Crear Entorno Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 6. Instalar Dependencias
```bash
cd core
pip install -r requirements.txt
```

#### 7. Configurar Variables de Entorno
Crear archivo `.env` en la carpeta `core/`:
```bash
nano .env
```

Contenido:
```env
# Base de Datos
POSTGRES_DB=gestion_tiendas
POSTGRES_USER=gestion_user
POSTGRES_PASSWORD=tu_contraseña_segura
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Django
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET_KEY=otra-clave-secreta-para-jwt
```

Guardar con `Ctrl+O`, Enter, `Ctrl+X`

#### 8. Levantar Base de Datos
Desde la raíz del proyecto:
```bash
docker compose up -d
```

Guardar con `Ctrl+O`, Enter, `Ctrl+X`

#### 9. Ejecutar Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 10. Crear Superusuario
```bash
python manage.py createsuperuser
```

#### 11. Ejecutar el Servidor
```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

---

## 🎮 Uso del Sistema

### Iniciar el Servidor de Desarrollo

**Windows:**
```cmd
cd *\Gestion_gastos\core
.venv\Scripts\activate
python manage.py runserver
```

**Linux:**
```bash
cd */Gestion_gastos/core
source .venv/bin/activate
python manage.py runserver
```

### Acceder al Sistema

1. **API REST**: `http://localhost:8000/api/`
2. **Panel de Administración**: `http://localhost:8000/admin/`
   - Usuario: el superusuario creado
   - Contraseña: la contraseña del superusuario

### Endpoints Principales

```
/api/users/          - Gestión de usuarios
/api/tiendas/        - Gestión de tiendas
/api/inventario/     - Gestión de inventario y lotes
/api/ventas/         - Registro de ventas y boletas
/api/servicios/      - Gestión de servicios
/api/finanzas/       - Control financiero y gastos
```

### Documentación (Swagger / OpenAPI)

Las rutas para la documentación automática de la API (Swagger / ReDoc / schema) son:

```
GET  /api/schema/    - OpenAPI schema (JSON)
GET  /api/docs/      - Swagger UI (documentación interactiva)
GET  /api/redoc/     - ReDoc UI (documentación alternativa)
```

Abre `/api/docs/` en tu servidor (por ejemplo `http://localhost:8000/api/docs/`) para ver la documentación completa y probar los endpoints.

## 📱 Desarrollo Móvil (Próximamente)

Este backend está diseñado para soportar una aplicación móvil. La API REST permite:
- Autenticación mediante JWT
- CRUD completo de todas las entidades
- Filtros y búsquedas avanzadas
- Reportes y estadísticas

## 🔒 Seguridad

- Autenticación basada en JWT
- Permisos por rol (Dueño, Administrador, Trabajador)
- Validación de datos en el backend
- Protección contra inyección SQL (ORM de Django)
- Variables sensibles en archivo `.env` (no incluido en el repositorio)

## 📝 Notas Importantes

1. **Archivo `.env`**: Nunca compartir este archivo. Contiene información sensible.
2. **Migraciones**: Ejecutar `python manage.py makemigrations` y `python manage.py migrate` después de cambios en los modelos.
3. **Entorno Virtual**: Siempre activar el entorno virtual antes de trabajar en el proyecto.
4. **Puerto 8000**: Asegurarse de que el puerto 8000 esté disponible o cambiar con `python manage.py runserver 8080`.

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
**Solución**: Activar el entorno virtual
```bash
# Windows
.venv\Scripts\activate

# Linux
source .venv/bin/activate
```

### Error de conexión a PostgreSQL
**Solución**: Verificar que el contenedor de Docker esté corriendo
```bash
docker compose ps
# Si no está corriendo:
docker compose up -d
```

### Error: "Port 8000 is already in use"
**Solución**: Usar otro puerto
```bash
python manage.py runserver 8080
```

## 👥 Contribución

Para contribuir al proyecto:
1. Crear una rama nueva: `git checkout -b feature/nueva-funcionalidad`
2. Realizar cambios y commit: `git commit -m "Descripción del cambio"`
3. Push a la rama: `git push origin feature/nueva-funcionalidad`
4. Crear un Pull Request

## 📄 Licencia

Este proyecto es privado y está destinado para uso interno.

## 📞 Soporte

Para preguntas o problemas, contactar al equipo de desarrollo.

---

**Versión**: 1.0.0  
**Última actualización**: Febrero 2026  
**Desarrollado con**: ❤️ y Django
