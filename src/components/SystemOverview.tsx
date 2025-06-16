import { SystemMetrics, DataSummary, ConsensusResults } from "../types/selflow";
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";
import { Activity, Database, Cpu, MemoryStick, Users, TrendingUp } from "lucide-react";

interface SystemOverviewProps {
  systemMetrics: SystemMetrics | null;
  dataSummary: DataSummary | undefined;
  consensus: ConsensusResults | undefined;
}

export default function SystemOverview({ systemMetrics, dataSummary, consensus }: SystemOverviewProps) {
  const eventTypeData = dataSummary ? Object.entries(dataSummary.event_types).map(([name, value]) => ({
    name: name.replace('_', ' ').toUpperCase(),
    value,
    color: name === 'file_op' ? '#0ea5e9' : '#d946ef'
  })) : [];

  const agentData = [
    { name: 'GeneralFileAgent', size: 95.2, params: '1M', color: '#0ea5e9' },
    { name: 'SystemAgent', size: 4.8, params: '200K', color: '#d946ef' }
  ];

  return (
    <div className="space-y-6">
      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          icon={<Activity className="w-6 h-6" />}
          title="Events Today"
          value={systemMetrics?.events_today?.toLocaleString() || '0'}
          subtitle="Real-time monitoring"
          color="primary"
        />
        
        <MetricCard
          icon={<Users className="w-6 h-6" />}
          title="Active Agents"
          value={systemMetrics?.active_agents?.toString() || '0'}
          subtitle={systemMetrics?.clustering_status || 'Unknown'}
          color="accent"
        />
        
        <MetricCard
          icon={<MemoryStick className="w-6 h-6" />}
          title="Memory Usage"
          value={`${systemMetrics?.memory_usage?.toFixed(1) || '0'}MB`}
          subtitle="System resources"
          color="neural"
        />
        
        <MetricCard
          icon={<TrendingUp className="w-6 h-6" />}
          title="Confidence Score"
          value={`${((consensus?.confidence_score || 0) * 100).toFixed(1)}%`}
          subtitle="Analysis quality"
          color="primary"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Event Distribution */}
        <div className="glass-panel rounded-xl p-6">
          <h3 className="text-lg font-semibold text-neural-900 mb-4 flex items-center gap-2">
            <Database className="w-5 h-5" />
            Event Distribution
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={eventTypeData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {eventTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value: number) => [value.toLocaleString(), 'Events']}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-2">
            {eventTypeData.map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-sm text-neural-600">{item.name}</span>
                </div>
                <span className="text-sm font-medium text-neural-900">
                  {item.value.toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Agent Architecture */}
        <div className="glass-panel rounded-xl p-6">
          <h3 className="text-lg font-semibold text-neural-900 mb-4 flex items-center gap-2">
            <Cpu className="w-5 h-5" />
            Recommended Agent Architecture
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={agentData} layout="horizontal">
                <XAxis type="number" domain={[0, 100]} />
                <YAxis dataKey="name" type="category" width={120} />
                <Tooltip 
                  formatter={(value: number) => [`${value}%`, 'Data Coverage']}
                />
                <Bar dataKey="size" fill="#0ea5e9" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-3">
            {agentData.map((agent, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-neural-50 rounded-lg">
                <div>
                  <div className="font-medium text-neural-900">{agent.name}</div>
                  <div className="text-sm text-neural-600">{agent.params} parameters</div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-neural-900">{agent.size}%</div>
                  <div className="text-sm text-neural-600">coverage</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Data Quality Summary */}
      {dataSummary && (
        <div className="glass-panel rounded-xl p-6">
          <h3 className="text-lg font-semibold text-neural-900 mb-4">Data Quality Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary-600">
                {dataSummary.total_events.toLocaleString()}
              </div>
              <div className="text-sm text-neural-600">Total Events Analyzed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-accent-600">
                {((dataSummary.data_quality_score || 0) * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-neural-600">Data Quality Score</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-neural-600">
                {Math.ceil((new Date().getTime() - new Date(dataSummary.time_range.start).getTime()) / (1000 * 60 * 60 * 24))}
              </div>
              <div className="text-sm text-neural-600">Days of Data</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

interface MetricCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  subtitle: string;
  color: 'primary' | 'accent' | 'neural';
}

function MetricCard({ icon, title, value, subtitle, color }: MetricCardProps) {
  const colorClasses = {
    primary: 'text-primary-600 bg-primary-50',
    accent: 'text-accent-600 bg-accent-50',
    neural: 'text-neural-600 bg-neural-50'
  };

  return (
    <div className="glass-panel rounded-xl p-6">
      <div className={`inline-flex p-3 rounded-lg ${colorClasses[color]} mb-4`}>
        {icon}
      </div>
      <div className="space-y-1">
        <p className="text-sm font-medium text-neural-600">{title}</p>
        <p className="text-2xl font-bold text-neural-900">{value}</p>
        <p className="text-xs text-neural-500">{subtitle}</p>
      </div>
    </div>
  );
} 