"""
Main FastAPI application for the Data Investigation Platform.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .core.module_loader import module_loader
from .api.v1 import api_router
from .api.ontology_showcase import router as ontology_showcase_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A Palantir-inspired data investigation and ontology platform",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include core API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(ontology_showcase_router, prefix=settings.API_V1_PREFIX)

# Load and register modules
def load_modules():
    """Load modules based on customer configuration."""
    customer_id = os.getenv("CUSTOMER_ID")

    if customer_id:
        # Load modules for specific customer
        enabled_modules = module_loader.get_enabled_modules_for_customer(customer_id)
        print(f"Loading modules for customer {customer_id}: {enabled_modules}")

        for module_name in enabled_modules:
            success = module_loader.load_module(module_name)
            if success:
                print(f"✓ Loaded module: {module_name}")
            else:
                print(f"✗ Failed to load module: {module_name}")
    else:
        # Load all available modules (development mode)
        available_modules = module_loader.discover_modules()
        print(f"Development mode: Loading all available modules: {available_modules}")

        for module_name in available_modules:
            module_loader.load_module(module_name)

    # Register module routes with the app
    module_loader.register_modules_with_app(app)

# Load modules on startup
load_modules()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Data Investigation Platform API",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
