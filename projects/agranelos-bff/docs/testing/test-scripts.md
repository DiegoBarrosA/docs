---
layout: default
title: Test Scripts
parent: Testing
---

<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.css">
<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-footer.css">
<script src="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.js"></script>

# Automated Test Scripts

## Available Test Scripts

### Main Test Script
**File:** `test-nuevas-funcionalidades.sh`

Comprehensive test script that validates all new warehouse management functionalities.

#### Usage
```bash
# Make executable
chmod +x test-nuevas-funcionalidades.sh

# Run tests
./test-nuevas-funcionalidades.sh
```

#### What it tests:
1. **BFF Availability** - Verifies service is running
2. **Warehouse Listing** - Tests basic endpoint functionality
3. **Product Query Endpoint** - Tests new warehouse product consultation
4. **Automatic Validation** - Tests safe deletion with validation
5. **Forced Deletion Structure** - Validates enhanced response format
6. **Existing Endpoint Compatibility** - Ensures no regression

#### Expected Output
```bash
Testing Enhanced Warehouse Management BFF
==========================================

Test 1: Verifying BFF availability...
BFF is available at http://localhost:8080

Test 2: Getting warehouse list...
Warehouse list obtained correctly (200)

Test 3: Testing new endpoint GET /api/bodegas/{id}/productos...
Warehouse products endpoint works (code: 200)

Test 4: Testing automatic validation in deletion...
Automatic validation works (code: 409)
ℹ️  Warehouse contains products (expected behavior)

Test 5: Testing forced deletion (response structure)...
Correct response structure in forced deletion

Test 6: Verifying existing endpoints compatibility...
GET /api/productos still works
POST /api/graphql still works

==========================================
Testing Summary
- New endpoints implemented and working
- Automatic validations active
- Compatibility with existing endpoints maintained
- BFF ready for production

Testing completed successfully!
```

## Custom Test Scripts

### Basic Connectivity Test
```bash
#!/bin/bash
BASE_URL="http://localhost:8080"

echo "Testing BFF connectivity..."

# Test health endpoint
response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/actuator/health")
if [ "$response" = "200" ]; then
    echo "Health endpoint OK"
else
    echo "Health endpoint failed (code: $response)"
    exit 1
fi

# Test main endpoints
endpoints=(
    "api/productos"
    "api/bodegas"
    "api/graphql"
)

for endpoint in "${endpoints[@]}"; do
    response=$(curl -s -o /dev/null -w "%{http_code}" -u user:myStrongPassword123 "$BASE_URL/$endpoint")
    if [ "$response" = "200" ]; then
        echo "$endpoint OK"
    else
        echo "$endpoint failed (code: $response)"
    fi
done
```

### Warehouse Management Flow Test
```bash
#!/bin/bash
BASE_URL="http://localhost:8080"
AUTH="user:myStrongPassword123"

echo "Testing warehouse management flow..."

# Step 1: Create test warehouse
echo "1. Creating test warehouse..."
create_response=$(curl -s -X POST "$BASE_URL/api/bodegas" \
    -H "Content-Type: application/json" \
    -u "$AUTH" \
    -d '{"nombre":"Test Warehouse","ubicacion":"Test Location","capacidad":1000}')

if echo "$create_response" | grep -q "id"; then
    echo "Test warehouse created"
    warehouse_id=$(echo "$create_response" | grep -o '"id":[0-9]*' | cut -d':' -f2)
else
    echo "Failed to create test warehouse"
    exit 1
fi

# Step 2: Query products in warehouse
echo "2. Querying products in warehouse..."
products_response=$(curl -s "$BASE_URL/api/bodegas/$warehouse_id/productos" -u "$AUTH")
echo "Products found: $products_response"

# Step 3: Attempt safe deletion
echo "3. Attempting safe deletion..."
delete_response=$(curl -s -X DELETE "$BASE_URL/api/bodegas/$warehouse_id" -u "$AUTH")
echo "Delete response: $delete_response"

# Step 4: Cleanup - forced deletion if needed
echo "4. Cleanup - forced deletion..."
force_response=$(curl -s -X DELETE "$BASE_URL/api/bodegas/$warehouse_id?force=true" -u "$AUTH")
echo "Force delete response: $force_response"

echo "Warehouse management flow test completed"
```

