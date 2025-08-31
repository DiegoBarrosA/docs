# BFF (Backend For Frontend) - Agranelos

Este proyecto implementa un BFF (Backend For Frontend) en Java con Spring Boot, encargado de exponer APIs RESTful para la gestión de productos y bodegas, orquestando llamadas a funciones serverless (Azure Functions) y devolviendo respuestas en formato JSON.

---

## 🚀 Endpoints REST

- `GET /api/productos` — Lista todos los productos.
- `GET /api/productos/{id}` — Obtiene un producto por ID.
- `POST /api/productos` — Crea un nuevo producto.
- `PUT /api/productos/{id}` — Actualiza un producto existente.
- `DELETE /api/productos/{id}` — Elimina un producto.

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

## 🐳 Uso con Docker

```bash
# Construir la imagen
docker build -t agranelos-bff .

# Ejecutar el contenedor
docker run -p 8080:8080 \
  -e AZURE_FUNCTIONS_BASE_URL="https://<tu-app>.azurewebsites.net/api" \
  -e AZURE_FUNCTIONS_API_KEY="<tu-api-key>" \
  agranelos-bff
```

---

## 🧪 Pruebas Locales

- Ejecuta las pruebas con Maven:
  ```bash
  mvn clean test
  ```
- Puedes usar Azure Functions Core Tools para simular funciones localmente.

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
      service/
      dto/
    resources/
      application.yml
  test/
    java/com/agranelos/bff/
Dockerfile
docker-compose.yml
pom.xml
README.md
```

---

## 📞 Contacto

Para dudas o soporte, contacta al equipo de desarrollo.