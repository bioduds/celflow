#!/usr/bin/env python3
"""
SelFlow macOS System Tray Integration

Provides a system tray icon that evolves based on the learning phases:
- Phase 0: Silent Observer (simple icon, minimal menu)
- Phase 1: Subtle Recognition (icon changes, gentle notifications)
- Phase 2: Quiet Assistant (interactive menu, agent status)
- Phase 3: Integrated Intelligence (full interface, agent chat)
"""

import asyncio
import logging
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import json

try:
    import rumps

    RUMPS_AVAILABLE = True
except ImportError:
    RUMPS_AVAILABLE = False
    print("Warning: rumps not available. Install with: pip install rumps")

from ..core.agent_manager import AgentManager


class SelFlowTrayApp(rumps.App):
    """
    macOS System Tray Application for SelFlow
    """

    def __init__(self, agent_manager: AgentManager, config: Dict[str, Any]):
        # Initialize the tray app
        super().__init__(
            name="SelFlow",
            title="🧬",  # DNA emoji for embryo phase
            icon=None,
            template=True,
            menu=None,
        )

        self.agent_manager = agent_manager
        self.config = config
        self.logger = logging.getLogger("SelFlowTray")

        # Learning phase tracking
        self.current_phase = 0  # Start in Silent Observer phase
        self.phase_start_time = datetime.now()
        self.phase_durations = {
            0: 4 * 7 * 24 * 3600,  # 4 weeks for Phase 0
            1: 4 * 7 * 24 * 3600,  # 4 weeks for Phase 1
            2: 8 * 7 * 24 * 3600,  # 8 weeks for Phase 2
            3: float("inf"),  # Phase 3 is permanent
        }

        # UI state
        self.last_update = datetime.now()
        self.notification_count = 0
        self.agent_birth_count = 0

        # Initialize menu based on current phase
        self._update_menu_for_phase()

        # Start background tasks
        self._start_background_tasks()

    def _start_background_tasks(self):
        """Start background monitoring tasks"""
        # Create background thread for async operations
        self.background_thread = threading.Thread(
            target=self._run_background_loop, daemon=True
        )
        self.background_thread.start()

    def _run_background_loop(self):
        """Run background async operations"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self._background_monitor())
        except Exception as e:
            self.logger.error(f"Background loop error: {e}")
        finally:
            loop.close()

    async def _background_monitor(self):
        """Background monitoring of system state"""
        while True:
            try:
                # Check for phase transitions
                await self._check_phase_transition()

                # Update tray based on system state
                await self._update_tray_state()

                # Check for agent births
                await self._check_agent_births()

                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                self.logger.error(f"Background monitor error: {e}")
                await asyncio.sleep(60)  # Wait longer on error

    async def _check_phase_transition(self):
        """Check if we should transition to next learning phase"""
        current_time = datetime.now()
        time_in_phase = (current_time - self.phase_start_time).total_seconds()

        phase_duration = self.phase_durations.get(self.current_phase, float("inf"))

        if time_in_phase >= phase_duration and self.current_phase < 3:
            # Transition to next phase
            old_phase = self.current_phase
            self.current_phase += 1
            self.phase_start_time = current_time

            self.logger.info(f"Phase transition: {old_phase} → {self.current_phase}")

            # Update UI for new phase
            rumps.notification(
                title="SelFlow Evolution",
                subtitle=f"Entering Learning Phase {self.current_phase}",
                message=self._get_phase_description(self.current_phase),
                sound=False,
            )

            self._update_menu_for_phase()
            self._update_icon_for_phase()

    def _get_phase_description(self, phase: int) -> str:
        """Get description for learning phase"""
        descriptions = {
            0: "Silent Observer - Learning your patterns quietly",
            1: "Subtle Recognition - Beginning to understand your workflow",
            2: "Quiet Assistant - Ready to help with gentle suggestions",
            3: "Integrated Intelligence - Full AI operating system active",
        }
        return descriptions.get(phase, "Unknown phase")

    def _update_icon_for_phase(self):
        """Update tray icon based on current phase"""
        phase_icons = {
            0: "🧬",  # DNA - embryonic stage
            1: "🌱",  # Seedling - growing awareness
            2: "🤖",  # Robot - assistant ready
            3: "✨",  # Sparkles - full intelligence
        }

        new_icon = phase_icons.get(self.current_phase, "🧬")
        self.title = new_icon

    def _update_menu_for_phase(self):
        """Update menu items based on current learning phase"""
        # Clear existing menu
        self.menu.clear()

        if self.current_phase == 0:
            # Phase 0: Silent Observer - Minimal menu
            self.menu = [
                rumps.MenuItem("SelFlow - Silent Observer", callback=None),
                rumps.separator,
                rumps.MenuItem("Learning your patterns...", callback=None),
                rumps.MenuItem(
                    f"Embryos: Observing", callback=self._show_embryo_status
                ),
                rumps.separator,
                rumps.MenuItem("Quit SelFlow", callback=rumps.quit_application),
            ]

        elif self.current_phase == 1:
            # Phase 1: Subtle Recognition - Show some awareness
            self.menu = [
                rumps.MenuItem("SelFlow - Subtle Recognition", callback=None),
                rumps.separator,
                rumps.MenuItem(
                    "Patterns detected", callback=self._show_pattern_summary
                ),
                rumps.MenuItem("Embryo status", callback=self._show_embryo_status),
                rumps.separator,
                rumps.MenuItem("Settings", callback=self._show_settings),
                rumps.MenuItem("Quit SelFlow", callback=rumps.quit_application),
            ]

        elif self.current_phase == 2:
            # Phase 2: Quiet Assistant - Interactive menu
            self.menu = [
                rumps.MenuItem("SelFlow - Quiet Assistant", callback=None),
                rumps.separator,
                rumps.MenuItem("Active Agents", callback=self._show_agents),
                rumps.MenuItem("System Status", callback=self._show_system_status),
                rumps.MenuItem("Recent Activity", callback=self._show_recent_activity),
                rumps.separator,
                rumps.MenuItem("Force Agent Birth", callback=self._force_agent_birth),
                rumps.MenuItem("Chat with Agents", callback=self._open_agent_chat),
                rumps.separator,
                rumps.MenuItem("Settings", callback=self._show_settings),
                rumps.MenuItem("Quit SelFlow", callback=rumps.quit_application),
            ]

        else:  # Phase 3: Integrated Intelligence
            # Phase 3: Full interface
            self.menu = [
                rumps.MenuItem("SelFlow - Integrated Intelligence", callback=None),
                rumps.separator,
                rumps.MenuItem("Agent Dashboard", callback=self._open_dashboard),
                rumps.MenuItem("Active Agents", callback=self._show_agents),
                rumps.MenuItem("System Analytics", callback=self._show_analytics),
                rumps.separator,
                rumps.MenuItem("Agent Chat", callback=self._open_agent_chat),
                rumps.MenuItem("Task Manager", callback=self._open_task_manager),
                rumps.MenuItem(
                    "Workflow Optimizer", callback=self._open_workflow_optimizer
                ),
                rumps.separator,
                rumps.MenuItem("Settings", callback=self._show_settings),
                rumps.MenuItem("About SelFlow", callback=self._show_about),
                rumps.MenuItem("Quit SelFlow", callback=rumps.quit_application),
            ]

    async def _update_tray_state(self):
        """Update tray state based on system activity"""
        try:
            # Get system status
            status = await self.agent_manager.get_system_status()

            # Update title with activity indicator if needed
            if self.current_phase >= 1:
                active_agents = status.get("system", {}).get("active_agents", 0)
                if active_agents > 0:
                    base_icon = {0: "🧬", 1: "🌱", 2: "🤖", 3: "✨"}[self.current_phase]
                    self.title = f"{base_icon}·{active_agents}"

        except Exception as e:
            self.logger.error(f"Error updating tray state: {e}")

    async def _check_agent_births(self):
        """Check for new agent births and notify user"""
        try:
            status = await self.agent_manager.get_system_status()
            current_births = status.get("system", {}).get("total_births", 0)

            if current_births > self.agent_birth_count:
                new_births = current_births - self.agent_birth_count
                self.agent_birth_count = current_births

                # Notify based on phase
                if self.current_phase >= 1:
                    recent_history = status.get("recent_history", [])
                    birth_events = [
                        e for e in recent_history if e.get("event") == "birth"
                    ]

                    if birth_events:
                        latest_birth = birth_events[-1]
                        agent_name = latest_birth.get("agent_name", "New Agent")

                        rumps.notification(
                            title="SelFlow Agent Birth",
                            subtitle=f"{agent_name} has been created",
                            message=f"Specialization: {latest_birth.get('specialization', 'General')}",
                            sound=self.current_phase >= 2,
                        )

        except Exception as e:
            self.logger.error(f"Error checking agent births: {e}")

    # Menu callback methods
    def _show_embryo_status(self, _):
        """Show embryo pool status"""
        asyncio.run_coroutine_threadsafe(
            self._async_show_embryo_status(), self._get_event_loop()
        )

    async def _async_show_embryo_status(self):
        """Async version of show embryo status"""
        try:
            status = await self.agent_manager.get_system_status()
            embryo_status = status.get("embryo_pool", {})

            message = f"""Embryo Pool Status:
            