### Performance Test Script
```bash
#!/bin/bash
BASE_URL="http://localhost:8080"
AUTH="user:myStrongPassword123"

echo "Performance testing BFF endpoints..."

# Function to measure response time
measure_endpoint() {
    local endpoint="$1"
    local method="${2:-GET}"
    local data="$3"
    
    if [ "$method" = "POST" ] && [ -n "$data" ]; then
        time_taken=$(curl -s -w "%{time_total}" -o /dev/null \
            -X "$method" "$BASE_URL/$endpoint" \
            -H "Content-Type: application/json" \
            -u "$AUTH" \
            -d "$data")
    else
        time_taken=$(curl -s -w "%{time_total}" -o /dev/null \
            -X "$method" "$BASE_URL/$endpoint" \
            -u "$AUTH")
    fi
    
    echo "$endpoint ($method): ${time_taken}s"
}

# Test key endpoints
measure_endpoint "api/productos" "GET"
measure_endpoint "api/bodegas" "GET"
measure_endpoint "api/bodegas/1/productos" "GET"
measure_endpoint "api/graphql" "POST" '{"query":"{ productos { id nombre } }"}'

echo "Performance testing completed"
```

## Container-based Testing

### Podman Test Container
Create a test container for isolated testing:

**Dockerfile.test:**
```dockerfile
FROM curlimages/curl:latest
RUN apk add --no-cache bash jq
WORKDIR /tests
COPY test-*.sh ./
RUN chmod +x *.sh
CMD ["./test-nuevas-funcionalidades.sh"]
```

**Run tests in container:**
```bash
# Build test container
podman build -f Dockerfile.test -t agranelos-bff-tests .

# Run tests against local BFF
podman run --rm --network host agranelos-bff-tests

# Run tests against containerized BFF
podman run --rm --network agranelos-network agranelos-bff-tests
```

### Test Compose Configuration
**compose.test.yml:**
```yaml
version: '3.8'
services:
  bff-tests:
    build:
      context: .
      dockerfile: Dockerfile.test
    depends_on:
      - agranelos-bff
    networks:
      - agranelos-network
    environment:
      - BASE_URL=http://agranelos-bff:8080
    command: ["./test-nuevas-funcionalidades.sh"]

  agranelos-bff:
    build: .
    ports:
      - "8080:8080"
    environment:
      - AZURE_FUNCTIONS_BASE_URL=https://mock-functions.example.com/api
    networks:
      - agranelos-network

networks:
  agranelos-network:
    driver: bridge
```

**Run test suite:**
```bash
podman compose -f compose.test.yml up --build --abort-on-container-exit
```

## CI/CD Integration

### GitHub Actions Test Step
```yaml
- name: Run BFF Tests
  run: |
    chmod +x test-nuevas-funcionalidades.sh
    ./test-nuevas-funcionalidades.sh
  env:
    BASE_URL: http://localhost:8080
```

### Test Result Parsing
```bash
#!/bin/bash
# Parse test results for CI/CD

test_output=$(./test-nuevas-funcionalidades.sh)
echo "$test_output"

# Check for failures
if echo "$test_output" | grep -q "FAIL"; then
    echo "Tests failed!"
    exit 1
else
    echo "All tests passed!"
    exit 0
fi
```

## Monitoring and Alerting

### Health Check Script
```bash
#!/bin/bash
# Continuous health monitoring

BASE_URL="http://localhost:8080"
INTERVAL=30  # seconds

while true; do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Check health endpoint
    if curl -sf "$BASE_URL/actuator/health" > /dev/null; then
        echo "[$timestamp] BFF healthy"
    else
        echo "[$timestamp] BFF unhealthy"
        # Add alerting logic here
    fi
    
    sleep $INTERVAL
done
```

### Load Test Script
```bash
#!/bin/bash
# Simple load testing

BASE_URL="http://localhost:8080"
AUTH="user:myStrongPassword123"
CONCURRENT=10
REQUESTS=100

echo "Load testing with $CONCURRENT concurrent users, $REQUESTS requests each..."

for i in $(seq 1 $CONCURRENT); do
    {
        for j in $(seq 1 $REQUESTS); do
            curl -s "$BASE_URL/api/productos" -u "$AUTH" > /dev/null
        done
        echo "Worker $i completed $REQUESTS requests"
    } &
done

wait
echo "Load test completed"
```