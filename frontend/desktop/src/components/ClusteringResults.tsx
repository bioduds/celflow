import { ClusteringResult, ConsensusResults, ClusteringAlgorithm } from "../types/celflow";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ScatterChart, Scatter } from "recharts";
import { Award, Target, TrendingUp, Layers } from "lucide-react";

interface ClusteringResultsProps {
  clusteringResults: Record<ClusteringAlgorithm, ClusteringResult>;
  consensus: ConsensusResults;
}

export default function ClusteringResults({ clusteringResults, consensus }: ClusteringResultsProps) {
  const algorithmData = Object.entries(clusteringResults).map(([algorithm, result]) => ({
    algorithm: algorithm.toUpperCase(),
    silhouette: result.silhouette_score,
    clusters: result.n_clusters,
    calinski: result.calinski_harabasz_score / 100, // Scale for visualization
    isBest: algorithm === consensus.best_algorithm
  }));

  const bestResult = consensus.best_algorithm ? clusteringResults[consensus.best_algorithm] : null;
  const clusterData = bestResult ? Object.entries(bestResult.cluster_analysis).map(([id, analysis]) => ({
    id: `Cluster ${id}`,
    size: analysis.size,
    percentage: analysis.percentage,
    pattern: analysis.dominant_pattern
  })) : [];

  return (
    <div className="space-y-6">
      {/* Consensus Summary */}
      <div className="glass-panel rounded-xl p-6">
        <h3 className="text-lg font-semibold text-neural-900 mb-4 flex items-center gap-2">
          <Award className="w-5 h-5" />
          Consensus Results
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">
              {consensus.best_algorithm?.toUpperCase() || 'N/A'}
            </div>
            <div className="text-sm text-neural-600">Best Algorithm</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-accent-600">
              {consensus.best_silhouette_score.toFixed(3)}
            </div>
            <div className="text-sm text-neural-600">Silhouette Score</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-neural-600">
              {consensus.consensus_clusters}
            </div>
            <div className="text-sm text-neural-600">Optimal Clusters</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">
              {((consensus.confidence_score || 0) * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-neural-600">Confidence</div>
          </div>
        </div>
      </div>

      {/* Algorithm Comparison */}
      <div className="glass-panel rounded-xl p-6">
        <h3 className="text-lg font-semibold text-neural-900 mb-4 flex items-center gap-2">
          <Target className="w-5 h-5" />
          Algorithm Performance Comparison
        </h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={algorithmData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="algorithm" />
              <YAxis />
              <Tooltip 
                formatter={(value: number, name: string) => [
                  name === 'silhouette' ? value.toFixed(3) : value.toFixed(0),
                  name === 'silhouette' ? 'Silhouette Score' : 
                  name === 'clusters' ? 'Clusters' : 'Calinski-Harabasz'
                ]}
              />
              <Bar dataKey="silhouette" fill="#0ea5e9" name="silhouette" />
              <Bar dataKey="clusters" fill="#d946ef" name="clusters" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {algorithmData.map((algo, index) => (
            <div 
              key={index} 
              className={`p-4 rounded-lg border-2 ${
                algo.isBest ? 'border-primary-300 bg-primary-50' : 'border-neural-200 bg-white'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-neural-900">{algo.algorithm}</span>
                {algo.isBest && <Award className="w-4 h-4 text-primary-600" />}
              </div>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-neural-600">Silhouette:</span>
                  <span className="font-medium">{algo.silhouette.toFixed(3)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neural-600">Clusters:</span>
                  <span className="font-medium">{algo.clusters}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cluster Analysis */}
      {bestResult && (
        <div className="glass-panel rounded-xl p-6">
          <h3 className="text-lg font-semibold text-neural-900 mb-4 flex items-center gap-2">
            <Layers className="w-5 h-5" />
            Detailed Cluster Analysis ({consensus.best_algorithm?.toUpperCase()})
          </h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Cluster Size Distribution */}
            <div>
              <h4 className="font-medium text-neural-800 mb-3">Cluster Size Distribution</h4>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={clusterData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="id" />
                    <YAxis />
                    <Tooltip 
                      formatter={(value: number) => [value.toLocaleString(), 'Events']}
                    />
                    <Bar dataKey="size" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Cluster Details */}
            <div>
              <h4 className="font-medium text-neural-800 mb-3">Cluster Characteristics</h4>
              <div className="space-y-4">
                {Object.entries(bestResult.cluster_analysis).map(([id, analysis]) => (
                  <div key={id} className="p-4 bg-neural-50 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-neural-900">Cluster {id}</span>
                      <span className="text-sm font-medium text-primary-600">
                        {analysis.percentage.toFixed(1)}%
                      </span>
                    </div>
                    <div className="text-sm text-neural-600 mb-2">
                      {analysis.dominant_pattern}
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-xs">
                      <div>
                        <span className="text-neural-500">Size:</span>
                        <span className="ml-1 font-medium">{analysis.size.toLocaleString()}</span>
                      </div>
                      <div>
                        <span className="text-neural-500">Peak:</span>
                        <span className="ml-1 font-medium">
                          {analysis.time_pattern.peak_hour}:00 {analysis.time_pattern.peak_day}
                        </span>
                      </div>
                    </div>
                    <div className="mt-2">
                      <div className="text-xs text-neural-500 mb-1">Top Sources:</div>
                      <div className="flex flex-wrap gap-1">
                        {Object.entries(analysis.top_sources).slice(0, 3).map(([source, count]) => (
                          <span 
                            key={source}
                            className="px-2 py-1 bg-white text-xs rounded text-neural-700"
                          >
                            {source}: {count.toLocaleString()}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Algorithm Details */}
      <div className="glass-panel rounded-xl p-6">
        <h3 className="text-lg font-semibold text-neural-900 mb-4 flex items-center gap-2">
          <TrendingUp className="w-5 h-5" />
          Algorithm Configuration
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.entries(clusteringResults).map(([algorithm, result]) => (
            <div 
              key={algorithm}
              className={`p-4 rounded-lg border ${
                algorithm === consensus.best_algorithm 
                  ? 'border-primary-300 bg-primary-50' 
                  : 'border-neural-200 bg-white'
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-neural-900">{algorithm.toUpperCase()}</h4>
                {algorithm === consensus.best_algorithm && (
                  <span className="px-2 py-1 bg-primary-100 text-primary-700 text-xs rounded-full">
                    Best
                  </span>
                )}
              </div>
              <div className="text-sm text-neural-600 mb-3">
                {result.description}
              </div>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-neural-500">Clusters:</span>
                  <span className="font-medium">{result.n_clusters}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neural-500">Silhouette:</span>
                  <span className="font-medium">{result.silhouette_score.toFixed(3)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neural-500">Calinski-Harabasz:</span>
                  <span className="font-medium">{result.calinski_harabasz_score.toFixed(1)}</span>
                </div>
                {result.algorithm_params.random_state && (
                  <div className="flex justify-between">
                    <span className="text-neural-500">Random State:</span>
                    <span className="font-medium">{result.algorithm_params.random_state}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 