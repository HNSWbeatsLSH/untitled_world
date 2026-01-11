"""
API v1 package.
"""
from fastapi import APIRouter
from . import entities, relationships, graph

api_router = APIRouter()

api_router.include_router(entities.router, prefix="/entities", tags=["entities"])
api_router.include_router(relationships.router, prefix="/relationships", tags=["relationships"])
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])
