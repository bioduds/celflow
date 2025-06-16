#!/usr/bin/env python3
"""
Test PatternValidator - Phase 3 Advanced Capabilities

This test validates the PatternValidator agent functionality including:
- Pattern classification validation
- Cross-agent validation
- System coherence auditing
- Conflict resolution
"""

import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_pattern_validator():
    """Test PatternValidator functionality"""

    print("🔍 TESTING PATTERN VALIDATOR - Phase 3 Advanced Capabilities")
    print("=" * 70)

    try:
        # Import required modules
        from app.ai.ollama_client import OllamaClient
        from app.ai.pattern_validator import (
            PatternValidator,
            PatternClassification,
        )

        # Initialize Ollama client
        print("\n1. 🤖 Initializing Ollama Client...")
        ollama_config = {
            "model_name": "gemma3:4b",
            "base_url": "http://localhost:11434",
            "timeout": 30,
        }

        ollama_client = OllamaClient(ollama_config)
        await ollama_client.start()

        # Test Ollama connection
        health = ollama_client.get_health_status()
        if not health.get("is_healthy", False):
            raise Exception("Ollama client not healthy")

        print(f"✅ Ollama client initialized: {health}")

        # Initialize PatternValidator
        print("\n2. 🔍 Initializing PatternValidator...")
        pattern_validator = PatternValidator(ollama_client)

        print("✅ PatternValidator initialized successfully")

        # Test 1: Single Pattern Validation
        print("\n3. 🎯 Testing Single Pattern Validation...")

        test_pattern = PatternClassification(
            pattern_id="test_pattern_001",
            category="PRODUCTIVITY",
            subcategory="task_management",
            confidence=0.85,
            source_agent="test_agent",
            timestamp=datetime.now(),
            metadata={"test": True},
        )

        validation_result = await pattern_validator.validate_single_pattern(
            test_pattern
        )

        print(f"✅ Single pattern validation completed:")
        print(f"   - Coherent: {validation_result.is_coherent}")
        print(f"   - Consistency Score: {validation_result.consistency_score:.2f}")
        print(f"   - Quality Score: {validation_result.quality_score:.2f}")
        print(f"   - Conflicts: {len(validation_result.conflicts_detected)}")
        print(f"   - Recommendations: {len(validation_result.recommendations)}")

        # Test 2: Cross-Agent Validation
        print("\n4. 🎭 Testing Cross-Agent Validation...")

        # Create multiple classifications for the same pattern from different agents
        classifications = [
            PatternClassification(
                pattern_id="shared_pattern_001",
                category="COMMUNICATION",
                subcategory="email_management",
                confidence=0.90,
                source_agent="agent_1",
                timestamp=datetime.now(),
            ),
            PatternClassification(
                pattern_id="shared_pattern_001",
                category="COMMUNICATION",
                subcategory="message_handling",
                confidence=0.85,
                source_agent="agent_2",
                timestamp=datetime.now(),
            ),
            PatternClassification(
                pattern_id="shared_pattern_001",
                category="PRODUCTIVITY",  # Different category - should create conflict
                subcategory="workflow_optimization",
                confidence=0.80,
                source_agent="agent_3",
                timestamp=datetime.now(),
            ),
        ]

        cross_validation_result = await pattern_validator.cross_validate_agents(
            "shared_pattern_001", classifications
        )

        print(f"✅ Cross-agent validation completed:")
        print(f"   - Pattern ID: {cross_validation_result['pattern_id']}")
        print(f"   - Agent Count: {cross_validation_result['agent_count']}")
        print(
            f"   - Consistency Score: {cross_validation_result['consistency_score']:.2f}"
        )
        print(f"   - Conflicts: {cross_validation_result['conflicts']}")
        print(
            f"   - Recommended Classification: {cross_validation_result['recommended_classification']}"
        )
        print(
            f"   - Actions Required: {len(cross_validation_result['actions_required'])}"
        )

        # Test 3: System Audit
        print("\n5. 🔍 Testing System Coherence Audit...")

        # Add some patterns to the registry first
        test_patterns = [
            PatternClassification(
                pattern_id="audit_pattern_001",
                category="SYSTEM",
                subcategory="maintenance",
                confidence=0.95,
                source_agent="system_agent",
                timestamp=datetime.now(),
            ),
            PatternClassification(
                pattern_id="audit_pattern_002",
                category="LEARNING",
                subcategory="skill_development",
                confidence=0.88,
                source_agent="learning_agent",
                timestamp=datetime.now(),
            ),
            PatternClassification(
                pattern_id="audit_pattern_003",
                category="CREATIVE",
                subcategory="content_creation",
                confidence=0.92,
                source_agent="creative_agent",
                timestamp=datetime.now(),
            ),
        ]

        # Add patterns to validator registry
        for pattern in test_patterns:
            pattern_validator.pattern_registry[pattern.pattern_id] = pattern

        audit_result = await pattern_validator.system_audit()

        print(f"✅ System audit completed:")
        print(f"   - Audit ID: {audit_result['audit_id']}")
        print(f"   - Total Patterns: {audit_result['total_patterns']}")
        print(f"   - System Health: {audit_result['system_health']}")
        print(f"   - Coherence Metrics: {audit_result['coherence_metrics']}")
        print(f"   - Critical Actions: {len(audit_result['critical_actions'])}")
        print(f"   - Recommendations: {audit_result['recommendations']}")

        # Test 4: Conflict Resolution
        print("\n6. ⚖️ Testing Conflict Resolution...")

        # Create a conflict scenario
        conflict_pattern_id = "conflict_pattern_001"
        pattern_validator.conflict_registry[conflict_pattern_id] = [
            "conflicting_classification_1",
            "conflicting_classification_2",
        ]

        # Add conflicting patterns to registry
        pattern_validator.pattern_registry["conflicting_classification_1"] = (
            PatternClassification(
                pattern_id="conflicting_classification_1",
                category="HEALTH",
                subcategory="fitness_tracking",
                confidence=0.85,
                source_agent="health_agent",
                timestamp=datetime.now(),
            )
        )

        pattern_validator.pattern_registry["conflicting_classification_2"] = (
            PatternClassification(
                pattern_id="conflicting_classification_2",
                category="PRODUCTIVITY",  # Different category
                subcategory="habit_tracking",
                confidence=0.80,
                source_agent="productivity_agent",
                timestamp=datetime.now(),
            )
        )

        conflict_resolution_result = await pattern_validator.resolve_conflicts(
            conflict_pattern_id
        )

        print(f"✅ Conflict resolution completed:")
        print(f"   - Pattern ID: {conflict_resolution_result['pattern_id']}")
        print(
            f"   - Conflicts Resolved: {conflict_resolution_result['conflicts_resolved']}"
        )
        print(
            f"   - Final Classification: {conflict_resolution_result['final_classification']}"
        )
        print(
            f"   - Resolution Actions: {len(conflict_resolution_result['resolution_actions'])}"
        )

        # Test 5: Validation Metrics
        print("\n7. 📊 Testing Validation Metrics...")

        metrics = pattern_validator.get_validation_metrics()

        print(f"✅ Validation metrics retrieved:")
        print(f"   - Validations Performed: {metrics['validations_performed']}")
        print(f"   - Conflicts Resolved: {metrics['conflicts_resolved']}")
        print(f"   - Pattern Registry Size: {metrics['pattern_registry_size']}")
        print(f"   - Active Conflicts: {metrics['active_conflicts']}")
        print(
            f"   - Average Consistency Score: {metrics['average_consistency_score']:.2f}"
        )
        print(f"   - Average Quality Score: {metrics['average_quality_score']:.2f}")

        # Test 6: System Health Status
        print("\n8. 🏥 Testing System Health Status...")

        health_status = pattern_validator.get_system_health()

        print(f"✅ System health status retrieved:")
        print(f"   - Status: {health_status['status']}")
        print(
            f"   - Consistency Score: {health_status.get('consistency_score', 'N/A')}"
        )
        print(f"   - Quality Score: {health_status.get('quality_score', 'N/A')}")
        print(f"   - Conflict Count: {health_status.get('conflict_count', 'N/A')}")

        # Test Summary
        print("\n" + "=" * 70)
        print("🎉 PATTERN VALIDATOR TEST SUMMARY")
        print("=" * 70)

        test_results = {
            "single_pattern_validation": validation_result.is_coherent,
            "cross_agent_validation": cross_validation_result["consistency_score"] > 0,
            "system_audit": audit_result["system_health"] in ["GOOD", "EXCELLENT"],
            "conflict_resolution": "pattern_id" in conflict_resolution_result,
            "metrics_retrieval": metrics["validations_performed"] > 0,
            "health_status": health_status["status"] != "CRITICAL",
        }

        passed_tests = sum(test_results.values())
        total_tests = len(test_results)

        print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   - {test_name}: {status}")

        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! PatternValidator is fully operational!")
            print("🚀 Phase 3 Advanced Capabilities: PatternValidator ✅ COMPLETE")
        else:
            print(
                f"\n⚠️  {total_tests - passed_tests} tests failed. Review implementation."
            )

        # Cleanup
        await ollama_client.close()

        return passed_tests == total_tests

    except Exception as e:
        logger.error(f"❌ Test failed with error: {str(e)}")
        print(f"\n❌ PATTERN VALIDATOR TEST FAILED: {str(e)}")
        return False


async def main():
    """Main test execution"""
    print("🔍 Starting PatternValidator Test Suite...")

    success = await test_pattern_validator()

    if success:
        print("\n🎉 PatternValidator test completed successfully!")
        exit(0)
    else:
        print("\n❌ PatternValidator test failed!")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
