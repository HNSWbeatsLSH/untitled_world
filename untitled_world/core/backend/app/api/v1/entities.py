"""
API endpoints for entity management.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...models import ontology as models
from ...schemas import ontology as schemas

router = APIRouter()


@router.get("/types", response_model=List[schemas.EntityType])
def list_entity_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List all entity types."""
    entity_types = db.query(models.EntityType).offset(skip).limit(limit).all()
    return entity_types


@router.post("/types", response_model=schemas.EntityType, status_code=201)
def create_entity_type(
    entity_type: schemas.EntityTypeCreate,
    db: Session = Depends(get_db),
):
    """Create a new entity type."""
    # Check if entity type already exists
    existing = db.query(models.EntityType).filter(
        models.EntityType.name == entity_type.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Entity type already exists")

    db_entity_type = models.EntityType(**entity_type.model_dump())
    db.add(db_entity_type)
    db.commit()
    db.refresh(db_entity_type)
    return db_entity_type


@router.get("/types/{entity_type_id}", response_model=schemas.EntityType)
def get_entity_type(entity_type_id: int, db: Session = Depends(get_db)):
    """Get a specific entity type by ID."""
    entity_type = db.query(models.EntityType).filter(
        models.EntityType.id == entity_type_id
    ).first()
    if not entity_type:
        raise HTTPException(status_code=404, detail="Entity type not found")
    return entity_type


@router.put("/types/{entity_type_id}", response_model=schemas.EntityType)
def update_entity_type(
    entity_type_id: int,
    entity_type_update: schemas.EntityTypeUpdate,
    db: Session = Depends(get_db),
):
    """Update an entity type."""
    db_entity_type = db.query(models.EntityType).filter(
        models.EntityType.id == entity_type_id
    ).first()
    if not db_entity_type:
        raise HTTPException(status_code=404, detail="Entity type not found")

    update_data = entity_type_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_entity_type, field, value)

    db.commit()
    db.refresh(db_entity_type)
    return db_entity_type


@router.delete("/types/{entity_type_id}", status_code=204)
def delete_entity_type(entity_type_id: int, db: Session = Depends(get_db)):
    """Delete an entity type."""
    db_entity_type = db.query(models.EntityType).filter(
        models.EntityType.id == entity_type_id
    ).first()
    if not db_entity_type:
        raise HTTPException(status_code=404, detail="Entity type not found")

    db.delete(db_entity_type)
    db.commit()
    return None


# Entity endpoints
@router.get("/", response_model=List[schemas.EntityWithType])
def list_entities(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    entity_type_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List entities with optional filtering."""
    query = db.query(models.Entity)

    if entity_type_id:
        query = query.filter(models.Entity.entity_type_id == entity_type_id)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(models.Entity.title.ilike(search_pattern))

    entities = query.offset(skip).limit(limit).all()
    return entities


@router.post("/", response_model=schemas.EntityWithType, status_code=201)
def create_entity(
    entity: schemas.EntityCreate,
    db: Session = Depends(get_db),
):
    """Create a new entity."""
    # Validate entity type exists
    entity_type = db.query(models.EntityType).filter(
        models.EntityType.id == entity.entity_type_id
    ).first()
    if not entity_type:
        raise HTTPException(status_code=400, detail="Entity type not found")

    db_entity = models.Entity(**entity.model_dump())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


@router.get("/{entity_id}", response_model=schemas.EntityWithType)
def get_entity(entity_id: int, db: Session = Depends(get_db)):
    """Get a specific entity by ID."""
    entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity


@router.put("/{entity_id}", response_model=schemas.EntityWithType)
def update_entity(
    entity_id: int,
    entity_update: schemas.EntityUpdate,
    db: Session = Depends(get_db),
):
    """Update an entity."""
    db_entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
    if not db_entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    update_data = entity_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_entity, field, value)

    db.commit()
    db.refresh(db_entity)
    return db_entity


@router.delete("/{entity_id}", status_code=204)
def delete_entity(entity_id: int, db: Session = Depends(get_db)):
    """Delete an entity."""
    db_entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
    if not db_entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    db.delete(db_entity)
    db.commit()
    return None


@router.get("/{entity_id}/relationships", response_model=List[schemas.RelationshipWithDetails])
def get_entity_relationships(
    entity_id: int,
    db: Session = Depends(get_db),
):
    """Get all relationships for an entity (both incoming and outgoing)."""
    entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    # Get both outgoing and incoming relationships
    outgoing = db.query(models.Relationship).filter(
        models.Relationship.from_entity_id == entity_id
    ).all()
    incoming = db.query(models.Relationship).filter(
        models.Relationship.to_entity_id == entity_id
    ).all()

    return outgoing + incoming
