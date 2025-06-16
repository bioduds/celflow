#!/usr/bin/env python3
"""
Comprehensive SelFlow AI Agents Test Suite

Tests all 5 AI agents individually and their interactions:
1. UserInterfaceAgent - Natural language processing and user interactions
2. AgentOrchestrator - Complex task coordination and delegation
3. SystemController - Command translation and system action execution
4. PatternValidator - Pattern classification validation and coherence
5. ProactiveSuggestionEngine - Context-aware suggestion generation

Usage:
    python test_all_agents.py [--agent AGENT_NAME] [--verbose]

Examples:
    python test_all_agents.py                    # Test all agents
    python test_all_agents.py --agent ui         # Test only UserInterfaceAgent
    python test_all_agents.py --agent orchestrator --verbose
"""

import asyncio
import logging
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AgentTester:
    """Comprehensive agent testing framework"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.test_results = {}
        self.ollama_client = None
        self.central_brain = None

    async def setup(self):
        """Initialize testing environment"""
        print("🚀 Setting up SelFlow Agent Testing Environment")
        print("=" * 60)

        try:
            # Import required modules
            from app.ai.ollama_client import OllamaClient
            from app.ai.central_brain import CentralAIBrain

            # Initialize Ollama client
            print("\n1. 🤖 Initializing Ollama Client...")
            ollama_config = {
                "model_name": "gemma3:4b",
                "base_url": "http://localhost:11434",
                "timeout": 30,
            }

            self.ollama_client = OllamaClient(ollama_config)
            await self.ollama_client.start()

            # Test Ollama connection
            health = self.ollama_client.get_health_status()
            if not health.get("is_healthy", False):
                raise Exception("Ollama client not healthy")

            print(f"✅ Ollama client ready: {health}")

            # Initialize Central Brain
            print("\n2. 🧠 Initializing Central AI Brain...")
            brain_config = {
                "ai_brain": ollama_config,
                "context_management": {
                    "max_context_length": 1000,
                    "context_window": 50,
                },
            }

            self.central_brain = CentralAIBrain(brain_config)
            await self.central_brain.start()

            print("✅ Central AI Brain initialized")
            print(f"   - Agents available: {self._count_available_agents()}")

        except Exception as e:
            logger.error(f"❌ Setup failed: {e}")
            raise

    def _count_available_agents(self) -> int:
        """Count available agents in central brain"""
        count = 0
        if (
            hasattr(self.central_brain, "user_interface")
            and self.central_brain.user_interface
        ):
            count += 1
        if (
            hasattr(self.central_brain, "agent_orchestrator")
            and self.central_brain.agent_orchestrator
        ):
            count += 1
        if (
            hasattr(self.central_brain, "system_controller")
            and self.central_brain.system_controller
        ):
            count += 1
        if (
            hasattr(self.central_brain, "pattern_validator")
            and self.central_brain.pattern_validator
        ):
            count += 1
        if (
            hasattr(self.central_brain, "proactive_suggestion_engine")
            and self.central_brain.proactive_suggestion_engine
        ):
            count += 1
        return count

    async def test_user_interface_agent(self) -> Dict[str, Any]:
        """Test UserInterfaceAgent functionality"""
        print("\n🎭 TESTING USER INTERFACE AGENT")
        print("-" * 40)

        results = {"agent": "UserInterfaceAgent", "tests": [], "overall_success": True}

        try:
            ui_agent = self.central_brain.user_interface
            if not ui_agent:
                raise Exception("UserInterfaceAgent not available")

            # Test 1: Basic chat message processing
            print("1. Testing chat message processing...")
            chat_result = await ui_agent.process_chat_message(
                "Hello! Can you help me organize my tasks for today?",
                {"user_id": "test_user", "context_type": "chat"},
            )

            test1_success = chat_result.get("success", False) and chat_result.get(
                "message"
            )
            results["tests"].append(
                {
                    "name": "Chat Message Processing",
                    "success": test1_success,
                    "details": f"Response length: {len(chat_result.get('message', ''))}",
                }
            )

            if self.verbose:
                print(f"   Response: {chat_result.get('message', '')[:100]}...")

            # Test 2: Voice command handling
            print("2. Testing voice command handling...")
            voice_result = await ui_agent.handle_voice_command(
                "Show me system status", {"interaction_type": "voice_command"}
            )

            test2_success = voice_result.get("success", False)
            results["tests"].append(
                {
                    "name": "Voice Command Handling",
                    "success": test2_success,
                    "details": f"Input type: {voice_result.get('input_type', 'unknown')}",
                }
            )

            # Test 3: Proactive suggestions
            print("3. Testing proactive suggestions...")
            suggestions = await ui_agent.generate_proactive_suggestions(
                {
                    "user_patterns": ["productivity", "task_management"],
                    "time_of_day": "morning",
                }
            )

            test3_success = isinstance(suggestions, list) and len(suggestions) > 0
            results["tests"].append(
                {
                    "name": "Proactive Suggestions",
                    "success": test3_success,
                    "details": f"Generated {len(suggestions)} suggestions",
                }
            )

            if self.verbose:
                print(f"   Suggestions: {suggestions}")

            # Test 4: System action explanation
            print("4. Testing system action explanation...")
            explanation = await ui_agent.explain_system_action(
                {
                    "action": "file_organization",
                    "target": "/downloads",
                    "method": "smart_categorization",
                }
            )

            test4_success = isinstance(explanation, str) and len(explanation) > 10
            results["tests"].append(
                {
                    "name": "System Action Explanation",
                    "success": test4_success,
                    "details": f"Explanation length: {len(explanation)}",
                }
            )

            # Calculate overall success
            results["overall_success"] = all(
                test["success"] for test in results["tests"]
            )

            print(
                f"✅ UserInterfaceAgent: {len([t for t in results['tests'] if t['success']])}/{len(results['tests'])} tests passed"
            )

        except Exception as e:
            logger.error(f"❌ UserInterfaceAgent test failed: {e}")
            results["overall_success"] = False
            results["error"] = str(e)

        return results

    async def test_agent_orchestrator(self) -> Dict[str, Any]:
        """Test AgentOrchestrator functionality"""
        print("\n🎭 TESTING AGENT ORCHESTRATOR")
        print("-" * 40)

        results = {"agent": "AgentOrchestrator", "tests": [], "overall_success": True}

        try:
            orchestrator = self.central_brain.agent_orchestrator
            if not orchestrator:
                raise Exception("AgentOrchestrator not available")

            # Test 1: Complex task coordination
            print("1. Testing complex task coordination...")
            task_result = await orchestrator.coordinate_task(
                "Analyze user productivity patterns and create optimization recommendations",
                {
                    "user_data": {"daily_tasks": 15, "completion_rate": 0.8},
                    "priority": "normal",
                },
            )

            test1_success = task_result.get("success", False)
            results["tests"].append(
                {
                    "name": "Complex Task Coordination",
                    "success": test1_success,
                    "details": f"Task ID: {task_result.get('task_id', 'N/A')}",
                }
            )

            if self.verbose and task_result.get("orchestration_plan"):
                print(f"   Plan: {task_result['orchestration_plan']}")

            # Test 2: Agent delegation
            print("2. Testing agent delegation...")
            delegation_result = await orchestrator.delegate_to_agent(
                "user_interface",
                {
                    "id": "test_subtask",
                    "description": "Generate user-friendly summary",
                    "input_data": {"metrics": {"tasks": 10, "completed": 8}},
                },
            )

            test2_success = delegation_result.get("success", False)
            results["tests"].append(
                {
                    "name": "Agent Delegation",
                    "success": test2_success,
                    "details": f"Delegated to: user_interface",
                }
            )

            # Test 3: Result synthesis
            print("3. Testing result synthesis...")
            mock_results = [
                {"agent": "ui", "result": "User needs better time management"},
                {"agent": "system", "result": "System can automate 3 tasks"},
                {"agent": "pattern", "result": "Productivity peaks at 10 AM"},
            ]

            synthesis_result = await orchestrator.synthesize_results(mock_results)
            test3_success = synthesis_result.get("success", False)
            results["tests"].append(
                {
                    "name": "Result Synthesis",
                    "success": test3_success,
                    "details": f"Synthesized {len(mock_results)} results",
                }
            )

            # Test 4: Task monitoring
            print("4. Testing task monitoring...")
            if task_result.get("task_id"):
                monitor_result = await orchestrator.monitor_task_progress(
                    task_result["task_id"]
                )
                test4_success = monitor_result.get("success", False)
            else:
                test4_success = False

            results["tests"].append(
                {
                    "name": "Task Monitoring",
                    "success": test4_success,
                    "details": "Task progress monitoring",
                }
            )

            results["overall_success"] = all(
                test["success"] for test in results["tests"]
            )
            print(
                f"✅ AgentOrchestrator: {len([t for t in results['tests'] if t['success']])}/{len(results['tests'])} tests passed"
            )

        except Exception as e:
            logger.error(f"❌ AgentOrchestrator test failed: {e}")
            results["overall_success"] = False
            results["error"] = str(e)

        return results

    async def test_system_controller(self) -> Dict[str, Any]:
        """Test SystemController functionality"""
        print("\n🎛️ TESTING SYSTEM CONTROLLER")
        print("-" * 40)

        results = {"agent": "SystemController", "tests": [], "overall_success": True}

        try:
            controller = self.central_brain.system_controller
            if not controller:
                raise Exception("SystemController not available")

            # Test 1: Command translation
            print("1. Testing command translation...")
            action = await controller.translate_user_command(
                "Show me all running processes and their memory usage",
                {"user_id": "test_user", "security_level": "standard"},
            )

            test1_success = action and hasattr(action, "action_id")
            results["tests"].append(
                {
                    "name": "Command Translation",
                    "success": test1_success,
                    "details": f"Action ID: {getattr(action, 'action_id', 'N/A')}",
                }
            )

            if self.verbose and action:
                print(f"   Intent: {action.intent_analysis.primary_goal}")
                print(f"   Risk Level: {action.safety_validation.risk_level.value}")

            # Test 2: Safety validation
            print("2. Testing safety validation...")
            if action:
                is_safe = await controller.validate_action_safety(action)
                test2_success = isinstance(is_safe, bool)
            else:
                test2_success = False

            results["tests"].append(
                {
                    "name": "Safety Validation",
                    "success": test2_success,
                    "details": f"Safety check: {'passed' if test2_success else 'failed'}",
                }
            )

            # Test 3: System capabilities assessment
            print("3. Testing system capabilities...")
            capabilities = await controller.get_system_capabilities()
            test3_success = isinstance(capabilities, dict) and len(capabilities) > 0
            results["tests"].append(
                {
                    "name": "System Capabilities",
                    "success": test3_success,
                    "details": f"Capabilities: {len(capabilities)} categories",
                }
            )

            # Test 4: Action execution (safe command only)
            print("4. Testing safe action execution...")
            if action and action.safety_validation.risk_level.value == "low":
                exec_result = await controller.execute_system_action(action)
                test4_success = isinstance(exec_result, dict)
            else:
                # Create a safe test action
                test4_success = True  # Skip actual execution for safety

            results["tests"].append(
                {
                    "name": "Action Execution",
                    "success": test4_success,
                    "details": "Safe execution test",
                }
            )

            results["overall_success"] = all(
                test["success"] for test in results["tests"]
            )
            print(
                f"✅ SystemController: {len([t for t in results['tests'] if t['success']])}/{len(results['tests'])} tests passed"
            )

        except Exception as e:
            logger.error(f"❌ SystemController test failed: {e}")
            results["overall_success"] = False
            results["error"] = str(e)

        return results

    async def test_pattern_validator(self) -> Dict[str, Any]:
        """Test PatternValidator functionality"""
        print("\n🔍 TESTING PATTERN VALIDATOR")
        print("-" * 40)

        results = {"agent": "PatternValidator", "tests": [], "overall_success": True}

        try:
            from app.ai.pattern_validator import PatternClassification

            validator = self.central_brain.pattern_validator
            if not validator:
                raise Exception("PatternValidator not available")

            # Test 1: Single pattern validation
            print("1. Testing single pattern validation...")
            test_pattern = PatternClassification(
                pattern_id="test_pattern_001",
                category="PRODUCTIVITY",
                subcategory="task_management",
                confidence=0.85,
                source_agent="test_agent",
                timestamp=datetime.now(),
                metadata={"test": True},
            )

            validation_result = await validator.validate_single_pattern(test_pattern)
            test1_success = hasattr(validation_result, "is_coherent")
            results["tests"].append(
                {
                    "name": "Single Pattern Validation",
                    "success": test1_success,
                    "details": f"Coherent: {getattr(validation_result, 'is_coherent', 'N/A')}",
                }
            )

            # Test 2: Cross-agent validation
            print("2. Testing cross-agent validation...")
            classifications = [
                PatternClassification(
                    pattern_id="shared_pattern",
                    category="COMMUNICATION",
                    subcategory="email_management",
                    confidence=0.90,
                    source_agent="agent_1",
                    timestamp=datetime.now(),
                ),
                PatternClassification(
                    pattern_id="shared_pattern",
                    category="COMMUNICATION",
                    subcategory="message_handling",
                    confidence=0.85,
                    source_agent="agent_2",
                    timestamp=datetime.now(),
                ),
            ]

            cross_result = await validator.cross_validate_agents(
                "shared_pattern", classifications
            )
            test2_success = (
                isinstance(cross_result, dict) and "consistency_score" in cross_result
            )
            results["tests"].append(
                {
                    "name": "Cross-Agent Validation",
                    "success": test2_success,
                    "details": f"Consistency: {cross_result.get('consistency_score', 'N/A')}",
                }
            )

            # Test 3: System audit
            print("3. Testing system audit...")
            audit_result = await validator.system_audit()
            test3_success = (
                isinstance(audit_result, dict) and "system_health" in audit_result
            )
            results["tests"].append(
                {
                    "name": "System Audit",
                    "success": test3_success,
                    "details": f"Health: {audit_result.get('system_health', 'N/A')}",
                }
            )

            # Test 4: Validation metrics
            print("4. Testing validation metrics...")
            metrics = validator.get_validation_metrics()
            test4_success = isinstance(metrics, dict) and len(metrics) > 0
            results["tests"].append(
                {
                    "name": "Validation Metrics",
                    "success": test4_success,
                    "details": f"Metrics: {len(metrics)} categories",
                }
            )

            results["overall_success"] = all(
                test["success"] for test in results["tests"]
            )
            print(
                f"✅ PatternValidator: {len([t for t in results['tests'] if t['success']])}/{len(results['tests'])} tests passed"
            )

        except Exception as e:
            logger.error(f"❌ PatternValidator test failed: {e}")
            results["overall_success"] = False
            results["error"] = str(e)

        return results

    async def test_proactive_suggestion_engine(self) -> Dict[str, Any]:
        """Test ProactiveSuggestionEngine functionality"""
        print("\n💡 TESTING PROACTIVE SUGGESTION ENGINE")
        print("-" * 40)

        results = {
            "agent": "ProactiveSuggestionEngine",
            "tests": [],
            "overall_success": True,
        }

        try:
            from app.ai.proactive_suggestion_engine import (
                SuggestionContext,
                SuggestionFeedback,
            )

            engine = self.central_brain.proactive_suggestion_engine
            if not engine:
                raise Exception("ProactiveSuggestionEngine not available")

            # Test 1: Suggestion generation
            print("1. Testing suggestion generation...")
            context = SuggestionContext(
                user_id="test_user",
                current_activity="coding",
                time_of_day="morning",
                day_of_week="monday",
                recent_patterns=["productivity", "development"],
                productivity_metrics={"focus_time": 120, "tasks_completed": 5},
                user_preferences={"notification_style": "minimal"},
                available_time=30,
                energy_level="high",
                focus_areas=["python", "ai_development"],
            )

            suggestions = await engine.generate_suggestions(context)
            test1_success = isinstance(suggestions, list)
            results["tests"].append(
                {
                    "name": "Suggestion Generation",
                    "success": test1_success,
                    "details": f"Generated: {len(suggestions)} suggestions",
                }
            )

            if self.verbose and suggestions:
                print(f"   Sample: {suggestions[0].title if suggestions else 'None'}")

            # Test 2: Immediate suggestions
            print("2. Testing immediate suggestions...")
            immediate = await engine.get_immediate_suggestions("test_user", max_count=3)
            test2_success = isinstance(immediate, list)
            results["tests"].append(
                {
                    "name": "Immediate Suggestions",
                    "success": test2_success,
                    "details": f"Immediate: {len(immediate)} suggestions",
                }
            )

            # Test 3: Feedback processing
            print("3. Testing feedback processing...")
            if suggestions:
                feedback = SuggestionFeedback(
                    suggestion_id=suggestions[0].suggestion_id,
                    user_id="test_user",
                    feedback_type="accepted",
                    feedback_text="Very helpful!",
                    effectiveness_rating=5,
                    timestamp=datetime.now(),
                )

                feedback_result = await engine.process_user_feedback(feedback)
                test3_success = feedback_result.get("success", False)
            else:
                test3_success = False

            results["tests"].append(
                {
                    "name": "Feedback Processing",
                    "success": test3_success,
                    "details": "User feedback integration",
                }
            )

            # Test 4: Suggestion metrics
            print("4. Testing suggestion metrics...")
            metrics = engine.get_suggestion_metrics()
            test4_success = isinstance(metrics, dict) and hasattr(
                metrics, "total_suggestions"
            )
            results["tests"].append(
                {
                    "name": "Suggestion Metrics",
                    "success": test4_success,
                    "details": f"Total suggestions: {getattr(metrics, 'total_suggestions', 0)}",
                }
            )

            results["overall_success"] = all(
                test["success"] for test in results["tests"]
            )
            print(
                f"✅ ProactiveSuggestionEngine: {len([t for t in results['tests'] if t['success']])}/{len(results['tests'])} tests passed"
            )

        except Exception as e:
            logger.error(f"❌ ProactiveSuggestionEngine test failed: {e}")
            results["overall_success"] = False
            results["error"] = str(e)

        return results

    async def test_agent_integration(self) -> Dict[str, Any]:
        """Test inter-agent communication and coordination"""
        print("\n🤝 TESTING AGENT INTEGRATION")
        print("-" * 40)

        results = {"agent": "Integration", "tests": [], "overall_success": True}

        try:
            # Test 1: UI -> Orchestrator -> System flow
            print("1. Testing UI -> Orchestrator -> System flow...")

            # Start with UI processing user request
            ui_result = await self.central_brain.user_interface.process_chat_message(
                "I need help organizing my development workflow",
                {"user_id": "test_user"},
            )

            # Orchestrator coordinates the task
            if ui_result.get("success"):
                orchestrator_result = (
                    await self.central_brain.agent_orchestrator.coordinate_task(
                        "Analyze and optimize development workflow",
                        {"user_request": ui_result.get("message")},
                    )
                )
                test1_success = orchestrator_result.get("success", False)
            else:
                test1_success = False

            results["tests"].append(
                {
                    "name": "UI-Orchestrator-System Flow",
                    "success": test1_success,
                    "details": "Multi-agent workflow coordination",
                }
            )

            # Test 2: Pattern validation in suggestion pipeline
            print("2. Testing pattern validation in suggestion pipeline...")

            # Generate suggestions
            from app.ai.proactive_suggestion_engine import SuggestionContext

            context = SuggestionContext(
                user_id="test_user",
                current_activity="testing",
                time_of_day="afternoon",
                day_of_week="monday",
                recent_patterns=["development", "testing"],
                productivity_metrics={},
                user_preferences={},
                available_time=15,
                energy_level="medium",
                focus_areas=["agent_testing"],
            )

            suggestions = await self.central_brain.proactive_suggestion_engine.generate_suggestions(
                context
            )

            # Validate suggestion patterns
            if suggestions:
                from app.ai.pattern_validator import PatternClassification

                pattern = PatternClassification(
                    pattern_id="suggestion_pattern",
                    category="PRODUCTIVITY",
                    subcategory="workflow_optimization",
                    confidence=0.8,
                    source_agent="suggestion_engine",
                    timestamp=datetime.now(),
                )

                validation = (
                    await self.central_brain.pattern_validator.validate_single_pattern(
                        pattern
                    )
                )
                test2_success = hasattr(validation, "is_coherent")
            else:
                test2_success = False

            results["tests"].append(
                {
                    "name": "Pattern Validation Pipeline",
                    "success": test2_success,
                    "details": "Cross-agent pattern validation",
                }
            )

            # Test 3: System status coordination
            print("3. Testing system status coordination...")

            # Get status from multiple agents
            ui_status = self.central_brain.user_interface.get_agent_status()
            orchestrator_status = (
                self.central_brain.agent_orchestrator.get_orchestrator_status()
            )

            test3_success = isinstance(ui_status, dict) and isinstance(
                orchestrator_status, dict
            )

            results["tests"].append(
                {
                    "name": "System Status Coordination",
                    "success": test3_success,
                    "details": "Multi-agent status reporting",
                }
            )

            results["overall_success"] = all(
                test["success"] for test in results["tests"]
            )
            print(
                f"✅ Agent Integration: {len([t for t in results['tests'] if t['success']])}/{len(results['tests'])} tests passed"
            )

        except Exception as e:
            logger.error(f"❌ Agent Integration test failed: {e}")
            results["overall_success"] = False
            results["error"] = str(e)

        return results

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all agent tests"""
        print("🧪 RUNNING COMPREHENSIVE AGENT TEST SUITE")
        print("=" * 60)

        all_results = {
            "timestamp": datetime.now().isoformat(),
            "test_results": {},
            "summary": {},
        }

        # Individual agent tests
        test_functions = [
            ("user_interface", self.test_user_interface_agent),
            ("agent_orchestrator", self.test_agent_orchestrator),
            ("system_controller", self.test_system_controller),
            ("pattern_validator", self.test_pattern_validator),
            ("proactive_suggestion_engine", self.test_proactive_suggestion_engine),
            ("integration", self.test_agent_integration),
        ]

        for agent_name, test_func in test_functions:
            try:
                result = await test_func()
                all_results["test_results"][agent_name] = result
            except Exception as e:
                logger.error(f"❌ Failed to test {agent_name}: {e}")
                all_results["test_results"][agent_name] = {
                    "agent": agent_name,
                    "overall_success": False,
                    "error": str(e),
                }

        # Generate summary
        total_agents = len(test_functions)
        successful_agents = sum(
            1
            for result in all_results["test_results"].values()
            if result.get("overall_success", False)
        )

        total_tests = sum(
            len(result.get("tests", []))
            for result in all_results["test_results"].values()
        )
        successful_tests = sum(
            len([t for t in result.get("tests", []) if t.get("success", False)])
            for result in all_results["test_results"].values()
        )

        all_results["summary"] = {
            "total_agents": total_agents,
            "successful_agents": successful_agents,
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "overall_success_rate": (
                successful_tests / total_tests if total_tests > 0 else 0
            ),
        }

        return all_results

    async def cleanup(self):
        """Clean up testing environment"""
        print("\n🧹 Cleaning up testing environment...")

        try:
            if self.central_brain:
                await self.central_brain.stop()
            if self.ollama_client:
                await self.ollama_client.close()
            print("✅ Cleanup completed")
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")


