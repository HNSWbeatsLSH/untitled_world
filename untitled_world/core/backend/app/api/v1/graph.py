"""
API endpoints for graph visualization and exploration.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...models import ontology as models
from ...schemas import ontology as schemas

router = APIRouter()


@router.get("/explore/{entity_id}", response_model=schemas.GraphData)
def explore_from_entity(
    entity_id: int,
    depth: int = Query(1, ge=1, le=5, description="Depth of graph traversal"),
    db: Session = Depends(get_db),
):
    """
    Explore the graph starting from a specific entity.
    Returns nodes and edges up to the specified depth.
    """
    # Verify the starting entity exists
    start_entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
    if not start_entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    visited_entities = set()
    visited_relationships = set()
    nodes_dict = {}
    edges_list = []

    def traverse(current_entity_id: int, current_depth: int):
        if current_depth > depth or current_entity_id in visited_entities:
            return

        visited_entities.add(current_entity_id)

        # Get the entity
        entity = db.query(models.Entity).filter(
            models.Entity.id == current_entity_id
        ).first()
        if not entity:
            return

        # Add node
        if current_entity_id not in nodes_dict:
            nodes_dict[current_entity_id] = schemas.GraphNode(
                id=entity.id,
                type="entity",
                title=entity.title,
                entity_type_id=entity.entity_type_id,
                entity_type_name=entity.entity_type.name,
                properties=entity.properties,
                color=entity.entity_type.color,
                icon=entity.entity_type.icon,
            )

        if current_depth < depth:
            # Get outgoing relationships
            outgoing = db.query(models.Relationship).filter(
                models.Relationship.from_entity_id == current_entity_id
            ).all()

            for rel in outgoing:
                if rel.id not in visited_relationships:
                    visited_relationships.add(rel.id)
                    edges_list.append(schemas.GraphEdge(
                        id=rel.id,
                        source=rel.from_entity_id,
                        target=rel.to_entity_id,
                        type="relationship",
                        label=rel.relationship_type.forward_label,
                        relationship_type_id=rel.relationship_type_id,
                        properties=rel.properties,
                        color=rel.relationship_type.color,
                    ))
                    traverse(rel.to_entity_id, current_depth + 1)

            # Get incoming relationships
            incoming = db.query(models.Relationship).filter(
                models.Relationship.to_entity_id == current_entity_id
            ).all()

            for rel in incoming:
                if rel.id not in visited_relationships:
                    visited_relationships.add(rel.id)
                    edges_list.append(schemas.GraphEdge(
                        id=rel.id,
                        source=rel.from_entity_id,
                        target=rel.to_entity_id,
                        type="relationship",
                        label=rel.relationship_type.forward_label,
                        relationship_type_id=rel.relationship_type_id,
                        properties=rel.properties,
                        color=rel.relationship_type.color,
                    ))
                    traverse(rel.from_entity_id, current_depth + 1)

    # Start traversal
    traverse(entity_id, 0)

    return schemas.GraphData(
        nodes=list(nodes_dict.values()),
        edges=edges_list,
    )


@router.get("/subgraph", response_model=schemas.GraphData)
def get_subgraph(
    entity_ids: str = Query(..., description="Comma-separated entity IDs"),
    db: Session = Depends(get_db),
):
    """
    Get a subgraph containing specific entities and their direct relationships.
    """
    try:
        entity_id_list = [int(id.strip()) for id in entity_ids.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid entity IDs format")

    # Get entities
    entities = db.query(models.Entity).filter(
        models.Entity.id.in_(entity_id_list)
    ).all()

    if not entities:
        raise HTTPException(status_code=404, detail="No entities found")

    # Build nodes
    nodes_list = []
    for entity in entities:
        nodes_list.append(schemas.GraphNode(
            id=entity.id,
            type="entity",
            title=entity.title,
            entity_type_id=entity.entity_type_id,
            entity_type_name=entity.entity_type.name,
            properties=entity.properties,
            color=entity.entity_type.color,
            icon=entity.entity_type.icon,
        ))

    # Get relationships between these entities
    relationships = db.query(models.Relationship).filter(
        models.Relationship.from_entity_id.in_(entity_id_list),
        models.Relationship.to_entity_id.in_(entity_id_list),
    ).all()

    edges_list = []
    for rel in relationships:
        edges_list.append(schemas.GraphEdge(
            id=rel.id,
            source=rel.from_entity_id,
            target=rel.to_entity_id,
            type="relationship",
            label=rel.relationship_type.forward_label,
            relationship_type_id=rel.relationship_type_id,
            properties=rel.properties,
            color=rel.relationship_type.color,
        ))

    return schemas.GraphData(
        nodes=nodes_list,
        edges=edges_list,
    )


@router.get("/stats", response_model=dict)
def get_graph_stats(db: Session = Depends(get_db)):
    """Get statistics about the graph."""
    entity_count = db.query(models.Entity).count()
    relationship_count = db.query(models.Relationship).count()
    entity_type_count = db.query(models.EntityType).count()
    relationship_type_count = db.query(models.RelationshipType).count()

    # Get entity counts by type
    entity_type_counts = db.query(
        models.EntityType.name,
        models.EntityType.display_name,
        db.func.count(models.Entity.id).label("count")
    ).outerjoin(models.Entity).group_by(
        models.EntityType.id,
        models.EntityType.name,
        models.EntityType.display_name
    ).all()

    return {
        "total_entities": entity_count,
        "total_relationships": relationship_count,
        "entity_types": entity_type_count,
        "relationship_types": relationship_type_count,
        "entities_by_type": [
            {"type": name, "display_name": display_name, "count": count}
            for name, display_name, count in entity_type_counts
        ],
    }
