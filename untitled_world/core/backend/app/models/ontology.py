"""
Ontology data models for entities, relationships, and schemas.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from ..core.database import Base


class EntityType(Base):
    """
    Defines types of entities in the ontology (e.g., Person, Company, Event).
    """
    __tablename__ = "entity_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(20), nullable=True)

    # Schema definition for properties
    property_schema = Column(JSON, nullable=False, default={})

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    entities = relationship("Entity", back_populates="entity_type", cascade="all, delete-orphan")


class Entity(Base):
    """
    Represents an entity instance in the ontology.
    """
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    entity_type_id = Column(Integer, ForeignKey("entity_types.id"), nullable=False, index=True)

    # Display information
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Flexible property storage
    properties = Column(JSON, nullable=False, default={})

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    entity_type = relationship("EntityType", back_populates="entities")
    outgoing_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.from_entity_id",
        back_populates="from_entity",
        cascade="all, delete-orphan"
    )
    incoming_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.to_entity_id",
        back_populates="to_entity",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_entity_type_title', 'entity_type_id', 'title'),
    )


class RelationshipType(Base):
    """
    Defines types of relationships between entities.
    """
    __tablename__ = "relationship_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Directional labels
    forward_label = Column(String(100), nullable=False)  # e.g., "works for"
    reverse_label = Column(String(100), nullable=False)  # e.g., "employs"

    # Visual styling
    color = Column(String(20), nullable=True)
    line_style = Column(String(20), nullable=True, default="solid")

    # Schema for relationship properties
    property_schema = Column(JSON, nullable=False, default={})

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    relationships = relationship("Relationship", back_populates="relationship_type")


class Relationship(Base):
    """
    Represents a relationship instance between two entities.
    """
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, index=True)
    relationship_type_id = Column(Integer, ForeignKey("relationship_types.id"), nullable=False, index=True)
    from_entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False, index=True)
    to_entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False, index=True)

    # Flexible property storage
    properties = Column(JSON, nullable=False, default={})

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    relationship_type = relationship("RelationshipType", back_populates="relationships")
    from_entity = relationship("Entity", foreign_keys=[from_entity_id], back_populates="outgoing_relationships")
    to_entity = relationship("Entity", foreign_keys=[to_entity_id], back_populates="incoming_relationships")

    __table_args__ = (
        Index('idx_relationship_entities', 'from_entity_id', 'to_entity_id'),
        Index('idx_relationship_type_from', 'relationship_type_id', 'from_entity_id'),
    )


class User(Base):
    """
    User model for authentication and ownership.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)

    is_active = Column(Integer, default=1)
    is_superuser = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
