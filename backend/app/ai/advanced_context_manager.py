"""
Advanced Context Manager - AI-Powered Context Intelligence

This module enhances the basic ContextManager with advanced AI capabilities:
- Intelligent context pattern recognition
- Proactive context building
- User behavior learning
- Contextual memory optimization
- Predictive context suggestions
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from collections import defaultdict, Counter
import numpy as np

from .ollama_client import OllamaClient
from .context_manager import ContextManager, ConversationExchange, UserProfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContextType(Enum):
    """Types of context for intelligent management"""

    CHAT = "chat"
    TASK = "task"
    LEARNING = "learning"
    SYSTEM = "system"
    CREATIVE = "creative"
    PROBLEM_SOLVING = "problem_solving"
    PLANNING = "planning"
    ANALYSIS = "analysis"


class LearningPattern(Enum):
    """Types of learning patterns detected"""

    REPETITIVE_TASK = "repetitive_task"
    SKILL_DEVELOPMENT = "skill_development"
    PREFERENCE_CHANGE = "preference_change"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    KNOWLEDGE_BUILDING = "knowledge_building"
    HABIT_FORMATION = "habit_formation"


class ContextPriority(Enum):
    """Priority levels for context elements"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ContextPattern:
    """Represents a detected context pattern"""

    pattern_id: str
    pattern_type: LearningPattern
    frequency: int
    confidence: float
    first_seen: datetime
    last_seen: datetime
    context_elements: List[str]
    user_benefit: str
    suggested_actions: List[str]


@dataclass
class ContextInsight:
    """AI-generated insight about user context"""

    insight_id: str
    insight_type: str
    description: str
    confidence: float
    supporting_evidence: List[str]
    actionable_suggestions: List[str]
    created_at: datetime


@dataclass
class ProactiveContext:
    """Proactively built context for user assistance"""

    context_id: str
    context_type: ContextType
    priority: ContextPriority
    content: Dict[str, Any]
    relevance_score: float
    expiry_time: datetime
    triggers: List[str]


@dataclass
class UserBehaviorProfile:
    """Advanced user behavior analysis"""

    user_id: str
    interaction_patterns: Dict[str, Any]
    preferred_context_types: List[str]
    peak_activity_hours: List[int]
    common_workflows: List[Dict[str, Any]]
    learning_preferences: Dict[str, Any]
    communication_style: Dict[str, Any]
    last_updated: datetime


