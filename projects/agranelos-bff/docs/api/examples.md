---
layout: default
title: Examples and Usage
parent: API Documentation
---

<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.css">
<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-footer.css">
<script src="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.js"></script>

# Practical Examples and Usage

## cURL Examples

### 1. Query Products in Warehouse
```bash
# Verify which products are in warehouse ID 5
curl -X GET "http://localhost:8080/api/bodegas/5/productos" \
     -H "Content-Type: application/json"
```

**Expected response:**
```json
[
  {
    "id": 1,
    "nombre": "Premium Rice",
    "cantidad": 150,
    "precio": 25.50
  },
  {
    "id": 3,
    "nombre": "Refined Sugar",
    "cantidad": 200,
    "precio": 20.00
  }
]
```

### 2. Safe Deletion (Automatic Validation)
```bash
# Attempt to delete warehouse with products
curl -X DELETE "http://localhost:8080/api/bodegas/5" \
     -H "Content-Type: application/json"
```

**Expected response (409 Conflict):**
```json
{
  "error": "Warehouse contains products",
  "mensaje": "Use parameter 'force=true' to delete warehouse and products, or reassign products first",
  "productos": [...],
  "bodegaId": "5"
}
```

### 3. Forced Deletion with Details
```bash
# Force deletion and get details of affected products
curl -X DELETE "http://localhost:8080/api/bodegas/5?force=true" \
     -H "Content-Type: application/json"
```

**Expected response (200 OK):**
```json
{
  "mensaje": "Warehouse deleted successfully",
  "bodegaId": "5",
  "productosAfectados": 2,
  "detalleProductos": [...],
  "advertencia": "Products have lost their assignment to this warehouse"
}
```

### 4. Empty Warehouse Deletion
```bash
# Delete warehouse without products
curl -X DELETE "http://localhost:8080/api/bodegas/10" \
     -H "Content-Type: application/json"
```

**Expected response (200 OK):**
```json
{
  "mensaje": "Warehouse deleted successfully",
  "bodegaId": "10",
  "productosAfectados": 0
}
```

## Complete Workflows

### Workflow A: Warehouse Closure Planning
```bash
# Step 1: Get general warehouse information
curl -X GET "http://localhost:8080/api/bodegas/5"

# Step 2: Verify assigned products
curl -X GET "http://localhost:8080/api/bodegas/5/productos"

# Step 3: Attempt safe deletion (will validate automatically)
curl -X DELETE "http://localhost:8080/api/bodegas/5"

# Step 4a: If products exist, reassign manually
curl -X PUT "http://localhost:8080/api/productos/1" \
     -H "Content-Type: application/json" \
     -d '{"nombre":"Premium Rice","bodegaId":3,"cantidad":150}'

# Step 4b: Or force deletion if necessary
curl -X DELETE "http://localhost:8080/api/bodegas/5?force=true"
```

### Workflow B: Impact Audit
```bash
# Step 1: List all warehouses
curl -X GET "http://localhost:8080/api/bodegas"

# Step 2: For each warehouse, verify products
for bodega_id in 1 2 3 4 5; do
  echo "=== Warehouse $bodega_id ==="
  curl -X GET "http://localhost:8080/api/bodegas/$bodega_id/productos"
  echo ""
done

# Step 3: Simulate deletion (without force) to see impact
curl -X DELETE "http://localhost:8080/api/bodegas/5"
```

## Automated Testing

### Complete Test Script
```bash
#!/bin/bash

BASE_URL="http://localhost:8080"
BODEGA_ID="5"

echo "=== Testing Enhanced Warehouse Management ==="

# Test 1: Product query
echo "1. Querying products in warehouse $BODEGA_ID..."
curl -s -X GET "$BASE_URL/api/bodegas/$BODEGA_ID/productos" | jq '.'

# Test 2: Automatic validation
echo "2. Testing automatic validation..."
response=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE_URL/api/bodegas/$BODEGA_ID")
if [ "$response" = "409" ]; then
  echo "✅ Validation works correctly (409 Conflict)"
else
  echo "❌ Validation failed (code: $response)"
fi

# Test 3: Forced deletion
echo "3. Testing forced deletion..."
response=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE_URL/api/bodegas/$BODEGA_ID?force=true")
if [ "$response" = "200" ]; then
  echo "✅ Forced deletion successful (200 OK)"
else
  echo "❌ Forced deletion failed (code: $response)"
fi

echo "=== Testing completed ==="
```

## Frontend Integration

### JavaScript/Fetch API
```javascript
class WarehouseManager {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  // Query products before deletion
  async getProductsInWarehouse(warehouseId) {
    const response = await fetch(`${this.baseUrl}/api/bodegas/${warehouseId}/productos`);
    return response.json();
  }

  // Safe deletion with validation
  async deleteWarehouseSafe(warehouseId) {
    const response = await fetch(`${this.baseUrl}/api/bodegas/${warehouseId}`, {
      method: 'DELETE'
    });
    
    if (response.status === 409) {
      const conflict = await response.json();
      throw new Error(`Warehouse contains ${conflict.productos.length} products`);
    }
    
    return response.json();
  }

  // Forced deletion with details
  async deleteWarehouseForced(warehouseId) {
    const response = await fetch(`${this.baseUrl}/api/bodegas/${warehouseId}?force=true`, {
      method: 'DELETE'
    });
    return response.json();
  }

  // Complete flow with confirmation
  async deleteWithConfirmation(warehouseId) {
    try {
      // Attempt safe deletion
      return await this.deleteWarehouseSafe(warehouseId);
    } catch (error) {
      // If conflict, ask for confirmation
      const confirmation = confirm(`${error.message}. Force deletion?`);
      if (confirmation) {
        return await this.deleteWarehouseForced(warehouseId);
      }
      throw error;
    }
  }
}

// Usage
const manager = new WarehouseManager('http://localhost:8080');
manager.deleteWithConfirmation(5)
  .then(result => console.log('Successful deletion:', result))
  .catch(error => console.error('Error:', error.message));
```