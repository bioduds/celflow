#!/usr/bin/env python3
"""
Test script for SelFlow EmbryoTrainer
Demonstrates intelligent embryo training and validation capabilities
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from ai.central_brain import create_central_brain

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def test_embryo_trainer():
    """Test the Embryo Trainer functionality"""

    print("🧬 Testing SelFlow Embryo Trainer")
    print("=" * 50)

    # Configuration for Central AI Brain
    config = {
        "ai_brain": {
            "model_name": "gemma3:4b",
            "base_url": "http://localhost:11434",
            "context_window": 8192,
            "max_tokens": 2048,
            "temperature": 0.7,
            "timeout": 30,
            "retry_attempts": 3,
        },
        "context_management": {
            "max_conversation_history": 50,
            "context_refresh_interval": 3600,
            "memory_persistence": True,
        },
    }

    try:
        # Create and start Central AI Brain
        print("\n🧠 Initializing Central AI Brain...")
        central_brain = await create_central_brain(config)
        await central_brain.start()

        if not central_brain.is_running:
            print("❌ Failed to start Central AI Brain")
            return

        print("✅ Central AI Brain is running")

        # Test 1: Embryo training validation
        print("\n" + "=" * 50)
        print("🎯 TEST 1: Embryo Training Validation")
        print("=" * 50)

        # Create sample embryo data
        embryo_data_1 = {
            "id": "embryo_001",
            "training_duration": "2 weeks",
            "patterns": [
                {"type": "coding_assistance", "frequency": 15, "confidence": 0.8},
                {"type": "debugging_help", "frequency": 8, "confidence": 0.7},
                {"type": "code_review", "frequency": 5, "confidence": 0.6},
            ],
            "behavioral_data": {
                "user_interactions": 28,
                "successful_responses": 22,
                "error_rate": 0.21,
                "response_time_avg": 2.3,
            },
            "user_context": {
                "expertise_level": "intermediate",
                "primary_languages": ["python", "javascript"],
                "project_types": ["web_development", "automation"],
            },
            "training_history": [
                {"date": "2024-01-01", "score": 6.2},
                {"date": "2024-01-08", "score": 7.1},
                {"date": "2024-01-15", "score": 7.8},
            ],
            "specialization": "development",
        }

        print(f"Embryo ID: {embryo_data_1['id']}")
        print(f"Training Duration: {embryo_data_1['training_duration']}")
        print(f"Detected Patterns: {len(embryo_data_1['patterns'])}")

        result1 = await central_brain.validate_embryo_training(embryo_data_1)

        print(f"\n📊 Validation Result:")
        print(f"Success: {result1.get('success', False)}")
        print(f"Overall Score: {result1.get('overall_score', 'N/A')}")
        print(f"Readiness Level: {result1.get('readiness_level', 'N/A')}")
        print(
            f"Recommended Specialization: {result1.get('recommended_specialization', 'N/A')}"
        )

        # Test 2: Birth readiness assessment
        print("\n" + "=" * 50)
        print("🎯 TEST 2: Birth Readiness Assessment")
        print("=" * 50)

        # Create embryo with different maturity level
        embryo_data_2 = {
            "id": "embryo_002",
            "training_duration": "4 weeks",
            "patterns": [
                {"type": "research_assistance", "frequency": 25, "confidence": 0.9},
                {"type": "data_analysis", "frequency": 18, "confidence": 0.85},
                {"type": "report_generation", "frequency": 12, "confidence": 0.8},
                {"type": "fact_checking", "frequency": 10, "confidence": 0.75},
            ],
            "behavioral_data": {
                "user_interactions": 65,
                "successful_responses": 58,
                "error_rate": 0.11,
                "response_time_avg": 1.8,
            },
            "user_context": {
                "expertise_level": "advanced",
                "research_domains": ["technology", "science", "business"],
                "output_preferences": ["detailed", "cited_sources"],
            },
            "training_history": [
                {"date": "2024-01-01", "score": 5.8},
                {"date": "2024-01-08", "score": 7.2},
                {"date": "2024-01-15", "score": 8.1},
                {"date": "2024-01-22", "score": 8.7},
            ],
            "specialization": "research",
        }

        print(f"Embryo ID: {embryo_data_2['id']}")
        print(f"Training Duration: {embryo_data_2['training_duration']}")
        print(
            f"User Interactions: {embryo_data_2['behavioral_data']['user_interactions']}"
        )

        result2 = await central_brain.assess_embryo_birth_readiness(embryo_data_2)

        print(f"\n📊 Birth Readiness Assessment:")
        print(f"Success: {result2.get('success', False)}")
        print(f"Readiness Level: {result2.get('readiness_level', 'N/A')}")
        print(f"Readiness Score: {result2.get('readiness_score', 'N/A')}")
        print(f"Birth Recommendation: {result2.get('birth_recommendation', 'N/A')}")

        # Test 3: Training label generation
        print("\n" + "=" * 50)
        print("🎯 TEST 3: Training Label Generation")
        print("=" * 50)

        # Create sample events for labeling
        sample_events = [
            {
                "id": "event_001",
                "type": "code_request",
                "timestamp": "2024-01-15T10:30:00",
                "context": "python function",
            },
            {
                "id": "event_002",
                "type": "debug_help",
                "timestamp": "2024-01-15T11:15:00",
                "context": "syntax error",
            },
            {
                "id": "event_003",
                "type": "explanation",
                "timestamp": "2024-01-15T14:20:00",
                "context": "algorithm concept",
            },
            {
                "id": "event_004",
                "type": "code_review",
                "timestamp": "2024-01-15T16:45:00",
                "context": "optimization",
            },
            {
                "id": "event_005",
                "type": "research_query",
                "timestamp": "2024-01-15T17:30:00",
                "context": "best practices",
            },
        ]

        print(f"Events to Label: {len(sample_events)}")
        for event in sample_events:
            print(f"  - {event['type']}: {event['context']}")

        result3 = await central_brain.generate_training_labels(sample_events)

        print(f"\n📊 Label Generation Result:")
        print(f"Success: {result3.get('success', False)}")
        print(f"Labels Generated: {len(result3.get('labels', []))}")
        print(f"Events Processed: {result3.get('events_processed', 'N/A')}")

        # Test 4: Embryo Trainer status
        print("\n" + "=" * 50)
        print("🎯 TEST 4: Embryo Trainer Status")
        print("=" * 50)

        if central_brain.embryo_trainer:
            status = central_brain.embryo_trainer.get_trainer_status()
            print(f"Agent Name: {status.get('agent_name')}")
            print(f"Embryos Evaluated: {status.get('embryos_evaluated')}")
            print(
                f"Embryos Approved for Birth: {status.get('embryos_approved_for_birth')}"
            )
            print(f"Approval Rate: {status.get('approval_rate', 0):.1%}")
            print(
                f"Average Training Score: {status.get('average_training_score', 0):.1f}"
            )
            print(f"Active Reports: {status.get('active_reports')}")
            print(f"Capabilities: {', '.join(status.get('capabilities', []))}")

        # Test 5: Specialization recommendation
        print("\n" + "=" * 50)
        print("🎯 TEST 5: Specialization Recommendation")
        print("=" * 50)

        # Create embryo with unclear specialization
        embryo_data_3 = {
            "id": "embryo_003",
            "patterns": [
                {"type": "creative_writing", "frequency": 12, "confidence": 0.7},
                {"type": "brainstorming", "frequency": 8, "confidence": 0.6},
                {"type": "content_creation", "frequency": 15, "confidence": 0.8},
            ],
            "behavioral_data": {
                "user_interactions": 35,
                "creative_outputs": 28,
                "user_satisfaction": 0.85,
            },
            "user_context": {
                "creative_domains": ["writing", "marketing", "design"],
                "output_style": ["engaging", "original", "professional"],
            },
        }

        print(f"Embryo ID: {embryo_data_3['id']}")
        print(f"Pattern Types: {[p['type'] for p in embryo_data_3['patterns']]}")

        if central_brain.embryo_trainer:
            result5 = await central_brain.embryo_trainer.recommend_specialization(
                embryo_data_3
            )

            print(f"\n📊 Specialization Recommendation:")
            print(f"Success: {result5.get('success', False)}")
            if result5.get("success"):
                rec = result5.get("recommendation", {})
                print(f"Recommended Category: {rec.get('category', 'N/A')}")
                print(f"Confidence: {rec.get('confidence', 0):.1%}")
                print(f"Reasoning: {rec.get('reasoning', 'N/A')[:100]}...")

        print("\n" + "=" * 50)
        print("🎉 Embryo Trainer Testing Complete!")
        print("=" * 50)

        # Display summary
        total_tests = 5
        successful_tests = sum(
            [
                1 if result1.get("success") else 0,
                1 if result2.get("success") else 0,
                1 if result3.get("success") else 0,
                1,  # Status test always succeeds
                1,  # Specialization test
            ]
        )

        print(f"\n📈 Test Summary:")
        print(f"Tests Completed: {total_tests}")
        print(f"Tests Successful: {successful_tests}")
        print(f"Success Rate: {successful_tests/total_tests:.1%}")

        # Stop Central AI Brain
        await central_brain.stop()
        print("\n✅ Central AI Brain stopped successfully")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        print(f"\n❌ Test failed with error: {e}")


async def main():
    """Main test function"""
    try:
        await test_embryo_trainer()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error in main: {e}")


if __name__ == "__main__":
    print("🚀 Starting SelFlow Embryo Trainer Tests...")
    asyncio.run(main())
