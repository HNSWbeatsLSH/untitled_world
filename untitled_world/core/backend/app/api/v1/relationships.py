"""
API endpoints for relationship management.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...models import ontology as models
from ...schemas import ontology as schemas

router = APIRouter()


@router.get("/types", response_model=List[schemas.RelationshipType])
def list_relationship_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List all relationship types."""
    relationship_types = db.query(models.RelationshipType).offset(skip).limit(limit).all()
    return relationship_types


@router.post("/types", response_model=schemas.RelationshipType, status_code=201)
def create_relationship_type(
    relationship_type: schemas.RelationshipTypeCreate,
    db: Session = Depends(get_db),
):
    """Create a new relationship type."""
    # Check if relationship type already exists
    existing = db.query(models.RelationshipType).filter(
        models.RelationshipType.name == relationship_type.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Relationship type already exists")

    db_relationship_type = models.RelationshipType(**relationship_type.model_dump())
    db.add(db_relationship_type)
    db.commit()
    db.refresh(db_relationship_type)
    return db_relationship_type


@router.get("/types/{relationship_type_id}", response_model=schemas.RelationshipType)
def get_relationship_type(relationship_type_id: int, db: Session = Depends(get_db)):
    """Get a specific relationship type by ID."""
    relationship_type = db.query(models.RelationshipType).filter(
        models.RelationshipType.id == relationship_type_id
    ).first()
    if not relationship_type:
        raise HTTPException(status_code=404, detail="Relationship type not found")
    return relationship_type


@router.put("/types/{relationship_type_id}", response_model=schemas.RelationshipType)
def update_relationship_type(
    relationship_type_id: int,
    relationship_type_update: schemas.RelationshipTypeUpdate,
    db: Session = Depends(get_db),
):
    """Update a relationship type."""
    db_relationship_type = db.query(models.RelationshipType).filter(
        models.RelationshipType.id == relationship_type_id
    ).first()
    if not db_relationship_type:
        raise HTTPException(status_code=404, detail="Relationship type not found")

    update_data = relationship_type_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_relationship_type, field, value)

    db.commit()
    db.refresh(db_relationship_type)
    return db_relationship_type


@router.delete("/types/{relationship_type_id}", status_code=204)
def delete_relationship_type(relationship_type_id: int, db: Session = Depends(get_db)):
    """Delete a relationship type."""
    db_relationship_type = db.query(models.RelationshipType).filter(
        models.RelationshipType.id == relationship_type_id
    ).first()
    if not db_relationship_type:
        raise HTTPException(status_code=404, detail="Relationship type not found")

    db.delete(db_relationship_type)
    db.commit()
    return None


# Relationship endpoints
@router.get("/", response_model=List[schemas.RelationshipWithDetails])
def list_relationships(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    relationship_type_id: Optional[int] = None,
    entity_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List relationships with optional filtering."""
    query = db.query(models.Relationship)

    if relationship_type_id:
        query = query.filter(models.Relationship.relationship_type_id == relationship_type_id)

    if entity_id:
        query = query.filter(
            (models.Relationship.from_entity_id == entity_id) |
            (models.Relationship.to_entity_id == entity_id)
        )

    relationships = query.offset(skip).limit(limit).all()
    return relationships


@router.post("/", response_model=schemas.RelationshipWithDetails, status_code=201)
def create_relationship(
    relationship: schemas.RelationshipCreate,
    db: Session = Depends(get_db),
):
    """Create a new relationship between entities."""
    # Validate relationship type exists
    relationship_type = db.query(models.RelationshipType).filter(
        models.RelationshipType.id == relationship.relationship_type_id
    ).first()
    if not relationship_type:
        raise HTTPException(status_code=400, detail="Relationship type not found")

    # Validate both entities exist
    from_entity = db.query(models.Entity).filter(
        models.Entity.id == relationship.from_entity_id
    ).first()
    to_entity = db.query(models.Entity).filter(
        models.Entity.id == relationship.to_entity_id
    ).first()

    if not from_entity or not to_entity:
        raise HTTPException(status_code=400, detail="One or both entities not found")

    db_relationship = models.Relationship(**relationship.model_dump())
    db.add(db_relationship)
    db.commit()
    db.refresh(db_relationship)
    return db_relationship


@router.get("/{relationship_id}", response_model=schemas.RelationshipWithDetails)
def get_relationship(relationship_id: int, db: Session = Depends(get_db)):
    """Get a specific relationship by ID."""
    relationship = db.query(models.Relationship).filter(
        models.Relationship.id == relationship_id
    ).first()
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return relationship


@router.put("/{relationship_id}", response_model=schemas.RelationshipWithDetails)
def update_relationship(
    relationship_id: int,
    relationship_update: schemas.RelationshipUpdate,
    db: Session = Depends(get_db),
):
    """Update a relationship."""
    db_relationship = db.query(models.Relationship).filter(
        models.Relationship.id == relationship_id
    ).first()
    if not db_relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")

    update_data = relationship_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_relationship, field, value)

    db.commit()
    db.refresh(db_relationship)
    return db_relationship


@router.delete("/{relationship_id}", status_code=204)
def delete_relationship(relationship_id: int, db: Session = Depends(get_db)):
    """Delete a relationship."""
    db_relationship = db.query(models.Relationship).filter(
        models.Relationship.id == relationship_id
    ).first()
    if not db_relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")

    db.delete(db_relationship)
    db.commit()
    return None
