---
layout: default
title: Endpoints Mapping
parent: API Documentation
---

<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.css">
<link rel="stylesheet" href="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-footer.css">
<script src="https://diegobarrosa.github.io/diegobarrosaraya-assets/shared-theme.js"></script>

# Agranelos BFF - Endpoints Mapping

## Azure Functions to BFF Endpoints

### Products (Implemented)
```
Azure Function                    →  BFF Endpoint
─────────────────────────────────────────────────────────
GET  /productos                   →  GET  /api/productos
GET  /productos/{id}              →  GET  /api/productos/{id}
POST /productos                   →  POST /api/productos
PUT  /productos/{id}              →  PUT  /api/productos/{id}
DELETE /productos/{id}            →  DELETE /api/productos/{id}
```

### Warehouses (Implemented + Enhanced)
```
Azure Function                    →  BFF Endpoint
─────────────────────────────────────────────────────────
GET  /bodegas                     →  GET  /api/bodegas
GET  /bodegas/{id}                →  GET  /api/bodegas/{id}
GET  /bodegas/{id}/productos      →  GET  /api/bodegas/{id}/productos    [NEW]
POST /bodegas                     →  POST /api/bodegas
PUT  /bodegas/{id}                →  PUT  /api/bodegas/{id}
DELETE /bodegas/{id}              →  DELETE /api/bodegas/{id}            [ENHANCED]
                                      - Parameter: ?force=true          [NEW]
                                      - Automatic validation           [NEW]
                                      - Product impact response        [NEW]
```

### GraphQL (Implemented)
```
Azure Function                    →  BFF Endpoint
─────────────────────────────────────────────────────────
POST /graphql                     →  GET  /api/graphql (info)
                                  →  POST /api/graphql (query)
```

### Other Azure Functions Endpoints
```
Endpoint                          Status
─────────────────────────────────────────────────────────
POST /init (InitializeDatabase)   Not exposed in BFF (internal operation)
```

## Files Created

```
agranelos-bff/
├── src/main/java/com/agranelos/bff/
│   ├── controller/
│   │   ├── BodegaController.java           [CREATED]
│   │   ├── GraphQLController.java          [CREATED]
│   │   └── ProductoController.java         [EXISTING]
│   └── dto/
│       ├── BodegaDto.java                  [CREATED]
│       ├── BodegaEliminacionResponseDto.java [CREATED]
│       ├── GraphQLRequestDto.java          [CREATED]
│       └── ProductoDto.java                [EXISTING]
├── docs/                                   [CREATED]
└── Agranelos-BFF.postman_collection.json   [UPDATED]
```

## Implementation Statistics

- **Controllers created:** 2
- **DTOs created:** 3 (+ BodegaEliminacionResponseDto)
- **Endpoints new:** 12 (+ GET /api/bodegas/{id}/productos)
- **Endpoints enhanced:** 1 (DELETE /api/bodegas/{id} with validations)
- **Endpoints total in BFF:** 17

## New Functionalities (October 2025)

- Prior product consultation in warehouses
- Automatic validation in warehouse deletion
- Forced deletion with detailed information
- Enhanced responses with affected product information

## Implementation Status: COMPLETE

All Azure Functions endpoints are now available through the BFF with enhanced warehouse management capabilities.