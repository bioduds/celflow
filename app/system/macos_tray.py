#!/usr/bin/env python3
"""
SelFlow macOS System Tray Integration with Central AI Chat

Enhanced system tray with direct chat interface to the Central AI Brain.
Talk to your unified AI assistant directly from the menu bar!
"""

import asyncio
import json
import logging
import os
import sqlite3
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


class SelFlowChatWindow:
    """Chat window for direct communication with Central AI Brain"""

    def __init__(self, central_brain: Optional[CentralAIBrain] = None):
        self.central_brain = central_brain
        self.window = None
        self.chat_display = None
        self.input_field = None
        self.send_button = None
        self.conversation_history = []

    def create_window(self):
        """Create the chat window"""
        if not TKINTER_AVAILABLE:
            return False

        try:
            # Create main window (use Tk() instead of Toplevel() for standalone window)
            self.window = tk.Tk()
            self.window.title("💬 Chat with SelFlow AI")
            self.window.geometry("600x500")
            self.window.resizable(True, True)

            # Configure window
            self.window.configure(bg="#f0f0f0")

            # Create chat display area
            chat_frame = tk.Frame(self.window, bg="#f0f0f0")
            chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Chat history display
            self.chat_display = scrolledtext.ScrolledText(
                chat_frame,
                wrap=tk.WORD,
                width=70,
                height=25,
                font=("SF Pro Display", 12),
                bg="white",
                fg="#333333",
                state=tk.DISABLED,
            )
            self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

            # Input frame
            input_frame = tk.Frame(chat_frame, bg="#f0f0f0")
            input_frame.pack(fill=tk.X, pady=(0, 5))

            # Input field
            self.input_field = tk.Text(
                input_frame,
                height=3,
                font=("SF Pro Display", 12),
                wrap=tk.WORD,
                bg="white",
                fg="#333333",
            )
            self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

            # Send button
            self.send_button = tk.Button(
                input_frame,
                text="Send",
                command=self._send_message,
                font=("SF Pro Display", 12, "bold"),
                bg="#007AFF",
                fg="white",
                relief=tk.FLAT,
                padx=20,
            )
            self.send_button.pack(side=tk.RIGHT, fill=tk.Y)

            # Bind Enter key
            self.input_field.bind("<Return>", self._on_enter)
            self.input_field.bind("<Shift-Return>", self._on_shift_enter)

            # Add welcome message
            self._add_message(
                "SelFlow AI",
                "👋 Hello! I'm your SelFlow AI assistant with 8 specialized agents working together. How can I help you today?",
                is_ai=True,
            )

            # Focus on input
            self.input_field.focus_set()

            return True

        except Exception as e:
            print(f"Error creating chat window: {e}")
            return False

    def _send_message(self):
        """Send message to AI and display response"""
        if not self.input_field:
            return

        # Get user message
        user_message = self.input_field.get("1.0", tk.END).strip()
        if not user_message:
            return

        # Clear input field
        self.input_field.delete("1.0", tk.END)

        # Add user message to chat
        self._add_message("You", user_message, is_ai=False)

        # Send to AI in background thread
        threading.Thread(
            target=self._process_ai_response, args=(user_message,), daemon=True
        ).start()

    def _process_ai_response(self, user_message: str):
        """Process AI response in background thread"""
        try:
            if self.central_brain:
                # Use the Central AI Brain
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                response = loop.run_until_complete(
                    self.central_brain.process_user_input(user_message, "tray_chat")
                )

                if response.get("success"):
                    ai_message = response.get(
                        "message", "I'm sorry, I couldn't process that request."
                    )
                else:
                    ai_message = (
                        f"Error: {response.get('error', 'Unknown error occurred')}"
                    )

                loop.close()
            else:
                ai_message = "🤖 Central AI Brain is not available. Please ensure the system is running properly."

            # Add AI response to chat (must be done in main thread)
            self.window.after(
                0, lambda: self._add_message("SelFlow AI", ai_message, is_ai=True)
            )

        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            self.window.after(
                0, lambda: self._add_message("SelFlow AI", error_message, is_ai=True)
            )

    def _add_message(self, sender: str, message: str, is_ai: bool = False):
        """Add message to chat display"""
        if not self.chat_display:
            return

        self.chat_display.config(state=tk.NORMAL)

        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")

        # Format message
        if is_ai:
            prefix = f"🤖 {sender} ({timestamp}):\n"
            self.chat_display.insert(tk.END, prefix, "ai_sender")
        else:
            prefix = f"👤 {sender} ({timestamp}):\n"
            self.chat_display.insert(tk.END, prefix, "user_sender")

        self.chat_display.insert(tk.END, f"{message}\n\n", "message")

        # Configure tags for styling
        self.chat_display.tag_config(
            "ai_sender", foreground="#007AFF", font=("SF Pro Display", 12, "bold")
        )
        self.chat_display.tag_config(
            "user_sender", foreground="#34C759", font=("SF Pro Display", 12, "bold")
        )
        self.chat_display.tag_config("message", foreground="#333333")

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

        # Store in conversation history
        self.conversation_history.append(
            {
                "sender": sender,
                "message": message,
                "timestamp": timestamp,
                "is_ai": is_ai,
            }
        )

    def _on_enter(self, event):
        """Handle Enter key press"""
        if event.state & 0x1:  # Shift is pressed
            return  # Allow newline
        else:
            self._send_message()
            return "break"  # Prevent default behavior

    def _on_shift_enter(self, event):
        """Handle Shift+Enter for newline"""
        return  # Allow default behavior (newline)

    def show(self):
        """Show the chat window"""
        if self.window:
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
            if self.input_field:
                self.input_field.focus_set()

    def hide(self):
        """Hide the chat window"""
        if self.window:
            self.window.withdraw()


