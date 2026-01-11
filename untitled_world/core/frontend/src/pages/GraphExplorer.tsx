/**
 * Graph exploration page.
 */
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { entityApi, graphApi } from '@/services/api';
import GraphViewer from '@/components/graph/GraphViewer';
import { GraphNode, GraphData } from '@/types/ontology';
import { Search, Layers } from 'lucide-react';

const GraphExplorer = () => {
  const [selectedEntityId, setSelectedEntityId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [depth, setDepth] = useState(1);

  const { data: entities } = useQuery({
    queryKey: ['entities', searchTerm],
    queryFn: () =>
      entityApi.list({ search: searchTerm || undefined, limit: 20 }).then(res => res.data),
  });

  const { data: graphData, isLoading: isLoadingGraph } = useQuery({
    queryKey: ['graph', selectedEntityId, depth],
    queryFn: () =>
      selectedEntityId
        ? graphApi.explore(selectedEntityId, depth).then(res => res.data)
        : Promise.resolve({ nodes: [], edges: [] } as GraphData),
    enabled: selectedEntityId !== null,
  });

  const handleNodeClick = (node: GraphNode) => {
    setSelectedEntityId(node.id);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Graph Explorer</h2>
          <p className="text-sm text-gray-500 mt-1">
            Search and explore entity relationships
          </p>
        </div>

        {/* Search */}
        <div className="p-4 border-b border-gray-200">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search entities..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Depth Control */}
        <div className="p-4 border-b border-gray-200">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Layers className="inline w-4 h-4 mr-1" />
            Exploration Depth: {depth}
          </label>
          <input
            type="range"
            min="1"
            max="3"
            value={depth}
            onChange={(e) => setDepth(parseInt(e.target.value))}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>1 level</span>
            <span>3 levels</span>
          </div>
        </div>

        {/* Entity List */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-4">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Entities</h3>
            <div className="space-y-2">
              {entities?.map((entity) => (
                <button
                  key={entity.id}
                  onClick={() => setSelectedEntityId(entity.id)}
                  className={`w-full text-left p-3 rounded-lg border transition-all ${
                    selectedEntityId === entity.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <div
                      className="w-3 h-3 rounded-full mt-1 flex-shrink-0"
                      style={{ backgroundColor: entity.entity_type.color || '#64748b' }}
                    />
                    <div className="flex-1 min-w-0">
                      <div className="text-xs text-gray-500 uppercase">
                        {entity.entity_type.display_name}
                      </div>
                      <div className="text-sm font-medium text-gray-900 truncate">
                        {entity.title}
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Graph Viewer */}
      <div className="flex-1 relative">
        {isLoadingGraph ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-gray-500">Loading graph...</div>
          </div>
        ) : graphData && graphData.nodes.length > 0 ? (
          <GraphViewer data={graphData} onNodeClick={handleNodeClick} />
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="text-gray-400 mb-2">
                <Search className="w-12 h-12 mx-auto" />
              </div>
              <p className="text-gray-500">
                Select an entity to explore its relationships
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GraphExplorer;
