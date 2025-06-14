#!/usr/bin/env python3
"""
Complete SelFlow System Test

Demonstrates the full agent lifecycle:
1. Embryo Pool with competing neural embryos
2. Pattern detection and natural selection
3. Agent Creator analyzing patterns and birthing agents
4. Agent Manager coordinating the entire lifecycle
"""

import asyncio
import logging
import sys
import time
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.agent_manager import AgentManager


async def test_complete_system():
    """Test the complete SelFlow system"""

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger("complete_system_test")
    logger.info("🌟 Starting Complete SelFlow System Test...")

    # System configuration
    config = {
        "embryo_pool": {
            "pool_size": 5,  # Smaller for testing
            "selection_pressure": 0.3,
            "mutation_rate": 0.1,
        },
        "agent_creation": {"min_pattern_threshold": 10, "personality_variation": 0.3},
        "max_active_agents": 3,  # Test with smaller limit
        "agent_birth_threshold": 20,  # Lower threshold for testing
        "agent_retirement_threshold": 0.3,
    }

    try:
        # Create and start the Agent Manager
        logger.info("🚀 Initializing SelFlow Agent Management System...")
        agent_manager = AgentManager(config)

        # Start the system
        await agent_manager.start()

        # Simulate system events to feed embryos
        logger.info("\n📡 Simulating system events to feed embryos...")

        # Simulate various system events
        test_events = [
            {"type": "file_operation", "action": "create", "path": "/docs/test.txt"},
            {"type": "file_operation", "action": "edit", "path": "/docs/test.txt"},
            {"type": "app_launch", "app": "vscode", "project": "/dev/selflow"},
            {"type": "development", "action": "git_commit", "repo": "selflow"},
            {"type": "file_operation", "action": "organize", "path": "/downloads"},
            {"type": "creative_work", "action": "design", "tool": "figma"},
            {"type": "development", "action": "debug", "language": "python"},
            {"type": "file_operation", "action": "search", "query": "project files"},
            {"type": "communication", "action": "email", "priority": "high"},
            {"type": "web_browsing", "action": "research", "topic": "AI development"},
        ]

        # Feed events to embryo pool
        for i, event in enumerate(test_events, 1):
            logger.info(f"Event {i}: {event['type']} - {event.get('action', 'N/A')}")
            await agent_manager.embryo_pool.process_event(event)
            await asyncio.sleep(0.5)  # Brief pause between events

        # Wait for embryos to process and evolve
        logger.info("\n🧬 Allowing embryos to evolve and compete...")
        await asyncio.sleep(5)

        # Get system status
        logger.info("\n📊 Getting system status after evolution...")
        status = await agent_manager.get_system_status()

        # Display embryo pool status
        embryo_status = status.get("embryo_pool", {})
        logger.info(f"Embryo Pool Status:")
        logger.info(f"  - Total embryos: {embryo_status.get('total_embryos', 0)}")
        logger.info(f"  - Active embryos: {embryo_status.get('active_embryos', 0)}")
        logger.info(f"  - Events processed: {embryo_status.get('events_processed', 0)}")

        if embryo_status.get("embryos"):
            logger.info(
                f"  - Top embryo patterns: {embryo_status['embryos'][0].get('patterns_detected', 0)}"
            )
            logger.info(
                f"  - Top embryo fitness: {embryo_status['embryos'][0].get('fitness_score', 0):.2f}"
            )

        # Force an agent birth to demonstrate the process
        logger.info("\n🎭 Forcing agent birth from best embryo...")
        new_agent = await agent_manager.force_agent_birth()

        if new_agent:
            logger.info(f"🎉 Agent born successfully!")
            logger.info(f"  - Name: {new_agent.blueprint.name}")
            logger.info(f"  - Specialization: {new_agent.blueprint.specialization}")
            logger.info(f"  - Autonomy: {new_agent.blueprint.autonomy_level}")
            logger.info(
                f"  - Introduction: {new_agent.blueprint.introduction_message[:100]}..."
            )
        else:
            logger.warning("❌ Agent birth failed")

        # Add more events to potentially trigger another birth
        logger.info("\n📡 Adding more specialized events...")
        specialized_events = [
            {"type": "development", "action": "code_review", "files": 15},
            {"type": "development", "action": "test_run", "results": "passed"},
            {"type": "development", "action": "deploy", "environment": "staging"},
            {"type": "development", "action": "debug", "issue": "memory_leak"},
            {"type": "development", "action": "refactor", "component": "auth"},
        ]

        for event in specialized_events:
            await agent_manager.embryo_pool.process_event(event)
            await asyncio.sleep(0.3)

        # Wait for processing
        await asyncio.sleep(3)

        # Try another forced birth
        logger.info("\n🎭 Attempting second agent birth...")
        second_agent = await agent_manager.force_agent_birth()

        if second_agent:
            logger.info(f"🎉 Second agent born!")
            logger.info(f"  - Name: {second_agent.blueprint.name}")
            logger.info(f"  - Specialization: {second_agent.blueprint.specialization}")

        # Get final system status
        logger.info("\n📈 Final System Status:")
        final_status = await agent_manager.get_system_status()

        system_info = final_status.get("system", {})
        logger.info(f"System Metrics:")
        logger.info(f"  - Total births: {system_info.get('total_births', 0)}")
        logger.info(f"  - Active agents: {system_info.get('active_agents', 0)}")
        logger.info(f"  - System uptime: {system_info.get('uptime', 'N/A')}")

        # Display active agents
        active_agents = final_status.get("active_agents", {})
        if active_agents.get("agents"):
            logger.info(f"\n🤖 Active Agents:")
            for agent in active_agents["agents"]:
                logger.info(f"  - {agent['name']} ({agent['specialization']})")
                logger.info(
                    f"    Autonomy: {agent['autonomy']} | Tasks: {agent['task_count']}"
                )

        # Display recent history
        history = final_status.get("recent_history", [])
        if history:
            logger.info(f"\n📜 Recent Agent History:")
            for event in history[-3:]:  # Show last 3 events
                logger.info(
                    f"  - {event['event'].title()}: {event['agent_name']} ({event['specialization']})"
                )

        # Test agent interactions
        logger.info(f"\n💬 Agent Introduction Showcase:")
        active_agent_list = await agent_manager.get_active_agents()

        for i, agent in enumerate(active_agent_list, 1):
            logger.info(f"\n--- Active Agent {i} ---")
            logger.info(f"🤖 {agent.blueprint.name}")
            logger.info(
                f"🏷️  [{agent.blueprint.autonomy_level.upper()} AUTONOMY | {agent.blueprint.specialization.upper()}]"
            )
            logger.info(f'💬 "{agent.blueprint.introduction_message}"')
            logger.info(
                f"⚡ Ready with {agent.blueprint.confidence_threshold:.0%} confidence threshold"
            )

        logger.info(f"\n✅ Complete System Test Successful!")
        logger.info(
            f"🎯 {len(active_agent_list)} agents are active and ready to serve!"
        )
        logger.info(f"🧬 Embryo pool continues evolving for future agent births...")

        # Stop the system
        await agent_manager.stop()

    except Exception as e:
        logger.error(f"❌ Complete system test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_complete_system())
