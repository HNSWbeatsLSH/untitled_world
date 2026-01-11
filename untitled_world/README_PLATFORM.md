# Data Investigation Platform

A Palantir-inspired data investigation and ontology platform for exploring complex datasets, visualizing relationships, and conducting collaborative analysis.

## Architecture

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Relational database with JSONB support
- **SQLAlchemy** - ORM for data modeling
- **Pydantic** - Data validation and settings management

### Frontend
- **React + TypeScript** - Modern UI framework
- **D3.js** - Graph and network visualizations
- **Recharts/Plotly** - Statistical charts and dashboards
- **React Flow** - Interactive node-based visualizations
- **TailwindCSS** - Utility-first styling

### Key Features (MVP)

1. **Ontology Engine**
   - Define custom entity types and properties
   - Model relationships between entities
   - Schema evolution and versioning

2. **Data Investigation**
   - Graph-based entity exploration
   - Relationship traversal and discovery
   - Search and filtering across entities

3. **Visualization & Dashboards**
   - Interactive network graphs
   - Statistical charts and metrics
   - Customizable dashboard layouts
   - Export and sharing capabilities

4. **Workspace Management**
   - Multiple investigation workspaces
   - Collaborative features
   - Query history and bookmarking

## Project Structure

```
untitled_world/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core configuration
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── ontology/         # Ontology engine
│   ├── tests/
│   ├── alembic/              # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API clients
│   │   ├── hooks/            # Custom hooks
│   │   ├── store/            # State management
│   │   └── types/            # TypeScript types
│   ├── public/
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker (optional)

### Quick Start

1. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

3. **Database Setup**
```bash
# Create database
createdb investigation_platform

# Run migrations
cd backend
alembic upgrade head
```

## Core Concepts

### Ontology Model
The platform uses a flexible ontology model where:
- **Entity Types**: Define categories (Person, Company, Event, etc.)
- **Properties**: Attributes with types and constraints
- **Relationships**: Typed connections between entities
- **Schemas**: Versioned definitions of your data model

### Investigation Workflow
1. Import or create entities
2. Define relationships and properties
3. Explore data through graph visualization
4. Create custom views and dashboards
5. Share insights and collaborate

## Development Roadmap

- [x] Project initialization
- [ ] Core ontology engine
- [ ] REST API implementation
- [ ] Graph visualization
- [ ] Dashboard builder
- [ ] Authentication system
- [ ] Data import/export
- [ ] Search and filtering
- [ ] Workspace management
- [ ] Collaboration features

## License

MIT