Active Embryos: {embryo_status.get('active_embryos', 0)}
Events Processed: {embryo_status.get('events_processed', 0)}
Generation: {embryo_status.get('generation', 0)}
Birth Queue: {embryo_status.get('birth_queue_size', 0)}

Top Specializations:
{self._format_specializations(embryo_status.get('top_specializations', {}))}"""

            rumps.alert(title="Embryo Pool Status", message=message, ok="OK")

        except Exception as e:
            rumps.alert(
                title="Error", message=f"Failed to get embryo status: {e}", ok="OK"
            )

    def _format_specializations(self, specs: Dict[str, int]) -> str:
        """Format specialization counts for display"""
        if not specs:
            return "None detected yet"

        lines = []
        for spec, count in sorted(specs.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"• {spec.replace('_', ' ').title()}: {count}")

        return "\n".join(lines[:5])  # Show top 5

    def _show_agents(self, _):
        """Show active agents"""
        asyncio.run_coroutine_threadsafe(
            self._async_show_agents(), self._get_event_loop()
        )

    async def _async_show_agents(self):
        """Async version of show agents"""
        try:
            agents = await self.agent_manager.get_active_agents()

            if not agents:
                rumps.alert(
                    title="Active Agents",
                    message="No agents are currently active.\n\nAgents will be born as embryos mature and specialize.",
                    ok="OK",
                )
                return

            agent_info = []
            for agent in agents:
                info = f"""🤖 {agent.blueprint.name}
