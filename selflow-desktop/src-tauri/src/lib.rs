use std::process::Command;
use serde::{Deserialize, Serialize};
use tauri::State;
use std::sync::Mutex;

#[derive(Debug, Serialize, Deserialize)]
struct AnalysisResults {
    timestamp: String,
    analysis_id: String,
    data_summary: serde_json::Value,
    clustering_results: serde_json::Value,
    consensus: serde_json::Value,
    recommendations: Vec<serde_json::Value>,
    analysis_duration_seconds: Option<f64>,
    error: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct SystemMetrics {
    events_today: u32,
    active_agents: u32,
    clustering_status: String,
    memory_usage: f64,
    cpu_usage: Option<f64>,
    last_analysis: Option<String>,
}

struct AppState {
    python_path: Mutex<String>,
}

#[tauri::command]
async fn get_latest_analysis(state: State<'_, AppState>) -> Result<AnalysisResults, String> {
    let python_path = state.python_path.lock().unwrap();
    
    // Execute Python script to get latest analysis
    let output = Command::new(&*python_path)
        .arg("app/analytics/advanced_clustering_engine.py")
        .arg("--export-json")
        .current_dir("../")
        .output()
        .map_err(|e| format!("Failed to execute Python script: {}", e))?;

    if !output.status.success() {
        return Err(format!("Python script failed: {}", String::from_utf8_lossy(&output.stderr)));
    }

    let json_str = String::from_utf8_lossy(&output.stdout);
    serde_json::from_str(&json_str)
        .map_err(|e| format!("Failed to parse JSON: {}", e))
}

#[tauri::command]
async fn get_system_metrics() -> Result<SystemMetrics, String> {
    // Mock system metrics for now - in production this would query actual system stats
    Ok(SystemMetrics {
        events_today: 8542,
        active_agents: 2,
        clustering_status: "Active".to_string(),
        memory_usage: 245.6,
        cpu_usage: Some(12.3),
        last_analysis: Some("2 minutes ago".to_string()),
    })
}

#[tauri::command]
async fn trigger_analysis(state: State<'_, AppState>) -> Result<String, String> {
    let python_path = state.python_path.lock().unwrap();
    
    // Execute Python script to trigger new analysis
    let output = Command::new(&*python_path)
        .arg("app/analytics/advanced_clustering_engine.py")
        .arg("--force-analysis")
        .current_dir("../")
        .output()
        .map_err(|e| format!("Failed to execute Python script: {}", e))?;

    if !output.status.success() {
        return Err(format!("Analysis failed: {}", String::from_utf8_lossy(&output.stderr)));
    }

    Ok("Analysis triggered successfully".to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // Detect Python path
    let python_path = detect_python_path();
    
    tauri::Builder::default()
        .manage(AppState {
            python_path: Mutex::new(python_path),
        })
        .invoke_handler(tauri::generate_handler![
            get_latest_analysis,
            get_system_metrics,
            trigger_analysis
        ])
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

fn detect_python_path() -> String {
    // Try different Python paths
    let candidates = vec![
        "python3",
        "python",
        "./selflow_env/bin/python",
        "./selflow_env/Scripts/python.exe",
    ];
    
    for candidate in candidates {
        if let Ok(output) = Command::new(candidate).arg("--version").output() {
            if output.status.success() {
                return candidate.to_string();
            }
        }
    }
    
    // Default fallback
    "python3".to_string()
}
