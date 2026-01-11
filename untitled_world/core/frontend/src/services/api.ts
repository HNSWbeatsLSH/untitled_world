/**
 * API client for the Data Investigation Platform.
 */
import axios from 'axios';
import type {
  EntityType,
  Entity,
  EntityWithType,
  RelationshipType,
  Relationship,
  RelationshipWithDetails,
  GraphData,
  GraphStats,
} from '@/types/ontology';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_V1 = `${API_BASE_URL}/api/v1`;

const api = axios.create({
  baseURL: API_V1,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Entity Types
export const entityTypeApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    api.get<EntityType[]>('/entities/types', { params }),

  get: (id: number) =>
    api.get<EntityType>(`/entities/types/${id}`),

  create: (data: Omit<EntityType, 'id' | 'created_at' | 'updated_at'>) =>
    api.post<EntityType>('/entities/types', data),

  update: (id: number, data: Partial<EntityType>) =>
    api.put<EntityType>(`/entities/types/${id}`, data),

  delete: (id: number) =>
    api.delete(`/entities/types/${id}`),
};

// Entities
export const entityApi = {
  list: (params?: {
    skip?: number;
    limit?: number;
    entity_type_id?: number;
    search?: string;
  }) =>
    api.get<EntityWithType[]>('/entities/', { params }),

  get: (id: number) =>
    api.get<EntityWithType>(`/entities/${id}`),

  create: (data: Omit<Entity, 'id' | 'created_at' | 'updated_at' | 'created_by'>) =>
    api.post<EntityWithType>('/entities/', data),

  update: (id: number, data: Partial<Entity>) =>
    api.put<EntityWithType>(`/entities/${id}`, data),

  delete: (id: number) =>
    api.delete(`/entities/${id}`),

  getRelationships: (id: number) =>
    api.get<RelationshipWithDetails[]>(`/entities/${id}/relationships`),
};

// Relationship Types
export const relationshipTypeApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    api.get<RelationshipType[]>('/relationships/types', { params }),

  get: (id: number) =>
    api.get<RelationshipType>(`/relationships/types/${id}`),

  create: (data: Omit<RelationshipType, 'id' | 'created_at' | 'updated_at'>) =>
    api.post<RelationshipType>('/relationships/types', data),

  update: (id: number, data: Partial<RelationshipType>) =>
    api.put<RelationshipType>(`/relationships/types/${id}`, data),

  delete: (id: number) =>
    api.delete(`/relationships/types/${id}`),
};

// Relationships
export const relationshipApi = {
  list: (params?: {
    skip?: number;
    limit?: number;
    relationship_type_id?: number;
    entity_id?: number;
  }) =>
    api.get<RelationshipWithDetails[]>('/relationships/', { params }),

  get: (id: number) =>
    api.get<RelationshipWithDetails>(`/relationships/${id}`),

  create: (data: Omit<Relationship, 'id' | 'created_at' | 'updated_at' | 'created_by'>) =>
    api.post<RelationshipWithDetails>('/relationships/', data),

  update: (id: number, data: Partial<Relationship>) =>
    api.put<RelationshipWithDetails>(`/relationships/${id}`, data),

  delete: (id: number) =>
    api.delete(`/relationships/${id}`),
};

// Graph
export const graphApi = {
  explore: (entityId: number, depth: number = 1) =>
    api.get<GraphData>(`/graph/explore/${entityId}`, { params: { depth } }),

  getSubgraph: (entityIds: number[]) =>
    api.get<GraphData>('/graph/subgraph', {
      params: { entity_ids: entityIds.join(',') },
    }),

  getStats: () =>
    api.get<GraphStats>('/graph/stats'),
};

export default api;
