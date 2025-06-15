"""
SelFlow Central AI Brain - Core Orchestrating Intelligence
The main brain that coordinates all AI capabilities and system interactions
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .ollama_client import OllamaClient
from .context_manager import ContextManager

logger = logging.getLogger(__name__)


class CentralAIBrain:
    """The orchestrating intelligence of SelFlow"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ai_config = config.get("ai_brain", {})
        self.context_config = config.get("context_management", {})

        # Core components
        self.ollama_client = None
        self.context_manager = None

        # Specialized agents (will be initialized later)
        self.user_interface = None
        self.agent_orchestrator = None
        self.embryo_trainer = None
        self.system_controller = None
        self.pattern_validator = None

        # State management
        self.is_running = False
        self.startup_time = None
        self.interaction_count = 0

        logger.info("CentralAIBrain initialized")

    async def start(self):
        """Initialize the Central AI Brain"""
        try:
            logger.info("🧠 Starting SelFlow Central AI Brain...")

            # Initialize core components
            self.ollama_client = OllamaClient(self.ai_config)
            await self.ollama_client.start()

            self.context_manager = ContextManager(self.context_config)

            # Validate that everything is working
            health_status = await self.get_health_status()
            if not health_status.get("ollama_healthy", False):
                raise Exception("Ollama client is not healthy")

            self.is_running = True
            self.startup_time = datetime.now()

            # Initialize specialized agents (placeholder for now)
            await self._initialize_specialized_agents()

            logger.info("✅ Central AI Brain started successfully")

        except Exception as e:
            logger.error(f"❌ Failed to start Central AI Brain: {e}")
            raise

    async def stop(self):
        """Shutdown the Central AI Brain"""
        try:
            logger.info("🛑 Stopping Central AI Brain...")

            if self.ollama_client:
                await self.ollama_client.close()

            self.is_running = False
            logger.info("✅ Central AI Brain stopped successfully")

        except Exception as e:
            logger.error(f"❌ Error stopping Central AI Brain: {e}")

    async def _initialize_specialized_agents(self):
        """Initialize specialized agent components (placeholder)"""
        # These will be implemented in subsequent phases
        logger.info("Specialized agents initialization (placeholder)")
        pass

    async def process_user_input(
        self, user_message: str, context_type: str = "chat"
    ) -> Dict[str, Any]:
        """Main entry point for user interactions"""

        if not self.is_running:
            return {
                "success": False,
                "error": "Central AI Brain is not running",
                "message": "I apologize, but I'm not currently available. Please try again later.",
            }

        try:
            self.interaction_count += 1
            start_time = datetime.now()

            # Build context for this interaction
            context = await self.context_manager.build_context(
                interaction_type=context_type, user_message=user_message
            )

            # Generate system prompt based on context type
            system_prompt = self._get_system_prompt(context_type)

            # Generate response using Ollama
            response = await self.ollama_client.generate_response(
                prompt=user_message,
                context={"conversation_history": context},
                system_prompt=system_prompt,
            )

            # Update context with this interaction
            await self.context_manager.update_context(
                {
                    "user_message": user_message,
                    "assistant_response": response,
                    "context_type": context_type,
                    "metadata": {
                        "interaction_id": self.interaction_count,
                        "response_time": (datetime.now() - start_time).total_seconds(),
                    },
                }
            )

            return {
                "success": True,
                "message": response,
                "context_type": context_type,
                "interaction_id": self.interaction_count,
                "response_time": (datetime.now() - start_time).total_seconds(),
            }

        except Exception as e:
            logger.error(f"Error processing user input: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "I apologize, but I encountered an error processing your request. Please try again.",
            }

    async def stream_user_response(self, user_message: str, context_type: str = "chat"):
        """Stream response for real-time chat interface"""

        if not self.is_running:
            yield "I apologize, but I'm not currently available. Please try again later."
            return

        try:
            # Build context
            context = await self.context_manager.build_context(
                interaction_type=context_type, user_message=user_message
            )

            system_prompt = self._get_system_prompt(context_type)

            # Stream response
            full_response = ""
            async for chunk in self.ollama_client.stream_response(
                prompt=user_message,
                context={"conversation_history": context},
                system_prompt=system_prompt,
            ):
                full_response += chunk
                yield chunk

            # Update context after streaming is complete
            await self.context_manager.update_context(
                {
                    "user_message": user_message,
                    "assistant_response": full_response,
                    "context_type": context_type,
                    "metadata": {"interaction_id": self.interaction_count},
                }
            )

        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            yield "I apologize, but I encountered an error. Please try again."

    def _get_system_prompt(self, context_type: str) -> str:
        """Get appropriate system prompt based on context type"""

        base_prompt = """You are the Central AI Brain of SelFlow, a self-creating AI operating system.

Your personality:
- Helpful and knowledgeable about the SelFlow system
- Clear and concise in explanations
- Proactive in offering assistance
- Respectful of user privacy and preferences
- Enthusiastic about AI and system capabilities

Your core capabilities:
- Answer questions about SelFlow functionality
- Execute user commands by coordinating with specialized agents
- Provide system status and insights
- Offer proactive suggestions based on user patterns
- Learn and adapt from interactions"""

        if context_type == "chat":
            return (
                base_prompt
                + "\n\nYou are in casual conversation mode. Be friendly and helpful."
            )

        elif context_type == "system_control":
            return (
                base_prompt
                + "\n\nYou are in system control mode. Focus on understanding and executing system commands safely."
            )

        elif context_type == "agent_orchestration":
            return (
                base_prompt
                + "\n\nYou are coordinating multiple agents. Focus on task delegation and result synthesis."
            )

        elif context_type == "embryo_training":
            return (
                base_prompt
                + "\n\nYou are evaluating embryo training. Focus on pattern analysis and specialization recommendations."
            )

        else:
            return base_prompt

    async def coordinate_system_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate complex system actions"""

        if not self.is_running:
            return {"success": False, "error": "Central AI Brain is not running"}

        try:
            action_type = action.get("type", "unknown")
            logger.info(f"Coordinating system action: {action_type}")

            # This is a placeholder for system action coordination
            # Will be implemented with specialized agents

            return {
                "success": True,
                "action_type": action_type,
                "message": f"System action '{action_type}' coordinated successfully",
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error coordinating system action: {e}")
            return {"success": False, "error": str(e)}

    async def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status of Central AI Brain"""

        status = {
            "central_brain_running": self.is_running,
            "startup_time": (
                self.startup_time.isoformat() if self.startup_time else None
            ),
            "interaction_count": self.interaction_count,
            "ollama_healthy": False,
            "context_manager_status": None,
        }

        # Check Ollama client health
        if self.ollama_client:
            ollama_status = self.ollama_client.get_health_status()
            status["ollama_healthy"] = ollama_status.get("is_healthy", False)
            status["ollama_model"] = ollama_status.get("model_name", "unknown")

        # Check context manager status
        if self.context_manager:
            status["context_manager_status"] = (
                self.context_manager.get_context_summary()
            )

        return status

    async def get_system_insights(self) -> Dict[str, Any]:
        """Get insights about system usage and patterns"""

        insights = {
            "interaction_statistics": {
                "total_interactions": self.interaction_count,
                "uptime_hours": 0,
            },
            "context_insights": {},
            "performance_metrics": {},
        }

        if self.startup_time:
            uptime = datetime.now() - self.startup_time
            insights["interaction_statistics"]["uptime_hours"] = (
                uptime.total_seconds() / 3600
            )

        if self.context_manager:
            insights["context_insights"] = self.context_manager.get_context_summary()

        return insights

    async def update_system_state(self, state_update: Dict[str, Any]):
        """Update system state information"""

        if self.context_manager:
            await self.context_manager.update_context(
                {
                    "system_state": state_update,
                    "metadata": {"update_time": datetime.now().isoformat()},
                }
            )

    async def validate_patterns(self, patterns: list) -> Dict[str, Any]:
        """Validate patterns using AI intelligence (placeholder)"""

        # This will be implemented with the PatternValidator agent
        return {
            "validated_patterns": patterns,
            "validation_score": 0.85,
            "recommendations": ["Pattern validation placeholder"],
        }

    async def generate_training_labels(self, events: list) -> Dict[str, Any]:
        """Generate intelligent training labels (placeholder)"""

        # This will be implemented with the EmbryoTrainer agent
        return {
            "training_labels": [],
            "confidence_scores": [],
            "recommendations": ["Training label generation placeholder"],
        }

    def get_status_summary(self) -> str:
        """Get a human-readable status summary"""

        if not self.is_running:
            return "🔴 Central AI Brain is offline"

        uptime = ""
        if self.startup_time:
            uptime_seconds = (datetime.now() - self.startup_time).total_seconds()
            uptime = f" (uptime: {uptime_seconds/3600:.1f}h)"

        return f"🟢 Central AI Brain is online{uptime} - {self.interaction_count} interactions processed"


# Utility functions
async def create_central_brain(config: Dict[str, Any]) -> CentralAIBrain:
    """Create and start a Central AI Brain instance"""
    brain = CentralAIBrain(config)
    await brain.start()
    return brain
