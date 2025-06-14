#!/usr/bin/env python3
"""
SelFlow Setup and Test Script

Sets up the environment and runs a basic test of the embryo pool.
"""

import subprocess
import sys
import os
from pathlib import Path


def install_dependencies():
    """Install required dependencies"""
    print("🔧 Installing dependencies...")
    
    # Core dependencies that are available
    dependencies = [
        'torch',
        'numpy',
        'asyncio',
        'pathlib',
        'logging',
        'typing'
    ]
    
    # Try to install PyTorch
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            'torch', 'torchvision', 'torchaudio',
            '--index-url', 'https://download.pytorch.org/whl/cpu'
        ])
        print("✅ PyTorch installed successfully")
    except subprocess.CalledProcessError:
        print("⚠️  PyTorch installation failed, using mock version")
        
    print("✅ Dependencies setup complete")


def run_embryo_test():
    """Run the embryo pool test"""
    print("\n🧬 Running Embryo Pool Test...")
    
    try:
        # Run the test script
        result = subprocess.run([
            sys.executable, 'test_embryo_pool.py'
        ], capture_output=True, text=True, timeout=60)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        if result.returncode == 0:
            print("✅ Embryo Pool Test Passed!")
        else:
            print("❌ Embryo Pool Test Failed!")
            
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out")
    except Exception as e:
        print(f"❌ Test error: {e}")


def main():
    """Main setup and test function"""
    print("🚀 SelFlow Embryo Pool Setup & Test")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
        
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Install dependencies
    install_dependencies()
    
    # Run test
    run_embryo_test()
    
    print("\n🎉 Setup and test complete!")
    print("\nNext steps:")
    print("1. Run: python test_embryo_pool.py")
    print("2. Check the logs for embryo activity")
    print("3. Watch for agent birth notifications")


if __name__ == '__main__':
    main() 