# Data Investigation Platform - Project Overview

## Introduction

This is a **Palantir-inspired data investigation and ontology platform** built from scratch using modern web technologies. The platform enables users to explore complex datasets through graph visualizations, create custom data models, and build interactive dashboards for collaborative analysis.

## Key Features

### 1. Ontology Engine
- **Flexible Schema Definition**: Define custom entity types (Person, Company, Event, etc.) with properties
- **Relationship Modeling**: Create typed relationships between entities with custom properties
- **Schema Evolution**: Modify schemas as your data model evolves
- **JSONB Storage**: Store flexible, semi-structured data without rigid schema constraints

### 2. Graph Visualization
- **Interactive Graph Explorer**: Navigate entity relationships visually using ReactFlow
- **Multi-level Traversal**: Explore connections up to 3 levels deep
- **Custom Styling**: Color-code entity types and relationships
- **Real-time Updates**: See changes reflected immediately in the graph

### 3. Data Analysis
- **Statistics Dashboard**: View aggregate metrics and entity distributions
- **Interactive Charts**: Bar charts, line charts, and custom visualizations
- **Search & Filter**: Find entities quickly with full-text search
- **Property Explorer**: Inspect entity properties and metadata

### 4. Investigation Workflows
- **Starting Point Selection**: Pick any entity to begin exploration
- **Relationship Discovery**: Uncover hidden connections
- **Path Finding**: Discover how entities are connected
- **Export Capabilities**: Share findings and visualizations

## Architecture

### Technology Stack

#### Backend (Python)
```
FastAPI          - Modern async web framework
PostgreSQL       - Relational database with JSONB support
SQLAlchemy       - ORM for database operations
Pydantic         - Data validation and serialization
Uvicorn          - ASGI server
```

#### Frontend (TypeScript/React)
```
React 18         - UI framework
TypeScript       - Type-safe JavaScript
Vite             - Build tool and dev server
TailwindCSS      - Utility-first CSS framework
ReactFlow        - Graph visualization
Recharts         - Chart library
TanStack Query   - Data fetching and caching
Zustand          - State management
```

### Database Schema

The platform uses a flexible ontology model:

```
┌─────────────────┐         ┌──────────────┐
│  EntityType     │         │   Entity     │
├─────────────────┤         ├──────────────┤
│ id              │◄────────│ id           │
│ name            │         │ entity_type_id
│ display_name    │         │ title        │
│ description     │         │ description  │
│ icon            │         │ properties   │ (JSONB)
│ color           │         │ created_at   │
│ property_schema │ (JSONB) │ updated_at   │
└─────────────────┘         └──────────────┘
                                    │
                                    │
                            ┌───────▼────────┐
                            │ Relationship   │
                            ├────────────────┤
                            │ id             │
                            │ from_entity_id │
                            │ to_entity_id   │
                            │ relationship_  │
                            │   type_id      │
                            │ properties     │ (JSONB)
                            │ created_at     │
                            └────────────────┘
                                    │
                                    │
┌─────────────────────┐             │
│ RelationshipType    │◄────────────┘
├─────────────────────┤
│ id                  │
│ name                │
│ display_name        │
│ forward_label       │
│ reverse_label       │
│ color               │
│ property_schema     │ (JSONB)
└─────────────────────┘
```

### API Design

RESTful API with the following endpoint groups:

**Entity Management**
- `GET /api/v1/entities/` - List entities with filtering
- `POST /api/v1/entities/` - Create new entity
- `GET /api/v1/entities/{id}` - Get entity details
- `PUT /api/v1/entities/{id}` - Update entity
- `DELETE /api/v1/entities/{id}` - Delete entity

**Entity Types**
- `GET /api/v1/entities/types` - List entity types
- `POST /api/v1/entities/types` - Create entity type
- `GET /api/v1/entities/types/{id}` - Get type details
- `PUT /api/v1/entities/types/{id}` - Update type
- `DELETE /api/v1/entities/types/{id}` - Delete type

**Relationships**
- `GET /api/v1/relationships/` - List relationships
- `POST /api/v1/relationships/` - Create relationship
- `GET /api/v1/relationships/{id}` - Get relationship
- `PUT /api/v1/relationships/{id}` - Update relationship
- `DELETE /api/v1/relationships/{id}` - Delete relationship

**Graph Operations**
- `GET /api/v1/graph/explore/{entity_id}?depth={n}` - Explore from entity
- `GET /api/v1/graph/subgraph?entity_ids={ids}` - Get subgraph
- `GET /api/v1/graph/stats` - Get graph statistics

## File Structure

```
untitled_world/
├── backend/                    # Python backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   └── v1/
│   │   │       ├── entities.py
│   │   │       ├── relationships.py
│   │   │       └── graph.py
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/            # SQLAlchemy models
│   │   │   └── ontology.py
│   │   ├── schemas/           # Pydantic schemas
│   │   │   └── ontology.py
│   │   └── main.py            # FastAPI application
│   ├── tests/                 # Backend tests
│   ├── seed_data.py           # Sample data script
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   └── graph/
│   │   │       ├── GraphViewer.tsx
│   │   │       └── EntityNode.tsx
│   │   ├── pages/             # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   └── GraphExplorer.tsx
│   │   ├── services/          # API clients
│   │   │   └── api.ts
│   │   ├── types/             # TypeScript types
│   │   │   └── ontology.ts
│   │   ├── App.tsx            # Main app component
│   │   ├── main.tsx           # Entry point
│   │   └── index.css          # Global styles
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── Dockerfile
│
├── docker-compose.yml          # Docker orchestration
├── .gitignore
├── SETUP.md                    # Setup instructions
├── README_PLATFORM.md          # Platform README
├── PROJECT_OVERVIEW.md         # This file
└── start.sh                    # Quick start script
```

