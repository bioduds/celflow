"""
SelFlow Central Integration Layer
Integrates Central AI Brain with existing SelFlow components
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from ..ai.central_brain import CentralAIBrain
from .agent_manager import AgentManager
from .embryo_pool import EmbryoPool
from .pattern_detector import PatternDetector

logger = logging.getLogger(__name__)


class CentralIntegration:
    """Integrates Central AI Brain with existing SelFlow components"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

        # Core components
        self.central_brain: Optional[CentralAIBrain] = None
        self.agent_manager: Optional[AgentManager] = None
        self.embryo_pool: Optional[EmbryoPool] = None
        self.pattern_detector: Optional[PatternDetector] = None

        # Integration state
        self.is_running = False
        self.startup_time = None

        logger.info("CentralIntegration initialized")

    async def start(self):
        """Start the integrated system"""
        try:
            logger.info("🔗 Starting Central Integration Layer...")

            # Initialize Central AI Brain
            self.central_brain = CentralAIBrain(self.config)
            await self.central_brain.start()

            # Initialize existing components
            await self._initialize_existing_components()

            # Set up integration hooks
            await self._setup_integration_hooks()

            self.is_running = True
            self.startup_time = datetime.now()

            logger.info("✅ Central Integration Layer started successfully")

        except Exception as e:
            logger.error(f"❌ Failed to start Central Integration: {e}")
            raise

    async def stop(self):
        """Stop the integrated system"""
        try:
            logger.info("🛑 Stopping Central Integration Layer...")

            if self.central_brain:
                await self.central_brain.stop()

            self.is_running = False
            logger.info("✅ Central Integration Layer stopped")

        except Exception as e:
            logger.error(f"❌ Error stopping Central Integration: {e}")

    async def _initialize_existing_components(self):
        """Initialize existing SelFlow components"""
        try:
            # Initialize AgentManager
            self.agent_manager = AgentManager(self.config)

            # Initialize EmbryoPool
            self.embryo_pool = EmbryoPool(self.config)

            # Initialize PatternDetector
            self.pattern_detector = PatternDetector(self.config)

            logger.info("Existing SelFlow components initialized")

        except Exception as e:
            logger.error(f"Failed to initialize existing components: {e}")
            # Continue without existing components for now
            logger.warning("Continuing without some existing components")

    async def _setup_integration_hooks(self):
        """Set up integration hooks between components"""
        try:
            # Update Central AI Brain with current system state
            if self.agent_manager and self.central_brain:
                agents_info = await self._get_agents_info()
                await self.central_brain.update_system_state(
                    {
                        "active_agents": list(agents_info.keys()),
                        "system_health": {"status": "operational"},
                        "integration_active": True,
                    }
                )

            logger.info("Integration hooks established")

        except Exception as e:
            logger.error(f"Failed to setup integration hooks: {e}")

    async def _get_agents_info(self) -> Dict[str, Any]:
        """Get information about current agents"""
        agents_info = {}

        if self.agent_manager:
            try:
                # This would integrate with actual AgentManager methods
                # For now, return placeholder data
                agents_info = {
                    "advisor_system_guardian": {
                        "name": "Advisor the System Guardian",
                        "specialization": "System Monitoring",
                        "status": "active",
                        "capabilities": ["system_monitoring", "resource_management"],
                    }
                }
            except Exception as e:
                logger.error(f"Failed to get agents info: {e}")

        return agents_info

    async def enhanced_agent_birth(self, embryo_data: Dict[str, Any]) -> Dict[str, Any]:
        """AI-enhanced agent birth process"""

        if not self.is_running or not self.central_brain:
            return {"success": False, "error": "Central Integration not running"}

        try:
            logger.info("🤖 Starting AI-enhanced agent birth process...")

            # Use Central AI Brain to evaluate embryo readiness
            training_assessment = await self.central_brain.generate_training_labels(
                [embryo_data]
            )

            # Get AI recommendation for specialization
            specialization_prompt = f"""
            Analyze this embryo data and recommend the best specialization:
            
            Embryo Data: {embryo_data}
            
            Consider:
            1. What patterns does this embryo show expertise in?
            2. What would be the most valuable specialization for the system?
            3. What capabilities should this agent have?
            
            Provide a clear recommendation for the agent's specialization and capabilities.
            """

            ai_recommendation = await self.central_brain.process_user_input(
                specialization_prompt, context_type="embryo_training"
            )

            # Create enhanced agent birth result
            birth_result = {
                "success": True,
                "embryo_id": embryo_data.get("id", "unknown"),
                "ai_assessment": training_assessment,
                "specialization_recommendation": ai_recommendation.get("message", ""),
                "birth_timestamp": datetime.now().isoformat(),
                "enhanced_by_ai": True,
            }

            # If we have an agent manager, create the actual agent
            if self.agent_manager:
                # This would integrate with actual agent creation
                logger.info("Agent creation would happen here with AgentManager")

            logger.info("✅ AI-enhanced agent birth completed")
            return birth_result

        except Exception as e:
            logger.error(f"❌ Enhanced agent birth failed: {e}")
            return {"success": False, "error": str(e)}

    async def intelligent_pattern_detection(self, events: list) -> Dict[str, Any]:
        """AI-enhanced pattern detection"""

        if not self.is_running or not self.central_brain:
            return {"success": False, "error": "Central Integration not running"}

        try:
            logger.info("🔍 Starting AI-enhanced pattern detection...")

            # Basic pattern detection first
            basic_patterns = []
            if self.pattern_detector:
                # This would use actual PatternDetector
                basic_patterns = [{"type": "placeholder", "confidence": 0.7}]

            # AI validation and enhancement
            validated_patterns = await self.central_brain.validate_patterns(
                basic_patterns
            )

            # Generate AI insights about patterns
            pattern_analysis_prompt = f"""
            Analyze these detected patterns and events:
            
            Events: {len(events)} events detected
            Basic Patterns: {basic_patterns}
            
            Provide insights:
            1. Are these patterns meaningful and coherent?
            2. What additional patterns might be present?
            3. How can these patterns help create better agents?
            4. What recommendations do you have for pattern improvement?
            """

            ai_insights = await self.central_brain.process_user_input(
                pattern_analysis_prompt, context_type="pattern_validation"
            )

            result = {
                "success": True,
                "basic_patterns": basic_patterns,
                "validated_patterns": validated_patterns,
                "ai_insights": ai_insights.get("message", ""),
                "events_analyzed": len(events),
                "analysis_timestamp": datetime.now().isoformat(),
            }

            logger.info("✅ AI-enhanced pattern detection completed")
            return result

        except Exception as e:
            logger.error(f"❌ Intelligent pattern detection failed: {e}")
            return {"success": False, "error": str(e)}

    async def process_user_command(self, command: str) -> Dict[str, Any]:
        """Process user commands through AI brain"""

        if not self.is_running or not self.central_brain:
            return {
                "success": False,
                "error": "Central Integration not running",
                "message": "I'm not currently available. Please try again later.",
            }

        try:
            # Process command through Central AI Brain
            response = await self.central_brain.process_user_input(
                command, context_type="system_control"
            )

            # If the AI suggests system actions, coordinate them
            if (
                response.get("success")
                and "action" in response.get("message", "").lower()
            ):
                # This is where we'd coordinate actual system actions
                logger.info("System action coordination would happen here")

            return response

        except Exception as e:
            logger.error(f"Error processing user command: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "I encountered an error processing your command.",
            }

    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""

        status = {
            "integration_running": self.is_running,
            "startup_time": (
                self.startup_time.isoformat() if self.startup_time else None
            ),
            "central_brain_status": None,
            "components_status": {
                "agent_manager": self.agent_manager is not None,
                "embryo_pool": self.embryo_pool is not None,
                "pattern_detector": self.pattern_detector is not None,
            },
        }

        # Get Central AI Brain status
        if self.central_brain:
            status["central_brain_status"] = (
                await self.central_brain.get_health_status()
            )

        return status

    async def chat_with_ai(self, message: str) -> Dict[str, Any]:
        """Direct chat interface with Central AI Brain"""

        if not self.is_running or not self.central_brain:
            return {
                "success": False,
                "message": "I'm not currently available. Please try again later.",
            }

        return await self.central_brain.process_user_input(message, context_type="chat")

    async def stream_chat_response(self, message: str):
        """Stream chat response from Central AI Brain"""

        if not self.is_running or not self.central_brain:
            yield "I'm not currently available. Please try again later."
            return

        async for chunk in self.central_brain.stream_user_response(
            message, context_type="chat"
        ):
            yield chunk

    def get_integration_summary(self) -> str:
        """Get human-readable integration summary"""

        if not self.is_running:
            return "🔴 Central Integration is offline"

        components = []
        if self.central_brain and self.central_brain.is_running:
            components.append("AI Brain")
        if self.agent_manager:
            components.append("Agent Manager")
        if self.embryo_pool:
            components.append("Embryo Pool")
        if self.pattern_detector:
            components.append("Pattern Detector")

        components_str = ", ".join(components) if components else "None"

        uptime = ""
        if self.startup_time:
            uptime_seconds = (datetime.now() - self.startup_time).total_seconds()
            uptime = f" (uptime: {uptime_seconds/3600:.1f}h)"

        return f"🟢 Central Integration online{uptime} - Components: {components_str}"


# Utility functions
async def create_integrated_system(config: Dict[str, Any]) -> CentralIntegration:
    """Create and start an integrated SelFlow system"""
    integration = CentralIntegration(config)
    await integration.start()
    return integration
