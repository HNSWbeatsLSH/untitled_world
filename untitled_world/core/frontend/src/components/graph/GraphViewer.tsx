/**
 * Graph visualization component using ReactFlow.
 */
import { useCallback, useEffect, useState } from 'react';
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  MiniMap,
  NodeTypes,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { GraphData, GraphNode as GraphNodeData, GraphEdge as GraphEdgeData } from '@/types/ontology';
import EntityNode from './EntityNode';

const nodeTypes: NodeTypes = {
  entity: EntityNode,
};

interface GraphViewerProps {
  data: GraphData;
  onNodeClick?: (node: GraphNodeData) => void;
  onEdgeClick?: (edge: GraphEdgeData) => void;
}

const GraphViewer = ({ data, onNodeClick, onEdgeClick }: GraphViewerProps) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Convert graph data to ReactFlow format
  useEffect(() => {
    const flowNodes: Node[] = data.nodes.map((node, index) => ({
      id: node.id.toString(),
      type: 'entity',
      position: {
        x: Math.cos((2 * Math.PI * index) / data.nodes.length) * 300 + 400,
        y: Math.sin((2 * Math.PI * index) / data.nodes.length) * 300 + 300,
      },
      data: node,
    }));

    const flowEdges: Edge[] = data.edges.map((edge) => ({
      id: edge.id.toString(),
      source: edge.source.toString(),
      target: edge.target.toString(),
      label: edge.label,
      type: 'smoothstep',
      animated: true,
      style: {
        stroke: edge.color || '#94a3b8',
        strokeWidth: 2,
      },
      data: edge,
    }));

    setNodes(flowNodes);
    setEdges(flowEdges);
  }, [data, setNodes, setEdges]);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const handleNodeClick = useCallback(
    (_event: React.MouseEvent, node: Node) => {
      if (onNodeClick && node.data) {
        onNodeClick(node.data as GraphNodeData);
      }
    },
    [onNodeClick]
  );

  const handleEdgeClick = useCallback(
    (_event: React.MouseEvent, edge: Edge) => {
      if (onEdgeClick && edge.data) {
        onEdgeClick(edge.data as GraphEdgeData);
      }
    },
    [onEdgeClick]
  );

  return (
    <div className="w-full h-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onNodeClick={handleNodeClick}
        onEdgeClick={handleEdgeClick}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
      >
        <Controls />
        <Background />
        <MiniMap
          nodeColor={(node) => {
            const nodeData = node.data as GraphNodeData;
            return nodeData.color || '#64748b';
          }}
          maskColor="rgba(0, 0, 0, 0.2)"
        />
      </ReactFlow>
    </div>
  );
};

export default GraphViewer;
