#!/usr/bin/env python3
"""
SelFlow - Self-Evolving AI Operating System Layer

Main application entry point that coordinates the embryo pool,
system monitoring, and user interface components.
"""

import asyncio
import logging
import sys
import signal
from typing import Optional
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer, QThread, pyqtSignal

from app.core.embryo_pool import EmbryoPool
from app.system.tray_icon import SelFlowTrayIcon
from app.core.data_stream import DataStreamMonitor
from app.system.permissions import PermissionManager


class SelFlowApp:
    """
    Main SelFlow application that coordinates all components.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('SelFlowApp')
        
        # Core components
        self.embryo_pool: Optional[EmbryoPool] = None
        self.data_monitor: Optional[DataStreamMonitor] = None
        self.tray_icon: Optional[SelFlowTrayIcon] = None
        self.permission_manager: Optional[PermissionManager] = None
        
        # Application state
        self.is_running = False
        self.config = self._load_config()
        
        # Setup Qt application
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setQuitOnLastWindowClosed(False)
        
    def _load_config(self) -> dict:
        """Load application configuration"""
        # Default configuration
        config = {
            'embryo_pool': {
                'max_concurrent': 15,
                'min_survival_threshold': 0.3,
                'data_buffer_limit_mb': 16
            },
            'privacy': {
                'filter_passwords': True,
                'filter_credit_cards': True,
                'filter_personal_info': True,
                'filter_sensitive_apps': [
                    'Banking', 'Password Manager', 'VPN', 'KeyChain Access',
                    'Wallet', 'Crypto', 'Finance'
                ]
            },
            'system': {
                'silent_mode': True,
                'learning_enabled': True,
                'resource_limit_cpu': 30,
                'resource_limit_memory_mb': 4096
            }
        }
        
        # Try to load from config file
        config_path = Path(__file__).parent.parent / 'config' / 'default.yaml'
        if config_path.exists():
            try:
                import yaml
                with open(config_path, 'r') as f:
                    file_config = yaml.safe_load(f)
                    config.update(file_config)
            except Exception as e:
                self.logger.warning(f"Could not load config file: {e}")
                
        return config
        
    async def initialize(self) -> bool:
        """Initialize all application components"""
        try:
            self.logger.info("Initializing SelFlow...")
            
            # Check and request permissions
            self.permission_manager = PermissionManager()
            if not await self.permission_manager.check_all_permissions():
                self.logger.error("Required permissions not granted")
                return False
                
            # Initialize embryo pool
            self.embryo_pool = EmbryoPool(self.config)
            await self.embryo_pool.initialize()
            
            # Initialize data stream monitor
            self.data_monitor = DataStreamMonitor(self.config)
            await self.data_monitor.initialize()
            
            # Connect data stream to embryo pool
            self.data_monitor.data_event.connect(self._handle_system_event)
            
            # Initialize system tray
            self.tray_icon = SelFlowTrayIcon()
            self.tray_icon.toggle_learning_requested.connect(self._toggle_learning)
            self.tray_icon.show()
            
            # Start background update timer
            self.update_timer = QTimer()
            self.update_timer.timeout.connect(self._update_status)
            self.update_timer.start(5000)  # Update every 5 seconds
            
            self.is_running = True
            self.logger.info("SelFlow initialization complete")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            return False
            
    async def _handle_system_event(self, event_data: dict):
        """Handle system event from data monitor"""
        try:
            if self.embryo_pool and self.is_running:
                patterns = await self.embryo_pool.feed_data(event_data)
                
                # Check for birth-ready embryos
                birth_ready = await self.embryo_pool.get_birth_ready_embryo()
                if birth_ready:
                    await self._handle_agent_birth(birth_ready)
                    
        except Exception as e:
            self.logger.error(f"Error handling system event: {e}")
            
    async def _handle_agent_birth(self, embryo):
        """Handle the birth of a new agent"""
        try:
            self.logger.info(f"Agent birth triggered for embryo {embryo.embryo_id}")
            
            # Prepare birth data
            birth_data = embryo.prepare_birth_data()
            
            # For now, just show notification
            # In phase 3, this would create actual agent
            if self.tray_icon:
                agent_info = {
                    'name': f"Agent {embryo.embryo_id[:8]}",
                    'specialization': birth_data['dominant_specialization']
                }
                self.tray_icon.show_agent_birth_notification(agent_info)
                
            # Mark embryo as processed
            embryo.birth_ready = False
            
        except Exception as e:
            self.logger.error(f"Error handling agent birth: {e}")
            
    def _update_status(self):
        """Update system status and UI"""
        try:
            if self.embryo_pool and self.tray_icon:
                pool_status = self.embryo_pool.get_pool_status()
                self.tray_icon.update_pool_status(pool_status)
                
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")
            
    def _toggle_learning(self):
        """Toggle learning on/off"""
        try:
            if self.data_monitor:
                if self.is_running:
                    self.is_running = False
                    self.data_monitor.pause()
                    self.logger.info("Learning paused")
                else:
                    self.is_running = True
                    self.data_monitor.resume()
                    self.logger.info("Learning resumed")
                    
        except Exception as e:
            self.logger.error(f"Error toggling learning: {e}")
            
    def run(self):
        """Run the main application loop"""
        try:
            # Handle graceful shutdown
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # Show startup notification
            if self.tray_icon:
                self.tray_icon.showMessage(
                    "SelFlow Started",
                    "Learning your patterns silently...",
                    self.tray_icon.MessageIcon.Information,
                    3000
                )
                
            # Start Qt event loop
            return self.qt_app.exec()
            
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            return 1
            
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown"""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        
    def shutdown(self):
        """Shutdown the application gracefully"""
        try:
            self.logger.info("Shutting down SelFlow...")
            
            self.is_running = False
            
            if self.data_monitor:
                self.data_monitor.stop()
                
            if self.tray_icon:
                self.tray_icon.hide()
                
            self.qt_app.quit()
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")


def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('selflow.log'),
            logging.StreamHandler()
        ]
    )


async def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger('main')
    
    try:
        # Create and initialize application
        app = SelFlowApp()
        
        if not await app.initialize():
            logger.error("Failed to initialize application")
            return 1
            
        logger.info("Starting SelFlow application...")
        return app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    try:
        # Run the async main function
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nSelFlow interrupted by user")
        sys.exit(0) 