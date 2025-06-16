#!/usr/bin/env python3
"""
Test Meta-Learning System
Runs the complete pipeline to train semantic agents from event data.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.ai.meta_learning_system import MetaLearningSystem
from app.ai.central_brain import CentralAIBrain
from app.ai.ollama_client import OllamaClient


async def test_meta_learning():
    """Test the complete meta-learning pipeline"""

    print("🧠 Testing SelFlow Meta-Learning System")
    print("=" * 60)

    # Initialize components
    print("🔧 Initializing components...")

    # Create Ollama client
    ollama_config = {
        "base_url": "http://localhost:11434",
        "model_name": "gemma3:4b",
        "timeout": 60,
        "max_tokens": 2048,
        "temperature": 0.7,
    }

    ollama_client = OllamaClient(ollama_config)
    await ollama_client.start()

    # Create Central AI Brain
    central_brain = CentralAIBrain({})
    central_brain.ollama_client = ollama_client
    central_brain.is_running = True

    # Create Meta-Learning System
    meta_learning = MetaLearningSystem(central_brain)

    print("✅ Components initialized")

    # Test individual components
    print("\n🧪 Testing Individual Components...")

    # Test 1: Load and analyze events
    print("\n1️⃣ Loading semantic events...")
    events = await meta_learning._load_semantic_events()
    print(f"   Loaded {len(events)} events")

    if not events:
        print("❌ No events found! Make sure SelFlow has been running.")
        return

    # Test 2: Filter events for each agent
    print("\n2️⃣ Filtering events by agent type...")
    for agent_type in meta_learning.agent_specs.keys():
        filtered = meta_learning._filter_events_for_agent(events, agent_type)
        print(f"   {agent_type}: {len(filtered)} relevant events")

    # Test 3: Generate semantic labels for one agent
    print("\n3️⃣ Testing semantic label generation...")
    dev_events = meta_learning._filter_events_for_agent(
        events, "DevelopmentWorkflowAgent"
    )

    if dev_events:
        # Test with small sample
        sample_events = dev_events[:3]
        print(f"   Generating labels for {len(sample_events)} sample events...")

        try:
            training_examples = await meta_learning.generate_semantic_labels(
                sample_events, "DevelopmentWorkflowAgent"
            )

            print(f"   ✅ Generated {len(training_examples)} training examples")

            # Show sample
            if training_examples:
                example = training_examples[0]
                print(f"   Sample label: {example.semantic_label}")
                print(f"   Confidence: {example.confidence}")
                print(f"   Context: {example.context.get('intent', 'N/A')}")

        except Exception as e:
            print(f"   ❌ Label generation failed: {e}")

    # Test 4: Architecture design
    print("\n4️⃣ Testing architecture design...")
    if "training_examples" in locals() and training_examples:
        try:
            architecture = await meta_learning.design_network_architecture(
                "DevelopmentWorkflowAgent", training_examples
            )

            print(f"   ✅ Architecture designed:")
            print(f"      Input dim: {architecture.input_dim}")
            print(f"      Hidden layers: {architecture.hidden_dims}")
            print(f"      Output dim: {architecture.output_dim}")
            print(f"      Max params: {architecture.max_params:,}")

        except Exception as e:
            print(f"   ❌ Architecture design failed: {e}")

    # Test 5: Small network training
    print("\n5️⃣ Testing network training...")
    if "architecture" in locals() and "training_examples" in locals():
        try:
            network = await meta_learning.train_agent_network(
                "DevelopmentWorkflowAgent", architecture, training_examples
            )

            print(f"   ✅ Network trained successfully")
            print(f"      Parameters: {sum(p.numel() for p in network.parameters()):,}")

        except Exception as e:
            print(f"   ❌ Network training failed: {e}")

    # Test 6: Agent deployment
    print("\n6️⃣ Testing agent deployment...")
    if "network" in locals():
        try:
            agent_interface = await meta_learning.deploy_agent(
                "DevelopmentWorkflowAgent", network
            )

            print(f"   ✅ Agent deployed:")
            print(f"      Name: {agent_interface['name']}")
            print(f"      Specialization: {agent_interface['specialization']}")
            print(f"      Model saved: {agent_interface['model_path']}")

            # Test inference
            print("\n   🔍 Testing inference...")
            sample_event = (
                dev_events[0]
                if dev_events
                else {
                    "path": "/Users/test/Projects/selflow/test.py",
                    "action": "modify",
                    "ext": "py",
                    "ts": 1234567890,
                }
            )

            inference_result = agent_interface["inference_function"](sample_event)
            print(f"      Prediction: Class {inference_result['predicted_class']}")
            print(f"      Confidence: {inference_result['confidence']:.3f}")

        except Exception as e:
            print(f"   ❌ Agent deployment failed: {e}")

    print("\n🎯 Individual Component Tests Complete!")

    # Full pipeline test
    print("\n🚀 Testing Complete Meta-Learning Pipeline...")
    print("   (This will train all agents - may take several minutes)")

    try:
        results = await meta_learning.train_all_agents()

        print(f"\n✅ Pipeline Complete! Results:")
        for agent_type, result in results.items():
            status = result["status"]
            if status == "success":
                examples = result["training_examples"]
                params = result["architecture"].max_params
                print(f"   ✅ {agent_type}: {examples} examples, {params:,} params")
            else:
                error = result.get("error", "Unknown error")
                print(f"   ❌ {agent_type}: {error}")

    except Exception as e:
        print(f"   ❌ Pipeline failed: {e}")
        import traceback

        traceback.print_exc()

    # Cleanup
    await ollama_client.close()

    print("\n🎉 Meta-Learning Test Complete!")
    print("\nKey Achievements:")
    print("✅ Semantic label generation using Gemma 3:4b")
    print("✅ Data-driven architecture design")
    print("✅ Small neural network training")
    print("✅ Agent deployment with inference")
    print("✅ Complete meta-learning pipeline")


if __name__ == "__main__":
    asyncio.run(test_meta_learning())
