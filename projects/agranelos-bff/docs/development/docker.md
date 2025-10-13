---
layout: default
title: Docker Deployment
parent: Development
---

<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.css">
<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-footer.css">
<script src="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.js"></script>

# Container-based Deployment

## Container Files

### Dockerfile
```dockerfile
FROM maven:3.9.4-openjdk-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

FROM openjdk:17-jre-slim
WORKDIR /app
COPY --from=build /app/target/agranelos-bff-*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Compose Configuration
```yaml
version: '3.8'
services:
  agranelos-bff:
    build: .
    container_name: agranelos-bff
    ports:
      - "8080:8080"
    environment:
      - AZURE_FUNCTIONS_BASE_URL=${AZURE_FUNCTIONS_BASE_URL:-http://localhost:7071/api}
      - SPRING_SECURITY_USER_NAME=${SPRING_SECURITY_USER_NAME:-user}
      - SPRING_SECURITY_USER_PASSWORD=${SPRING_SECURITY_USER_PASSWORD:-myStrongPassword123}
      - SPRING_PROFILES_ACTIVE=${SPRING_PROFILES_ACTIVE:-prod}
    networks:
      - agranelos-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  agranelos-network:
    driver: bridge
```

## Podman Deployment (Recommended)

### Build and Run with Podman Compose
```bash
# Set environment variables
export AZURE_FUNCTIONS_BASE_URL="https://your-functions.azurewebsites.net/api"
export SPRING_SECURITY_USER_PASSWORD="your-secure-password"

# Build and run
podman compose up --build -d

# Check logs
podman compose logs -f agranelos-bff

# Stop services
podman compose down
```

### Using Podman Play Kube

Create a Kubernetes manifest `k8s-deployment.yml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agranelos-bff-config
data:
  AZURE_FUNCTIONS_BASE_URL: "https://your-functions.azurewebsites.net/api"
  SPRING_SECURITY_USER_NAME: "user"
  SPRING_PROFILES_ACTIVE: "prod"

---
apiVersion: v1
kind: Secret
metadata:
  name: agranelos-bff-secret
type: Opaque
stringData:
  SPRING_SECURITY_USER_PASSWORD: "myStrongPassword123"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agranelos-bff-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: agranelos-bff
  template:
    metadata:
      labels:
        app: agranelos-bff
    spec:
      containers:
      - name: agranelos-bff
        image: localhost/agranelos-bff:latest
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: agranelos-bff-config
        - secretRef:
            name: agranelos-bff-secret
        livenessProbe:
          httpGet:
            path: /actuator/health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /actuator/health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: agranelos-bff-service
spec:
  selector:
    app: agranelos-bff
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP
```

Deploy with Podman:
```bash
# Build image first
podman build -t localhost/agranelos-bff:latest .

# Deploy with play kube
podman play kube k8s-deployment.yml

# Check status
podman pod ls
podman logs agranelos-bff-deployment-pod-*

# Clean up
podman play kube --down k8s-deployment.yml
```

## Docker Deployment

### Build and Run with Docker
```bash
# Build image
docker build -t agranelos-bff .

# Run container
docker run -d \
  --name agranelos-bff \
  -p 8080:8080 \
  -e AZURE_FUNCTIONS_BASE_URL="https://your-functions.azurewebsites.net/api" \
  -e SPRING_SECURITY_USER_PASSWORD="your-secure-password" \
  agranelos-bff

# Check logs
docker logs -f agranelos-bff

# Stop container
docker stop agranelos-bff
docker rm agranelos-bff
```

### Docker Compose
```bash
# Using existing compose.yml
docker compose up --build -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## Production Considerations

### Environment Variables
Set appropriate values for production:

```bash
export AZURE_FUNCTIONS_BASE_URL="https://prod-functions.azurewebsites.net/api"
export SPRING_SECURITY_USER_PASSWORD="$(openssl rand -base64 32)"
export SPRING_PROFILES_ACTIVE="prod"
```

### Resource Limits
Add resource limits to your compose file:

```yaml
services:
  agranelos-bff:
    # ... other configuration
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

### Security Considerations
- Use secrets management for sensitive data
- Run containers as non-root user
- Enable security scanning for images
- Use specific image tags, not 'latest'
- Regularly update base images

### Monitoring
- Configure proper logging levels
- Use health checks for container orchestration
- Monitor memory and CPU usage
- Set up alerts for application failures

### Backup and Recovery
- Document configuration requirements
- Maintain infrastructure as code
- Test disaster recovery procedures
- Keep deployment scripts version controlled

## Troubleshooting Containers

### Common Issues

**Container fails to start:**
```bash
# Check logs
podman logs container-name

# Inspect container
podman inspect container-name

# Check resource usage
podman stats container-name
```

**Network connectivity issues:**
```bash
# Test from inside container
podman exec -it container-name /bin/bash
curl -I http://localhost:8080/actuator/health

# Check network configuration
podman network ls
podman network inspect network-name
```

**Performance issues:**
```bash
# Monitor resource usage
podman stats --all

# Check system resources
free -h
df -h
```