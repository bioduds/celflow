// TypeScript types matching our Pydantic models

export enum ClusteringAlgorithm {
  KMEANS = "kmeans",
  SPECTRAL = "spectral",
  GMM = "gmm",
  HDBSCAN = "hdbscan"
}

export enum EventType {
  FILE_OP = "file_op",
  APP_EVENT = "app_event",
  SYSTEM_EVENT = "system_event",
  USER_ACTION = "user_action"
}

export interface TimePattern {
  peak_hour?: number;
  peak_day?: string;
  activity_spread: Record<string, number>;
}

export interface ClusterAnalysis {
  size: number;
  percentage: number;
  event_types: Record<string, number>;
  top_sources: Record<string, number>;
  time_pattern: TimePattern;
  dominant_pattern: string;
}

export interface AlgorithmParams {
  n_clusters?: number;
  min_cluster_size?: number;
  min_samples?: number;
  random_state?: number;
  affinity?: string;
  n_components?: number;
  n_init?: number;
}

export interface ClusteringResult {
  algorithm: ClusteringAlgorithm;
  n_clusters: number;
  silhouette_score: number;
  calinski_harabasz_score: number;
  algorithm_params: AlgorithmParams;
  description: string;
  cluster_analysis: Record<string, ClusterAnalysis>;
  labels: number[];
  error?: string;
}

export interface DataSummary {
  total_events: number;
  event_types: Record<string, number>;
  time_range: Record<string, string>;
  data_quality_score?: number;
}

export interface ConsensusResults {
  best_algorithm?: ClusteringAlgorithm;
  best_silhouette_score: number;
  average_clusters: number;
  algorithm_agreement: boolean;
  consensus_clusters: number;
  confidence_score?: number;
}

export interface Recommendation {
  priority: string;
  category: string;
  message: string;
  action_required: boolean;
  technical_details?: string;
}

export interface AnalysisResults {
  timestamp: string;
  analysis_id: string;
  data_summary: DataSummary;
  clustering_results: Record<ClusteringAlgorithm, ClusteringResult>;
  consensus: ConsensusResults;
  recommendations: Recommendation[];
  analysis_duration_seconds?: number;
  error?: string;
}

export interface AnalysisConfig {
  data_limit: number;
  days_back: number;
  algorithms: ClusteringAlgorithm[];
  cache_duration_hours: number;
  min_events_for_analysis: number;
  feature_scaling: boolean;
}

// UI-specific types
export interface SystemMetrics {
  events_today: number;
  active_agents: number;
  clustering_status: string;
  memory_usage: number;
  cpu_usage?: number;
  last_analysis?: string;
}

export interface ChartDataPoint {
  name: string;
  value: number;
  color?: string;
}

export interface PatternEvolutionPoint {
  timestamp: string;
  pattern_count: number;
  confidence: number;
  algorithm: ClusteringAlgorithm;
} 