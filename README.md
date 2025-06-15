# SelFlow - Self-Creating AI Operating System

**The first AI system that creates specialized agents from your behavior patterns.**

SelFlow is a revolutionary AI operating system layer that observes your computer usage, learns behavioral patterns, and autonomously creates specialized AI agents tailored to your workflow. The system starts with simple pattern detection and evolves into a personalized ecosystem of intelligent agents.

## 🧬 How It Works

SelFlow operates through a unique **embryo-to-agent evolution process**:

1. **Silent Observation** - The system monitors your computer activity (file operations, app usage, etc.)
2. **Pattern Detection** - Advanced algorithms identify behavioral patterns in your workflow
3. **Embryo Development** - Virtual "embryos" develop specialized intelligence based on detected patterns
4. **Agent Birth** - When embryos reach maturity, they become specialized AI agents
5. **Ecosystem Growth** - Agents coordinate to provide intelligent assistance

## ✨ Key Features

- 🔒 **Privacy-First**: All processing happens locally on your machine
- 🧠 **Intelligent Learning**: Advanced pattern detection from real user behavior
- 🤖 **Autonomous Agent Creation**: System creates agents without user intervention
- 🎯 **Specialized Intelligence**: Each agent develops unique capabilities
- 🖥️ **Native macOS Integration**: Beautiful system tray interface
- 📊 **Real-Time Monitoring**: Live system status and performance metrics

## 🚀 Quick Start

### Prerequisites

- **macOS** (tested on macOS 14.3+)
- **Python 3.8+**
- **4GB RAM minimum**
- **Accessibility permissions** (for system monitoring)

### Installation

```bash
# Clone the repository
git clone https://github.com/bioduds/selflow.git
cd selflow

# Create and activate virtual environment
python3 -m venv selflow_env
source selflow_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Grant necessary permissions (follow prompts)
python app/system/permissions.py
```

### Running SelFlow

The easiest way to run SelFlow is using the launcher script:

```bash
# Start the complete system
./launch_selflow.sh start

# Check system status
./launch_selflow.sh status

# Monitor system logs
./launch_selflow.sh logs

# Stop the system
./launch_selflow.sh stop

# Restart the system
./launch_selflow.sh restart

# Restart just the tray
./launch_selflow.sh tray
```

### System Tray Interface

Once running, SelFlow appears in your macOS menu bar with a 🧬 DNA icon. Click it to access:

- **System Status** - Current system state and statistics
- **Active Agents** - View born agents and their specializations
- **Embryo Pool** - Monitor embryo development progress
- **Force Agent Birth** - Manually trigger agent creation
- **Performance** - System resource usage and health
- **Settings** - Configuration options

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SelFlow Architecture                     │
├─────────────────────────────────────────────────────────────┤
│  🧬 System Tray (macOS Menu Bar Integration)               │
├─────────────────────────────────────────────────────────────┤
│  🤖 Agent Manager (Agent Lifecycle & Coordination)         │
├─────────────────────────────────────────────────────────────┤
│  🥚 Embryo Pool (Developing Agent Intelligence)            │
├─────────────────────────────────────────────────────────────┤
│  🔍 Pattern Detector (Behavioral Analysis Engine)          │
├─────────────────────────────────────────────────────────────┤
│  📡 Event Capture (System Activity Monitoring)             │
├─────────────────────────────────────────────────────────────┤
│  💾 SQLite Database (Event Storage & Pattern Data)         │
└─────────────────────────────────────────────────────────────┘
```

## 🧠 Core Components

### Event Capture System
- **File Operations**: Monitors file creation, modification, deletion
- **Application Usage**: Tracks app launches, focus changes, quit events
- **System Events**: Captures system-level activities
- **Privacy Filtering**: Automatically filters sensitive information

### Pattern Detection Engine
- **Behavioral Analysis**: Identifies recurring patterns in user activity
- **Temporal Patterns**: Detects time-based usage patterns
- **Application Workflows**: Learns application usage sequences
- **File Organization**: Understands file management patterns

### Embryo Pool
- **Virtual Embryos**: Develop specialized intelligence from patterns
- **Maturation Process**: Embryos grow by processing events and patterns
- **Specialization**: Each embryo develops unique capabilities
- **Birth Readiness**: Mature embryos trigger agent creation

### Agent Manager
- **Agent Creation**: Transforms mature embryos into specialized agents
- **Lifecycle Management**: Handles agent birth, operation, and coordination
- **Specialization Assignment**: Assigns roles based on detected patterns
- **Performance Monitoring**: Tracks agent effectiveness and health

## 📊 System Status

You can monitor SelFlow's operation through:

### Command Line
```bash
# System status
./launch_selflow.sh status

# Live logs
./launch_selflow.sh logs