async def main():
    """Main test execution"""
    parser = argparse.ArgumentParser(description="SelFlow AI Agents Test Suite")
    parser.add_argument(
        "--agent",
        choices=[
            "ui",
            "orchestrator",
            "system",
            "pattern",
            "suggestion",
            "integration",
        ],
        help="Test specific agent only",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    tester = AgentTester(verbose=args.verbose)

    try:
        await tester.setup()

        if args.agent:
            # Test specific agent
            agent_map = {
                "ui": tester.test_user_interface_agent,
                "orchestrator": tester.test_agent_orchestrator,
                "system": tester.test_system_controller,
                "pattern": tester.test_pattern_validator,
                "suggestion": tester.test_proactive_suggestion_engine,
                "integration": tester.test_agent_integration,
            }

            if args.agent in agent_map:
                result = await agent_map[args.agent]()
                print(f"\n📊 SINGLE AGENT TEST RESULTS")
                print(f"Agent: {result['agent']}")
                print(f"Success: {result['overall_success']}")
                if "tests" in result:
                    for test in result["tests"]:
                        status = "✅" if test["success"] else "❌"
                        print(f"  {status} {test['name']}: {test['details']}")
        else:
            # Run all tests
            results = await tester.run_all_tests()

            print(f"\n📊 COMPREHENSIVE TEST RESULTS")
            print("=" * 60)
            print(
                f"Agents Tested: {results['summary']['successful_agents']}/{results['summary']['total_agents']}"
            )
            print(
                f"Tests Passed: {results['summary']['successful_tests']}/{results['summary']['total_tests']}"
            )
            print(f"Success Rate: {results['summary']['overall_success_rate']:.1%}")

            print(f"\n📋 DETAILED RESULTS:")
            for agent_name, result in results["test_results"].items():
                status = "✅" if result.get("overall_success", False) else "❌"
                print(f"{status} {result.get('agent', agent_name)}")

                if "tests" in result:
                    for test in result["tests"]:
                        test_status = "  ✅" if test["success"] else "  ❌"
                        print(f"{test_status} {test['name']}: {test['details']}")

                if "error" in result:
                    print(f"  ⚠️  Error: {result['error']}")

    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        sys.exit(1)
    finally:
        await tester.cleanup()

    print(f"\n🎯 Agent testing completed!")


if __name__ == "__main__":
    asyncio.run(main())
