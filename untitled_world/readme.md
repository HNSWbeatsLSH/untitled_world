# Data Investigation Platform

> A Palantir-inspired data investigation and ontology platform for exploring complex datasets, visualizing relationships, and conducting collaborative analysis.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This platform enables you to:
- 🔍 **Investigate** complex datasets through interactive graph visualizations
- 🎨 **Model** custom data with flexible ontology definitions
- 📊 **Visualize** entity relationships and patterns
- 📈 **Analyze** data with customizable dashboards
- 🔗 **Connect** disparate data sources into a unified graph

Perfect for: fraud detection, intelligence analysis, knowledge graphs, network analysis, research, and any scenario requiring exploration of connected data.

## Quick Start

```bash
# Clone or navigate to the project
cd untitled_world

# Start the entire platform with one command
./start.sh

# Access the platform
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it! The platform will start with sample data ready to explore.

## Features

### 🎯 Core Capabilities

- **Flexible Ontology Engine**: Define custom entity and relationship types
- **Graph Exploration**: Interactive visualization with depth-based traversal
- **Search & Discovery**: Find entities and explore their connections
- **Analytics Dashboard**: Statistics, charts, and metrics
- **RESTful API**: Complete CRUD operations with automatic documentation
- **Type Safety**: TypeScript frontend + Pydantic backend validation

### 📦 What's Included

- ✅ Complete backend API (FastAPI + PostgreSQL)
- ✅ Modern frontend (React + TypeScript)
- ✅ Interactive graph visualization (ReactFlow)
- ✅ Sample dataset with 8 entities and 10 relationships
- ✅ Docker Compose setup for easy deployment
- ✅ Comprehensive documentation

## Screenshots

**Dashboard:**
```
┌─────────────────────────────────────────────────┐
│  📊 Dashboard                                   │
├─────────────────────────────────────────────────┤
│  Total Entities: 8    Relationships: 10         │
│  [Bar Chart showing entity distribution]        │
└─────────────────────────────────────────────────┘
```

**Graph Explorer:**
```
┌──────────────┬──────────────────────────────────┐
│  Search      │                                  │
│  [Alice]     │     Alice ──works for──> TechCorp│
│              │       │                     │     │
│  Depth: 2    │       │                     │     │
│  [━━━━━━━]   │       └──knows──> Bob ──────┘     │
│              │                                  │
│  Entities    │     [Interactive Graph View]     │
│  • Alice     │                                  │
│  • Bob       │                                  │
│  • TechCorp  │                                  │
└──────────────┴──────────────────────────────────┘
```

## Architecture

```
┌─────────────────┐
│   React UI      │  ← Interactive dashboards and graph visualization
│  (TypeScript)   │
└────────┬────────┘
         │ HTTP/REST
┌────────▼────────┐
│  FastAPI Server │  ← RESTful API with automatic documentation
│    (Python)     │
└────────┬────────┘
         │ SQLAlchemy ORM
┌────────▼────────┐
│   PostgreSQL    │  ← Relational DB with JSONB for flexible schemas
│   Database      │
└─────────────────┘
```

### Tech Stack

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL 15
- SQLAlchemy ORM
- Pydantic validation

**Frontend:**
- React 18
- TypeScript
- Vite
- TailwindCSS
- ReactFlow (graphs)
- Recharts (analytics)

## Documentation

- **[Getting Started](GETTING_STARTED.md)** - Your first steps with the platform
- **[Setup Guide](SETUP.md)** - Detailed installation instructions
- **[Project Overview](PROJECT_OVERVIEW.md)** - Architecture and design
- **[Build Summary](BUILD_SUMMARY.md)** - What was built and how it works

## Usage Examples

### Create a New Entity Type

```bash
curl -X POST http://localhost:8000/api/v1/entities/types \
  -H "Content-Type: application/json" \
  -d '{
    "name": "customer",
    "display_name": "Customer",
    "description": "A customer entity",
    "color": "#3b82f6",
    "property_schema": {
      "email": {"type": "string", "required": true},
      "tier": {"type": "string", "required": false}
    }
  }'
```

### Create an Entity

```bash
curl -X POST http://localhost:8000/api/v1/entities/ \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type_id": 1,
    "title": "John Doe",
    "properties": {
      "email": "john@example.com",
      "tier": "premium"
    }
  }'
```

### Explore Graph from Entity

```bash
curl "http://localhost:8000/api/v1/graph/explore/1?depth=2"
```

## Sample Data

The platform includes a demo dataset:

**Entity Types:**
- 👤 Person (employees, contacts)
- 🏢 Company (organizations)
- 📍 Location (cities, offices)
- 📅 Event (conferences, meetings)

**Sample Network:**
- Alice, Bob, Carol (people)
- TechCorp, Data Solutions (companies)
- Employment relationships
- Personal connections
- Event attendance

Try exploring "Alice Johnson" in the Graph Explorer to see the network!

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Run Tests

```bash
cd backend
pytest
```

## Deployment

### Using Docker (Production)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Deployment

See [SETUP.md](SETUP.md) for detailed instructions on deploying to production environments.

## Customization

### Add Your Data Model

1. Define entity types for your domain
2. Create relationships between entities
3. Import your data via API or scripts
4. Build custom visualizations

### Example Use Cases

- **Fraud Detection**: Model transactions, accounts, and suspicious patterns
- **Knowledge Graphs**: Connect research papers, authors, and citations
- **Network Analysis**: Map social connections and influence
- **Intelligence Analysis**: Track entities, events, and relationships
- **Business Analytics**: Visualize customer journeys and touchpoints

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json

## Project Structure

```
untitled_world/
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── api/     # REST endpoints
│   │   ├── models/  # Database models
│   │   ├── schemas/ # Pydantic schemas
│   │   └── core/    # Configuration
│   └── seed_data.py # Sample data
├── frontend/         # React frontend
│   └── src/
│       ├── components/  # React components
│       ├── pages/       # Page components
│       ├── services/    # API clients
│       └── types/       # TypeScript types
└── docker-compose.yml
```

## Contributing

Areas where contributions are welcome:
- Additional visualization types
- Data import/export tools
- Advanced graph algorithms
- Performance optimizations
- Documentation improvements

## Roadmap

**Current Version (v0.1.0)**
- ✅ Core ontology engine
- ✅ Graph visualization
- ✅ Basic analytics
- ✅ Sample data

**Next Version (v0.2.0)**
- [ ] User authentication (JWT)
- [ ] Advanced search
- [ ] Data import (CSV, JSON)
- [ ] Export functionality

**Future**
- [ ] Real-time collaboration
- [ ] Machine learning integration
- [ ] Natural language queries
- [ ] Mobile app

## Troubleshooting

**Can't access the platform?**
- Ensure Docker is running
- Check if ports 3000, 8000, 5432 are available
- Run `docker-compose logs` to see errors

**No sample data?**
- Run `docker-compose exec backend python seed_data.py`

**Frontend can't connect to backend?**
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS settings in `backend/app/core/config.py`

See [SETUP.md](SETUP.md) for more troubleshooting tips.

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with inspiration from:
- Palantir Foundry
- Neo4j Bloom
- Databricks
- Apache Superset

Technologies used:
- FastAPI
- React
- PostgreSQL
- ReactFlow
- And many other amazing open-source projects

## Support

- 📖 Read the [documentation](GETTING_STARTED.md)
- 🐛 Report issues on GitHub
- 💬 Join discussions
- ⭐ Star the project if you find it useful

---

**Built with ❤️ for data investigators everywhere**

Start exploring: `./start.sh` → http://localhost:3000