Specialization: {agent.blueprint.specialization.replace('_', ' ').title()}
Autonomy: {agent.blueprint.autonomy_level.title()}
Tasks: {agent.task_count}
Success Rate: {agent.success_rate:.1%}"""
                agent_info.append(info)

            message = f"Active Agents ({len(agents)}):\n\n" + "\n\n".join(agent_info)

            rumps.alert(title="Active Agents", message=message, ok="OK")

        except Exception as e:
            rumps.alert(
                title="Error", message=f"Failed to get agent status: {e}", ok="OK"
            )

    def _show_system_status(self, _):
        """Show overall system status"""
        asyncio.run_coroutine_threadsafe(
            self._async_show_system_status(), self._get_event_loop()
        )

    async def _async_show_system_status(self):
        """Async version of show system status"""
        try:
            status = await self.agent_manager.get_system_status()
            system_info = status.get("system", {})

            message = f"""SelFlow System Status:

Phase: {self.current_phase} - {self._get_phase_description(self.current_phase)}
Uptime: {system_info.get('uptime', 'Unknown')}

Agents:
• Active: {system_info.get('active_agents', 0)}
• Total Births: {system_info.get('total_births', 0)}
• Retirements: {system_info.get('total_retirements', 0)}

Embryo Pool:
• Active Embryos: {status.get('embryo_pool', {}).get('active_embryos', 0)}
• Events Processed: {status.get('embryo_pool', {}).get('events_processed', 0)}
• Generation: {status.get('embryo_pool', {}).get('generation', 0)}"""

            rumps.alert(title="System Status", message=message, ok="OK")

        except Exception as e:
            rumps.alert(
                title="Error", message=f"Failed to get system status: {e}", ok="OK"
            )

    def _force_agent_birth(self, _):
        """Force creation of a new agent"""
        asyncio.run_coroutine_threadsafe(
            self._async_force_agent_birth(), self._get_event_loop()
        )

    async def _async_force_agent_birth(self):
        """Async version of force agent birth"""
        try:
            agent = await self.agent_manager.force_agent_birth()

            if agent:
                rumps.alert(
                    title="Agent Birth Successful!",
                    message=f"""🎉 New agent created:

