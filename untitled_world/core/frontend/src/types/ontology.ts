/**
 * Type definitions for the ontology system.
 */

export interface EntityType {
  id: number;
  name: string;
  display_name: string;
  description?: string;
  icon?: string;
  color?: string;
  property_schema: Record<string, any>;
  created_at: string;
  updated_at?: string;
}

export interface Entity {
  id: number;
  entity_type_id: number;
  title: string;
  description?: string;
  properties: Record<string, any>;
  created_at: string;
  updated_at?: string;
  created_by?: number;
}

export interface EntityWithType extends Entity {
  entity_type: EntityType;
}

export interface RelationshipType {
  id: number;
  name: string;
  display_name: string;
  description?: string;
  forward_label: string;
  reverse_label: string;
  color?: string;
  line_style?: string;
  property_schema: Record<string, any>;
  created_at: string;
  updated_at?: string;
}

export interface Relationship {
  id: number;
  relationship_type_id: number;
  from_entity_id: number;
  to_entity_id: number;
  properties: Record<string, any>;
  created_at: string;
  updated_at?: string;
  created_by?: number;
}

export interface RelationshipWithDetails extends Relationship {
  relationship_type: RelationshipType;
  from_entity: Entity;
  to_entity: Entity;
}

export interface GraphNode {
  id: number;
  type: string;
  title: string;
  entity_type_id: number;
  entity_type_name: string;
  properties: Record<string, any>;
  color?: string;
  icon?: string;
}

export interface GraphEdge {
  id: number;
  source: number;
  target: number;
  type: string;
  label: string;
  relationship_type_id: number;
  properties: Record<string, any>;
  color?: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface GraphStats {
  total_entities: number;
  total_relationships: number;
  entity_types: number;
  relationship_types: number;
  entities_by_type: Array<{
    type: string;
    display_name: string;
    count: number;
  }>;
}