# Database statistics
sqlite3 data/events.db "SELECT COUNT(*) as total_events FROM events;"
```

### System Tray
- Real-time event processing statistics
- Agent birth notifications
- Embryo development progress
- System health indicators

### Log Files
- `logs/selflow_main.log` - Main system operations
- `logs/selflow_tray.log` - System tray activities
- `agent_births.log` - Agent creation records

## 🛡️ Privacy & Security

SelFlow is designed with privacy as a core principle:

### Local Processing
- **No Cloud Dependencies**: All processing happens on your machine
- **No Data Transmission**: Your data never leaves your computer
- **Offline Operation**: Works completely offline

### Data Protection
- **Encrypted Storage**: All pattern data is encrypted
- **Sensitive Data Filtering**: Automatically filters passwords, keys, PII
- **Granular Controls**: Fine-grained privacy settings
- **Secure Deletion**: Proper data cleanup on uninstall

### Permissions
- **Accessibility**: Required for system event monitoring
- **Full Disk Access**: Needed for comprehensive file monitoring
- **Screen Recording**: Optional, for advanced pattern detection

## 🗂️ Project Structure

```
selflow/
├── app/
│   ├── core/
│   │   ├── agent_manager.py     # Agent lifecycle management
│   │   ├── embryo_pool.py       # Embryo development system
│   │   ├── pattern_detector.py  # Behavioral pattern analysis
│   │   └── event_capture.py     # System activity monitoring
│   ├── system/
│   │   ├── macos_tray.py        # System tray interface
│   │   └── permissions.py       # macOS permission handling
│   └── utils/
│       ├── database.py          # SQLite database operations
│       └── logging_config.py    # Logging configuration
├── data/
│   ├── events.db               # Event storage database
│   └── patterns/               # Pattern analysis data
├── logs/
│   ├── selflow_main.log        # Main system logs
│   └── selflow_tray.log        # Tray application logs
├── config/
│   └── default.yaml            # System configuration
├── launch_selflow.sh           # System launcher script
├── launch_tray.py              # Tray launcher
├── run_selflow_live.py         # Main system runner
└── requirements.txt            # Python dependencies
```

## 🎯 Agent Specializations

SelFlow creates agents with various specializations based on your usage patterns:

- **System Guardian** - System monitoring and maintenance
- **File Manager** - File organization and management
- **Workflow Optimizer** - Process automation and optimization
- **Pattern Analyst** - Advanced behavioral analysis
- **Task Coordinator** - Task management and scheduling
- **Development Assistant** - Programming and development support
- **Communication Manager** - Email and messaging optimization

## 🔧 Configuration

### System Configuration (`config/default.yaml`)
```yaml
embryo_pool:
  max_embryos: 15
  birth_threshold_mb: 0.001  # Low threshold for quick births
  
agent_manager:
  max_agents: 20
  
event_capture:
  capture_rate: 1.0  # Events per second
  
privacy:
  filter_sensitive: true
  encrypt_storage: true
```

### Environment Variables
```bash
export SELFLOW_LOG_LEVEL=INFO
export SELFLOW_DATA_DIR=./data
export SELFLOW_CONFIG_DIR=./config
```

## 🚨 Troubleshooting

### Common Issues

**System won't start:**
```bash
# Check permissions
python app/system/permissions.py

# Check virtual environment
source selflow_env/bin/activate
pip install -r requirements.txt
```

**Tray crashes:**
```bash
# Restart just the tray
./launch_selflow.sh tray

# Check tray logs
tail -f logs/selflow_tray.log
```

**No agents being born:**
```bash
# Check system status
./launch_selflow.sh status

# Force agent birth
# Use "Force Agent Birth" in system tray menu
```

**Database issues:**
```bash
# Check database
sqlite3 data/events.db ".tables"

# Reset database (WARNING: loses all data)
rm data/events.db
./launch_selflow.sh restart
```

### Getting Help

1. Check the logs: `./launch_selflow.sh logs`
2. Verify system status: `./launch_selflow.sh status`
3. Review permissions: `python app/system/permissions.py`
4. Open an issue on GitHub with logs and system info

## 🛣️ Roadmap

### Current Status ✅
- ✅ Event capture system
- ✅ Pattern detection engine
- ✅ Embryo pool development
- ✅ Agent birth system
- ✅ System tray interface
- ✅ Crash-resistant operation

### Next Phase 🚧
- 🚧 Enhanced agent specialization
- 🚧 Agent communication system
- 🚧 Voice interface integration
- 🚧 Predictive assistance
- 🚧 Cross-application automation

### Future Vision 🔮
- 🔮 Natural language agent interaction
- 🔮 Proactive workflow optimization
- 🔮 Multi-device synchronization
- 🔮 Advanced AI model integration
- 🔮 Plugin ecosystem

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues** - Found a bug? Open an issue
2. **Improve Documentation** - Help make the docs clearer
3. **Add Features** - Implement new capabilities
4. **Test & Feedback** - Try the system and share your experience
5. **Privacy Enhancements** - Strengthen security and privacy

### Development Setup
```bash
# Clone and setup
git clone https://github.com/bioduds/selflow.git
cd selflow
python3 -m venv selflow_env
source selflow_env/bin/activate
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Start development
./launch_selflow.sh start
```

## 📄 License

SelFlow is released under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built with ❤️ for the future of human-AI collaboration
- Inspired by biological evolution and emergent intelligence
- Thanks to the open-source community for foundational tools

---

**SelFlow - Where AI Creates Itself** 🧬✨ 