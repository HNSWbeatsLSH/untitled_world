# Getting Started with the Data Investigation Platform

Welcome! This guide will help you get up and running with your new data investigation platform in just a few minutes.

## What You Just Built

You now have a fully functional Palantir-style data investigation platform with:

✅ **Backend API** (FastAPI + PostgreSQL)
- RESTful API with automatic documentation
- Flexible ontology engine for custom data models
- Graph traversal and exploration endpoints
- Sample data included

✅ **Frontend Application** (React + TypeScript)
- Interactive dashboard with statistics
- Graph visualization with ReactFlow
- Search and filtering capabilities
- Responsive, modern UI

✅ **Complete Development Setup**
- Docker Compose for easy deployment
- Hot-reload development servers
- Sample data for testing
- Comprehensive documentation

## Quick Start (2 minutes)

### Option 1: Docker (Recommended)

Simply run:
```bash
./start.sh
```

That's it! The script will:
1. Start PostgreSQL database
2. Start the backend API
3. Start the frontend application
4. Load sample data

Access the platform at **http://localhost:3000**

### Option 2: Manual Setup

If you prefer to run services manually:

**Terminal 1 - Database:**
```bash
# Make sure PostgreSQL is running
createdb investigation_platform
```

**Terminal 2 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
python seed_data.py
uvicorn app.main:app --reload
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Your First Steps

### 1. Explore the Dashboard (2 min)

Visit http://localhost:3000

You'll see:
- **Statistics**: Total entities, relationships, and types
- **Charts**: Visual breakdown of your data
- **Quick Actions**: Links to explore further

### 2. Try the Graph Explorer (5 min)

Click on "Graph Explorer" in the sidebar

1. **Search** for an entity (try "Alice" or "TechCorp")
2. **Click** on an entity to explore its connections
3. **Adjust depth** slider to see more connections
4. **Click nodes** in the graph to navigate further

### 3. Check the API Documentation (3 min)

Visit http://localhost:8000/docs

You'll find:
- Interactive API documentation
- Try out endpoints directly in the browser
- See request/response schemas
- Test with the sample data

## Understanding the Sample Data

The platform comes with a small business network:

**People:**
- Alice Johnson (Software Engineer at TechCorp)
- Bob Smith (Product Manager at TechCorp)
- Carol Williams (Data Scientist at Data Solutions)

**Companies:**
- TechCorp Inc. (San Francisco)
- Data Solutions Ltd. (New York)

**Connections:**
- Employment relationships
- Personal connections (Alice knows Bob and Carol)
- Event attendance (all attended Tech Summit 2024)

Try exploring these in the Graph Explorer!

## Common Tasks

### Creating a New Entity Type

```bash
curl -X POST http://localhost:8000/api/v1/entities/types \
  -H "Content-Type: application/json" \
  -d '{
    "name": "project",
    "display_name": "Project",
    "description": "A work project",
    "color": "#10b981",
    "property_schema": {
      "budget": {"type": "number"},
      "deadline": {"type": "string"}
    }
  }'
```

### Creating a New Entity

```bash
curl -X POST http://localhost:8000/api/v1/entities/ \
  -H "Content-Type: application/json" \
  -d '{
    "entity_type_id": 1,
    "title": "New Entity",
    "description": "Description here",
    "properties": {
      "custom_field": "custom_value"
    }
  }'
```

### Creating a Relationship

```bash
curl -X POST http://localhost:8000/api/v1/relationships/ \
  -H "Content-Type: application/json" \
  -d '{
    "relationship_type_id": 1,
    "from_entity_id": 1,
    "to_entity_id": 2,
    "properties": {}
  }'
```

## Customization Ideas

Now that you have the platform running, here are some ideas:

### 1. Add Your Own Data Model

Think about your use case:
- **Sales**: Customers, Products, Orders, Transactions
- **Research**: Papers, Authors, Citations, Institutions
- **Security**: Users, Devices, Events, Threats
- **Social**: People, Posts, Comments, Likes

Create entity types and relationships that match your domain.

### 2. Import Your Data

Write a script to:
1. Create your entity types
2. Import entities from your data source
3. Create relationships based on your data

Example:
```python
import pandas as pd
from app.core.database import SessionLocal
from app.models.ontology import Entity

df = pd.read_csv("your_data.csv")
db = SessionLocal()

for _, row in df.iterrows():
    entity = Entity(
        entity_type_id=1,
        title=row['name'],
        properties=row.to_dict()
    )
    db.add(entity)

db.commit()
```

### 3. Build Custom Dashboards

Add new visualizations in `frontend/src/pages/`:
- Timeline views for temporal data
- Geographic maps for location data
- Custom charts for your metrics
- Specialized search interfaces

### 4. Extend the API

Add business logic in `backend/app/api/v1/`:
- Custom analytics endpoints
- Data aggregation queries
- Export functionality
- Integration with external services

## Next Steps

### Learn More
- Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for architecture details
- Check [README_PLATFORM.md](README_PLATFORM.md) for feature documentation
- Review [SETUP.md](SETUP.md) for deployment options

### Develop Further
1. **Authentication**: Add user management (JWT tokens)
2. **Permissions**: Implement role-based access control
3. **Real-time**: Add WebSocket support for live updates
4. **Analytics**: Integrate with data science libraries
5. **Export**: Add CSV/JSON export functionality
6. **Import**: Build data import wizards

### Production Deployment
When you're ready to deploy:
1. Set up a production database (AWS RDS, Google Cloud SQL, etc.)
2. Configure environment variables
3. Build the frontend: `npm run build`
4. Deploy with Docker or cloud platforms
5. Set up monitoring and backups

## Troubleshooting

**Services won't start?**
- Check if ports 3000, 8000, or 5432 are already in use
- Verify Docker is running (for Docker setup)
- Check logs: `docker-compose logs`

**Can't see sample data?**
- Make sure you ran `python seed_data.py`
- Check database connection in `.env` file
- Try restarting the backend: `docker-compose restart backend`

**Frontend can't connect to backend?**
- Verify backend is running: http://localhost:8000/health
- Check CORS settings in `backend/app/core/config.py`
- Clear browser cache and reload

**Graph not displaying?**
- Make sure you selected an entity first
- Check browser console for errors
- Verify entities have relationships in the database

## Resources

- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **Database**: localhost:5432/investigation_platform

## Getting Help

If you run into issues:
1. Check the logs: `docker-compose logs -f`
2. Review the documentation files
3. Try the troubleshooting steps above
4. Check that all services are running

## What's Next?

You have a solid foundation for a data investigation platform. The possibilities are endless:

- Build industry-specific solutions (fraud detection, knowledge graphs, network analysis)
- Integrate with machine learning models for predictions
- Add natural language processing for text analysis
- Create mobile applications
- Build plugins and extensions

The platform is yours to customize and extend!

Happy investigating! 🔍