## Sample Data

The platform includes a comprehensive sample dataset:

**Entity Types:**
- Person (blue) - Individuals
- Company (green) - Organizations
- Location (orange) - Geographic places
- Event (purple) - Occurrences

**Sample Entities:**
- 3 People: Alice, Bob, Carol
- 2 Companies: TechCorp, Data Solutions
- 2 Locations: San Francisco, New York
- 1 Event: Tech Summit 2024

**Relationship Types:**
- Works For - Employment relationships
- Located In - Geographic placement
- Attended - Event participation
- Knows - Personal connections

**Sample Network:**
```
Alice (Person) ──[works for]──> TechCorp (Company) ──[located in]──> San Francisco
    │                                  ▲
    │                                  │
    └──[knows]──> Bob (Person) ────────┘
    │
    └──[knows]──> Carol (Person) ──[works for]──> Data Solutions ──[located in]──> New York
```

## User Interface

### Dashboard
- **Statistics Overview**: Total entities, relationships, types
- **Visual Charts**: Entity distribution by type
- **Quick Actions**: Shortcuts to common tasks

### Graph Explorer
- **Search Panel**: Find entities by name or properties
- **Depth Control**: Adjust exploration depth (1-3 levels)
- **Interactive Graph**: Click nodes to explore further
- **Node Details**: View entity properties on selection

### Features (Coming Soon)
- Entity creation and editing forms
- Schema management interface
- Advanced search and filtering
- Custom dashboard builder
- Workspace management
- User authentication
- Collaboration features

## Extending the Platform

### Adding New Entity Types

```python
# In seed_data.py or via API
product_type = EntityType(
    name="product",
    display_name="Product",
    description="A product or service",
    icon="package",
    color="#ec4899",
    property_schema={
        "price": {"type": "number", "required": True},
        "sku": {"type": "string", "required": True},
        "in_stock": {"type": "boolean", "required": False},
    }
)
```

### Adding Custom Visualizations

```typescript
// Create new chart component
import { LineChart, Line, XAxis, YAxis } from 'recharts';

const CustomChart = ({ data }) => (
  <LineChart data={data}>
    <XAxis dataKey="name" />
    <YAxis />
    <Line type="monotone" dataKey="value" stroke="#3b82f6" />
  </LineChart>
);
```

### Adding New API Endpoints

```python
# In backend/app/api/v1/custom.py
@router.get("/custom-analysis")
def custom_analysis(db: Session = Depends(get_db)):
    # Your custom logic
    return {"result": "data"}
```

## Performance Considerations

1. **Database Indexing**: Key fields are indexed for fast queries
2. **Pagination**: All list endpoints support pagination
3. **Query Optimization**: Eager loading to prevent N+1 queries
4. **Caching**: TanStack Query caches API responses
5. **Graph Depth Limits**: Prevent expensive deep traversals

## Security Features (To Be Implemented)

- JWT-based authentication
- Role-based access control (RBAC)
- Row-level security for multi-tenancy
- API rate limiting
- Input validation and sanitization
- SQL injection prevention (via ORM)
- XSS protection

## Deployment

### Development
```bash
./start.sh
```

### Production
1. Build frontend: `npm run build`
2. Use production database
3. Set secure environment variables
4. Enable HTTPS
5. Use production ASGI server (gunicorn)
6. Set up monitoring and logging

## Comparison with Similar Platforms

| Feature | This Platform | Palantir | Databricks |
|---------|--------------|----------|------------|
| Open Source | ✓ | ✗ | ✗ |
| Graph Visualization | ✓ | ✓ | Limited |
| Custom Ontology | ✓ | ✓ | ✗ |
| Data Processing | Basic | Advanced | Advanced |
| ML Integration | Planned | ✓ | ✓ |
| Self-Hosted | ✓ | ✗ | Cloud |
| Cost | Free | $$$$$ | $$$$ |

## Future Enhancements

### Short Term
- [ ] Entity creation UI
- [ ] Relationship creation UI
- [ ] Schema management interface
- [ ] Advanced search
- [ ] Export functionality

### Medium Term
- [ ] User authentication
- [ ] Multi-workspace support
- [ ] Real-time collaboration
- [ ] Data import from CSV/JSON
- [ ] Advanced graph algorithms (shortest path, centrality)
- [ ] Timeline visualization

### Long Term
- [ ] Machine learning integration
- [ ] Natural language queries
- [ ] Automated relationship discovery
- [ ] Integration with external data sources
- [ ] Mobile application
- [ ] Plugin architecture

## Contributing

Areas where contributions are welcome:
1. Additional visualization types
2. Data connectors (CSV, JSON, APIs)
3. Graph algorithms implementation
4. UI/UX improvements
5. Performance optimizations
6. Documentation
7. Test coverage

## License

MIT License - Free to use, modify, and distribute

## Resources

- FastAPI Documentation: https://fastapi.tiangolo.com
- React Documentation: https://react.dev
- ReactFlow Documentation: https://reactflow.dev
- SQLAlchemy Documentation: https://www.sqlalchemy.org
- PostgreSQL Documentation: https://www.postgresql.org/docs
