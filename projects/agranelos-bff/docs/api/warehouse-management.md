---
layout: default
title: Warehouse Management
parent: API Documentation
---

<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.css">
<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-footer.css">
<script src="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.js"></script>

# Enhanced Warehouse Management

## Overview

Enhanced warehouse deletion functionality provides intelligent handling of products when warehouses are deleted, offering validation, detailed information, and granular control over the deletion process.

## Implemented Functionalities

### 1. Product Query Endpoint 
**Endpoint:** `GET /api/bodegas/{id}/productos`

Allows querying which products are assigned to a specific warehouse before proceeding with deletion.

**Example response:**
```json
[
  {
    "id": 1,
    "nombre": "Premium Rice",
    "cantidad": 150,
    "precio": 25.50
  },
  {
    "id": 2,
    "nombre": "Black Beans",
    "cantidad": 80,
    "precio": 30.00
  }
]
```

### 2. Safe Deletion by Default
**Endpoint:** `DELETE /api/bodegas/{id}`

- **Behavior:** Automatically validates if warehouse contains products
- **If contains products:** Returns `409 Conflict` error with details
- **If empty:** Proceeds with normal deletion

**Example conflict response:**
```json
{
  "error": "Warehouse contains products",
  "mensaje": "Use parameter 'force=true' to delete warehouse and products, or reassign products first",
  "productos": [...],
  "bodegaId": "5"
}
```

### 3. Forced Deletion with Details
**Endpoint:** `DELETE /api/bodegas/{id}?force=true`

- **Behavior:** Deletes warehouse without prior validations
- **Detailed information:** Includes affected products in response
- **Transparency:** Client knows exactly which products lost their assignment

**Example successful response:**
```json
{
  "mensaje": "Warehouse deleted successfully",
  "bodegaId": "5",
  "productosAfectados": 12,
  "detalleProductos": [...],
  "advertencia": "Products have lost their assignment to this warehouse"
}
```

## Recommended Workflows

### Workflow 1: Careful Deletion
```bash
# 1. Query warehouse products
GET /api/bodegas/5/productos

# 2. If products exist, reassign or manage manually
PUT /api/productos/{id}  # Update products individually

# 3. Delete empty warehouse
DELETE /api/bodegas/5
```

### Workflow 2: Emergency Deletion
```bash
# 1. Force direct deletion (exceptional situations)
DELETE /api/bodegas/5?force=true

# 2. Process orphaned products according to response
# Products still exist but without warehouse assignment
```

### Workflow 3: Validation and Decision
```bash
# 1. Attempt normal deletion
DELETE /api/bodegas/5

# 2. If conflict (409), review returned products
# 3. Decide between reassignment or forced deletion
DELETE /api/bodegas/5?force=true  # If necessary
```

## HTTP Response States

| Code | Scenario | Description |
|------|----------|-------------|
| `200 OK` | Successful deletion | Warehouse deleted (empty or forced) |
| `404 Not Found` | Non-existent warehouse | Warehouse ID not found |
| `409 Conflict` | Warehouse with products | Preventive validation activated |
| `500 Internal Server Error` | Backend error | Problem in Azure Functions |

## Use Cases

### Case 1: Branch Closure
```
Scenario: Planned closure of a branch
Flow: 
1. GET /api/bodegas/10/productos (review inventory)
2. Reassign products to other warehouses
3. DELETE /api/bodegas/10 (safe deletion)
```

### Case 2: Operational Emergency
```
Scenario: Fire in warehouse, urgent deletion
Flow: 
1. DELETE /api/bodegas/15?force=true
2. Process orphaned products according to response
3. Adjust inventory in system
```

### Case 3: Data Cleanup
```
Scenario: Deletion of test/obsolete warehouses
Flow: 
1. GET /api/bodegas/test/productos (verify empty)
2. DELETE /api/bodegas/test (automatic deletion)
```

## Implementation Benefits

- **Error prevention**: Avoids accidental deletions
- **Total transparency**: Client knows exact impact
- **Operational flexibility**: Allows both validation and force
- **Complete traceability**: Detailed logs of affected products
- **Improved user experience**: Clear and useful messages

## Compatibility

- **Previous version**: Existing clients continue to work
- **New parameters**: `force=true` is optional
- **New endpoints**: `/productos` is completely new
- **Enhanced responses**: More information without breaking changes