#!/usr/bin/env python3
"""
SelFlow Live Agent System

Run the complete SelFlow system with real-time agent monitoring.
Watch your agents work in real-time!
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path
from datetime import datetime

from app.system.system_integration import SelFlowSystemIntegration

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


class SelFlowLiveMonitor:
    """Live monitoring and dashboard for SelFlow agents"""

    def __init__(self):
        self.running = False
        self.start_time = None
        self.stats = {
            "events_processed": 0,
            "patterns_detected": 0,
            "agents_active": 0,
            "embryos_active": 0,
            "births_total": 0,
        }

    async def start_complete_system(self):
        """Start the complete SelFlow system"""

        # Configuration for live system
        config = {
            "max_embryos": 15,
            "data_buffer_limit_mb": 0.001,  # Quick births for demo
            "agent_manager": {
                "max_agents": 20,  # More agents for demo
                "agent_birth_threshold": 3,
            },
            "use_high_performance": True,
            "event_capture": {
                "enable_persistence": True,
                "persistence": {
                    "database_path": "data/events.db",
                },
            },
        }

        print("🚀 Starting Complete SelFlow System...")
        print("=" * 60)

        # Initialize system components
        self.system_integration = SelFlowSystemIntegration(config)

        # Initialize first, then start
        if not await self.system_integration.initialize():
            raise Exception("Failed to initialize system integration")

        await self.system_integration.start()

        self.agent_manager = self.system_integration.agent_manager
        self.embryo_pool = self.system_integration.embryo_pool

        print("✅ SelFlow System Online!")
        print("🤖 Agent Manager: Active")
        print("🧬 Embryo Pool: Active")
        print("📡 Event Capture: Active")
        print("🎭 Tray Integration: Active")
        print("=" * 60)

        self.running = True
        self.start_time = datetime.now()

        # Start monitoring dashboard
        await self.run_live_dashboard()

    async def run_live_dashboard(self):
        """Run the live monitoring dashboard"""

        print("\n🎭 SELFLOW LIVE AGENT DASHBOARD")
        print("=" * 60)
        print("Press Ctrl+C to stop monitoring...\n")

        dashboard_cycle = 0

        while self.running:
            try:
                # Clear screen and show header
                if dashboard_cycle % 10 == 0:  # Refresh header every 10 cycles
                    self.show_dashboard_header()

                # Update stats
                await self.update_stats()

                # Show current status
                await self.show_live_status()

                # Show agent activity
                await self.show_agent_activity()

                # Show embryo status
                await self.show_embryo_status()

                dashboard_cycle += 1

                # Sleep in smaller chunks to be more responsive to interruption
                for _ in range(20):  # 20 * 0.1 = 2 seconds total
                    if not self.running:
                        break
                    await asyncio.sleep(0.1)

            except KeyboardInterrupt:
                print("\n🛑 Stopping SelFlow system...")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Dashboard error: {e}")
                await asyncio.sleep(1)

        await self.stop_system()

    def show_dashboard_header(self):
        """Show the dashboard header"""
        print("\033[2J\033[H")  # Clear screen and move cursor to top
        print("🎭 " + "=" * 56 + " 🎭")
        print("    SelFlow Live Agent System - Real-Time Monitor")
        print("🎭 " + "=" * 56 + " 🎭")

        # System uptime
        if self.start_time:
            uptime = datetime.now() - self.start_time
            print(f"⏱️  System Uptime: {uptime}")
        print()

    async def update_stats(self):
        """Update system statistics"""
        try:
            # Get embryo pool stats
            if hasattr(self.embryo_pool, "get_pool_status"):
                pool_stats = self.embryo_pool.get_pool_status()
                self.stats["embryos_active"] = pool_stats.get("active_embryos", 0)
                self.stats["events_processed"] = pool_stats.get("events_processed", 0)
                self.stats["patterns_detected"] = pool_stats.get("patterns_detected", 0)

            # Get agent manager stats
            if hasattr(self.agent_manager, "get_agent_count"):
                self.stats["agents_active"] = await self.agent_manager.get_agent_count()

            if hasattr(self.agent_manager, "total_births"):
                self.stats["births_total"] = self.agent_manager.total_births

        except Exception as e:
            print(f"⚠️ Stats update error: {e}")

    async def show_live_status(self):
        """Show live system status"""
        print("📊 SYSTEM STATUS:")
        print(f"   🤖 Active Agents: {self.stats['agents_active']}")
        print(f"   🧬 Active Embryos: {self.stats['embryos_active']}")
        print(f"   📡 Events Processed: {self.stats['events_processed']:,}")
        print(f"   🎯 Patterns Detected: {self.stats['patterns_detected']:,}")
        print(f"   🎉 Total Births: {self.stats['births_total']}")
        print()

    async def show_agent_activity(self):
        """Show current agent activity"""
        print("🤖 AGENT ACTIVITY:")

        try:
            # Get active agents
            if hasattr(self.agent_manager, "agents"):
                active_agents = [
                    a for a in self.agent_manager.agents.values() if a.is_active
                ]

                if active_agents:
                    for i, agent in enumerate(active_agents[:5]):  # Show top 5
                        specialization = getattr(agent, "specialization", "general")
                        status = getattr(agent, "status", "active")
                        patterns = getattr(agent, "patterns_processed", 0)

                        print(
                            f"   🎭 Agent {agent.agent_id[:8]}: {specialization} ({status}) - {patterns} patterns"
                        )
                else:
                    print("   ⏳ No active agents yet...")
            else:
                print("   ⏳ Agent manager initializing...")

        except Exception as e:
            print(f"   ⚠️ Agent activity error: {e}")

        print()

    async def show_embryo_status(self):
        """Show embryo development status"""
        print("🧬 EMBRYO DEVELOPMENT:")

        try:
            if hasattr(self.embryo_pool, "embryos"):
                active_embryos = [
                    e for e in self.embryo_pool.embryos.values() if e.is_active
                ]

                if active_embryos:
                    # Show top 3 embryos
                    for i, embryo in enumerate(active_embryos[:3]):
                        patterns = embryo.stats.patterns_detected
                        buffer_size = embryo.data_buffer_size_mb
                        fitness = embryo.calculate_fitness()
                        ready = "🎉 READY" if embryo.birth_ready else "🌱 Growing"

                        print(
                            f"   🧬 Embryo {embryo.embryo_id[:8]}: {patterns} patterns, "
                            f"{buffer_size:.3f}MB, fitness {fitness:.2f} - {ready}"
                        )

                    # Show birth queue
                    if hasattr(self.embryo_pool, "birth_queue"):
                        queue_size = len(self.embryo_pool.birth_queue)
                        print(f"   🎯 Birth Queue: {queue_size} embryos ready")
                else:
                    print("   ⏳ No active embryos...")
            else:
                print("   ⏳ Embryo pool initializing...")

        except Exception as e:
            print(f"   ⚠️ Embryo status error: {e}")

        print()
        print("-" * 60)
        print()

    async def stop_system(self):
        """Stop the SelFlow system"""
        self.running = False

        print("🛑 Shutting down SelFlow system...")

        if hasattr(self, "system_integration"):
            await self.system_integration.stop()

        print("✅ SelFlow system stopped")


async def main():
    """Main entry point"""

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("selflow_live.log"), logging.StreamHandler()],
    )

    monitor = SelFlowLiveMonitor()

    # Handle shutdown gracefully
    def signal_handler(signum, frame):
        print("\n🛑 Received shutdown signal...")
        monitor.running = False
        # Force exit if needed
        import os

        os._exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await monitor.start_complete_system()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback

        traceback.print_exc()

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
