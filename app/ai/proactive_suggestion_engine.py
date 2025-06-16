"""
Proactive Suggestion Engine - AI-Powered User Assistance

This module provides intelligent, proactive suggestions based on:
- User behavior patterns and preferences
- Context analysis and prediction
- Task optimization opportunities
- Learning and productivity insights
- Workflow enhancement recommendations
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import uuid
from collections import defaultdict, deque

from .ollama_client import OllamaClient
from .advanced_context_manager import AdvancedContextManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SuggestionType(Enum):
    """Types of proactive suggestions"""

    PRODUCTIVITY = "productivity"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    LEARNING_OPPORTUNITY = "learning_opportunity"
    TASK_REMINDER = "task_reminder"
    HABIT_FORMATION = "habit_formation"
    SKILL_DEVELOPMENT = "skill_development"
    TIME_MANAGEMENT = "time_management"
    HEALTH_WELLNESS = "health_wellness"
    CREATIVE_INSPIRATION = "creative_inspiration"
    SYSTEM_OPTIMIZATION = "system_optimization"


class SuggestionPriority(Enum):
    """Priority levels for suggestions"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class SuggestionTiming(Enum):
    """When to deliver suggestions"""

    IMMEDIATE = "immediate"
    NEXT_SESSION = "next_session"
    DAILY_DIGEST = "daily_digest"
    WEEKLY_SUMMARY = "weekly_summary"
    CONTEXTUAL_TRIGGER = "contextual_trigger"


class SuggestionStatus(Enum):
    """Status of suggestions"""

    PENDING = "pending"
    DELIVERED = "delivered"
    ACCEPTED = "accepted"
    DISMISSED = "dismissed"
    EXPIRED = "expired"


@dataclass
class ProactiveSuggestion:
    """A proactive suggestion for the user"""

    suggestion_id: str
    suggestion_type: SuggestionType
    priority: SuggestionPriority
    timing: SuggestionTiming
    title: str
    description: str
    rationale: str
    actionable_steps: List[str]
    expected_benefit: str
    confidence_score: float
    created_at: datetime
    expires_at: datetime
    status: SuggestionStatus
    context_triggers: List[str]
    user_feedback: Optional[str] = None
    effectiveness_score: Optional[float] = None


@dataclass
class SuggestionContext:
    """Context information for suggestion generation"""

    user_id: str
    current_activity: str
    time_of_day: str
    day_of_week: str
    recent_patterns: List[str]
    productivity_metrics: Dict[str, Any]
    user_preferences: Dict[str, Any]
    available_time: int  # minutes
    energy_level: str
    focus_areas: List[str]


@dataclass
class SuggestionFeedback:
    """User feedback on suggestions"""

    suggestion_id: str
    user_id: str
    feedback_type: str  # accepted, dismissed, modified
    feedback_text: Optional[str]
    effectiveness_rating: Optional[int]  # 1-5 scale
    timestamp: datetime


@dataclass
class SuggestionMetrics:
    """Metrics for suggestion system performance"""

    total_suggestions: int
    delivered_suggestions: int
    accepted_suggestions: int
    dismissed_suggestions: int
    average_confidence: float
    average_effectiveness: float
    user_satisfaction: float
    response_rate: float