class AdvancedContextManager:
    """
    AI-Powered Advanced Context Management System

    Enhances basic context management with intelligent learning,
    pattern recognition, and proactive context building.
    """

    def __init__(
        self, ollama_client: OllamaClient, base_context_manager: ContextManager
    ):
        """Initialize the Advanced Context Manager"""
        self.ollama_client = ollama_client
        self.base_context_manager = base_context_manager

        # Advanced context storage
        self.context_patterns: Dict[str, ContextPattern] = {}
        self.context_insights: List[ContextInsight] = []
        self.proactive_contexts: Dict[str, ProactiveContext] = {}
        self.user_behavior_profiles: Dict[str, UserBehaviorProfile] = {}

        # Learning and analysis state
        self.pattern_detection_enabled = True
        self.proactive_building_enabled = True
        self.learning_threshold = 3  # Minimum occurrences to detect pattern

        # Performance metrics
        self.metrics = {
            "patterns_detected": 0,
            "insights_generated": 0,
            "proactive_contexts_created": 0,
            "context_accuracy_score": 0.0,
            "user_satisfaction_score": 0.0,
        }

        # Load prompt template
        self.prompt_template = self._load_prompt_template()

        logger.info("AdvancedContextManager initialized successfully")

    def _load_prompt_template(self) -> str:
        """Load the advanced context management prompt template"""
        try:
            with open("app/ai/prompts/advanced_context.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.error("Advanced context prompt template not found")
            return "You are an advanced context management AI. Analyze user interactions and provide intelligent context insights."

    async def analyze_interaction_patterns(
        self, user_id: str = "default_user"
    ) -> Dict[str, Any]:
        """Analyze user interaction patterns using AI"""
        try:
            # Get recent conversation history
            recent_exchanges = (
                self.base_context_manager.conversation_history.get_recent(50)
            )

            if not recent_exchanges:
                return {"patterns": [], "insights": [], "recommendations": []}

            # Build analysis context
            analysis_context = self._build_pattern_analysis_context(recent_exchanges)

            # Get AI analysis
            ai_response = await self._get_ai_pattern_analysis(analysis_context)

            # Process AI response
            analysis_result = self._process_pattern_analysis(ai_response, user_id)

            # Update user behavior profile
            await self._update_user_behavior_profile(user_id, analysis_result)

            logger.info(f"Pattern analysis completed for user {user_id}")
            return analysis_result

        except Exception as e:
            logger.error(f"Error analyzing interaction patterns: {str(e)}")
            return {"patterns": [], "insights": [], "recommendations": []}

    async def build_proactive_context(
        self, context_type: ContextType, user_id: str = "default_user"
    ) -> Optional[ProactiveContext]:
        """Build proactive context based on user patterns and current state"""
        try:
            # Get user behavior profile
            user_profile = self.user_behavior_profiles.get(user_id)
            if not user_profile:
                user_profile = await self._create_user_behavior_profile(user_id)

            # Get relevant patterns
            relevant_patterns = self._get_relevant_patterns(context_type, user_profile)

            # Build context using AI
            context_content = await self._build_ai_proactive_context(
                context_type, user_profile, relevant_patterns
            )

            if context_content:
                proactive_context = ProactiveContext(
                    context_id=f"proactive_{uuid.uuid4().hex[:8]}",
                    context_type=context_type,
                    priority=self._calculate_context_priority(context_content),
                    content=context_content,
                    relevance_score=context_content.get("relevance_score", 0.5),
                    expiry_time=datetime.now() + timedelta(hours=2),
                    triggers=context_content.get("triggers", []),
                )

                self.proactive_contexts[proactive_context.context_id] = (
                    proactive_context
                )
                self.metrics["proactive_contexts_created"] += 1

                logger.info(
                    f"Proactive context created: {proactive_context.context_id}"
                )
                return proactive_context

            return None

        except Exception as e:
            logger.error(f"Error building proactive context: {str(e)}")
            return None

    async def generate_context_insights(
        self, interaction_data: Dict[str, Any]
    ) -> List[ContextInsight]:
        """Generate AI-powered insights about user context"""
        try:
            # Build insight generation context
            insight_context = self._build_insight_context(interaction_data)

            # Get AI insights
            ai_response = await self._get_ai_insights(insight_context)

            # Process insights
            insights = self._process_ai_insights(ai_response)

            # Store insights
            self.context_insights.extend(insights)
            self.metrics["insights_generated"] += len(insights)

            logger.info(f"Generated {len(insights)} context insights")
            return insights

        except Exception as e:
            logger.error(f"Error generating context insights: {str(e)}")
            return []

    async def optimize_context_memory(self) -> Dict[str, Any]:
        """Optimize context memory using AI-driven importance scoring"""
        try:
            # Analyze context importance
            importance_analysis = await self._analyze_context_importance()

            # Optimize storage
            optimization_result = await self._optimize_context_storage(
                importance_analysis
            )

            # Update metrics
            self.metrics["context_accuracy_score"] = optimization_result.get(
                "accuracy_improvement", 0.0
            )

            logger.info("Context memory optimization completed")
            return optimization_result

        except Exception as e:
            logger.error(f"Error optimizing context memory: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def predict_user_needs(
        self, current_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Predict user needs based on context patterns and AI analysis"""
        try:
            # Get user behavior profile
            user_id = current_context.get("user_id", "default_user")
            user_profile = self.user_behavior_profiles.get(user_id)

            if not user_profile:
                return []

            # Build prediction context
            prediction_context = self._build_prediction_context(
                current_context, user_profile
            )

            # Get AI predictions
            ai_response = await self._get_ai_predictions(prediction_context)

            # Process predictions
            predictions = self._process_ai_predictions(ai_response)

            logger.info(f"Generated {len(predictions)} user need predictions")
            return predictions

        except Exception as e:
            logger.error(f"Error predicting user needs: {str(e)}")
            return []

    def _build_pattern_analysis_context(
        self, exchanges: List[ConversationExchange]
    ) -> str:
        """Build context for pattern analysis"""
        context_parts = [
            "PATTERN_ANALYSIS_REQUEST",
            f"TOTAL_EXCHANGES: {len(exchanges)}",
            f"TIME_RANGE: {exchanges[0].timestamp.isoformat()} to {exchanges[-1].timestamp.isoformat()}",
            "",
        ]

        # Add exchange summaries
        for i, exchange in enumerate(exchanges[-10:]):  # Last 10 exchanges
            context_parts.extend(
                [
                    f"EXCHANGE_{i+1}:",
                    f"  Time: {exchange.timestamp.isoformat()}",
                    f"  Type: {exchange.context_type}",
                    f"  User: {exchange.user_message[:100]}...",
                    f"  Assistant: {exchange.assistant_response[:100]}...",
                    "",
                ]
            )

        # Add analysis request
        context_parts.extend(
            [
                "ANALYSIS_REQUEST:",
                "1. Identify recurring patterns in user interactions",
                "2. Detect learning opportunities and skill development",
                "3. Recognize workflow optimization possibilities",
                "4. Suggest proactive assistance opportunities",
                "5. Analyze communication style and preferences",
                "",
            ]
        )

        return "\n".join(context_parts)

    async def _get_ai_pattern_analysis(self, context: str) -> str:
        """Get AI analysis of interaction patterns"""
        full_prompt = (
            f"{self.prompt_template}\n\n{context}\n\nProvide pattern analysis:"
        )

        try:
            response = await self.ollama_client.generate_response(prompt=full_prompt)
            return response
        except Exception as e:
            logger.error(f"Error getting AI pattern analysis: {str(e)}")
            return self._create_fallback_analysis()

    def _process_pattern_analysis(
        self, ai_response: str, user_id: str
    ) -> Dict[str, Any]:
        """Process AI pattern analysis response"""
        try:
            # Try to parse structured response
            if ai_response.strip().startswith("{"):
                return json.loads(ai_response)

            # Fallback: extract patterns from text
            patterns = self._extract_patterns_from_text(ai_response)
            insights = self._extract_insights_from_text(ai_response)
            recommendations = self._extract_recommendations_from_text(ai_response)

            return {
                "patterns": patterns,
                "insights": insights,
                "recommendations": recommendations,
                "analysis_timestamp": datetime.now().isoformat(),
                "user_id": user_id,
            }

        except Exception as e:
            logger.error(f"Error processing pattern analysis: {str(e)}")
            return {"patterns": [], "insights": [], "recommendations": []}

    async def _update_user_behavior_profile(
        self, user_id: str, analysis_result: Dict[str, Any]
    ):
        """Update user behavior profile with analysis results"""
        try:
            if user_id not in self.user_behavior_profiles:
                self.user_behavior_profiles[user_id] = UserBehaviorProfile(
                    user_id=user_id,
                    interaction_patterns={},
                    preferred_context_types=[],
                    peak_activity_hours=[],
                    common_workflows=[],
                    learning_preferences={},
                    communication_style={},
                    last_updated=datetime.now(),
                )

            profile = self.user_behavior_profiles[user_id]

            # Update with new analysis
            for pattern in analysis_result.get("patterns", []):
                pattern_id = pattern.get(
                    "id", f"pattern_{len(profile.interaction_patterns)}"
                )
                profile.interaction_patterns[pattern_id] = pattern

            # Update preferences
            for insight in analysis_result.get("insights", []):
                if "preference" in insight.get("type", "").lower():
                    profile.learning_preferences.update(insight.get("data", {}))

            profile.last_updated = datetime.now()

            logger.info(f"Updated behavior profile for user {user_id}")

        except Exception as e:
            logger.error(f"Error updating user behavior profile: {str(e)}")

    async def _create_user_behavior_profile(self, user_id: str) -> UserBehaviorProfile:
        """Create initial user behavior profile"""
        profile = UserBehaviorProfile(
            user_id=user_id,
            interaction_patterns={},
            preferred_context_types=["chat"],
            peak_activity_hours=[9, 10, 11, 14, 15, 16],  # Default business hours
            common_workflows=[],
            learning_preferences={"style": "interactive", "pace": "moderate"},
            communication_style={"formality": "casual", "detail_level": "medium"},
            last_updated=datetime.now(),
        )

        self.user_behavior_profiles[user_id] = profile
        return profile

    def _get_relevant_patterns(
        self, context_type: ContextType, user_profile: UserBehaviorProfile
    ) -> List[ContextPattern]:
        """Get patterns relevant to the context type and user"""
        relevant_patterns = []

        for pattern in self.context_patterns.values():
            # Check if pattern is relevant to context type
            if context_type.value in pattern.context_elements:
                relevant_patterns.append(pattern)

            # Check if pattern matches user preferences
            for workflow in user_profile.common_workflows:
                if any(
                    element in workflow.get("elements", [])
                    for element in pattern.context_elements
                ):
                    relevant_patterns.append(pattern)
                    break

        # Sort by confidence and frequency
        relevant_patterns.sort(key=lambda p: (p.confidence, p.frequency), reverse=True)
        return relevant_patterns[:5]  # Top 5 most relevant

    async def _build_ai_proactive_context(
        self,
        context_type: ContextType,
        user_profile: UserBehaviorProfile,
        patterns: List[ContextPattern],
    ) -> Optional[Dict[str, Any]]:
        """Build proactive context using AI"""
        try:
            # Build context for AI
            context_prompt = self._build_proactive_context_prompt(
                context_type, user_profile, patterns
            )

            # Get AI response
            ai_response = await self.ollama_client.generate_response(
                prompt=context_prompt
            )

            # Process response
            if ai_response.strip().startswith("{"):
                return json.loads(ai_response)
            else:
                return self._parse_proactive_context_text(ai_response)

        except Exception as e:
            logger.error(f"Error building AI proactive context: {str(e)}")
            return None

    def _build_proactive_context_prompt(
        self,
        context_type: ContextType,
        user_profile: UserBehaviorProfile,
        patterns: List[ContextPattern],
    ) -> str:
        """Build prompt for proactive context generation"""
        prompt_parts = [
            f"PROACTIVE_CONTEXT_REQUEST: {context_type.value}",
            f"USER_PROFILE:",
            f"  Preferred Types: {user_profile.preferred_context_types}",
            f"  Communication Style: {user_profile.communication_style}",
            f"  Learning Preferences: {user_profile.learning_preferences}",
            "",
            "RELEVANT_PATTERNS:",
        ]

        for i, pattern in enumerate(patterns):
            prompt_parts.extend(
                [
                    f"  Pattern {i+1}:",
                    f"    Type: {pattern.pattern_type.value}",
                    f"    Confidence: {pattern.confidence}",
                    f"    Elements: {pattern.context_elements}",
                    f"    Benefit: {pattern.user_benefit}",
                    "",
                ]
            )

        prompt_parts.extend(
            [
                "Generate proactive context that:",
                "1. Anticipates user needs based on patterns",
                "2. Provides relevant information or suggestions",
                "3. Matches user communication style",
                "4. Offers actionable next steps",
                "5. Includes relevance score (0.0-1.0)",
                "",
            ]
        )

        return "\n".join(prompt_parts)

    def _calculate_context_priority(
        self, context_content: Dict[str, Any]
    ) -> ContextPriority:
        """Calculate priority for proactive context"""
        relevance_score = context_content.get("relevance_score", 0.5)
        urgency_indicators = context_content.get("urgency_indicators", [])

        if relevance_score > 0.8 or "urgent" in urgency_indicators:
            return ContextPriority.CRITICAL
        elif relevance_score > 0.6 or "important" in urgency_indicators:
            return ContextPriority.HIGH
        elif relevance_score > 0.4:
            return ContextPriority.NORMAL
        else:
            return ContextPriority.LOW

    def _build_insight_context(self, interaction_data: Dict[str, Any]) -> str:
        """Build context for insight generation"""
        return f"""
INSIGHT_GENERATION_REQUEST

INTERACTION_DATA:
{json.dumps(interaction_data, indent=2)}

CURRENT_PATTERNS: {len(self.context_patterns)}
RECENT_INSIGHTS: {len(self.context_insights[-5:])}

Generate insights about:
1. User behavior patterns
2. Optimization opportunities
3. Learning and development areas
4. Workflow improvements
5. Proactive assistance possibilities
"""

    async def _get_ai_insights(self, context: str) -> str:
        """Get AI-generated insights"""
        full_prompt = f"{self.prompt_template}\n\n{context}\n\nProvide insights:"

        try:
            response = await self.ollama_client.generate_response(prompt=full_prompt)
            return response
        except Exception as e:
            logger.error(f"Error getting AI insights: {str(e)}")
            return "No insights available due to AI error."

    def _process_ai_insights(self, ai_response: str) -> List[ContextInsight]:
        """Process AI insights response"""
        insights = []

        try:
            if ai_response.strip().startswith("["):
                insight_data = json.loads(ai_response)
                for data in insight_data:
                    insight = ContextInsight(
                        insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                        insight_type=data.get("type", "general"),
                        description=data.get("description", ""),
                        confidence=data.get("confidence", 0.5),
                        supporting_evidence=data.get("evidence", []),
                        actionable_suggestions=data.get("suggestions", []),
                        created_at=datetime.now(),
                    )
                    insights.append(insight)
            else:
                # Fallback: create single insight from text
                insight = ContextInsight(
                    insight_id=f"insight_{uuid.uuid4().hex[:8]}",
                    insight_type="text_analysis",
                    description=ai_response[:200],
                    confidence=0.6,
                    supporting_evidence=["AI text analysis"],
                    actionable_suggestions=["Review AI analysis"],
                    created_at=datetime.now(),
                )
                insights.append(insight)

        except Exception as e:
            logger.error(f"Error processing AI insights: {str(e)}")

        return insights

    async def _analyze_context_importance(self) -> Dict[str, Any]:
        """Analyze importance of stored context elements"""
        # Simplified importance analysis
        return {
            "high_importance": len(self.proactive_contexts),
            "medium_importance": len(self.context_patterns),
            "low_importance": len(self.context_insights),
            "optimization_opportunities": [
                "Remove expired contexts",
                "Consolidate similar patterns",
            ],
        }

    async def _optimize_context_storage(
        self, importance_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize context storage based on importance analysis"""
        optimized_count = 0

        # Remove expired proactive contexts
        current_time = datetime.now()
        expired_contexts = [
            ctx_id
            for ctx_id, ctx in self.proactive_contexts.items()
            if ctx.expiry_time < current_time
        ]

        for ctx_id in expired_contexts:
            del self.proactive_contexts[ctx_id]
            optimized_count += 1

        # Remove old insights (keep last 50)
        if len(self.context_insights) > 50:
            self.context_insights = self.context_insights[-50:]
            optimized_count += len(self.context_insights) - 50

        return {
            "status": "completed",
            "items_optimized": optimized_count,
            "accuracy_improvement": 0.1 if optimized_count > 0 else 0.0,
        }

    def _build_prediction_context(
        self, current_context: Dict[str, Any], user_profile: UserBehaviorProfile
    ) -> str:
        """Build context for user need prediction"""
        return f"""
USER_NEED_PREDICTION_REQUEST

CURRENT_CONTEXT:
{json.dumps(current_context, indent=2)}

USER_PROFILE:
  Interaction Patterns: {len(user_profile.interaction_patterns)}
  Preferred Types: {user_profile.preferred_context_types}
  Communication Style: {user_profile.communication_style}
  Learning Preferences: {user_profile.learning_preferences}

AVAILABLE_PATTERNS: {len(self.context_patterns)}
RECENT_INSIGHTS: {len(self.context_insights[-3:])}

Predict user needs based on:
1. Current context and activity
2. Historical interaction patterns
3. Time of day and usage patterns
4. Recent behavior changes
5. Workflow optimization opportunities
"""

    async def _get_ai_predictions(self, context: str) -> str:
        """Get AI predictions for user needs"""
        full_prompt = f"{self.prompt_template}\n\n{context}\n\nProvide predictions:"

        try:
            response = await self.ollama_client.generate_response(prompt=full_prompt)
            return response
        except Exception as e:
            logger.error(f"Error getting AI predictions: {str(e)}")
            return "[]"

    def _process_ai_predictions(self, ai_response: str) -> List[Dict[str, Any]]:
        """Process AI predictions response"""
        try:
            if ai_response.strip().startswith("["):
                return json.loads(ai_response)
            else:
                # Fallback: create basic prediction
                return [
                    {
                        "prediction_type": "general_assistance",
                        "description": "User may need general assistance",
                        "confidence": 0.5,
                        "suggested_actions": ["Offer help", "Check user status"],
                    }
                ]
        except Exception as e:
            logger.error(f"Error processing AI predictions: {str(e)}")
            return []

    def _create_fallback_analysis(self) -> str:
        """Create fallback analysis when AI fails"""
        return json.dumps(
            {
                "patterns": [
                    {
                        "id": "fallback_pattern",
                        "type": "general_usage",
                        "description": "General usage pattern detected",
                        "confidence": 0.5,
                    }
                ],
                "insights": [
                    {
                        "type": "system_status",
                        "description": "AI analysis temporarily unavailable",
                        "confidence": 1.0,
                    }
                ],
                "recommendations": [
                    "Continue normal usage",
                    "AI analysis will resume when available",
                ],
            }
        )

    def _extract_patterns_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract patterns from AI text response"""
        # Simplified pattern extraction
        patterns = []
        if "pattern" in text.lower():
            patterns.append(
                {
                    "id": f"text_pattern_{uuid.uuid4().hex[:8]}",
                    "type": "text_detected",
                    "description": "Pattern detected in text analysis",
                    "confidence": 0.6,
                }
            )
        return patterns

    def _extract_insights_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract insights from AI text response"""
        # Simplified insight extraction
        insights = []
        if "insight" in text.lower() or "recommend" in text.lower():
            insights.append(
                {
                    "type": "text_insight",
                    "description": text[:100] + "..." if len(text) > 100 else text,
                    "confidence": 0.6,
                }
            )
        return insights

    def _extract_recommendations_from_text(self, text: str) -> List[str]:
        """Extract recommendations from AI text response"""
        # Simplified recommendation extraction
        recommendations = []
        if "suggest" in text.lower() or "recommend" in text.lower():
            recommendations.append("Review AI analysis for detailed recommendations")
        return recommendations

    def _parse_proactive_context_text(self, text: str) -> Dict[str, Any]:
        """Parse proactive context from text response"""
        return {
            "content": text,
            "relevance_score": 0.6,
            "triggers": ["text_analysis"],
            "suggestions": ["Review generated content"],
        }

    def get_advanced_metrics(self) -> Dict[str, Any]:
        """Get advanced context management metrics"""
        return {
            **self.metrics,
            "active_patterns": len(self.context_patterns),
            "stored_insights": len(self.context_insights),
            "proactive_contexts": len(self.proactive_contexts),
            "user_profiles": len(self.user_behavior_profiles),
            "last_analysis": datetime.now().isoformat(),
        }

    def get_user_context_summary(self, user_id: str = "default_user") -> Dict[str, Any]:
        """Get comprehensive context summary for user"""
        user_profile = self.user_behavior_profiles.get(user_id)

        return {
            "user_id": user_id,
            "profile_exists": user_profile is not None,
            "interaction_patterns": (
                len(user_profile.interaction_patterns) if user_profile else 0
            ),
            "preferred_types": (
                user_profile.preferred_context_types if user_profile else []
            ),
            "recent_insights": len(
                [
                    i
                    for i in self.context_insights
                    if i.created_at > datetime.now() - timedelta(days=1)
                ]
            ),
            "active_proactive_contexts": len(
                [
                    c
                    for c in self.proactive_contexts.values()
                    if c.expiry_time > datetime.now()
                ]
            ),
            "context_health": "good" if user_profile else "needs_initialization",
        }
