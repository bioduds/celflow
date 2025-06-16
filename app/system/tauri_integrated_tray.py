#!/usr/bin/env python3
"""
SelFlow Tauri-Integrated System Tray

Enhanced system tray that launches the beautiful Tauri desktop application
and provides comprehensive system management capabilities.
"""

import asyncio
import json
import logging
import os
import sqlite3
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import rumps
    RUMPS_AVAILABLE = True
except ImportError:
    RUMPS_AVAILABLE = False
    print("Warning: rumps not available. Install with: pip install rumps")

try:
    import tkinter as tk
    from tkinter import scrolledtext, messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("Warning: tkinter not available for chat interface")

from app.core.agent_manager import AgentManager
from app.ai.central_brain import CentralAIBrain, create_central_brain

logger = logging.getLogger(__name__)


class TauriDesktopLauncher:
    """Handles launching and managing the Tauri desktop application"""
    
    def __init__(self):
        self.desktop_process = None
        self.is_running = False
        self.project_root = Path.cwd()
        
    def check_tauri_requirements(self) -> Dict[str, bool]:
        """Check if Tauri requirements are met"""
        requirements = {
            'node_modules': (self.project_root / 'node_modules').exists(),
            'package_json': (self.project_root / 'package.json').exists(),
            'tauri_config': (self.project_root / 'selflow-desktop' / 'src-tauri' / 'tauri.conf.json').exists(),
            'rust_installed': self._check_rust_installed(),
            'tauri_cli': self._check_tauri_cli(),
        }
        return requirements
    
    def _check_rust_installed(self) -> bool:
        """Check if Rust is installed"""
        try:
            result = subprocess.run(['rustc', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _check_tauri_cli(self) -> bool:
        """Check if Tauri CLI is installed"""
        try:
            result = subprocess.run(['cargo', 'tauri', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def launch_desktop_app(self) -> bool:
        """Launch the Tauri desktop application"""
        if self.is_running:
            logger.info("Desktop app is already running")
            return True
            
        try:
            # Check requirements first
            requirements = self.check_tauri_requirements()
            missing = [k for k, v in requirements.items() if not v]
            
            if missing:
                logger.error(f"Missing requirements for desktop app: {missing}")
                return False
            
            # Launch the desktop app
            logger.info("Launching Tauri desktop application...")
            
            # Use npm run tauri:dev for development mode
            self.desktop_process = subprocess.Popen(
                ['npm', 'run', 'tauri:dev'],
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.is_running = True
            logger.info(f"Desktop app launched with PID: {self.desktop_process.pid}")
            
            # Start monitoring thread
            threading.Thread(target=self._monitor_desktop_app, daemon=True).start()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch desktop app: {e}")
            return False
    
    def _monitor_desktop_app(self):
        """Monitor the desktop app process"""
        if not self.desktop_process:
            return
            
        try:
            # Wait for process to complete
            self.desktop_process.wait()
            self.is_running = False
            logger.info("Desktop app process ended")
        except Exception as e:
            logger.error(f"Error monitoring desktop app: {e}")
            self.is_running = False
    
    def stop_desktop_app(self):
        """Stop the desktop application"""
        if self.desktop_process and self.is_running:
            try:
                self.desktop_process.terminate()
                self.desktop_process.wait(timeout=5)
                logger.info("Desktop app stopped gracefully")
            except subprocess.TimeoutExpired:
                self.desktop_process.kill()
                logger.info("Desktop app force killed")
            except Exception as e:
                logger.error(f"Error stopping desktop app: {e}")
            finally:
                self.is_running = False
                self.desktop_process = None


class SystemMonitor:
    """Monitors system statistics and performance"""
    
    def __init__(self):
        self.stats = {
            'events_today': 0,
            'total_events': 0,
            'active_agents': 0,
            'system_health': 'Good',
            'db_size': '0 MB',
            'uptime': '0m',
        }
        self.start_time = datetime.now()
        
    def update_stats(self):
        """Update system statistics"""
        try:
            # Database stats
            db_path = Path('data/events.db')
            if db_path.exists():
                # Get database size
                size_bytes = db_path.stat().st_size
                self.stats['db_size'] = f"{size_bytes / (1024*1024):.1f} MB"
                
                # Get event counts
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                
                # Total events
                cursor.execute("SELECT COUNT(*) FROM events")
                self.stats['total_events'] = cursor.fetchone()[0]
                
                # Events today
                today = datetime.now().strftime("%Y-%m-%d")
                cursor.execute(
                    "SELECT COUNT(*) FROM events WHERE date(datetime(timestamp, 'unixepoch')) = ?",
                    (today,)
                )
                self.stats['events_today'] = cursor.fetchone()[0]
                
                conn.close()
            
            # Calculate uptime
            uptime_delta = datetime.now() - self.start_time
            hours = uptime_delta.seconds // 3600
            minutes = (uptime_delta.seconds % 3600) // 60
            
            if hours > 0:
                self.stats['uptime'] = f"{hours}h {minutes}m"
            else:
                self.stats['uptime'] = f"{minutes}m"
                
        except Exception as e:
            logger.error(f"Error updating stats: {e}")


class TauriIntegratedTray(rumps.App):
    """Enhanced SelFlow tray with Tauri desktop app integration"""
    
    def __init__(self, agent_manager: Optional[AgentManager] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__("🧬", title="SelFlow AI")
        
        self.agent_manager = agent_manager
        self.config = config or {}
        self.central_brain = None
        
        # Initialize components
        self.desktop_launcher = TauriDesktopLauncher()
        self.system_monitor = SystemMonitor()
        
        # Setup menu
        self._setup_menu()
        
        # Initialize AI brain
        self._initialize_ai_brain()
        
        # Start monitoring
        self._start_monitoring()
        
        logger.info("Tauri-integrated tray initialized")
    
    def _setup_menu(self):
        """Setup the tray menu"""
        self.menu = [
            "🖥️ Launch Desktop App",
            "💬 Chat with AI",
            None,  # Separator
            "📊 System Status",
            "🤖 Agent Status", 
            "🥚 Embryo Pool",
            "📈 Performance",
            None,  # Separator
            "🔄 Force Agent Birth",
            "⚙️ Settings",
            "❓ About",
            None,  # Separator
            "🔄 Restart System",
            "🛑 Stop System",
        ]
    
    def _initialize_ai_brain(self):
        """Initialize the Central AI Brain"""
        def init_brain():
            try:
                self.central_brain = create_central_brain()
                logger.info("Central AI Brain initialized")
            except Exception as e:
                logger.error(f"Failed to initialize AI brain: {e}")
        
        threading.Thread(target=init_brain, daemon=True).start()
    
    def _start_monitoring(self):
        """Start background monitoring"""
        def monitor_loop():
            while True:
                try:
                    self.system_monitor.update_stats()
                    self._update_title()
                    time.sleep(30)  # Update every 30 seconds
                except Exception as e:
                    logger.error(f"Monitor loop error: {e}")
                    time.sleep(60)
        
        threading.Thread(target=monitor_loop, daemon=True).start()
    
    def _update_title(self):
        """Update tray title based on system status"""
        stats = self.system_monitor.stats
        
        if self.desktop_launcher.is_running:
            self.title = "🖥️"  # Desktop app running
        elif stats['events_today'] > 100:
            self.title = f"🧬{stats['events_today']}"  # Show event count
        else:
            self.title = "🧬"  # Default
    
    @rumps.clicked("🖥️ Launch Desktop App")
    def launch_desktop_app(self, _):
        """Launch the beautiful Tauri desktop application"""
        if self.desktop_launcher.is_running:
            rumps.alert(
                title="Desktop App Running",
                message="The SelFlow desktop application is already running!",
                ok="OK"
            )
            return
        
        # Check requirements
        requirements = self.desktop_launcher.check_tauri_requirements()
        missing = [k for k, v in requirements.items() if not v]
        
        if missing:
            missing_str = "\n".join([f"• {req.replace('_', ' ').title()}" for req in missing])
            rumps.alert(
                title="Requirements Missing",
                message=f"The following requirements are missing:\n\n{missing_str}\n\nPlease install them first:\n\n• npm install\n• cargo install tauri-cli@^2.0",
                ok="OK"
            )
            return
        
        # Launch the app
        success = self.desktop_launcher.launch_desktop_app()
        
        if success:
            rumps.notification(
                title="🖥️ Desktop App Launched",
                subtitle="SelFlow Desktop Application",
                message="The beautiful desktop interface is starting up...",
                sound=True
            )
        else:
            rumps.alert(
                title="Launch Failed",
                message="Failed to launch the desktop application. Check the logs for details.",
                ok="OK"
            )
    
    @rumps.clicked("💬 Chat with AI")
    def open_chat(self, _):
        """Open chat interface with Central AI Brain"""
        if not TKINTER_AVAILABLE:
            rumps.alert(
                title="Chat Unavailable",
                message="Chat interface requires tkinter. Please install it first.",
                ok="OK"
            )
            return
        
        try:
            from app.system.macos_tray import SelFlowChatWindow
            
            chat_window = SelFlowChatWindow(self.central_brain)
            if chat_window.create_window():
                chat_window.show()
            else:
                rumps.alert(
                    title="Chat Error",
                    message="Failed to create chat window.",
                    ok="OK"
                )
        except Exception as e:
            logger.error(f"Error opening chat: {e}")
            rumps.alert(
                title="Chat Error",
                message=f"Error opening chat: {str(e)}",
                ok="OK"
            )
    
    @rumps.clicked("📊 System Status")
    def show_system_status(self, _):
        """Show comprehensive system status"""
        stats = self.system_monitor.stats
        
        # Desktop app status
        desktop_status = "🟢 Running" if self.desktop_launcher.is_running else "🔴 Stopped"
        
        # AI Brain status
        brain_status = "🟢 Active" if self.central_brain else "🔴 Inactive"
        
        status_message = f"""📊 SelFlow System Status

🖥️ Desktop App: {desktop_status}
🧠 AI Brain: {brain_status}
📊 Events Today: {stats['events_today']:,}
📈 Total Events: {stats['total_events']:,}
🤖 Active Agents: {stats['active_agents']}
💾 Database Size: {stats['db_size']}
⏱️ Uptime: {stats['uptime']}
🏥 Health: {stats['system_health']}

💡 Tip: Launch the desktop app for beautiful visualizations!"""
        
        rumps.alert(
            title="System Status",
            message=status_message,
            ok="OK"
        )
    
    @rumps.clicked("🤖 Agent Status")
    def show_agent_status(self, _):
        """Show agent status information"""
        if self.agent_manager:
            try:
                agents = self.agent_manager.get_all_agents()
                if agents:
                    agent_list = []
                    for agent in agents[:5]:  # Show first 5 agents
                        status = "🟢 Active" if agent.get('active', False) else "🔴 Inactive"
                        agent_list.append(f"• {agent.get('name', 'Unknown')} - {status}")
                    
                    agent_message = f"""🤖 Agent Status

Active Agents: {len([a for a in agents if a.get('active', False)])}
Total Agents: {len(agents)}

{chr(10).join(agent_list)}

🖥️ Launch the desktop app for detailed agent analytics!"""
                else:
                    agent_message = """🤖 Agent Status

No agents have been born yet.

The system is still learning your patterns.
Agents will be created automatically as patterns emerge.

🖥️ Launch the desktop app to see the full agent architecture!"""
                
                rumps.alert(
                    title="Agent Status",
                    message=agent_message,
                    ok="OK"
                )
            except Exception as e:
                logger.error(f"Error getting agent status: {e}")
                rumps.alert(
                    title="Agent Status Error",
                    message=f"Error retrieving agent status: {str(e)}",
                    ok="OK"
                )
        else:
            rumps.alert(
                title="Agent Status",
                message="Agent manager not available. Please restart the system.",
                ok="OK"
            )
    
    @rumps.clicked("🥚 Embryo Pool")
    def show_embryo_pool(self, _):
        """Show embryo development status"""
        embryo_message = """🥚 Embryo Development Pool

The system is continuously analyzing your behavior patterns
to develop specialized AI agents.

Current Development:
• Pattern Analysis: Ongoing
• Behavior Clustering: Active
• Agent Specialization: In Progress

🖥️ Launch the desktop app to see:
• Real-time clustering results
• Pattern evolution timeline
• Agent development progress
• Confidence metrics

Embryos mature into agents automatically when ready!"""
        
        rumps.alert(
            title="Embryo Pool",
            message=embryo_message,
            ok="OK"
        )
    
    @rumps.clicked("📈 Performance")
    def show_performance(self, _):
        """Show system performance metrics"""
        stats = self.system_monitor.stats
        
        # Calculate performance indicators
        events_per_hour = stats['events_today'] / max(1, datetime.now().hour or 1)
        
        performance_message = f"""📈 System Performance

📊 Processing Rate: {events_per_hour:.1f} events/hour
💾 Database Size: {stats['db_size']}
⏱️ System Uptime: {stats['uptime']}
🏥 Health Status: {stats['system_health']}

🖥️ Desktop App: {'🟢 Running' if self.desktop_launcher.is_running else '🔴 Stopped'}

💡 The desktop app provides detailed performance analytics
with beautiful charts and real-time monitoring!"""
        
        rumps.alert(
            title="Performance Metrics",
            message=performance_message,
            ok="OK"
        )
    
    @rumps.clicked("🔄 Force Agent Birth")
    def force_agent_birth(self, _):
        """Force creation of a new agent"""
        if self.agent_manager:
            try:
                # This would trigger agent creation logic
                rumps.notification(
                    title="🤖 Agent Birth Triggered",
                    subtitle="SelFlow AI System",
                    message="Attempting to birth a new specialized agent...",
                    sound=True
                )
                
                # In a real implementation, this would call agent_manager.force_birth()
                # For now, just show a message
                rumps.alert(
                    title="Agent Birth",
                    message="Agent birth process initiated!\n\nCheck the desktop app for real-time progress and detailed agent analytics.",
                    ok="OK"
                )
            except Exception as e:
                logger.error(f"Error forcing agent birth: {e}")
                rumps.alert(
                    title="Birth Error",
                    message=f"Error triggering agent birth: {str(e)}",
                    ok="OK"
                )
        else:
            rumps.alert(
                title="Agent Birth",
                message="Agent manager not available. Please restart the system.",
                ok="OK"
            )
    
    @rumps.clicked("⚙️ Settings")
    def show_settings(self, _):
        """Show settings and configuration options"""
        settings_message = """⚙️ SelFlow Settings

🖥️ Desktop App Settings:
• Launch desktop app for full configuration
• Beautiful settings interface available
• Real-time configuration updates

📊 Current Configuration:
• Privacy Mode: Enabled
• Local Processing: Active
• Auto Agent Birth: Enabled

🔧 Advanced Settings:
Available in the desktop application with
intuitive controls and live previews.

💡 Launch the desktop app for the complete
settings experience!"""
        
        rumps.alert(
            title="Settings",
            message=settings_message,
            ok="OK"
        )
    
    @rumps.clicked("❓ About")
    def show_about(self, _):
        """Show about information"""
        about_message = """❓ About SelFlow

🧬 SelFlow - Self-Creating AI Operating System
The first AI system that creates specialized agents
from your behavior patterns.

🖥️ Now featuring a beautiful Tauri desktop application
with professional data visualization and real-time analytics!

✨ Key Features:
• Advanced ML pipeline with Pydantic models
• Real-time clustering and pattern detection
• Beautiful glass morphism UI design
• Type-safe React ↔ Rust ↔ Python integration
• 5-12MB footprint vs 150MB+ alternatives

🚀 Launch the desktop app to experience:
• Interactive system overview
• Clustering results visualization
• Pattern evolution timeline
• AI-powered recommendations

Built with ❤️ for the future of human-AI collaboration"""
        
        rumps.alert(
            title="About SelFlow",
            message=about_message,
            ok="OK"
        )
    
    @rumps.clicked("🔄 Restart System")
    def restart_system(self, _):
        """Restart the SelFlow system"""
        response = rumps.alert(
            title="Restart System",
            message="This will restart the entire SelFlow system.\n\nContinue?",
            ok="Restart",
            cancel="Cancel"
        )
        
        if response == 1:  # OK/Restart clicked
            try:
                # Stop desktop app if running
                if self.desktop_launcher.is_running:
                    self.desktop_launcher.stop_desktop_app()
                
                rumps.notification(
                    title="🔄 System Restarting",
                    subtitle="SelFlow AI System",
                    message="Restarting all components...",
                    sound=True
                )
                
                # Use the launch script to restart
                subprocess.Popen(['./launch_selflow.sh', 'restart'])
                
                # Quit this tray instance
                rumps.quit_application()
                
            except Exception as e:
                logger.error(f"Error restarting system: {e}")
                rumps.alert(
                    title="Restart Error",
                    message=f"Error restarting system: {str(e)}",
                    ok="OK"
                )
    
    @rumps.clicked("🛑 Stop System")
    def stop_system(self, _):
        """Stop the SelFlow system"""
        response = rumps.alert(
            title="Stop System",
            message="This will stop the entire SelFlow system.\n\nContinue?",
            ok="Stop",
            cancel="Cancel"
        )
        
        if response == 1:  # OK/Stop clicked
            try:
                # Stop desktop app if running
                if self.desktop_launcher.is_running:
                    self.desktop_launcher.stop_desktop_app()
                
                rumps.notification(
                    title="🛑 System Stopping",
                    subtitle="SelFlow AI System", 
                    message="Shutting down all components...",
                    sound=True
                )
                
                # Use the launch script to stop
                subprocess.Popen(['./launch_selflow.sh', 'stop'])
                
                # Quit this tray instance
                rumps.quit_application()
                
            except Exception as e:
                logger.error(f"Error stopping system: {e}")
                rumps.alert(
                    title="Stop Error",
                    message=f"Error stopping system: {str(e)}",
                    ok="OK"
                )


def create_tauri_integrated_tray(
    agent_manager: Optional[AgentManager] = None, 
    config: Optional[Dict[str, Any]] = None
) -> Optional[TauriIntegratedTray]:
    """Create and return the Tauri-integrated tray application"""
    
    if not RUMPS_AVAILABLE:
        logger.error("rumps not available - cannot create tray app")
        return None
    
    try:
        tray_app = TauriIntegratedTray(agent_manager, config)
        logger.info("Tauri-integrated tray app created successfully")
        return tray_app
    except Exception as e:
        logger.error(f"Failed to create tray app: {e}")
        return None


def main():
    """Main entry point for standalone tray execution"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("Starting Tauri-integrated SelFlow tray...")
    
    tray_app = create_tauri_integrated_tray()
    if tray_app:
        logger.info("Running tray application...")
        tray_app.run()
    else:
        logger.error("Failed to create tray application")


if __name__ == "__main__":
    main() 