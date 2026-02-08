/**
 * Main dashboard page.
 */
import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { graphApi } from '@/services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Database, Network, Link } from 'lucide-react';

const Dashboard = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['graph-stats'],
    queryFn: () => graphApi.getStats().then(res => res.data),
  });

  // Fetch machine supervisor stats
  const { data: machineStats } = useQuery({
    queryKey: ['machine-stats'],
    queryFn: () => fetch('/api/v1/machines/stats/overview/').then(res => res.json()),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">Loading statistics...</div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-gray-500">No data available</div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">Overview of your investigation platform</p>
      </div>

      {/* Stats Grid - Investigation Platform */}
      <div>
        <h2 className="text-lg font-semibold text-gray-700 mb-3">Investigation Platform</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Entities"
            value={stats.total_entities}
            icon={<Database className="w-6 h-6" />}
            color="bg-blue-500"
          />
          <StatCard
            title="Relationships"
            value={stats.total_relationships}
            icon={<Link className="w-6 h-6" />}
            color="bg-green-500"
          />
          <StatCard
            title="Entity Types"
            value={stats.entity_types}
            icon={<Network className="w-6 h-6" />}
            color="bg-purple-500"
          />
          <StatCard
            title="Relationship Types"
            value={stats.relationship_types}
            icon={<Activity className="w-6 h-6" />}
            color="bg-orange-500"
          />
        </div>
      </div>

      {/* Machine Supervisors Summary */}
      {machineStats && (
        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-gray-700">Factory Operations</h2>
            <a href="/machines" className="text-sm text-blue-600 hover:text-blue-700">
              View All Machines →
            </a>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <MiniStatCard
              label="Total Machines"
              value={machineStats.total_machines}
              color="text-gray-900"
            />
            <MiniStatCard
              label="Running"
              value={machineStats.status_breakdown.running || 0}
              color="text-green-600"
            />
            <MiniStatCard
              label="Idle"
              value={machineStats.status_breakdown.idle || 0}
              color="text-blue-600"
            />
            <MiniStatCard
              label="Maintenance"
              value={machineStats.status_breakdown.maintenance || 0}
              color="text-yellow-600"
            />
            <MiniStatCard
              label="Avg Health"
              value={`${machineStats.avg_health.toFixed(1)}%`}
              color="text-purple-600"
            />
          </div>
        </div>
      )}

      {/* Entity Distribution Chart */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Entities by Type
        </h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={stats.entities_by_type}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="display_name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="count" fill="#3b82f6" name="Number of Entities" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <ActionCard
            title="Create Entity"
            description="Add a new entity to your investigation"
            href="/entities/new"
          />
          <ActionCard
            title="Explore Graph"
            description="Visualize entity relationships"
            href="/graph"
          />
          <ActionCard
            title="Manage Schema"
            description="Define entity and relationship types"
            href="/schema"
          />
        </div>
      </div>
    </div>
  );
};

interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: string;
}

const StatCard = ({ title, value, icon, color }: StatCardProps) => {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        <div className={`${color} text-white p-3 rounded-lg`}>
          {icon}
        </div>
      </div>
    </div>
  );
};

interface ActionCardProps {
  title: string;
  description: string;
  href: string;
}

const ActionCard = ({ title, description, href }: ActionCardProps) => {
  return (
    <a
      href={href}
      className="block p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-md transition-all"
    >
      <h3 className="font-semibold text-gray-900">{title}</h3>
      <p className="text-sm text-gray-500 mt-1">{description}</p>
    </a>
  );
};

interface MiniStatCardProps {
  label: string;
  value: string | number;
  color: string;
}

const MiniStatCard = ({ label, value, color }: MiniStatCardProps) => {
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">{label}</p>
      <p className={`text-2xl font-bold mt-2 ${color}`}>{value}</p>
    </div>
  );
};

export default Dashboard;
