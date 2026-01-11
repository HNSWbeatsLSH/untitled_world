/**
 * Custom node component for entity visualization.
 */
import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { GraphNode } from '@/types/ontology';
import { Database } from 'lucide-react';

const EntityNode = ({ data }: NodeProps<GraphNode>) => {
  const bgColor = data.color || '#64748b';

  return (
    <div
      className="px-4 py-3 rounded-lg border-2 shadow-lg min-w-[180px] bg-white"
      style={{ borderColor: bgColor }}
    >
      <Handle type="target" position={Position.Top} className="w-3 h-3" />

      <div className="flex items-start gap-2">
        <div
          className="p-2 rounded"
          style={{ backgroundColor: `${bgColor}20` }}
        >
          <Database size={20} style={{ color: bgColor }} />
        </div>

        <div className="flex-1 min-w-0">
          <div className="text-xs font-medium text-gray-500 uppercase tracking-wide">
            {data.entity_type_name}
          </div>
          <div className="text-sm font-semibold text-gray-900 mt-1 truncate">
            {data.title}
          </div>

          {Object.keys(data.properties).length > 0 && (
            <div className="mt-2 space-y-1">
              {Object.entries(data.properties).slice(0, 2).map(([key, value]) => (
                <div key={key} className="text-xs text-gray-600">
                  <span className="font-medium">{key}:</span>{' '}
                  <span className="truncate">{String(value)}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} className="w-3 h-3" />
    </div>
  );
};

export default memo(EntityNode);
