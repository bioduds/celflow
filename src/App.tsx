import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import Dashboard from "./components/Dashboard";
import { AnalysisResults, SystemMetrics } from "./types/selflow";

function App() {
  const [analysisData, setAnalysisData] = useState<AnalysisResults | null>(null);
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Load initial data
    loadAnalysisData();
    loadSystemMetrics();
    
    // Set up periodic updates
    const interval = setInterval(() => {
      loadSystemMetrics();
    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const loadAnalysisData = async () => {
    try {
      setLoading(true);
      // This will call our Rust backend which will interface with Python
      const data = await invoke<AnalysisResults>("get_latest_analysis");
      setAnalysisData(data);
      setError(null);
    } catch (err) {
      console.error("Failed to load analysis data:", err);
      setError(err as string);
      // For development, use mock data
      setAnalysisData(getMockAnalysisData());
    } finally {
      setLoading(false);
    }
  };

  const loadSystemMetrics = async () => {
    try {
      const metrics = await invoke<SystemMetrics>("get_system_metrics");
      setSystemMetrics(metrics);
    } catch (err) {
      console.error("Failed to load system metrics:", err);
      // For development, use mock data
      setSystemMetrics(getMockSystemMetrics());
    }
  };

  const triggerNewAnalysis = async () => {
    try {
      setLoading(true);
      await invoke("trigger_analysis");
      // Reload data after analysis
      setTimeout(() => {
        loadAnalysisData();
      }, 2000);
    } catch (err) {
      console.error("Failed to trigger analysis:", err);
      setError(err as string);
    }
  };

  if (loading && !analysisData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-neural-50 to-primary-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin-slow w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-neural-700">Loading SelFlow Analysis...</h2>
          <p className="text-neural-500 mt-2">Connecting to AI pattern engine</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-neural-50 to-primary-50">
      <Dashboard
        analysisData={analysisData}
        systemMetrics={systemMetrics}
        onRefresh={loadAnalysisData}
        onTriggerAnalysis={triggerNewAnalysis}
        loading={loading}
        error={error}
      />
    </div>
  );
}

// Mock data for development
function getMockAnalysisData(): AnalysisResults {
  return {
    timestamp: new Date().toISOString(),
    analysis_id: "mock-analysis-001",
    data_summary: {
      total_events: 130542,
      event_types: {
        "file_op": 129742,
        "app_event": 800
      },
      time_range: {
        "start": "2024-06-01T00:00:00Z",
        "end": "2024-06-16T15:00:00Z"
      },
      data_quality_score: 0.94
    },
    clustering_results: {
      "kmeans": {
        algorithm: "kmeans" as const,
        n_clusters: 2,
        silhouette_score: 0.85,
        calinski_harabasz_score: 1250.5,
        algorithm_params: {
          n_clusters: 2,
          random_state: 42,
          n_init: 10
        },
        description: "GeneralFileAgent (95.2%) and SystemAgent (4.8%)",
        cluster_analysis: {
          "0": {
            size: 124316,
            percentage: 95.2,
            event_types: { "file_op": 124316 },
            top_sources: { "VS Code": 45000, "Browser Cache": 35000, "System Files": 44316 },
            time_pattern: {
              peak_hour: 14,
              peak_day: "Tuesday",
              activity_spread: { "morning": 0.3, "afternoon": 0.5, "evening": 0.2 }
            },
            dominant_pattern: "Cache and state file operations"
          },
          "1": {
            size: 6226,
            percentage: 4.8,
            event_types: { "file_op": 5426, "app_event": 800 },
            top_sources: { "Temp Files": 3000, "Log Files": 2426, "System Events": 800 },
            time_pattern: {
              peak_hour: 10,
              peak_day: "Monday",
              activity_spread: { "morning": 0.4, "afternoon": 0.4, "evening": 0.2 }
            },
            dominant_pattern: "Temporary file management"
          }
        },
        labels: []
      }
    },
    consensus: {
      best_algorithm: "kmeans" as const,
      best_silhouette_score: 0.85,
      average_clusters: 2,
      algorithm_agreement: true,
      consensus_clusters: 2,
      confidence_score: 0.92
    },
    recommendations: [
      {
        priority: "HIGH",
        category: "Architecture",
        message: "Implement GeneralFileAgent (1M params) for 95.2% of file operations",
        action_required: true,
        technical_details: "Focus on cache/state file handling with optimized parameters"
      },
      {
        priority: "MEDIUM",
        category: "Optimization",
        message: "Deploy SystemAgent (200K params) for temporary file management",
        action_required: true,
        technical_details: "Handle 4.8% of operations with specialized temp file logic"
      }
    ],
    analysis_duration_seconds: 12.5
  };
}

function getMockSystemMetrics(): SystemMetrics {
  return {
    events_today: 8542,
    active_agents: 2,
    clustering_status: "Active",
    memory_usage: 245.6,
    cpu_usage: 12.3,
    last_analysis: "2 minutes ago"
  };
}

export default App; 