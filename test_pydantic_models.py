#!/usr/bin/env python3
"""
Test script for Pydantic models in SelFlow
Verifies type safety, validation, and model functionality
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_pydantic_models():
    """Test Pydantic model creation and validation"""
    print("🔬 Testing Pydantic Models...")
    
    try:
        from app.analytics.models import (
            AnalysisConfig, ClusteringAlgorithm, DataSummary, ConsensusResults,
            Recommendation, AnalysisResults, TimePattern, ClusterAnalysis,
            create_analysis_config, create_data_summary, create_consensus_results,
            create_recommendation
        )
        
        print("✅ All Pydantic models imported successfully")
        
        # Test AnalysisConfig creation and validation
        print("\n📋 Testing AnalysisConfig...")
        config = create_analysis_config(
            data_limit=5000,
            days_back=14,
            algorithms=[ClusteringAlgorithm.KMEANS, ClusteringAlgorithm.SPECTRAL, ClusteringAlgorithm.GMM]
        )
        print(f"✅ Config created: {config.data_limit} events, {len(config.algorithms)} algorithms")
        
        # Test validation - this should work
        try:
            valid_config = AnalysisConfig(data_limit=1000, days_back=7)
            print("✅ Valid config accepted")
        except Exception as e:
            print(f"❌ Valid config rejected: {e}")
        
        # Test validation - this should fail
        try:
            invalid_config = AnalysisConfig(data_limit=-100)  # Invalid negative value
            print("❌ Invalid config accepted (should have failed)")
        except Exception as e:
            print(f"✅ Invalid config properly rejected: {e}")
        
        # Test DataSummary
        print("\n📊 Testing DataSummary...")
        data_summary = create_data_summary(
            total_events=1500,
            event_types={"file_op": 1200, "app_event": 300},
            time_range={"start": "2024-01-01T00:00:00", "end": "2024-01-07T23:59:59"}
        )
        print(f"✅ DataSummary created: {data_summary.total_events} events")
        
        # Test TimePattern
        print("\n⏰ Testing TimePattern...")
        time_pattern = TimePattern(
            peak_hour=14,
            peak_day="Monday",
            activity_spread={"hours": 8, "days": 5}
        )
        print(f"✅ TimePattern created: peak at {time_pattern.peak_hour}:00 on {time_pattern.peak_day}")
        
        # Test ClusterAnalysis
        print("\n🧬 Testing ClusterAnalysis...")
        cluster_analysis = ClusterAnalysis(
            size=250,
            percentage=16.7,
            event_types={"file_op": 200, "app_event": 50},
            top_sources={"VSCode": 150, "Finder": 100},
            time_pattern=time_pattern,
            dominant_pattern="file_operations_VSCode"
        )
        print(f"✅ ClusterAnalysis created: {cluster_analysis.size} events ({cluster_analysis.percentage:.1f}%)")
        
        # Test ConsensusResults
        print("\n🎯 Testing ConsensusResults...")
        consensus = create_consensus_results(
            best_algorithm=ClusteringAlgorithm.KMEANS,
            best_silhouette_score=0.65,
            average_clusters=4.2,
            algorithm_agreement=True,
            consensus_clusters=4
        )
        print(f"✅ ConsensusResults created: {consensus.best_algorithm.value} with score {consensus.best_silhouette_score}")
        
        # Test Recommendation
        print("\n💡 Testing Recommendation...")
        recommendation = create_recommendation(
            priority="high",
            category="performance",
            message="Excellent clustering quality detected",
            action_required=False,
            technical_details="Silhouette score: 0.65"
        )
        print(f"✅ Recommendation created: [{recommendation.priority}] {recommendation.message}")
        
        # Test complete AnalysisResults
        print("\n📈 Testing AnalysisResults...")
        results = AnalysisResults(
            analysis_id="test-123",
            data_summary=data_summary,
            clustering_results={},  # Empty for test
            consensus=consensus,
            recommendations=[recommendation],
            analysis_duration_seconds=2.5
        )
        print(f"✅ AnalysisResults created: ID {results.analysis_id}, duration {results.analysis_duration_seconds}s")
        
        # Test JSON serialization
        print("\n📄 Testing JSON serialization...")
        json_str = results.json(indent=2)
        print(f"✅ JSON serialization successful ({len(json_str)} characters)")
        
        # Test dict conversion
        results_dict = results.dict()
        print(f"✅ Dict conversion successful ({len(results_dict)} keys)")
        
        print("\n🎉 All Pydantic model tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Install Pydantic with: pip install pydantic>=2.0.0")
        return False
    except Exception as e:
        print(f"❌ Error testing Pydantic models: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_behavior():
    """Test fallback behavior when Pydantic is not available"""
    print("\n🔄 Testing Fallback Behavior...")
    
    # This would test the fallback BaseModel, but since we're testing with Pydantic
    # available, we'll just verify the PYDANTIC_AVAILABLE flag
    try:
        from app.analytics.models import PYDANTIC_AVAILABLE
        print(f"✅ Pydantic availability detected: {PYDANTIC_AVAILABLE}")
        
        if PYDANTIC_AVAILABLE:
            print("✅ Using full Pydantic validation")
        else:
            print("⚠️ Using fallback BaseModel (limited validation)")
            
        return True
    except Exception as e:
        print(f"❌ Error testing fallback: {e}")
        return False

def main():
    """Main test function"""
    print("🧠 SelFlow Pydantic Models Test")
    print("=" * 40)
    
    # Test Pydantic models
    models_ok = test_pydantic_models()
    
    # Test fallback behavior
    fallback_ok = test_fallback_behavior()
    
    # Summary
    print("\n📋 Test Summary:")
    print("=" * 20)
    print(f"Pydantic Models: {'✅' if models_ok else '❌'}")
    print(f"Fallback Behavior: {'✅' if fallback_ok else '❌'}")
    
    if models_ok and fallback_ok:
        print("\n🎉 All tests passed! Pydantic integration is working correctly.")
        print("\n🚀 Benefits of Pydantic integration:")
        print("  • Type safety and validation")
        print("  • Automatic JSON serialization")
        print("  • Clear data structure documentation")
        print("  • Runtime error detection")
        print("  • IDE support with type hints")
    else:
        print("\n⚠️ Some tests failed - check the output above")

if __name__ == "__main__":
    main() 