class ProactiveSuggestionEngine:
    """
    AI-Powered Proactive Suggestion Engine

    Analyzes user patterns and context to provide intelligent,
    timely suggestions for productivity and workflow optimization.
    """

    def __init__(
        self,
        ollama_client: OllamaClient,
        advanced_context_manager: AdvancedContextManager,
    ):
        """Initialize the Proactive Suggestion Engine"""
        self.ollama_client = ollama_client
        self.advanced_context_manager = advanced_context_manager

        # Suggestion storage
        self.active_suggestions: Dict[str, ProactiveSuggestion] = {}
        self.suggestion_history: List[ProactiveSuggestion] = []
        self.user_feedback: List[SuggestionFeedback] = []

        # Suggestion queues by timing
        self.immediate_queue: deque = deque(maxlen=5)
        self.session_queue: deque = deque(maxlen=10)
        self.daily_queue: deque = deque(maxlen=20)
        self.contextual_triggers: Dict[str, List[str]] = defaultdict(list)

        # Learning and adaptation
        self.user_preferences: Dict[str, Dict[str, Any]] = {}
        self.effectiveness_tracking: Dict[str, List[float]] = defaultdict(list)

        # Configuration
        self.max_daily_suggestions = 10
        self.min_confidence_threshold = 0.6
        self.suggestion_cooldown = timedelta(hours=1)

        # Performance metrics
        self.metrics = SuggestionMetrics(
            total_suggestions=0,
            delivered_suggestions=0,
            accepted_suggestions=0,
            dismissed_suggestions=0,
            average_confidence=0.0,
            average_effectiveness=0.0,
            user_satisfaction=0.0,
            response_rate=0.0,
        )

        # Load prompt template
        self.prompt_template = self._load_prompt_template()

        logger.info("ProactiveSuggestionEngine initialized successfully")

    def _load_prompt_template(self) -> str:
        """Load the proactive suggestion prompt template"""
        try:
            with open("app/ai/prompts/proactive_suggestions.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.error("Proactive suggestions prompt template not found")
            return "You are a proactive AI assistant. Generate helpful suggestions based on user patterns and context."

    async def generate_suggestions(
        self, context: SuggestionContext
    ) -> List[ProactiveSuggestion]:
        """Generate proactive suggestions based on current context"""
        try:
            # Get user behavior insights
            user_insights = await self._get_user_insights(context.user_id)

            # Build suggestion generation context
            generation_context = self._build_suggestion_context(context, user_insights)

            # Get AI-generated suggestions
            ai_response = await self._get_ai_suggestions(generation_context)

            # Process and validate suggestions
            suggestions = self._process_ai_suggestions(ai_response, context)

            # Filter and prioritize suggestions
            filtered_suggestions = self._filter_suggestions(suggestions, context)

            # Store suggestions
            for suggestion in filtered_suggestions:
                self.active_suggestions[suggestion.suggestion_id] = suggestion
                self._queue_suggestion(suggestion)

            self.metrics.total_suggestions += len(filtered_suggestions)

            logger.info(
                f"Generated {len(filtered_suggestions)} proactive suggestions for user {context.user_id}"
            )
            return filtered_suggestions

        except Exception as e:
            logger.error(f"Error generating proactive suggestions: {str(e)}")
            return []

    async def get_immediate_suggestions(
        self, user_id: str, max_count: int = 3
    ) -> List[ProactiveSuggestion]:
        """Get immediate suggestions for the user"""
        try:
            suggestions = []

            # Get from immediate queue
            while len(suggestions) < max_count and self.immediate_queue:
                suggestion = self.immediate_queue.popleft()
                if suggestion.status == SuggestionStatus.PENDING:
                    suggestions.append(suggestion)

            # Mark as delivered
            for suggestion in suggestions:
                suggestion.status = SuggestionStatus.DELIVERED
                self.metrics.delivered_suggestions += 1

            logger.info(
                f"Delivered {len(suggestions)} immediate suggestions to user {user_id}"
            )
            return suggestions

        except Exception as e:
            logger.error(f"Error getting immediate suggestions: {str(e)}")
            return []

    async def process_user_feedback(
        self, feedback: SuggestionFeedback
    ) -> Dict[str, Any]:
        """Process user feedback on suggestions"""
        try:
            # Store feedback
            self.user_feedback.append(feedback)

            # Update suggestion status
            if feedback.suggestion_id in self.active_suggestions:
                suggestion = self.active_suggestions[feedback.suggestion_id]

                if feedback.feedback_type == "accepted":
                    suggestion.status = SuggestionStatus.ACCEPTED
                    self.metrics.accepted_suggestions += 1
                elif feedback.feedback_type == "dismissed":
                    suggestion.status = SuggestionStatus.DISMISSED
                    self.metrics.dismissed_suggestions += 1

                # Store effectiveness rating
                if feedback.effectiveness_rating:
                    suggestion.effectiveness_score = feedback.effectiveness_rating / 5.0
                    self.effectiveness_tracking[
                        suggestion.suggestion_type.value
                    ].append(suggestion.effectiveness_score)

                suggestion.user_feedback = feedback.feedback_text

            # Update user preferences based on feedback
            await self._update_user_preferences(feedback)

            # Update metrics
            self._update_metrics()

            logger.info(f"Processed feedback for suggestion {feedback.suggestion_id}")
            return {
                "success": True,
                "message": "Feedback processed successfully",
                "updated_preferences": True,
            }

        except Exception as e:
            logger.error(f"Error processing user feedback: {str(e)}")
            return {"success": False, "error": str(e)}

    async def _get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get user behavior insights from Advanced Context Manager"""
        try:
            # Get user context summary
            context_summary = self.advanced_context_manager.get_user_context_summary(
                user_id
            )

            # Get recent patterns analysis
            patterns_analysis = (
                await self.advanced_context_manager.analyze_interaction_patterns(
                    user_id
                )
            )

            return {
                "context_summary": context_summary,
                "patterns_analysis": patterns_analysis,
                "user_profile": self.advanced_context_manager.user_behavior_profiles.get(
                    user_id
                ),
            }

        except Exception as e:
            logger.error(f"Error getting user insights: {str(e)}")
            return {}

    def _build_suggestion_context(
        self, context: SuggestionContext, user_insights: Dict[str, Any]
    ) -> str:
        """Build context for AI suggestion generation"""
        context_parts = [
            "PROACTIVE_SUGGESTION_REQUEST",
            "",
            "USER_CONTEXT:",
            f"  User ID: {context.user_id}",
            f"  Current Activity: {context.current_activity}",
            f"  Time: {context.time_of_day} on {context.day_of_week}",
            f"  Available Time: {context.available_time} minutes",
            f"  Energy Level: {context.energy_level}",
            f"  Focus Areas: {context.focus_areas}",
            "",
            "RECENT_PATTERNS:",
        ]

        for pattern in context.recent_patterns:
            context_parts.append(f"  - {pattern}")

        context_parts.extend(
            [
                "",
                "PRODUCTIVITY_METRICS:",
                json.dumps(context.productivity_metrics, indent=2),
                "",
                "USER_PREFERENCES:",
                json.dumps(context.user_preferences, indent=2),
                "",
                "SUGGESTION_REQUIREMENTS:",
                "1. Generate 3-5 actionable suggestions",
                "2. Focus on immediate value and relevance",
                "3. Consider user's available time and energy",
                "4. Provide clear rationale and expected benefits",
                "5. Include confidence scores (0.0-1.0)",
                "6. Suggest appropriate timing for each suggestion",
                "",
            ]
        )

        return "\n".join(context_parts)

    async def _get_ai_suggestions(self, context: str) -> str:
        """Get AI-generated suggestions"""
        full_prompt = (
            f"{self.prompt_template}\n\n{context}\n\nGenerate proactive suggestions:"
        )

        try:
            response = await self.ollama_client.generate_response(prompt=full_prompt)
            return response
        except Exception as e:
            logger.error(f"Error getting AI suggestions: {str(e)}")
            return self._create_fallback_suggestions()

    def _process_ai_suggestions(
        self, ai_response: str, context: SuggestionContext
    ) -> List[ProactiveSuggestion]:
        """Process AI suggestions response"""
        suggestions = []

        try:
            if ai_response.strip().startswith("["):
                suggestion_data = json.loads(ai_response)
            else:
                # Try to extract structured data from text
                suggestion_data = self._extract_suggestions_from_text(ai_response)

            for data in suggestion_data:
                suggestion = ProactiveSuggestion(
                    suggestion_id=f"suggestion_{uuid.uuid4().hex[:8]}",
                    suggestion_type=SuggestionType(data.get("type", "productivity")),
                    priority=SuggestionPriority(data.get("priority", "normal")),
                    timing=SuggestionTiming(data.get("timing", "immediate")),
                    title=data.get("title", "Productivity Suggestion"),
                    description=data.get("description", ""),
                    rationale=data.get("rationale", ""),
                    actionable_steps=data.get("actionable_steps", []),
                    expected_benefit=data.get("expected_benefit", ""),
                    confidence_score=data.get("confidence_score", 0.7),
                    created_at=datetime.now(),
                    expires_at=datetime.now() + timedelta(days=1),
                    status=SuggestionStatus.PENDING,
                    context_triggers=data.get("context_triggers", []),
                )
                suggestions.append(suggestion)

        except Exception as e:
            logger.error(f"Error processing AI suggestions: {str(e)}")
            # Create fallback suggestion
            suggestions.append(self._create_fallback_suggestion(context))

        return suggestions

    def _filter_suggestions(
        self, suggestions: List[ProactiveSuggestion], context: SuggestionContext
    ) -> List[ProactiveSuggestion]:
        """Filter and prioritize suggestions"""
        filtered = []

        for suggestion in suggestions:
            # Check confidence threshold
            if suggestion.confidence_score < self.min_confidence_threshold:
                continue

            # Check for duplicates
            if self._is_duplicate_suggestion(suggestion):
                continue

            filtered.append(suggestion)

        # Sort by priority and confidence
        filtered.sort(
            key=lambda s: (s.priority.value, s.confidence_score), reverse=True
        )

        # Limit daily suggestions
        if len(filtered) > self.max_daily_suggestions:
            filtered = filtered[: self.max_daily_suggestions]

        return filtered

    def _queue_suggestion(self, suggestion: ProactiveSuggestion):
        """Queue suggestion based on timing"""
        if suggestion.timing == SuggestionTiming.IMMEDIATE:
            self.immediate_queue.append(suggestion)
        elif suggestion.timing == SuggestionTiming.NEXT_SESSION:
            self.session_queue.append(suggestion)
        elif suggestion.timing == SuggestionTiming.DAILY_DIGEST:
            self.daily_queue.append(suggestion)
        elif suggestion.timing == SuggestionTiming.CONTEXTUAL_TRIGGER:
            for trigger in suggestion.context_triggers:
                self.contextual_triggers[trigger].append(suggestion.suggestion_id)

    def _is_duplicate_suggestion(self, suggestion: ProactiveSuggestion) -> bool:
        """Check if suggestion is a duplicate"""
        for existing in self.active_suggestions.values():
            if (
                existing.suggestion_type == suggestion.suggestion_type
                and existing.title == suggestion.title
                and existing.status == SuggestionStatus.PENDING
            ):
                return True
        return False

    async def _update_user_preferences(self, feedback: SuggestionFeedback):
        """Update user preferences based on feedback"""
        user_id = feedback.user_id

        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                "preferred_types": [],
                "dismissed_types": [],
                "preferred_timing": [],
                "effectiveness_scores": {},
            }

        prefs = self.user_preferences[user_id]

        if feedback.suggestion_id in self.active_suggestions:
            suggestion = self.active_suggestions[feedback.suggestion_id]

            if feedback.feedback_type == "accepted":
                if suggestion.suggestion_type.value not in prefs["preferred_types"]:
                    prefs["preferred_types"].append(suggestion.suggestion_type.value)
                if suggestion.timing.value not in prefs["preferred_timing"]:
                    prefs["preferred_timing"].append(suggestion.timing.value)

            elif feedback.feedback_type == "dismissed":
                if suggestion.suggestion_type.value not in prefs["dismissed_types"]:
                    prefs["dismissed_types"].append(suggestion.suggestion_type.value)

            if feedback.effectiveness_rating:
                prefs["effectiveness_scores"][
                    suggestion.suggestion_type.value
                ] = feedback.effectiveness_rating

    def _update_metrics(self):
        """Update performance metrics"""
        if self.metrics.delivered_suggestions > 0:
            self.metrics.response_rate = (
                len(self.user_feedback) / self.metrics.delivered_suggestions
            )

        if self.active_suggestions:
            confidences = [s.confidence_score for s in self.active_suggestions.values()]
            self.metrics.average_confidence = sum(confidences) / len(confidences)

        effectiveness_scores = []
        for suggestion in self.active_suggestions.values():
            if suggestion.effectiveness_score:
                effectiveness_scores.append(suggestion.effectiveness_score)

        if effectiveness_scores:
            self.metrics.average_effectiveness = sum(effectiveness_scores) / len(
                effectiveness_scores
            )

        # Calculate user satisfaction based on feedback
        positive_feedback = sum(
            1 for f in self.user_feedback if f.feedback_type == "accepted"
        )
        total_feedback = len(self.user_feedback)
        if total_feedback > 0:
            self.metrics.user_satisfaction = positive_feedback / total_feedback

    def _create_fallback_suggestions(self) -> str:
        """Create fallback suggestions when AI fails"""
        return json.dumps(
            [
                {
                    "type": "productivity",
                    "priority": "normal",
                    "timing": "immediate",
                    "title": "Take a Short Break",
                    "description": "Consider taking a 5-minute break to refresh your focus",
                    "rationale": "Regular breaks improve productivity and mental clarity",
                    "actionable_steps": [
                        "Stand up and stretch",
                        "Take deep breaths",
                        "Look away from screen",
                    ],
                    "expected_benefit": "Improved focus and reduced fatigue",
                    "confidence_score": 0.8,
                    "context_triggers": ["long_work_session"],
                }
            ]
        )

    def _extract_suggestions_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract suggestions from AI text response"""
        return [
            {
                "type": "productivity",
                "priority": "normal",
                "timing": "immediate",
                "title": "AI-Generated Suggestion",
                "description": text[:200] + "..." if len(text) > 200 else text,
                "rationale": "Based on AI analysis",
                "actionable_steps": ["Review AI suggestion"],
                "expected_benefit": "Potential productivity improvement",
                "confidence_score": 0.6,
                "context_triggers": ["ai_analysis"],
            }
        ]

    def _create_fallback_suggestion(
        self, context: SuggestionContext
    ) -> ProactiveSuggestion:
        """Create a fallback suggestion"""
        return ProactiveSuggestion(
            suggestion_id=f"fallback_{uuid.uuid4().hex[:8]}",
            suggestion_type=SuggestionType.PRODUCTIVITY,
            priority=SuggestionPriority.NORMAL,
            timing=SuggestionTiming.IMMEDIATE,
            title="Stay Focused",
            description="Continue with your current task and maintain focus",
            rationale="Consistency in task execution leads to better outcomes",
            actionable_steps=["Complete current task", "Minimize distractions"],
            expected_benefit="Task completion and productivity",
            confidence_score=0.7,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=2),
            status=SuggestionStatus.PENDING,
            context_triggers=["focus_session"],
        )

    def get_suggestion_metrics(self) -> Dict[str, Any]:
        """Get comprehensive suggestion system metrics"""
        return {
            "total_suggestions": self.metrics.total_suggestions,
            "delivered_suggestions": self.metrics.delivered_suggestions,
            "accepted_suggestions": self.metrics.accepted_suggestions,
            "dismissed_suggestions": self.metrics.dismissed_suggestions,
            "active_suggestions": len(self.active_suggestions),
            "queued_immediate": len(self.immediate_queue),
            "queued_session": len(self.session_queue),
            "queued_daily": len(self.daily_queue),
            "average_confidence": self.metrics.average_confidence,
            "average_effectiveness": self.metrics.average_effectiveness,
            "user_satisfaction": self.metrics.user_satisfaction,
            "response_rate": self.metrics.response_rate,
            "system_health": (
                "good" if self.metrics.user_satisfaction > 0.6 else "needs_improvement"
            ),
        }

    def get_user_suggestion_summary(self, user_id: str) -> Dict[str, Any]:
        """Get suggestion summary for specific user"""
        user_suggestions = [s for s in self.active_suggestions.values()]
        user_feedback = [f for f in self.user_feedback if f.user_id == user_id]

        return {
            "user_id": user_id,
            "active_suggestions": len(user_suggestions),
            "total_feedback": len(user_feedback),
            "preferences": self.user_preferences.get(user_id, {}),
            "recent_suggestions": [
                {
                    "id": s.suggestion_id,
                    "type": s.suggestion_type.value,
                    "title": s.title,
                    "status": s.status.value,
                    "confidence": s.confidence_score,
                }
                for s in user_suggestions[-5:]
            ],
        }
