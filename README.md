# CelFlow - Self-Evolving AI Operating System Layer

CelFlow is an innovative AI system that learns your digital patterns and evolves specialized agents to enhance your computing experience. It operates silently in the background, observing your interactions and gradually developing intelligent assistants tailored to your unique workflow.

## 🧬 What is CelFlow?

CelFlow represents a new paradigm in personal AI - instead of using pre-built assistants, it grows its own agents based on your actual usage patterns. Think of it as an AI ecosystem that evolves alongside your digital life.

### Key Features

- **Silent Learning**: Monitors your system activity without interruption
- **Agent Evolution**: Develops specialized AI agents based on your patterns  
- **Privacy-First**: All processing happens locally on your machine
- **Adaptive Intelligence**: Continuously learns and improves over time
- **Seamless Integration**: Works invisibly in the background

## 🚀 Quick Start

### Prerequisites

- macOS 10.15+ (Catalina or later)
- Python 3.9+
- 4GB+ RAM recommended
- Accessibility permissions (for system monitoring)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/celflow/celflow.git
   cd celflow
   ```

2. **Set up the environment**
   ```bash
   # Create virtual environment
   python3 -m venv environments/celflow_env
   source environments/celflow_env/bin/activate
   
   # Install dependencies
   pip install -r backend/requirements/base.txt
   ```

3. **Grant permissions**
   - Go to System Preferences → Security & Privacy → Privacy
   - Enable "Accessibility" for Terminal or your IDE
   - Enable "Full Disk Access" if prompted

4. **Start CelFlow**
   ```bash
   ./launch_celflow.sh start
   ```

## 📊 System Architecture

CelFlow consists of several integrated components:

- **Event Capture**: Monitors system events and user interactions
- **Embryo Pool**: Manages developing agent patterns
- **Central AI Brain**: Coordinates learning and decision-making
- **Agent Manager**: Handles agent lifecycle and specialization
- **System Tray**: Provides user interface and controls

## 🎯 How It Works

1. **Observation Phase**: CelFlow silently monitors your digital activities
2. **Pattern Recognition**: Identifies recurring patterns in your behavior
3. **Embryo Development**: Creates potential agents based on detected patterns
4. **Agent Birth**: Specialized agents emerge when patterns reach maturity
5. **Continuous Evolution**: Agents adapt and improve based on feedback

## 🛠️ Usage

### Basic Commands

```bash
# Start the system
./launch_celflow.sh start

# Check status
./launch_celflow.sh status

# Stop the system
./launch_celflow.sh stop

# Restart everything
./launch_celflow.sh restart

# View logs
./launch_celflow.sh logs
```

### System Tray

CelFlow runs in your system tray with a 🧬 icon. Right-click to access:

- System status and statistics
- Agent management controls
- Learning toggle (pause/resume)
- Configuration options
- Logs and diagnostics

### Dashboard

Access the web dashboard at `http://localhost:8080` to view:

- Real-time system activity
- Agent development progress
- Pattern evolution graphs
- System performance metrics

## 🔧 Configuration

CelFlow can be configured through YAML files in the `config/` directory:

- `default.yaml`: Core system settings
- `ai_config.yaml`: AI model and learning parameters
- `emergent_agents.yaml`: Agent templates and evolution rules

## 📈 Development Phases

CelFlow development follows a structured approach:

### Phase 1: Foundation ✅
- Event capture system
- Basic pattern detection
- Data persistence
- System tray integration

### Phase 2: Intelligence 🔄
- Central AI brain
- Advanced pattern recognition
- Embryo development system
- Agent orchestration

### Phase 3: Evolution 📋
- Agent birth and specialization
- Meta-learning capabilities
- Advanced user interaction
- Performance optimization

## 🔒 Privacy & Security

CelFlow is designed with privacy as a core principle:

- **Local Processing**: All AI processing happens on your device
- **No Data Transmission**: Your data never leaves your machine
- **Sensitive Content Filtering**: Automatically excludes passwords, financial data
- **Granular Controls**: Fine-tune what gets monitored
- **Transparent Operation**: Full visibility into system activities

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
pip install -r backend/requirements/dev.txt

# Run tests
python -m pytest backend/tests/

# Code formatting
black backend/
flake8 backend/
```

## 📚 Documentation

- [Architecture Overview](docs/architecture/ARCHITECTURE.md)
- [Agent Development Guide](docs/guides/AGENT_DEVELOPMENT.md)
- [API Reference](docs/api/README.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🐛 Troubleshooting

### Common Issues

**Permission Denied Errors**
- Ensure Accessibility permissions are granted
- Try running with `sudo` if needed

**High CPU Usage**
- Check system resource limits in config
- Reduce monitoring frequency if needed

**Agents Not Developing**
- Verify sufficient activity patterns
- Check embryo development thresholds

### Getting Help

- Check the [Issues](https://github.com/celflow/celflow/issues) page
- Join our [Discord Community](https://discord.gg/celflow)
- Email support: help@celflow.com

## 📄 License

CelFlow is released under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai) for local AI processing
- Uses [Tauri](https://tauri.app) for desktop integration
- Inspired by biological evolution and emergence

---

**CelFlow** - Where AI evolves with you 🧬 