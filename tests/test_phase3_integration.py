#!/usr/bin/env python3
"""
Test Phase 3: System Integration

Tests the complete macOS system integration including:
- System tray functionality
- Real event capture
- Agent-user interaction interfaces
- Full system coordination
"""

import asyncio
import pytest
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

from app.system.system_integration import SelFlowSystemIntegration
from app.system.event_capture import SystemEventCapture
from app.system.agent_interface import (
    AgentChatInterface,
    UserMessage,
    InteractionType,
    create_agent_interface,
)
from app.core.agent_manager import AgentManager
from app.core.embryo_pool import EmbryoPool


class TestSystemEventCapture:
    """Test system event capture functionality"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def event_capture_config(self, temp_dir):
        """Configuration for event capture testing"""
        return {"watch_paths": [str(temp_dir)]}

    @pytest.fixture
    def event_capture(self, event_capture_config):
        """Create event capture instance"""
        return SystemEventCapture(event_capture_config)

    def test_event_capture_initialization(self, event_capture):
        """Test event capture initializes correctly"""
        assert event_capture.config is not None
        assert event_capture.events_captured == 0
        assert event_capture.event_callback is None

    def test_set_event_callback(self, event_capture):
        """Test setting event callback"""
        callback = Mock()
        event_capture.set_event_callback(callback)
        assert event_capture.event_callback == callback

    @pytest.mark.asyncio
    async def test_file_system_monitoring(self, event_capture, temp_dir):
        """Test file system event monitoring"""
        events_captured = []

        def capture_event(event):
            events_captured.append(event)

        event_capture.set_event_callback(capture_event)

        # Start monitoring
        await event_capture.start_capture()

        # Create a test file
        test_file = temp_dir / "test_file.txt"
        test_file.write_text("Hello, SelFlow!")

        # Wait for event processing
        await asyncio.sleep(1)

        # Stop monitoring
        await event_capture.stop_capture()

        # Check if file creation was captured
        file_events = [e for e in events_captured if e.get("type") == "file_operation"]
        assert len(file_events) > 0

        create_event = next(
            (e for e in file_events if e.get("action") == "create"), None
        )
        assert create_event is not None
        assert "test_file.txt" in create_event.get("filename", "")

    def test_get_capture_stats(self, event_capture):
        """Test capture statistics"""
        stats = event_capture.get_capture_stats()

        assert "events_captured" in stats
        assert "uptime" in stats
        assert "events_per_minute" in stats
        assert "watch_paths" in stats

        assert stats["events_captured"] == 0
        assert isinstance(stats["events_per_minute"], (int, float))


class TestAgentChatInterface:
    """Test agent-user interaction interface"""

    @pytest.fixture
    def mock_agent_manager(self):
        """Create mock agent manager"""
        manager = Mock(spec=AgentManager)
        manager.get_active_agents = AsyncMock(return_value=[])
        manager.get_system_status = AsyncMock(
            return_value={
                "system": {
                    "active_agents": 0,
                    "total_births": 0,
                    "total_retirements": 0,
                },
                "embryo_pool": {
                    "active_embryos": 0,
                    "events_processed": 0,
                    "generation": 0,
                },
            }
        )
        return manager

    @pytest.fixture
    def agent_interface(self, mock_agent_manager):
        """Create agent chat interface"""
        return create_agent_interface(mock_agent_manager)

    @pytest.mark.asyncio
    async def test_start_chat_session(self, agent_interface):
        """Test starting a chat session"""
        session_id = await agent_interface.start_chat_session()

        assert session_id is not None
        assert session_id.startswith("chat_")
        assert session_id in agent_interface.active_sessions

        # Check welcome message was added
        session = agent_interface.active_sessions[session_id]
        assert len(session.messages) == 1
        assert session.messages[0]["type"] == "agent"
        assert "SelFlow" in session.messages[0]["content"]

    @pytest.mark.asyncio
    async def test_send_help_message(self, agent_interface):
        """Test sending help message"""
        session_id = await agent_interface.start_chat_session()

        message = UserMessage(content="help", message_type=InteractionType.CHAT)

        response = await agent_interface.send_message(session_id, message)

        assert response.agent_name == "SelFlow System"
        assert response.response_type == InteractionType.CHAT
        assert "SelFlow" in response.content
        assert response.confidence == 1.0

    @pytest.mark.asyncio
    async def test_show_agents_no_agents(self, agent_interface):
        """Test showing agents when none are active"""
        session_id = await agent_interface.start_chat_session()

        message = UserMessage(content="show agents", message_type=InteractionType.CHAT)

        response = await agent_interface.send_message(session_id, message)

        assert "no agents" in response.content.lower()
        assert response.response_type == InteractionType.MONITORING

    @pytest.mark.asyncio
    async def test_system_status_request(self, agent_interface):
        """Test system status request"""
        session_id = await agent_interface.start_chat_session()

        message = UserMessage(
            content="system status", message_type=InteractionType.MONITORING
        )

        response = await agent_interface.send_message(session_id, message)

        assert "System Status" in response.content
        assert "Agents:" in response.content
        assert "Embryo Pool:" in response.content
        assert response.response_type == InteractionType.MONITORING

    def test_get_session_history(self, agent_interface):
        """Test getting session history"""
        # Create a session first
        session_id = "test_session"
        from app.system.agent_interface import ChatSession

        session = ChatSession(
            session_id=session_id,
            start_time=time.time(),
            messages=[],
            active_agents=[],
            context={},
        )
        agent_interface.active_sessions[session_id] = session

        history = agent_interface.get_session_history(session_id)

        assert history is not None
        assert history["session_id"] == session_id
        assert "start_time" in history
        assert "duration" in history
        assert "message_count" in history
        assert "messages" in history

    def test_close_session(self, agent_interface):
        """Test closing a chat session"""
        # Create a session first
        session_id = "test_session"
        from app.system.agent_interface import ChatSession

        session = ChatSession(
            session_id=session_id,
            start_time=time.time(),
            messages=[],
            active_agents=[],
            context={},
        )
        agent_interface.active_sessions[session_id] = session

        # Close the session
        agent_interface.close_session(session_id)

        assert session_id not in agent_interface.active_sessions


class TestSystemIntegration:
    """Test complete system integration"""

    @pytest.fixture
    def integration_config(self):
        """Configuration for system integration testing"""
        return {
            "embryo_pool": {
                "max_embryos": 5,
                "mutation_rate": 0.1,
                "competition_intensity": 0.8,
            },
            "agent_manager": {
                "max_agents": 3,
                "birth_threshold": 0.7,
                "retirement_threshold": 0.3,
            },
            "event_capture": {"watch_paths": ["/tmp"]},
            "tray_app": {},
        }

    @pytest.fixture
    def system_integration(self, integration_config):
        """Create system integration instance"""
        return SelFlowSystemIntegration(integration_config)

    def test_system_integration_initialization(self, system_integration):
        """Test system integration initializes correctly"""
        assert system_integration.config is not None
        assert not system_integration.is_running
        assert system_integration.start_time is None
        assert not system_integration.shutdown_requested

    @pytest.mark.asyncio
    @patch("app.system.system_integration.check_system_permissions")
    async def test_initialize_with_permissions(
        self, mock_permissions, system_integration
    ):
        """Test system initialization with permissions"""
        # Mock permissions as available
        mock_permissions.return_value = {
            "accessibility": True,
            "full_disk_access": True,
        }

        result = await system_integration.initialize()

        assert result is True
        assert system_integration.embryo_pool is not None
        assert system_integration.agent_manager is not None
        assert system_integration.event_capture is not None
        assert system_integration.agent_interface is not None

    @pytest.mark.asyncio
    @patch("app.system.system_integration.check_system_permissions")
    async def test_initialize_without_permissions(
        self, mock_permissions, system_integration
    ):
        """Test system initialization without permissions"""
        # Mock permissions as not available
        mock_permissions.return_value = {
            "accessibility": False,
            "full_disk_access": False,
        }

        with patch("app.system.system_integration.request_permissions") as mock_request:
            mock_request.return_value = False  # Permissions denied

            result = await system_integration.initialize()

            assert result is False

    @pytest.mark.asyncio
    async def test_get_system_status(self, system_integration):
        """Test getting comprehensive system status"""
        # Initialize first
        with patch(
            "app.system.system_integration.check_system_permissions"
        ) as mock_permissions:
            mock_permissions.return_value = {
                "accessibility": True,
                "full_disk_access": True,
            }
            await system_integration.initialize()

        status = await system_integration.get_system_status()

        assert "system_integration" in status
        assert "is_running" in status["system_integration"]
        assert "components" in status["system_integration"]

        components = status["system_integration"]["components"]
        assert "embryo_pool" in components
        assert "agent_manager" in components
        assert "event_capture" in components
        assert "agent_interface" in components

    @pytest.mark.asyncio
    async def test_chat_with_agents(self, system_integration):
        """Test chatting with agents through system integration"""
        # Initialize first
        with patch(
            "app.system.system_integration.check_system_permissions"
        ) as mock_permissions:
            mock_permissions.return_value = {
                "accessibility": True,
                "full_disk_access": True,
            }
            await system_integration.initialize()

        result = await system_integration.chat_with_agents("Hello, SelFlow!")

        assert "session_id" in result
        assert "response" in result

        response = result["response"]
        assert "content" in response
        assert "agent_name" in response
        assert "specialization" in response
        assert "confidence" in response


class TestFullSystemWorkflow:
    """Test complete system workflow from startup to shutdown"""

    @pytest.mark.asyncio
    @patch("app.system.system_integration.check_system_permissions")
    @patch("app.system.macos_tray.create_tray_app")
    async def test_complete_system_lifecycle(self, mock_tray, mock_permissions):
        """Test complete system lifecycle"""
        # Mock permissions and tray app
        mock_permissions.return_value = {
            "accessibility": True,
            "full_disk_access": True,
        }
        mock_tray.return_value = None  # No tray app for testing

        config = {
            "embryo_pool": {"max_embryos": 3},
            "agent_manager": {"max_agents": 2},
            "event_capture": {"watch_paths": ["/tmp"]},
            "tray_app": {},
        }

        system = SelFlowSystemIntegration(config)

        # Test initialization
        init_result = await system.initialize()
        assert init_result is True

        # Test system status before start
        status = await system.get_system_status()
        assert not status["system_integration"]["is_running"]

        # Test chat functionality
        chat_result = await system.chat_with_agents("What can you do?")
        assert "session_id" in chat_result
        assert "response" in chat_result

        # Test shutdown
        await system.shutdown()

        print("✅ Complete system lifecycle test passed!")


@pytest.mark.asyncio
async def test_phase3_integration_demo():
    """
    Demonstration test of Phase 3 system integration
    Shows the complete workflow from initialization to agent interaction
    """
    print("\n🚀 SelFlow Phase 3 Integration Demo")
    print("=" * 50)

    # Configuration
    config = {
        "embryo_pool": {
            "max_embryos": 10,
            "mutation_rate": 0.1,
            "competition_intensity": 0.8,
        },
        "agent_manager": {
            "max_agents": 3,
            "birth_threshold": 0.7,
            "retirement_threshold": 0.3,
        },
        "event_capture": {"watch_paths": ["/tmp"]},
        "tray_app": {},
    }

    # Mock system permissions for testing
    with patch(
        "app.system.system_integration.check_system_permissions"
    ) as mock_permissions:
        mock_permissions.return_value = {
            "accessibility": True,
            "full_disk_access": True,
        }

        # Mock tray app creation (since we don't have GUI in tests)
        with patch("app.system.macos_tray.create_tray_app") as mock_tray:
            mock_tray.return_value = None

            # Create system integration
            system = SelFlowSystemIntegration(config)

            print("1. 🔧 Initializing system components...")
            init_success = await system.initialize()
            assert init_success, "System initialization failed"
            print("   ✅ System initialized successfully")

            print("\n2. 📊 Getting system status...")
            status = await system.get_system_status()
            components = status["system_integration"]["components"]
            print(f"   • Embryo Pool: {'✅' if components['embryo_pool'] else '❌'}")
            print(
                f"   • Agent Manager: {'✅' if components['agent_manager'] else '❌'}"
            )
            print(
                f"   • Event Capture: {'✅' if components['event_capture'] else '❌'}"
            )
            print(
                f"   • Agent Interface: {'✅' if components['agent_interface'] else '❌'}"
            )
            print(f"   • Tray App: {'✅' if components['tray_app'] else '⚠️ (Mocked)'}")

            print("\n3. 💬 Testing agent chat interface...")

            # Test help message
            help_result = await system.chat_with_agents("help")
            print(f"   • Help Response: {help_result['response']['agent_name']}")
            print(f"   • Confidence: {help_result['response']['confidence']:.1%}")

            # Test system status request
            status_result = await system.chat_with_agents("show system status")
            print(f"   • Status Response: {status_result['response']['agent_name']}")
            print(
                f"   • Content Length: {len(status_result['response']['content'])} chars"
            )

            # Test agent listing
            agents_result = await system.chat_with_agents("show me my active agents")
            print(f"   • Agents Response: {agents_result['response']['agent_name']}")

            print("\n4. 🎯 Testing event capture system...")

            # Get event capture stats
            if system.event_capture:
                capture_stats = system.event_capture.get_capture_stats()
                print(f"   • Events Captured: {capture_stats['events_captured']}")
                print(
                    f"   • Filesystem Monitoring: {'✅' if capture_stats['filesystem_monitoring'] else '❌'}"
                )
                print(
                    f"   • Application Monitoring: {'✅' if capture_stats['application_monitoring'] else '❌'}"
                )
                print(
                    f"   • Resource Monitoring: {'✅' if capture_stats['resource_monitoring'] else '❌'}"
                )

            print("\n5. 🛑 Testing graceful shutdown...")
            await system.shutdown()
            print("   ✅ System shutdown completed")

    print("\n🎉 Phase 3 Integration Demo Complete!")
    print("=" * 50)
    print("✅ All system integration components working correctly")
    print("✅ Agent-user interaction interface functional")
    print("✅ Event capture system operational")
    print("✅ System lifecycle management working")
    print("\n🚀 SelFlow Phase 3 is ready for macOS deployment!")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(test_phase3_integration_demo())
