---
layout: default
title: Postman Collection
parent: Testing
---

<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.css">
<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-footer.css">
<script src="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.js"></script>

# Postman Collection Testing

## Collection Overview

The Postman collection provides comprehensive testing capabilities for all BFF endpoints including the enhanced warehouse management features.

## Files Structure

### Main Collection
- **Agranelos-BFF.postman_collection.json** (in repository root)
  - Complete collection with all endpoints and new functionalities
  - 20 requests organized in 4 folders
  - HTTP Basic Authentication configured
  - **New functionalities included**:
    - Warehouse product consultation
    - Safe deletion with automatic validation
    - Forced deletion with details
    - Complete workflow examples

### Environment Files
Located in `postman/` directory:

1. **Local.postman_environment.json**
   - For local development (Spring Boot running directly)
   - URL: `http://localhost:8080`

2. **Docker.postman_environment.json**
   - For local Docker/Podman containers
   - URL: `http://localhost:8080`

3. **AWS.postman_environment.json**
   - For AWS deployment (ECS, Elastic Beanstalk, etc.)
   - URL: `https://your-bff-domain.amazonaws.com` (customize)

4. **Azure.postman_environment.json**
   - For Azure App Service deployment
   - URL: `https://your-bff-app.azurewebsites.net` (customize)

## Import Instructions

### 1. Import Collection
1. Open Postman
2. Click **Import**
3. Select `Agranelos-BFF.postman_collection.json`
4. Click **Import**

### 2. Import Environments
1. Click **Import**
2. Select all `.postman_environment.json` files from `postman/` folder
3. Click **Import**

### 3. Select Environment
1. In the top-right dropdown (shows "No Environment")
2. Select desired environment:
   - **Local** → For local development
   - **Docker/Podman** → For local containers
   - **AWS** → For AWS production
   - **Azure** → For Azure production

### 4. Configure Variables (if necessary)

#### For cloud environments (AWS/Azure):
1. Click the eye icon next to environment selector
2. Click **Edit** next to selected environment
3. Update `base_url` with your real URL
4. Save changes

## Collection Structure

```
├── Products
│   ├── GET    List all products
│   ├── GET    Get product by ID
│   ├── POST   Create new product
│   ├── PUT    Update existing product
│   └── DELETE Delete product
│
├── Warehouses
│   ├── GET    List all warehouses
│   ├── GET    Get warehouse by ID
│   ├── GET    [NEW] Query products in warehouse
│   ├── POST   Create new warehouse
│   ├── PUT    Update existing warehouse
│   ├── DELETE [ENHANCED] Delete warehouse (automatic validation)
│   └── DELETE [NEW] Delete warehouse (forced with details)
│
├── GraphQL
│   ├── GET  GraphQL endpoint info
│   ├── POST GraphQL Query - List products
│   ├── POST GraphQL Query - List warehouses
│   ├── POST GraphQL Query - Product by ID
│   └── POST GraphQL Query - Warehouse by ID
│
└── [NEW] Workflow Examples - Warehouse Management
    ├── Flow A: Prior Consultation and Safe Deletion
    │   ├── 1. Query products in warehouse
    │   ├── 2. Attempt safe deletion
    │   └── 3. Forced deletion (if necessary)
    ├── Flow B: Direct Deletion with Details
    │   └── Direct forced deletion
    └── Flow C: Warehouse Audit
        ├── List all warehouses
        ├── Verify products in each warehouse
        └── Simulate deletion (without force)
```

## Authentication

All endpoints require **HTTP Basic Authentication**.

### Default Credentials:
- **Username:** `user`
- **Password:** `myStrongPassword123`

Authentication is configured at collection level and applies automatically to all requests.

### Change Credentials:
1. Right-click on collection in Postman
2. Select **Edit**
3. Go to **Authorization** tab
4. Update username and password
5. Save

## New Functionalities (October 2025)

### Enhanced Warehouse Deletion Management

#### Product Prior Consultation
Before deleting a warehouse, you can query which products it contains:
```http
GET {{base_url}}/api/bodegas/5/productos
```

#### Safe Deletion (Automatic Validation)
Normal deletion now automatically validates if warehouse has products:
```http
DELETE {{base_url}}/api/bodegas/5
```
- **If has products**: Returns `409 Conflict` with details
- **If empty**: Deletes normally

#### Forced Deletion with Details
To force deletion and get information about affected products:
```http
DELETE {{base_url}}/api/bodegas/5?force=true
```

### Included Workflow Examples

The collection now includes **3 complete flows**:

1. **Flow A**: Prior Consultation → Safe Deletion → Conflict Management
2. **Flow B**: Direct Deletion with Detailed Information
3. **Flow C**: Multiple Warehouse Audit

### Enhanced Responses

All deletion responses now include:
- Number and details of affected products
- Clear warnings about orphaned products
- Suggestions for next steps

## Testing Workflows

### Basic Testing Flow
1. **Setup**: Select appropriate environment
2. **Authentication**: Verify credentials are correct
3. **Basic Operations**: Test CRUD operations for products and warehouses
4. **Enhanced Features**: Test new warehouse management features
5. **Workflows**: Execute complete workflow examples

### Warehouse Management Testing
1. **Create test warehouse** with products
2. **Query products** using new endpoint
3. **Attempt safe deletion** (should get 409 Conflict)
4. **Review conflict response** with product details
5. **Execute forced deletion** if appropriate
6. **Verify enhanced response** with affected products

### GraphQL Testing
1. **Test simple queries** (products, warehouses)
2. **Test parameterized queries** (by ID)
3. **Test mutations** (create, update, delete)
4. **Verify response structure** matches GraphQL schema

## Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `base_url` | BFF base URL | `http://localhost:8080` |
| `producto_id` | Product ID for testing | `1` |
| `bodega_id` | Warehouse ID for testing | `1` |
| `bodega_test_id` | Warehouse ID for deletion testing | `5` |
| `username` | HTTP Basic Auth username | `user` |
| `password` | HTTP Basic Auth password | `myStrongPassword123` |

## Troubleshooting

### Common Issues

**Authentication errors:**
- Verify username/password in collection settings
- Check if credentials match server configuration
- Ensure HTTP Basic Auth is enabled

**Connection errors:**
- Verify base_url is correct
- Check if BFF service is running
- Test network connectivity

**Unexpected responses:**
- Check Azure Functions backend is available
- Verify environment variables in BFF
- Review server logs for errors

### Debugging Tips

**Use Postman Console:**
1. View → Show Postman Console
2. Execute requests and review logs
3. Check request/response details

**Test Environment Variables:**
1. Add `console.log(pm.environment.get("base_url"))` in Pre-request Script
2. Execute request and check console output

**Validate Responses:**
1. Use Tests tab to add assertions
2. Verify status codes and response structure
3. Chain requests using environment variables