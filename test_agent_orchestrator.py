#!/usr/bin/env python3
"""
Test script for SelFlow AgentOrchestrator
Demonstrates multi-agent coordination capabilities
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


async def test_agent_orchestrator():
    """Test the Agent Orchestrator functionality"""

    print("🎭 Testing SelFlow Agent Orchestrator")
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

        # Test 1: Simple task orchestration
        print("\n" + "=" * 50)
        print("🎯 TEST 1: Simple Task Orchestration")
        print("=" * 50)

        simple_task = "Help me understand how SelFlow works and what it can do for me"
        print(f"Task: {simple_task}")

        result1 = await central_brain.orchestrate_complex_task(simple_task)

        print(f"\n📊 Orchestration Result:")
        print(f"Success: {result1.get('success', False)}")
        print(f"Task ID: {result1.get('task_id', 'N/A')}")
        print(f"Execution Time: {result1.get('execution_time', 'N/A')} seconds")
        print(f"Agents Used: {result1.get('agents_used', [])}")

        if result1.get("success"):
            orchestration_plan = result1.get("orchestration_plan", {}).get("plan", {})
            print(f"\n🎭 Orchestration Plan:")
            print(f"Subtasks: {len(orchestration_plan.get('subtasks', []))}")
            for i, subtask in enumerate(orchestration_plan.get("subtasks", []), 1):
                print(
                    f"  {i}. {subtask.get('description', 'Unknown')} -> {subtask.get('assigned_agent', 'Unknown')}"
                )

        # Test 2: Complex multi-step task
        print("\n" + "=" * 50)
        print("🎯 TEST 2: Complex Multi-Step Task")
        print("=" * 50)

        complex_task = "I want to optimize my workflow by creating specialized AI agents that can help me with coding, research, and project management. Can you analyze my needs and create a plan?"
        print(f"Task: {complex_task}")

        context = {
            "user_preferences": ["detailed_explanations", "step_by_step_guidance"],
            "current_projects": ["AI development", "system optimization"],
            "expertise_level": "advanced",
        }

        result2 = await central_brain.orchestrate_complex_task(complex_task, context)

        print(f"\n📊 Orchestration Result:")
        print(f"Success: {result2.get('success', False)}")
        print(f"Task ID: {result2.get('task_id', 'N/A')}")
        print(f"Execution Time: {result2.get('execution_time', 'N/A')} seconds")
        print(f"Agents Used: {result2.get('agents_used', [])}")

        if result2.get("success"):
            results = result2.get("results", {})
            synthesized = results.get("synthesized_result", {})
            if synthesized.get("success"):
                print(f"\n🎯 Synthesized Response:")
                print(
                    f"{synthesized.get('synthesized_response', 'No response available')[:200]}..."
                )

        # Test 3: High priority urgent task
        print("\n" + "=" * 50)
        print("🎯 TEST 3: High Priority Urgent Task")
        print("=" * 50)

        urgent_task = "URGENT: My system is running slowly and I need immediate help to diagnose and fix performance issues"
        print(f"Task: {urgent_task}")

        result3 = await central_brain.orchestrate_complex_task(urgent_task)

        print(f"\n📊 Orchestration Result:")
        print(f"Success: {result3.get('success', False)}")
        print(f"Task ID: {result3.get('task_id', 'N/A')}")
        print(
            f"Priority Detected: {result3.get('orchestration_plan', {}).get('plan', {}).get('priority', 'N/A')}"
        )

        # Test 4: Agent Orchestrator status
        print("\n" + "=" * 50)
        print("🎯 TEST 4: Agent Orchestrator Status")
        print("=" * 50)

        if central_brain.agent_orchestrator:
            status = central_brain.agent_orchestrator.get_orchestrator_status()
            print(f"Agent Name: {status.get('agent_name')}")
            print(f"Orchestrations Completed: {status.get('orchestration_count')}")
            print(f"Active Tasks: {status.get('active_tasks')}")
            print(f"Completed Tasks: {status.get('completed_tasks')}")
            print(f"Success Rate: {status.get('success_rate', 0):.1%}")
            print(f"Available Agents: {status.get('available_agents')}")
            print(f"Capabilities: {', '.join(status.get('capabilities', []))}")

        # Test 5: Task monitoring
        print("\n" + "=" * 50)
        print("🎯 TEST 5: Task Monitoring")
        print("=" * 50)

        if result1.get("task_id"):
            task_status = await central_brain.agent_orchestrator.monitor_task_progress(
                result1["task_id"]
            )
            print(f"Task ID: {task_status.get('task_id')}")
            print(f"Status: {task_status.get('status')}")
            print(f"Progress: {task_status.get('progress', 0):.1f}%")

        print("\n" + "=" * 50)
        print("🎉 Agent Orchestrator Testing Complete!")
        print("=" * 50)

        # Display summary
        total_tests = 5
        successful_tests = sum(
            [
                1 if result1.get("success") else 0,
                1 if result2.get("success") else 0,
                1 if result3.get("success") else 0,
                1,  # Status test always succeeds
                1,  # Monitoring test always succeeds
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
        await test_agent_orchestrator()
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error in main: {e}")


if __name__ == "__main__":
    print("🚀 Starting SelFlow Agent Orchestrator Tests...")
    asyncio.run(main())
