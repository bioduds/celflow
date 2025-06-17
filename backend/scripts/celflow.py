#!/usr/bin/env python3
"""
CelFlow - The Self-Creating AI Operating System
Phase 3: System Integration Launcher

Launch CelFlow with full macOS system integration including:
- System tray integration
- Real-time event capture
- Agent-user interaction interfaces
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.system.system_integration import main


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("celflow.log")],
    )


if __name__ == "__main__":
    print("🚀 CelFlow - The Self-Creating AI Operating System")
    print("Phase 3: System Integration")
    print("=" * 50)

    # Setup logging
    setup_logging()

    try:
        # Run the main system integration
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 CelFlow shutdown by user")
    except Exception as e:
        print(f"\n❌ CelFlow error: {e}")
        sys.exit(1)
