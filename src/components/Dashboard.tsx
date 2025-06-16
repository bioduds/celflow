import { useState } from "react";
import { AnalysisResults, SystemMetrics } from "../types/selflow";
import SystemOverview from "./SystemOverview";
import ClusteringResults from "./ClusteringResults";
import RecommendationsPanel from "./RecommendationsPanel";
import PatternEvolution from "./PatternEvolution";
import { RefreshCw, Zap, AlertCircle } from "lucide-react";

interface DashboardProps {
  analysisData: AnalysisResults | null;
  systemMetrics: SystemMetrics | null;
  onRefresh: () => void;
  onTriggerAnalysis: () => void;
  loading: boolean;
  error: string | null;
}

export default function Dashboard({
  analysisData,
  systemMetrics,
  onRefresh,
  onTriggerAnalysis,
  loading,
  error
}: DashboardProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'clustering' | 'patterns' | 'recommendations'>('overview');

  return (
    <div className="min-h-screen p-6">
      {/* Header */}
      <header className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-neural-900 mb-2">
              SelFlow <span className="text-primary-600">AI Analysis</span>
            </h1>
            <p className="text-neural-600">
              Real-time pattern recognition and agent optimization
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            {error && (
              <div className="flex items-center gap-2 px-4 py-2 bg-red-100 text-red-700 rounded-lg">
                <AlertCircle size={16} />
                <span className="text-sm">Connection Error</span>
              </div>
            )}
            
            <button
              onClick={onRefresh}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 transition-colors"
            >
              <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
              Refresh
            </button>
            
            <button
              onClick={onTriggerAnalysis}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-accent-600 text-white rounded-lg hover:bg-accent-700 disabled:opacity-50 transition-colors"
            >
              <Zap size={16} />
              New Analysis
            </button>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="mb-8">
        <div className="flex space-x-1 bg-white/50 backdrop-blur-sm rounded-lg p-1">
          {[
            { id: 'overview', label: 'System Overview' },
            { id: 'clustering', label: 'Clustering Results' },
            { id: 'patterns', label: 'Pattern Evolution' },
            { id: 'recommendations', label: 'Recommendations' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-6 py-3 rounded-md font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-white text-primary-700 shadow-sm'
                  : 'text-neural-600 hover:text-neural-900 hover:bg-white/50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="space-y-6">
        {activeTab === 'overview' && (
          <SystemOverview 
            systemMetrics={systemMetrics}
            dataSummary={analysisData?.data_summary}
            consensus={analysisData?.consensus}
          />
        )}
        
        {activeTab === 'clustering' && analysisData && (
          <ClusteringResults 
            clusteringResults={analysisData.clustering_results}
            consensus={analysisData.consensus}
          />
        )}
        
        {activeTab === 'patterns' && (
          <PatternEvolution 
            analysisData={analysisData}
          />
        )}
        
        {activeTab === 'recommendations' && analysisData && (
          <RecommendationsPanel 
            recommendations={analysisData.recommendations}
            analysisId={analysisData.analysis_id}
          />
        )}
      </main>

      {/* Status Bar */}
      <footer className="mt-12 pt-6 border-t border-neural-200">
        <div className="flex items-center justify-between text-sm text-neural-500">
          <div className="flex items-center gap-6">
            <span>
              Last Analysis: {analysisData?.timestamp ? 
                new Date(analysisData.timestamp).toLocaleString() : 
                'Never'
              }
            </span>
            {analysisData?.analysis_duration_seconds && (
              <span>
                Duration: {analysisData.analysis_duration_seconds.toFixed(1)}s
              </span>
            )}
          </div>
          
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${
              systemMetrics?.clustering_status === 'Active' ? 'bg-green-500' : 'bg-red-500'
            }`}></div>
            <span>
              {systemMetrics?.clustering_status || 'Unknown'} Status
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
} 