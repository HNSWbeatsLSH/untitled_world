# Setup Guide

This guide will help you set up and run the Data Investigation Platform.

## Prerequisites

Make sure you have the following installed:
- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL 15 or higher
- Git

Alternatively, you can use Docker and Docker Compose (recommended for quick setup).

## Quick Start with Docker

The easiest way to get started is using Docker Compose:

```bash
# 1. Start all services
docker-compose up -d

# 2. Wait for services to be healthy (about 30 seconds)

# 3. Seed the database with sample data
docker-compose exec backend python seed_data.py

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

To stop the services:
```bash
docker-compose down
```

## Manual Setup

If you prefer to run the services manually without Docker:

### 1. Database Setup

Create a PostgreSQL database:

```bash
# Create database
createdb investigation_platform

# Or using psql
psql -U postgres
CREATE DATABASE investigation_platform;
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file with your database credentials
# DATABASE_URL=postgresql://username:password@localhost:5432/investigation_platform

# Seed the database with sample data
python seed_data.py

# Run the backend server
uvicorn app.main:app --reload
```

The backend API will be available at http://localhost:8000

### 3. Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file (optional)
echo "VITE_API_URL=http://localhost:8000" > .env

# Start the development server
npm run dev
```

The frontend will be available at http://localhost:3000

## Accessing the Application

Once both services are running:

1. **Frontend UI**: http://localhost:3000
   - Dashboard with statistics and charts
   - Graph Explorer for visualizing entity relationships

2. **Backend API**: http://localhost:8000
   - Interactive API documentation: http://localhost:8000/docs
   - OpenAPI spec: http://localhost:8000/api/v1/openapi.json

## Sample Data

The seed script creates:
- **Entity Types**: Person, Company, Location, Event
- **Sample Entities**: 3 people, 2 companies, 2 locations, 1 event
- **Relationship Types**: Works For, Located In, Attended, Knows
- **Sample Relationships**: Employment, location, event attendance, and personal connections

## Development

### Backend Development

```bash
cd backend
source venv/bin/activate

# Run tests
pytest

# Check code
python -m pylint app

# Run with auto-reload
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Run development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## API Usage Examples

### List all entities
```bash
curl http://localhost:8000/api/v1/entities/
```

### Get entity types
```bash
curl http://localhost:8000/api/v1/entities/types
```

### Explore graph from an entity
```bash
curl "http://localhost:8000/api/v1/graph/explore/1?depth=2"
```

### Get graph statistics
```bash
curl http://localhost:8000/api/v1/graph/stats
```

## Architecture

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API**: RESTful with automatic OpenAPI documentation
- **Port**: 8000

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: TanStack Query (React Query)
- **Graph Visualization**: ReactFlow
- **Charts**: Recharts
- **Port**: 3000

## Troubleshooting

### Database Connection Issues

If you see database connection errors:
1. Ensure PostgreSQL is running
2. Check your DATABASE_URL in `.env` is correct
3. Verify the database exists: `psql -l`

### Port Already in Use

If port 8000 or 3000 is already in use:
```bash
# Backend: Change port in uvicorn command
uvicorn app.main:app --reload --port 8001

# Frontend: Change port in vite.config.ts or use environment variable
PORT=3001 npm run dev
```

### Module Import Errors

Make sure you've installed all dependencies:
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

## Next Steps

1. Explore the sample data in the Graph Explorer
2. Create your own entity types in the Schema section
3. Add custom entities and relationships
4. Build custom dashboards and visualizations
5. Extend the API with additional endpoints
6. Implement authentication and multi-user support

## Production Deployment

For production deployment:
1. Set a secure `SECRET_KEY` in `.env`
2. Use a production-grade database (managed PostgreSQL)
3. Build the frontend: `npm run build`
4. Serve the frontend with nginx or similar
5. Run the backend with gunicorn or similar ASGI server
6. Use environment variables for all configuration
7. Enable HTTPS
8. Set up proper monitoring and logging

## Support

For issues or questions:
- Check the API documentation at http://localhost:8000/docs
- Review the code in [README_PLATFORM.md](README_PLATFORM.md)
- Open an issue on GitHub (if applicable)
