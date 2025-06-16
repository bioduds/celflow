#!/usr/bin/env python3
"""
Test script for Enhanced Analysis Tray
Run this to test the clustering analysis functionality
"""

import os
import sys
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_clustering_engine():
    """Test the clustering engine independently"""
    print("🔬 Testing Clustering Engine...")
    
    try:
        from app.analytics.advanced_clustering_engine import AdvancedClusteringEngine
        from app.analytics.models import create_analysis_config, ClusteringAlgorithm
        
        # Initialize engine with custom config
        config = create_analysis_config(
            data_limit=100,  # Small test
            algorithms=[ClusteringAlgorithm.KMEANS, ClusteringAlgorithm.SPECTRAL]
        )
        engine = AdvancedClusteringEngine(config=config)
        print("✅ Clustering engine initialized with Pydantic config")
        
        # Test data loading
        df = engine.load_events_data()  # Uses config defaults
        print(f"✅ Loaded {len(df)} events for testing")
        
        if len(df) > 10:  # Only run full analysis if we have some data
            # Test clustering analysis
            print("🔍 Running test clustering analysis...")
            results = engine.perform_clustering_analysis(force_new=True)
            
            if results.error:
                print(f"❌ Analysis error: {results.error}")
            else:
                print("✅ Clustering analysis completed!")
                print(f"📊 Summary: {engine.get_summary_for_tray()}")
                
                # Show detailed summary
                detailed = engine.get_detailed_summary()
                print("\n" + detailed)
                
                # Test Pydantic model features
                print(f"\n🔬 Analysis ID: {results.analysis_id}")
                print(f"⏱️ Duration: {results.analysis_duration_seconds:.2f}s")
                print(f"🎯 Best Algorithm: {results.consensus.best_algorithm.value if results.consensus.best_algorithm else 'None'}")
                
                # Test JSON export
                if engine.export_results_json("test_results.json"):
                    print("✅ Results exported to test_results.json")
        else:
            print("⚠️ Not enough data for full clustering test")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure required packages are installed:")
        print("pip install scikit-learn pandas numpy")
        return False
    except Exception as e:
        print(f"❌ Error testing clustering engine: {e}")
        return False
    
    return True

def test_tray_interface():
    """Test the tray interface (macOS only)"""
    print("\n🖥️ Testing Tray Interface...")
    
    try:
        import rumps
        print("✅ rumps available for tray interface")
        
        # Test creating the enhanced tray
        from app.system.enhanced_analysis_tray import create_enhanced_analysis_tray
        
        app = create_enhanced_analysis_tray()
        if app:
            print("✅ Enhanced analysis tray created successfully")
            print("🚀 You can now run the tray with: python -c 'from app.system.enhanced_analysis_tray import create_enhanced_analysis_tray; app = create_enhanced_analysis_tray(); app.run()'")
            return True
        else:
            print("❌ Failed to create tray app")
            return False
            
    except ImportError:
        print("❌ rumps not available - this is normal on non-macOS systems")
        print("To install rumps on macOS: pip install rumps")
        return False
    except Exception as e:
        print(f"❌ Error testing tray interface: {e}")
        return False

def check_data_availability():
    """Check if we have data to analyze"""
    print("📊 Checking Data Availability...")
    
    db_path = Path("data/events.db")
    if not db_path.exists():
        print("❌ No events database found at data/events.db")
        print("Make sure SelFlow has been running to collect data")
        return False
    
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM events")
        total_events = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM events WHERE timestamp > ?", 
                      (time.time() - 7*24*3600,))  # Last 7 days
        recent_events = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Database found with {total_events:,} total events")
        print(f"📅 Recent events (7 days): {recent_events:,}")
        
        if recent_events < 10:
            print("⚠️ Very little recent data - clustering may not be meaningful")
        elif recent_events < 100:
            print("⚠️ Limited recent data - clustering results may be basic")
        else:
            print("✅ Sufficient data for meaningful clustering analysis")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def main():
    """Main test function"""
    print("🧠 SelFlow Enhanced Analysis Tray Test")
    print("=" * 50)
    
    # Check system requirements
    print("🔧 Checking Requirements...")
    
    # Check data availability
    data_ok = check_data_availability()
    
    # Test clustering engine
    clustering_ok = test_clustering_engine()
    
    # Test tray interface
    tray_ok = test_tray_interface()
    
    # Summary
    print("\n📋 Test Summary:")
    print("=" * 30)
    print(f"Data Available: {'✅' if data_ok else '❌'}")
    print(f"Clustering Engine: {'✅' if clustering_ok else '❌'}")
    print(f"Tray Interface: {'✅' if tray_ok else '❌'}")
    
    if data_ok and clustering_ok:
        print("\n🎉 Core functionality working!")
        print("You can now run clustering analysis from the tray")
        
        if tray_ok:
            print("\n🚀 To start the enhanced tray:")
            print("python -m app.system.enhanced_analysis_tray")
        else:
            print("\n💻 To run analysis directly:")
            print("python -c 'from app.analytics.advanced_clustering_engine import AdvancedClusteringEngine; engine = AdvancedClusteringEngine(); results = engine.perform_clustering_analysis(); print(engine.get_detailed_summary())'")
    else:
        print("\n⚠️ Some components need attention before full functionality")

if __name__ == "__main__":
    main() 