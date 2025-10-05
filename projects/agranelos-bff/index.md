# BFF (Backend For Frontend) - Agranelos

Este proyecto implementa un BFF (Backend For Frontend) en Java con Spring Boot, encargado de exponer APIs RESTful para la gestión de productos, bodegas y consultas GraphQL, orquestando llamadas a funciones serverless (Azure Functions) y devolviendo respuestas en formato JSON.

---

## 🚀 Endpoints REST

### Productos
- `GET /api/productos` — Lista todos los productos.
- `GET /api/productos/{id}` — Obtiene un producto por ID.
- `POST /api/productos` — Crea un nuevo producto.
- `PUT /api/productos/{id}` — Actualiza un producto existente.
- `DELETE /api/productos/{id}` — Elimina un producto.

### Bodegas
- `GET /api/bodegas` — Lista todas las bodegas.
- `GET /api/bodegas/{id}` — Obtiene una bodega por ID.
- `POST /api/bodegas` — Crea una nueva bodega.
- `PUT /api/bodegas/{id}` — Actualiza una bodega existente.
- `DELETE /api/bodegas/{id}` — Elimina una bodega.

### GraphQL
- `GET /api/graphql` — Información del endpoint GraphQL.
- `POST /api/graphql` — Ejecuta consultas GraphQL sobre productos y bodegas.

Para más detalles sobre los endpoints y ejemplos de uso, consulta [ENDPOINTS_MAPPING.md](ENDPOINTS_MAPPING.md) y [IMPLEMENTACION_ENDPOINTS.md](IMPLEMENTACION_ENDPOINTS.md).

---

## 🛠️ Tecnologías

- Java 17+
- Spring Boot 3.x
- Docker
- Maven
- Azure Functions (invocación vía HTTP)
- Variables de entorno para configuración sensible

---

## ⚙️ Configuración

1. **Variables de entorno**  
   Configura las siguientes variables antes de ejecutar el BFF:
   - `AZURE_FUNCTIONS_BASE_URL`: URL base de las funciones serverless.
   - `AZURE_FUNCTIONS_API_KEY`: (si aplica) API Key para invocar funciones protegidas.

2. **Archivo de configuración**  
   Puedes sobreescribir propiedades en `src/main/resources/application.yml`.

---

## 🐳 Uso con Docker/Podman

```bash
# Construir la imagen con Docker
docker build -t agranelos-bff .

# O con Podman
podman build -t agranelos-bff .

# Ejecutar el contenedor
docker run -p 8080:8080 \
  -e AZURE_FUNCTIONS_BASE_URL="https://<tu-app>.azurewebsites.net/api" \
  -e SPRING_SECURITY_USER_NAME="user" \
  -e SPRING_SECURITY_USER_PASSWORD="myStrongPassword123" \
  agranelos-bff

# O con Podman
podman run -d --name agranelos-bff -p 8080:8080 \
  -e AZURE_FUNCTIONS_BASE_URL="https://<tu-app>.azurewebsites.net/api" \
  -e SPRING_SECURITY_USER_NAME="user" \
  -e SPRING_SECURITY_USER_PASSWORD="myStrongPassword123" \
  agranelos-bff
```

Ver [PRUEBAS_PODMAN.md](PRUEBAS_PODMAN.md) para más detalles sobre pruebas con contenedores.

---

## 🧪 Pruebas Locales

### Maven
- Ejecuta las pruebas con Maven:
  ```bash
  mvn clean test
  ```
- Puedes usar Azure Functions Core Tools para simular funciones localmente.

### Postman
- Importa la colección `Agranelos-BFF.postman_collection.json` en Postman.
- Importa los entornos desde la carpeta `postman/`:
  - **Local.postman_environment.json** - Para desarrollo local
  - **Docker.postman_environment.json** - Para contenedores locales
  - **AWS.postman_environment.json** - Para despliegue en AWS
  - **Azure.postman_environment.json** - Para despliegue en Azure
- La colección incluye ejemplos organizados para:
  - **Productos:** 5 endpoints con datos de prueba
  - **Bodegas:** 5 endpoints con datos de prueba
  - **GraphQL:** 5 consultas de ejemplo (productos, bodegas, queries parametrizadas)
- Variables preconfiguradas:
  - `base_url`: http://localhost:8080
  - `producto_id`: 1
  - `bodega_id`: 1
  - `username`: user
  - `password`: myStrongPassword123

### Ejemplos con cURL

```bash
# Listar productos
curl -u user:myStrongPassword123 http://localhost:8080/api/productos

# Crear bodega
curl -u user:myStrongPassword123 -X POST http://localhost:8080/api/bodegas \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Bodega Norte","ubicacion":"Calle 123","capacidad":3000}'

# Consulta GraphQL
curl -u user:myStrongPassword123 -X POST http://localhost:8080/api/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ productos { id nombre precio } }"}'
```

---

## 🔒 Buenas Prácticas

- No expongas información sensible en logs ni respuestas de error.
- Valida y sanitiza todas las entradas del usuario.
- Usa control de versiones (Git) y sigue buenas prácticas de colaboración.

---

## 📂 Estructura del Proyecto

```
src/
  main/
    java/com/agranelos/bff/
      controller/
        ProductoController.java
        BodegaController.java
        GraphQLController.java
      dto/
        ProductoDto.java
        BodegaDto.java
        GraphQLRequestDto.java
      config/
        SecurityConfig.java
      exception/
        GlobalExceptionHandler.java
      BffApplication.java
    resources/
      application.yml
  test/
    java/com/agranelos/bff/
Dockerfile
docker-compose.yml
pom.xml
README.md
Agranelos-BFF.postman_collection.json
ENDPOINTS_MAPPING.md
IMPLEMENTACION_ENDPOINTS.md
```

---

## 📞 Contacto

Para dudas o soporte, contacta al equipo de desarrollo.