Name: {agent.blueprint.name}
Specialization: {agent.blueprint.specialization.replace('_', ' ').title()}
Autonomy: {agent.blueprint.autonomy_level.title()}

The agent is now active and ready to assist!""",
                    ok="Great!",
                )
            else:
                rumps.alert(
                    title="Agent Birth Failed",
                    message="Unable to create new agent. This could be because:\n\n• Maximum agents reached\n• No suitable embryos available\n• Embryos need more time to mature",
                    ok="OK",
                )

        except Exception as e:
            rumps.alert(title="Error", message=f"Failed to create agent: {e}", ok="OK")

    def _show_settings(self, _):
        """Show settings dialog"""
        rumps.alert(
            title="SelFlow Settings",
            message=f"""Current Configuration:

Learning Phase: {self.current_phase}
Phase Duration: {self._get_phase_description(self.current_phase)}

Settings will be expanded in future versions to include:
• Privacy controls
• Learning preferences  
• Agent behavior tuning
• Notification settings""",
            ok="OK",
        )

    def _open_agent_chat(self, _):
        """Open agent chat interface (placeholder)"""
        rumps.alert(
            title="Agent Chat",
            message="Agent chat interface coming soon!\n\nThis will allow direct communication with your active agents for task delegation and assistance.",
            ok="OK",
        )

    def _open_dashboard(self, _):
        """Open agent dashboard (placeholder)"""
        rumps.alert(
            title="Agent Dashboard",
            message="Full agent dashboard coming soon!\n\nThis will provide comprehensive monitoring and control of your AI agents.",
            ok="OK",
        )

    def _show_about(self, _):
        """Show about dialog"""
        rumps.alert(
            title="About SelFlow",
            message=f"""SelFlow - The Self-Creating AI Operating System

Version: Phase 3 Development
Phase: {self.current_phase} - {self._get_phase_description(self.current_phase)}

SelFlow creates specialized AI agents through biological evolution, 
starting with neural embryos that compete and evolve into 
personalized assistants tailored to your workflow.

🧬 Embryo Pool → 🎭 Agent Creator → 🤖 Specialized Agents

Built with love for the future of human-AI collaboration.""",
            ok="Amazing!",
        )

    def _get_event_loop(self):
        """Get the background event loop"""
        # This is a simplified approach - in production would need proper loop management
        return asyncio.new_event_loop()

    # Placeholder methods for future features
    def _show_pattern_summary(self, _):
        rumps.alert("Pattern Summary", "Pattern analysis coming soon!", ok="OK")

    def _show_recent_activity(self, _):
        rumps.alert("Recent Activity", "Activity timeline coming soon!", ok="OK")

    def _show_analytics(self, _):
        rumps.alert("System Analytics", "Advanced analytics coming soon!", ok="OK")

    def _open_task_manager(self, _):
        rumps.alert("Task Manager", "Task management interface coming soon!", ok="OK")

    def _open_workflow_optimizer(self, _):
        rumps.alert("Workflow Optimizer", "Workflow optimization coming soon!", ok="OK")


def create_tray_app(
    agent_manager: AgentManager, config: Dict[str, Any]
) -> Optional[SelFlowTrayApp]:
    """Create and return the tray application"""
    if not RUMPS_AVAILABLE:
        print("Cannot create tray app: rumps not available")
        return None

    try:
        app = SelFlowTrayApp(agent_manager, config)
        return app
    except Exception as e:
        print(f"Failed to create tray app: {e}")
        return None
