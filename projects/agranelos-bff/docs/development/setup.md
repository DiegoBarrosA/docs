---
layout: default
title: Setup and Configuration
parent: Development
---

<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.css">
<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-footer.css">
<script src="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.js"></script>

# Setup and Configuration

## Prerequisites

- Java 17+
- Maven 3.6+
- Podman or Docker
- Access to Azure Functions backend

## Environment Configuration

### Required Environment Variables

```bash
export AZURE_FUNCTIONS_BASE_URL="http://localhost:7071/api"
export SPRING_SECURITY_USER_NAME="user"
export SPRING_SECURITY_USER_PASSWORD="myStrongPassword123"
```

### Application Configuration

The application uses `src/main/resources/application.yml` for configuration:

```yaml
server:
  port: 8080

spring:
  application:
    name: agranelos-bff

azure:
  functions:
    base-url: ${AZURE_FUNCTIONS_BASE_URL:http://localhost:7071/api}

logging:
  level:
    root: INFO
    org.springframework.web: INFO

management:
  endpoints:
    web:
      exposure:
        include: health,info
```

## Local Development

### Method 1: Direct Maven Execution
```bash
# Clone repository
git clone https://github.com/DiegoBarrosA/agranelos-bff.git
cd agranelos-bff

# Set environment variables
export AZURE_FUNCTIONS_BASE_URL="https://your-functions.azurewebsites.net/api"

# Run application
mvn spring-boot:run
```

### Method 2: Container Development (Recommended)

Create a `compose.yml` file for local development:

```yaml
version: '3.8'
services:
  agranelos-bff:
    build: .
    ports:
      - "8080:8080"
    environment:
      - AZURE_FUNCTIONS_BASE_URL=https://your-functions.azurewebsites.net/api
      - SPRING_SECURITY_USER_NAME=user
      - SPRING_SECURITY_USER_PASSWORD=myStrongPassword123
    networks:
      - agranelos-network

networks:
  agranelos-network:
    driver: bridge
```

Run with Podman:
```bash
podman compose up --build
```

## Project Structure

```
agranelos-bff/
├── src/
│   ├── main/
│   │   ├── java/com/agranelos/bff/
│   │   │   ├── controller/          # REST Controllers
│   │   │   ├── dto/                 # Data Transfer Objects  
│   │   │   ├── config/              # Configuration classes
│   │   │   └── exception/           # Exception handlers
│   │   └── resources/
│   │       └── application.yml      # Application configuration
│   └── test/                        # Test classes
├── docs/                            # Documentation (Jekyll)
├── postman/                         # Postman environments
├── Dockerfile                       # Container definition
├── compose.yml                      # Podman/Docker compose
└── pom.xml                         # Maven configuration
```

## Development Guidelines

### Code Style
- Follow Spring Boot conventions
- Use meaningful variable and method names
- Add appropriate JavaDoc comments
- Implement proper error handling

### Testing
- Write unit tests for controllers
- Integration tests for complete workflows
- Use Postman collection for API testing

### Configuration Management
- Use environment variables for sensitive data
- Keep default values in `application.yml`
- Document all configuration options

## IDE Setup

### IntelliJ IDEA
1. Import as Maven project
2. Set JDK to Java 17+
3. Enable Spring Boot support
4. Configure code style to follow project conventions

### VS Code
1. Install Java Extension Pack
2. Install Spring Boot Extension Pack
3. Configure workspace settings for Maven
4. Set up debugging configuration

## Health Checks

The application exposes health endpoints:

- **Health**: `GET /actuator/health`
- **Info**: `GET /actuator/info`

Use these endpoints to verify the application is running correctly.

## Troubleshooting

### Common Issues

**Connection to Azure Functions fails:**
- Verify `AZURE_FUNCTIONS_BASE_URL` is correct
- Check network connectivity
- Ensure Azure Functions are running

**Authentication errors:**
- Verify username and password configuration
- Check HTTP Basic Auth headers
- Ensure security configuration is correct

**Port conflicts:**
- Change port in `application.yml`
- Kill processes using port 8080
- Use different port mapping in containers

### Debug Mode

Run with debug logging:
```bash
mvn spring-boot:run -Dspring.profiles.active=debug
```

Or set environment variable:
```bash
export LOGGING_LEVEL_ROOT=DEBUG
```