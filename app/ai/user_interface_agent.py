"""
SelFlow Central AI Brain - User Interface Agent
Handles all natural language user interactions with intelligence and personality
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class UserInterfaceAgent:
    """Handles all natural language user interactions"""

    def __init__(self, central_brain):
        self.central_brain = central_brain
        self.prompt_template = self._load_prompt_template()
        self.interaction_count = 0
        self.user_preferences = {}
        self.conversation_patterns = {}

        logger.info("UserInterfaceAgent initialized")

    def _load_prompt_template(self) -> str:
        """Load the system prompt template"""
        try:
            prompt_path = Path("app/ai/prompts/user_interface.txt")
            if prompt_path.exists():
                return prompt_path.read_text()
            else:
                # Fallback prompt if file doesn't exist
                return self._get_fallback_prompt()
        except Exception as e:
            logger.error(f"Failed to load prompt template: {e}")
            return self._get_fallback_prompt()

    def _get_fallback_prompt(self) -> str:
        """Fallback prompt template"""
        return """You are the User Interface Agent of SelFlow, a self-creating AI operating system.

Your role is to be helpful, friendly, and knowledgeable about SelFlow's capabilities.

Current context:
- System status: {system_status}
- Active agents: {active_agents}
- User message: {user_message}

Respond helpfully and naturally to the user's message."""

    async def process_chat_message(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process user chat messages and generate responses"""

        try:
            self.interaction_count += 1
            start_time = datetime.now()

            # Build context for the interaction
            interaction_context = await self._build_interaction_context(
                message, context
            )

            # Format the prompt with context
            formatted_prompt = self._format_prompt(message, interaction_context)

            # Generate response through Central AI Brain
            response = await self.central_brain.ollama_client.generate_response(
                prompt=message,
                context=interaction_context,
                system_prompt=formatted_prompt,
            )

            # Analyze and learn from the interaction
            await self._learn_from_interaction(message, response, interaction_context)

            # Update conversation patterns
            self._update_conversation_patterns(message, response)

            response_time = (datetime.now() - start_time).total_seconds()

            return {
                "success": True,
                "message": response,
                "agent": "user_interface",
                "interaction_id": self.interaction_count,
                "response_time": response_time,
                "context_used": interaction_context is not None,
            }

        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "I apologize, but I encountered an error processing your message. Please try again.",
                "agent": "user_interface",
            }

    async def handle_voice_command(
        self, command: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process voice commands and execute actions"""

        try:
            # Voice commands often need more direct action interpretation
            voice_context = context or {}
            voice_context["interaction_type"] = "voice_command"
            voice_context["requires_action"] = True

            # Process as a chat message but with voice-specific context
            result = await self.process_chat_message(command, voice_context)

            # Check if the response suggests system actions
            if result.get("success") and self._suggests_system_action(
                result.get("message", "")
            ):
                # Coordinate with system controller for action execution
                action_result = await self._coordinate_system_action(
                    command, result["message"]
                )
                result["system_action"] = action_result

            result["input_type"] = "voice"
            return result

        except Exception as e:
            logger.error(f"Error handling voice command: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "I couldn't process that voice command. Please try again.",
                "input_type": "voice",
            }

    async def generate_proactive_suggestions(
        self, context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Generate helpful suggestions based on user patterns"""

        try:
            # Analyze user patterns and system state
            suggestions_prompt = self._build_suggestions_prompt(context)

            response = await self.central_brain.ollama_client.generate_response(
                prompt="Generate 3-5 helpful suggestions for the user based on their patterns and current system state.",
                system_prompt=suggestions_prompt,
            )

            # Parse suggestions from response
            suggestions = self._parse_suggestions(response)

            return suggestions

        except Exception as e:
            logger.error(f"Error generating proactive suggestions: {e}")
            return ["I'm here to help! Feel free to ask me anything about SelFlow."]

    async def explain_system_action(self, action: Dict[str, Any]) -> str:
        """Explain what the system is doing in user-friendly terms"""

        try:
            explanation_prompt = f"""
            Explain this system action in simple, user-friendly terms:
            
            Action: {action}
            
            Guidelines:
            - Use plain language, avoid technical jargon
            - Explain what's happening and why
            - Mention any benefits to the user
            - Keep it concise but informative
            """

            explanation = await self.central_brain.ollama_client.generate_response(
                prompt="Explain this system action to the user",
                system_prompt=explanation_prompt,
            )

            return explanation

        except Exception as e:
            logger.error(f"Error explaining system action: {e}")
            return "The system is performing an action to improve your experience."

    async def _build_interaction_context(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build comprehensive context for the interaction"""

        interaction_context = context or {}

        # Add system status
        if self.central_brain.context_manager:
            system_summary = self.central_brain.context_manager.get_context_summary()
            interaction_context.update(
                {
                    "system_status": system_summary.get("system_state", {}).get(
                        "system_health", "operational"
                    ),
                    "active_agents": system_summary.get("system_state", {}).get(
                        "active_agents", 0
                    ),
                    "recent_activity": f"{system_summary.get('conversation_history', {}).get('recent_activity', 0)} recent interactions",
                }
            )

        # Add user preferences
        interaction_context["user_preferences"] = self.user_preferences

        # Add conversation patterns
        interaction_context["conversation_patterns"] = self.conversation_patterns

        # Add interaction metadata
        interaction_context.update(
            {
                "interaction_count": self.interaction_count,
                "timestamp": datetime.now().isoformat(),
                "message_length": len(message),
                "agent": "user_interface",
            }
        )

        return interaction_context

    def _format_prompt(self, message: str, context: Dict[str, Any]) -> str:
        """Format the prompt template with current context"""

        try:
            return self.prompt_template.format(
                system_status=context.get("system_status", "operational"),
                active_agents=context.get("active_agents", "unknown"),
                user_profile=context.get("user_preferences", {}),
                recent_activity=context.get("recent_activity", "none"),
                conversation_history=context.get("conversation_patterns", {}),
                user_message=message,
            )
        except Exception as e:
            logger.error(f"Error formatting prompt: {e}")
            return f"User message: {message}\n\nRespond helpfully."

    async def _learn_from_interaction(
        self, message: str, response: str, context: Dict[str, Any]
    ):
        """Learn from the interaction to improve future responses"""

        try:
            # Update user preferences based on interaction
            if "prefer" in message.lower() or "like" in message.lower():
                self._extract_preferences(message)

            # Update context manager with this interaction
            if self.central_brain.context_manager:
                await self.central_brain.context_manager.update_context(
                    {
                        "user_message": message,
                        "assistant_response": response,
                        "context_type": "user_interface",
                        "metadata": {
                            "agent": "user_interface",
                            "interaction_count": self.interaction_count,
                            "context_used": context,
                        },
                    }
                )

        except Exception as e:
            logger.error(f"Error learning from interaction: {e}")

    def _extract_preferences(self, message: str):
        """Extract user preferences from message"""

        # Simple preference extraction (could be enhanced with NLP)
        message_lower = message.lower()

        if "prefer" in message_lower:
            # Extract preference patterns
            if "detailed" in message_lower:
                self.user_preferences["response_style"] = "detailed"
            elif "brief" in message_lower or "short" in message_lower:
                self.user_preferences["response_style"] = "brief"

        if "help" in message_lower and "proactive" in message_lower:
            self.user_preferences["proactive_suggestions"] = "help" in message_lower

    def _update_conversation_patterns(self, message: str, response: str):
        """Update conversation patterns for better future interactions"""

        # Track message types
        message_type = self._classify_message_type(message)
        if message_type not in self.conversation_patterns:
            self.conversation_patterns[message_type] = 0
        self.conversation_patterns[message_type] += 1

        # Track response effectiveness (placeholder for future enhancement)
        self.conversation_patterns["total_interactions"] = self.interaction_count
        self.conversation_patterns["last_interaction"] = datetime.now().isoformat()

    def _classify_message_type(self, message: str) -> str:
        """Classify the type of user message"""

        message_lower = message.lower()

        if any(
            word in message_lower
            for word in ["?", "what", "how", "why", "when", "where"]
        ):
            return "question"
        elif any(
            word in message_lower
            for word in ["please", "can you", "could you", "would you"]
        ):
            return "request"
        elif any(
            word in message_lower
            for word in ["hello", "hi", "hey", "good morning", "good afternoon"]
        ):
            return "greeting"
        elif any(word in message_lower for word in ["thank", "thanks", "appreciate"]):
            return "gratitude"
        elif any(word in message_lower for word in ["help", "assist", "support"]):
            return "help_request"
        else:
            return "general"

    def _suggests_system_action(self, response: str) -> bool:
        """Check if the response suggests a system action should be taken"""

        action_indicators = [
            "let me",
            "i'll",
            "i will",
            "i can",
            "i should",
            "executing",
            "running",
            "starting",
            "stopping",
            "creating",
            "updating",
            "modifying",
            "configuring",
        ]

        response_lower = response.lower()
        return any(indicator in response_lower for indicator in action_indicators)

    async def _coordinate_system_action(
        self, command: str, response: str
    ) -> Dict[str, Any]:
        """Coordinate with system controller for action execution"""

        try:
            # This would coordinate with the SystemController agent
            action_request = {
                "type": "user_requested_action",
                "original_command": command,
                "ai_response": response,
                "timestamp": datetime.now().isoformat(),
            }

            # For now, return a placeholder result
            return {
                "action_coordinated": True,
                "action_type": "placeholder",
                "message": "Action coordination would happen here",
            }

        except Exception as e:
            logger.error(f"Error coordinating system action: {e}")
            return {"action_coordinated": False, "error": str(e)}

    def _build_suggestions_prompt(
        self, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build prompt for generating proactive suggestions"""

        context = context or {}

        return f"""
        You are generating proactive suggestions for a SelFlow user.
        
        User patterns: {self.conversation_patterns}
        User preferences: {self.user_preferences}
        System context: {context}
        
        Generate 3-5 helpful, specific suggestions that would be valuable to this user.
        Focus on:
        - SelFlow capabilities they haven't explored
        - Productivity improvements
        - System optimizations
        - Learning opportunities
        
        Format as a simple list of actionable suggestions.
        """

    def _parse_suggestions(self, response: str) -> List[str]:
        """Parse suggestions from AI response"""

        try:
            # Simple parsing - split by lines and clean up
            lines = response.strip().split("\n")
            suggestions = []

            for line in lines:
                line = line.strip()
                if line and len(line) > 10:  # Filter out very short lines
                    # Remove bullet points and numbering
                    line = line.lstrip("•-*123456789. ")
                    if line:
                        suggestions.append(line)

            # Limit to 5 suggestions
            return (
                suggestions[:5]
                if suggestions
                else ["Feel free to ask me anything about SelFlow!"]
            )

        except Exception as e:
            logger.error(f"Error parsing suggestions: {e}")
            return ["I'm here to help! Ask me about SelFlow's capabilities."]

    def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of the User Interface Agent"""

        return {
            "agent_name": "UserInterfaceAgent",
            "interaction_count": self.interaction_count,
            "user_preferences": self.user_preferences,
            "conversation_patterns": self.conversation_patterns,
            "capabilities": [
                "natural_language_chat",
                "voice_command_processing",
                "proactive_suggestions",
                "system_action_explanation",
                "user_preference_learning",
            ],
        }
