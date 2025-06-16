#!/usr/bin/env python3
"""
Test script for the Visual SelFlow System
Verifies all components work correctly before full launch.
"""

import asyncio
import logging
import sys
import time
import threading
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app"))


def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")

    try:
        from app.ai.visual_meta_learning import VisualMetaLearningSystem, EmbryoStage

        print("✅ Visual meta-learning system import OK")
    except ImportError as e:
        print(f"❌ Visual meta-learning system import failed: {e}")
        return False

    try:
        from app.web.dashboard_server import DashboardServer

        print("✅ Dashboard server import OK")
    except ImportError as e:
        print(f"❌ Dashboard server import failed: {e}")
        return False

    try:
        import torch

        print("✅ PyTorch import OK")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False

    try:
        import aiohttp

        print("✅ Aiohttp import OK")
    except ImportError as e:
        print(f"❌ Aiohttp import failed: {e}")
        return False

    # Optional imports
    try:
        from app.system.enhanced_tray import EnhancedSelFlowTray

        print("✅ Enhanced tray import OK")
    except ImportError as e:
        print(f"⚠️  Enhanced tray import failed (OK if not on macOS): {e}")

    return True


def test_meta_learning_system():
    """Test the visual meta-learning system"""
    print("\n🧠 Testing meta-learning system...")

    try:
        from app.ai.visual_meta_learning import VisualMetaLearningSystem

        # Create system
        system = VisualMetaLearningSystem()
        print("✅ Meta-learning system created")

        # Test data retrieval
        data = system.get_dashboard_data()
        print(f"✅ Dashboard data retrieved: {len(data)} sections")

        # Test embryo creation
        pattern_data = {
            "type": "TestPattern",
            "data_needed": 100,
            "estimated_training_time": 60,
            "specialization": "Testing",
        }
        embryo_id = system.create_embryo(pattern_data)
        print(f"✅ Test embryo created: {embryo_id}")

        # Test callbacks
        callback_called = False

        def test_callback(embryo):
            nonlocal callback_called
            callback_called = True

        system.set_callbacks(on_embryo_created=test_callback)
        print("✅ Callbacks set successfully")

        # Start and stop processing
        system.start_processing()
        print("✅ Processing started")

        time.sleep(2)  # Let it run briefly

        system.stop_processing()
        print("✅ Processing stopped")

        return True

    except Exception as e:
        print(f"❌ Meta-learning system test failed: {e}")
        return False


def test_dashboard_server():
    """Test the dashboard server"""
    print("\n🌐 Testing dashboard server...")

    try:
        from app.web.dashboard_server import DashboardServer

        # Create server
        server = DashboardServer(
            host="localhost", port=8081
        )  # Use different port for testing
        print("✅ Dashboard server created")

        # Test data manager
        data = server.data_manager.get_current_data()
        print(f"✅ Data manager working: {len(data)} data sections")

        # Test stats update
        server.data_manager.update_data()
        print("✅ Data update successful")

        return True

    except Exception as e:
        print(f"❌ Dashboard server test failed: {e}")
        return False


def test_dashboard_html():
    """Test that dashboard HTML file exists and is valid"""
    print("\n📄 Testing dashboard HTML...")

    try:
        dashboard_path = Path("app/web/dashboard.html")

        if not dashboard_path.exists():
            print("❌ Dashboard HTML file not found")
            return False

        with open(dashboard_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for key elements
        required_elements = [
            "<title>SelFlow Meta-Learning Dashboard</title>",
            'id="embryo-list"',
            'id="agent-list"',
            "Chart.js",
            "WebSocket",
        ]

        for element in required_elements:
            if element not in content:
                print(f"❌ Missing required element: {element}")
                return False

        print(f"✅ Dashboard HTML valid ({len(content)} characters)")
        return True

    except Exception as e:
        print(f"❌ Dashboard HTML test failed: {e}")
        return False


def test_database_access():
    """Test database access"""
    print("\n🗄️  Testing database access...")

    try:
        import sqlite3
        from datetime import datetime

        # Test with demo database if events.db doesn't exist
        db_path = "data/events.db"
        if not Path(db_path).exists():
            print("⚠️  Events database not found, creating test database...")

            # Create test database
            Path("data").mkdir(exist_ok=True)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Create events table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY,
                    timestamp REAL,
                    event_type TEXT,
                    path TEXT,
                    details TEXT
                )
            """
            )

            # Insert test data
            test_events = [
                (time.time(), "file_modify", "/test/file1.py", '{"size": 1024}'),
                (time.time(), "file_create", "/test/file2.py", '{"size": 512}'),
                (time.time(), "app_focus", "VSCode", '{"duration": 300}'),
            ]

            cursor.executemany(
                "INSERT INTO events (timestamp, event_type, path, details) VALUES (?, ?, ?, ?)",
                test_events,
            )

            conn.commit()
            conn.close()
            print("✅ Test database created")

        # Test reading from database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM events")
        count = cursor.fetchone()[0]

        conn.close()

        print(f"✅ Database access successful: {count} events")
        return True

    except Exception as e:
        print(f"❌ Database access test failed: {e}")
        return False


def test_async_functionality():
    """Test async functionality"""
    print("\n⚡ Testing async functionality...")

    try:

        async def test_async():
            # Test basic async functionality
            await asyncio.sleep(0.1)
            return "async_test_passed"

        # Run async test
        result = asyncio.run(test_async())

        if result == "async_test_passed":
            print("✅ Async functionality working")
            return True
        else:
            print("❌ Async test returned unexpected result")
            return False

    except Exception as e:
        print(f"❌ Async functionality test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("🧬 SelFlow Visual System Test Suite")
    print("=" * 50)

    tests = [
        ("Imports", test_imports),
        ("Meta-Learning System", test_meta_learning_system),
        ("Dashboard Server", test_dashboard_server),
        ("Dashboard HTML", test_dashboard_html),
        ("Database Access", test_database_access),
        ("Async Functionality", test_async_functionality),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! System is ready to launch.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements_visual.txt")
        print("2. Launch system: python run_visual_selflow.py")
        print("3. Open dashboard: http://localhost:8080")
        return True
    else:
        print("⚠️  Some tests failed. Please fix issues before launching.")
        print("\nTroubleshooting:")
        print("- Check that all dependencies are installed")
        print("- Ensure you're running Python 3.8+")
        print("- Verify file permissions and paths")
        return False


def main():
    """Main test entry point"""

    # Set up logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise during testing

    # Run tests
    success = run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
