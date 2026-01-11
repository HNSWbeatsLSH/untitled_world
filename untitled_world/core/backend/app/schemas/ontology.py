"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime


# Entity Type Schemas
class EntityTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    property_schema: Dict[str, Any] = Field(default_factory=dict)


class EntityTypeCreate(EntityTypeBase):
    pass


class EntityTypeUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    property_schema: Optional[Dict[str, Any]] = None


class EntityType(EntityTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Entity Schemas
class EntityBase(BaseModel):
    entity_type_id: int
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)


class EntityCreate(EntityBase):
    pass


class EntityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None


class Entity(EntityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class EntityWithType(Entity):
    """Entity with embedded type information."""
    entity_type: EntityType


# Relationship Type Schemas
class RelationshipTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    forward_label: str = Field(..., min_length=1, max_length=100)
    reverse_label: str = Field(..., min_length=1, max_length=100)
    color: Optional[str] = None
    line_style: Optional[str] = "solid"
    property_schema: Dict[str, Any] = Field(default_factory=dict)


class RelationshipTypeCreate(RelationshipTypeBase):
    pass


class RelationshipTypeUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    forward_label: Optional[str] = None
    reverse_label: Optional[str] = None
    color: Optional[str] = None
    line_style: Optional[str] = None
    property_schema: Optional[Dict[str, Any]] = None


class RelationshipType(RelationshipTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Relationship Schemas
class RelationshipBase(BaseModel):
    relationship_type_id: int
    from_entity_id: int
    to_entity_id: int
    properties: Dict[str, Any] = Field(default_factory=dict)


class RelationshipCreate(RelationshipBase):
    pass


class RelationshipUpdate(BaseModel):
    properties: Optional[Dict[str, Any]] = None


class Relationship(RelationshipBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class RelationshipWithDetails(Relationship):
    """Relationship with embedded type and entity information."""
    relationship_type: RelationshipType
    from_entity: Entity
    to_entity: Entity


# Graph Schemas
class GraphNode(BaseModel):
    """Node representation for graph visualization."""
    id: int
    type: str
    title: str
    entity_type_id: int
    entity_type_name: str
    properties: Dict[str, Any]
    color: Optional[str] = None
    icon: Optional[str] = None


class GraphEdge(BaseModel):
    """Edge representation for graph visualization."""
    id: int
    source: int
    target: int
    type: str
    label: str
    relationship_type_id: int
    properties: Dict[str, Any]
    color: Optional[str] = None


class GraphData(BaseModel):
    """Complete graph data structure."""
    nodes: List[GraphNode]
    edges: List[GraphEdge]


# User Schemas
class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