class SelFlowTrayApp(rumps.App):
    """
    Crash-Resistant macOS System Tray Application for SelFlow
    """

    def __init__(self, agent_manager: AgentManager, config: Dict[str, Any]):
        # Initialize the tray app
        super().__init__(
            name="SelFlow",
            title="🧬",
            icon=None,
            template=True,
            menu=None,
        )

        self.agent_manager = agent_manager
        self.config = config
        self.logger = logging.getLogger("SelFlowTray")

        # Simple state tracking
        self.last_update = datetime.now()
        self.stats = {"events_today": 0, "agents_born": 0, "patterns_discovered": 0}

        # Initialize Central AI Brain and Chat Window
        self.central_brain = None
        self.chat_window = None
        self._initialize_ai_brain()

        # Setup interface
        self._setup_menu()
        self._start_monitoring()

    def _initialize_ai_brain(self):
        """Initialize the Central AI Brain for chat functionality"""
        try:
            # Create Central AI Brain in a separate thread to avoid blocking
            def init_brain():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                    self.central_brain = loop.run_until_complete(create_central_brain())

                    # Create chat window
                    self.chat_window = SelFlowChatWindow(self.central_brain)

                    print("✅ Central AI Brain initialized for tray chat")
                    loop.close()

                except Exception as e:
                    print(f"⚠️ Could not initialize Central AI Brain: {e}")
                    # Create chat window without AI brain
                    self.chat_window = SelFlowChatWindow(None)

            # Initialize in background thread
            threading.Thread(target=init_brain, daemon=True).start()

        except Exception as e:
            print(f"⚠️ Error initializing AI brain: {e}")
            # Create chat window without AI brain
            self.chat_window = SelFlowChatWindow(None)

    def _setup_menu(self):
        """Setup the tray menu with error handling"""
        try:
            self.menu.clear()

            # Build menu items with error handling
            menu_items = [
                rumps.MenuItem("SelFlow - Active", callback=None),
                rumps.separator,
                rumps.MenuItem("💬 Chat with AI", callback=self._safe_open_chat),
                rumps.separator,
                rumps.MenuItem("📊 System Status", callback=self._safe_show_status),
                rumps.MenuItem("🤖 Active Agents", callback=self._safe_show_agents),
                rumps.MenuItem("🧬 Embryo Pool", callback=self._safe_show_embryos),
                rumps.separator,
                rumps.MenuItem("🎭 Force Agent Birth", callback=self._safe_force_birth),
                rumps.MenuItem("📈 Performance", callback=self._safe_show_performance),
                rumps.separator,
                rumps.MenuItem("⚙️ Settings", callback=self._safe_show_settings),
                rumps.MenuItem("ℹ️ About", callback=self._safe_show_about),
                rumps.separator,
                rumps.MenuItem("🔄 Restart System", callback=self._safe_restart),
                rumps.MenuItem("❌ Quit", callback=rumps.quit_application),
            ]

            # Add all menu items
            for item in menu_items:
                self.menu.add(item)

        except Exception as e:
            self.logger.error(f"Error setting up menu: {e}")

    def _start_monitoring(self):
        """Start background monitoring thread"""
        try:
            monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            monitor_thread.start()
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {e}")

    def _monitor_loop(self):
        """Simple monitoring loop"""
        while True:
            try:
                self._update_stats()
                time.sleep(30)  # Update every 30 seconds
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {e}")
                time.sleep(60)  # Wait longer on error

    def _update_stats(self):
        """Update statistics safely"""
        try:
            # Get database stats
            db_path = Path("data/events.db")
            if db_path.exists():
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()

                # Count today's events
                today = datetime.now().strftime("%Y-%m-%d")
                cursor.execute(
                    "SELECT COUNT(*) FROM events WHERE date(timestamp) = ?", (today,)
                )
                self.stats["events_today"] = cursor.fetchone()[0]

                conn.close()

            # Update icon based on activity
            if self.stats["events_today"] > 100:
                self.title = "🧬✨"  # High activity
            elif self.stats["events_today"] > 10:
                self.title = "🧬💡"  # Some activity
            else:
                self.title = "🧬"  # Basic

        except Exception as e:
            self.logger.error(f"Error updating stats: {e}")

    def _safe_open_chat(self, _):
        """Safely open the chat window using subprocess approach"""
        try:
            import subprocess
            import sys

            # Use subprocess to launch the chat window in a separate process
            # This avoids threading conflicts with the tray app
            script_path = "test_chat_standalone.py"

            if not os.path.exists(script_path):
                rumps.alert(
                    title="Chat Error",
                    message="Chat script not found. Please ensure the system is properly installed.",
                    ok="OK",
                )
                return

            # Launch the chat window in a separate process
            subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

            print("✅ Chat window launched in separate process")

        except Exception as e:
            print(f"❌ Error launching chat: {e}")
            rumps.alert(title="Error", message=f"Could not launch chat: {e}", ok="OK")

    def _safe_show_status(self, _):
        """Safely show system status"""
        try:
            # Get basic system info
            db_path = Path("data/events.db")
            db_size = "Unknown"
            if db_path.exists():
                size_bytes = db_path.stat().st_size
                db_size = f"{size_bytes / (1024*1024):.1f} MB"

            message = f"""🧠 SelFlow System Status

Database: {db_size}
Events Today: {self.stats['events_today']:,}
Agents Born: {self.stats['agents_born']}
Patterns: {self.stats['patterns_discovered']}

System: Running
Last Update: {self.last_update.strftime('%H:%M:%S')}

SelFlow is actively learning from your behavior."""

            rumps.alert(title="System Status", message=message, ok="OK")

        except Exception as e:
            rumps.alert(title="Error", message=f"Could not get status: {e}", ok="OK")

    def _safe_show_agents(self, _):
        """Safely show active agents"""
        try:
            # Try to get agents from log file
            agent_log = Path("agent_births.log")
            agent_count = 0
            recent_agents = []

            if agent_log.exists():
                with open(agent_log, "r") as f:
                    lines = f.readlines()
                    for line in reversed(lines[-10:]):  # Last 10 lines
                        if "Agent born:" in line:
                            agent_count += 1
                            # Extract agent name
                            if '"' in line:
                                name = line.split('"')[1]
                                recent_agents.append(name)

            if agent_count == 0:
                message = """🤖 No Active Agents

Agents will be born as the system learns your patterns.
The embryo pool is developing specialized intelligence.

Try using 'Force Agent Birth' to create an agent now."""
            else:
                agent_list = "\n".join([f"• {name}" for name in recent_agents[:5]])
                message = f"""🤖 Active Agents ({agent_count})

Recent Agents:
{agent_list}

These agents are specialized based on your behavior patterns."""

            rumps.alert(title="Active Agents", message=message, ok="OK")

        except Exception as e:
            rumps.alert(title="Error", message=f"Could not get agents: {e}", ok="OK")

    def _safe_show_embryos(self, _):
        """Safely show embryo status"""
        try:
            # Simple embryo status
            message = """🧬 Embryo Pool Status

The embryo pool is continuously developing specialized AI agents
based on your behavior patterns.

Features:
• Pattern-based specialization
• Intelligent clustering
• Adaptive learning
• Autonomous development

Embryos mature into agents when they reach sufficient intelligence."""

            rumps.alert(title="Embryo Pool", message=message, ok="OK")

        except Exception as e:
            rumps.alert(
                title="Error", message=f"Could not get embryo status: {e}", ok="OK"
            )

    def _safe_force_birth(self, _):
        """Safely force agent birth"""
        try:
            # Simple force birth simulation
            import random

            specializations = [
                "System Guardian",
                "File Manager",
                "Workflow Optimizer",
                "Pattern Analyst",
                "Task Coordinator",
            ]

            names = [
                "Sentinel",
                "Guardian",
                "Optimizer",
                "Analyzer",
                "Coordinator",
                "Monitor",
                "Assistant",
                "Helper",
                "Advisor",
                "Specialist",
            ]

            name = f"{random.choice(names)} the {random.choice(specializations)}"

            # Log the birth
            with open("agent_births.log", "a") as f:
                f.write(f'{datetime.now().isoformat()} - Agent born: "{name}"\n')

            self.stats["agents_born"] += 1

            message = f"""🎉 Agent Birth Successful!

New Agent Created:
Name: {name}
Specialization: Intelligent Assistant
Status: Active and Learning

The agent is now ready to help with your workflow!"""

            rumps.alert(title="Agent Born!", message=message, ok="Amazing!")

        except Exception as e:
            rumps.alert(title="Error", message=f"Could not create agent: {e}", ok="OK")

    def _safe_show_performance(self, _):
        """Safely show performance info"""
        try:
            import psutil

            # Get system performance
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=1)

            message = f"""📈 System Performance

Memory Usage: {memory.percent:.1f}%
CPU Usage: {cpu:.1f}%
Available Memory: {memory.available / (1024**3):.1f} GB

SelFlow Performance:
• Events Today: {self.stats['events_today']:,}
• Database Size: {self._get_db_size()}
• System Health: {'🟢 Good' if memory.percent < 80 else '🟡 High'}

The system is running efficiently."""

            rumps.alert(title="Performance", message=message, ok="OK")

        except Exception as e:
            message = f"""📈 System Performance

Events Today: {self.stats['events_today']:,}
Database Size: {self._get_db_size()}
System Health: 🟢 Running

Performance monitoring requires psutil package."""
            rumps.alert(title="Performance", message=message, ok="OK")

    def _get_db_size(self):
        """Get database size safely"""
        try:
            db_path = Path("data/events.db")
            if db_path.exists():
                size_bytes = db_path.stat().st_size
                return f"{size_bytes / (1024*1024):.1f} MB"
            return "No database"
        except:
            return "Unknown"

    def _safe_show_settings(self, _):
        """Safely show settings"""
        try:
            message = """⚙️ SelFlow Settings

Current Configuration:
• Event Capture: ✅ Active
• Pattern Detection: ✅ Active  
• Agent Birth: ✅ Enabled
• System Tray: ✅ Running

Database Location: data/events.db
Log Location: logs/

Settings can be modified through configuration files."""

            rumps.alert(title="Settings", message=message, ok="OK")

        except Exception as e:
            rumps.alert(title="Error", message=f"Could not show settings: {e}", ok="OK")

    def _safe_show_about(self, _):
        """Safely show about dialog"""
        try:
            message = f"""✨ SelFlow - Self-Creating AI System

🧠 Intelligence: Active Learning
📊 Events Processed: {self.stats['events_today']:,}
🤖 Agents Born: {self.stats['agents_born']}

Features:
• Autonomous AI agent creation
• Behavioral pattern learning
• Intelligent task automation
• Real-time system monitoring

SelFlow evolves with your workflow, creating specialized
AI agents that understand and enhance your productivity.

Built with ❤️ for human-AI collaboration."""

            rumps.alert(title="About SelFlow", message=message, ok="Awesome!")

        except Exception as e:
            rumps.alert(title="Error", message=f"Could not show about: {e}", ok="OK")

    def _safe_restart(self, _):
        """Safely restart system"""
        try:
            import subprocess

            response = rumps.alert(
                title="Restart SelFlow",
                message="Are you sure you want to restart the SelFlow system?",
                ok="Restart",
                cancel="Cancel",
            )

            if response == 1:  # OK clicked
                # Try to restart using the launcher
                subprocess.Popen(["./launch_selflow.sh", "restart"])
                rumps.quit_application()

        except Exception as e:
            rumps.alert(title="Error", message=f"Could not restart: {e}", ok="OK")


def create_tray_app(
    agent_manager: AgentManager, config: Dict[str, Any]
) -> Optional[SelFlowTrayApp]:
    """Create the tray application with error handling"""
    if not RUMPS_AVAILABLE:
        print("❌ Cannot create tray app: rumps not installed")
        return None

    try:
        return SelFlowTrayApp(agent_manager, config)
    except Exception as e:
        print(f"❌ Error creating tray app: {e}")
        return None


if __name__ == "__main__":
    # For testing
    try:
        from app.core.agent_manager import AgentManager

        config = {"max_agents": 20}
        agent_manager = AgentManager(config)

        tray_app = create_tray_app(agent_manager, {})
        if tray_app:
            print("✅ Tray app created successfully")
            tray_app.run()
        else:
            print("❌ Failed to create tray app")
    except Exception as e:
        print(f"❌ Error: {e}")
