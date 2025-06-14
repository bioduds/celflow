#!/usr/bin/env python3
"""
Test script for SelFlow Agent Creator

Demonstrates the agent creation process from embryo patterns
and shows the first agent birth with personality generation.
"""

import asyncio
import logging
import sys
import time
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.agent_creator import AgentCreator


async def test_agent_creator():
    """Test the Agent Creator functionality"""

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger("test_agent_creator")
    logger.info("🤖 Starting SelFlow Agent Creator Test...")

    # Configuration
    config = {
        "agent_creation": {"min_pattern_threshold": 10, "personality_variation": 0.3}
    }

    try:
        # Create Agent Creator
        logger.info("Creating Agent Creator...")
        agent_creator = AgentCreator(config)

        # Simulate different embryo data scenarios
        test_scenarios = [
            {
                "name": "File Operations Specialist",
                "embryo_data": {
                    "embryo_id": "embryo-001",
                    "creation_time": "2025-06-14T02:00:00",
                    "patterns_detected": 85,
                    "fitness_score": 0.82,
                    "specialization_scores": {
                        "file_operations": 0.9,
                        "development": 0.3,
                        "communication": 0.1,
                        "creative_work": 0.1,
                        "app_launches": 0.2,
                        "web_browsing": 0.1,
                        "system_maintenance": 0.3,
                        "temporal_patterns": 0.4,
                    },
                    "dominant_specialization": "file_operations",
                    "specialization_strength": 0.9,
                },
            },
            {
                "name": "Development Assistant",
                "embryo_data": {
                    "embryo_id": "embryo-002",
                    "creation_time": "2025-06-14T02:00:00",
                    "patterns_detected": 127,
                    "fitness_score": 0.91,
                    "specialization_scores": {
                        "file_operations": 0.4,
                        "development": 0.95,
                        "communication": 0.2,
                        "creative_work": 0.1,
                        "app_launches": 0.7,
                        "web_browsing": 0.6,
                        "system_maintenance": 0.5,
                        "temporal_patterns": 0.3,
                    },
                    "dominant_specialization": "development",
                    "specialization_strength": 0.95,
                },
            },
            {
                "name": "Creative Workflow Helper",
                "embryo_data": {
                    "embryo_id": "embryo-003",
                    "creation_time": "2025-06-14T02:00:00",
                    "patterns_detected": 63,
                    "fitness_score": 0.74,
                    "specialization_scores": {
                        "file_operations": 0.3,
                        "development": 0.1,
                        "communication": 0.4,
                        "creative_work": 0.88,
                        "app_launches": 0.5,
                        "web_browsing": 0.3,
                        "system_maintenance": 0.2,
                        "temporal_patterns": 0.6,
                    },
                    "dominant_specialization": "creative_work",
                    "specialization_strength": 0.88,
                },
            },
        ]

        created_agents = []

        # Test agent creation for each scenario
        for i, scenario in enumerate(test_scenarios, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"🧬 AGENT BIRTH SCENARIO {i}: {scenario['name']}")
            logger.info(f"{'='*60}")

            embryo_data = scenario["embryo_data"]

            # Display embryo stats
            logger.info(f"📊 Embryo Statistics:")
            logger.info(f"  - Patterns detected: {embryo_data['patterns_detected']}")
            logger.info(f"  - Fitness score: {embryo_data['fitness_score']:.2f}")
            logger.info(
                f"  - Dominant specialization: {embryo_data['dominant_specialization']}"
            )
            logger.info(
                f"  - Specialization strength: {embryo_data['specialization_strength']:.2f}"
            )

            # Create agent
            logger.info("\n🎭 Creating specialized agent...")
            agent = await agent_creator.create_agent(embryo_data)

            if agent:
                created_agents.append(agent)

                # Display agent details
                logger.info(f"\n🎉 AGENT BIRTH SUCCESSFUL!")
                logger.info(f"✨ Agent Details:")
                logger.info(f"  - Name: {agent.name}")
                logger.info(f"  - Specialization: {agent.specialization}")
                logger.info(f"  - Autonomy Level: {agent.autonomy_level}")
                logger.info(
                    f"  - Confidence Threshold: {agent.confidence_threshold:.2f}"
                )

                logger.info(f"\n🧠 Personality Profile:")
                for trait, value in agent.personality_traits.items():
                    logger.info(f"  - {trait.title()}: {value:.2f}")

                logger.info(f"\n🛠️ Capabilities & Tools:")
                logger.info(f"  - Capabilities: {', '.join(agent.capabilities[:5])}...")
                logger.info(f"  - Tools: {', '.join(agent.tools[:5])}...")

                logger.info(f"\n💬 Introduction Message:")
                logger.info(f'"{agent.introduction_message}"')

            else:
                logger.error(
                    f"❌ Failed to create agent from embryo {embryo_data['embryo_id']}"
                )

            await asyncio.sleep(1)  # Brief pause between creations

        # Display creation statistics
        logger.info(f"\n{'='*60}")
        logger.info("📈 AGENT CREATION SUMMARY")
        logger.info(f"{'='*60}")

        stats = agent_creator.get_creation_stats()
        logger.info(f"Total agents created: {stats['total_agents']}")
        logger.info(f"Specializations: {stats.get('specializations', {})}")
        logger.info(f"Autonomy levels: {stats.get('autonomy_levels', {})}")

        if stats.get("latest_creation"):
            latest = stats["latest_creation"]
            logger.info(f"\nLatest creation: {latest['agent_name']}")
            logger.info(f"Personality summary: {latest['personality_summary']}")

        # Test agent interaction simulation
        logger.info(f"\n{'='*60}")
        logger.info("🎭 AGENT INTRODUCTION SIMULATION")
        logger.info(f"{'='*60}")

        for i, agent in enumerate(created_agents, 1):
            logger.info(f"\n--- Agent {i} Introduction ---")
            logger.info(f"Agent: {agent.name}")
            logger.info(
                f"[{agent.autonomy_level.upper()} AUTONOMY | {agent.specialization.upper()}]"
            )
            logger.info(f"\n{agent.introduction_message}")
            logger.info(
                f"\n[Ready for user interaction with {agent.confidence_threshold:.0%} confidence threshold]"
            )

        logger.info(f"\n✅ Agent Creator Test Completed Successfully!")
        logger.info(f"🎯 {len(created_agents)} agents are ready to serve!")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_agent_creator())
