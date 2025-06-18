# CelFlow - Self-Creating AI Operating System

CelFlow is a revolutionary AI system that creates specialized agents based on your behavior patterns. It features a beautiful Tauri desktop application with real-time analytics and an integrated chat interface.

## Features

- **Intelligent Agent Creation**: Automatically creates specialized AI agents based on your workflow patterns
- **Beautiful Desktop Interface**: Modern Tauri app with real-time analytics and integrated chat
- **Pattern Evolution**: Continuously learns and adapts to your behavior
- **Complete Privacy**: All processing happens locally on your machine
- **Lightweight**: 5-12MB footprint vs 150MB+ alternatives

### 🚀 New Features (Phase 1 Complete!)

- **🎨 Advanced Visualization Engine**: 
  - 10+ chart types (line, bar, pie, scatter, radar, network graphs, heatmaps)
  - Real-time data streaming with live updates
  - D3.js, Chart.js, and Plotly.js integration
  - Interactive visualizations with zoom, pan, and drill-down

- **🧠 AI Lambda Capability**: 
  - Dynamic code execution sandbox (like AWS Lambda but local)
  - AI can write and execute Python code on-demand
  - Secure sandbox with resource limits and safety validation
  - Perfect for complex calculations, custom algorithms, and data processing

- **📊 Multimodal Processing**:
  - Image analysis and screenshot capture
  - CSV/JSON/Excel data processing with AI insights
  - Code analysis for Python, JavaScript, TypeScript
  - PDF and document text extraction
  - Automatic visualization suggestions

- **💬 Enhanced Chat-Stage Coordination**:
  - AI always talks via chat AND shows via stage
  - Clean interface with on-demand visualizations
  - Context-aware responses with conversation memory
  - Proactive suggestions based on usage patterns

## Installation

1. Clone the repository:
```bash
git clone https://github.com/celflow/celflow.git
cd celflow
```

2. Install dependencies:
```bash
# Python dependencies
python3 -m venv celflow_env
source celflow_env/bin/activate
pip install -r backend/requirements/base.txt

# Frontend dependencies
cd frontend/desktop
npm install
```

3. Install Tauri requirements:
- Node.js and npm
- Rust and Cargo
- Tauri CLI (`cargo install tauri-cli`)

## Usage

1. Start CelFlow:
```bash
./launch_celflow.sh start
```

2. The Tauri desktop app will launch automatically, providing:
- Real-time system analytics
- Pattern evolution visualization
- Integrated chat interface
- Agent management
- System configuration

3. Stop CelFlow:
```bash
./launch_celflow.sh stop
```

## Architecture

CelFlow consists of several key components:

1. **Main System**: Core Python backend that handles:
   - Event capture and processing
   - Pattern detection and analysis
   - Agent creation and management

2. **Desktop App**: Beautiful Tauri interface featuring:
   - Real-time analytics dashboard
   - Integrated chat interface
   - Pattern visualization
   - System configuration
   - Agent management

3. **AI Components**:
   - Central AI Brain with Gemma 3:4b for coordinating agents
   - Pattern detection system with advanced clustering
   - Agent specialization logic with embryo training
   - Dynamic code execution sandbox (Lambda capability)
   - Multimodal processing for images, data, and code
   - Real-time visualization engine

## Development

1. Start in development mode:
```bash
./launch_celflow.sh start
```

2. The system will:
- Launch the main Python backend
- Start the Tauri desktop app in dev mode
- Enable hot reloading for frontend changes

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

Copyright © 2024 CelFlow. All rights reserved.

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

## 🧠 AI Lambda Capability

CelFlow's AI can now write and execute custom Python code on-demand, similar to AWS Lambda but running locally:

### When AI Uses Code Execution

The AI automatically recognizes when to use code execution for:
- Complex mathematical calculations (prime numbers, Fibonacci, factorials)
- Data processing and transformation
- Custom algorithm implementation
- Statistical analysis and machine learning
- Dynamic visualization generation

### Example Interactions

**User**: "Calculate the first 20 prime numbers"
**AI**: *Writes and executes code, returns actual results*

**User**: "Analyze this CSV file and show me correlations"
**AI**: *Processes data with pandas, generates visualization*

**User**: "Create a custom sorting algorithm for my specific needs"
**AI**: *Implements and tests the algorithm in real-time*

### Security Features

- AST-based code validation prevents dangerous operations
- Resource limits (memory and execution time)
- Sandboxed execution environment
- Whitelisted imports only
- No file system or network access

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

### Phase 1: Real Visualization Engine Foundation ✅ COMPLETE!
- ✅ Advanced visualization library integration (Chart.js, D3.js, Plotly.js)
- ✅ 10+ interactive chart types with real-time updates
- ✅ Live data streaming from CelFlow systems
- ✅ Network graphs for clustering and relationships
- ✅ Heatmaps and 3D visualization support

### Phase 1.6: Multimodal AI Capabilities ✅ COMPLETE!
- ✅ Image processing and screenshot analysis
- ✅ CSV/JSON/Excel file processing with AI insights
- ✅ Code analysis and documentation generation
- ✅ PDF and document text extraction
- ✅ Mermaid diagram generation

### Phase 1.5: Context & Memory System ✅ COMPLETE!
- ✅ Persistent conversation memory
- ✅ Context-aware responses
- ✅ Session management
- ✅ Smart context pruning

### NEW: AI Lambda Capability ✅ COMPLETE!
- ✅ Dynamic code execution sandbox
- ✅ AI can write and execute Python code on-demand
- ✅ Secure execution with resource limits
- ✅ Lambda-style event-driven functions
- ✅ Matplotlib visualization generation

### Phase 2: Enhanced Central AI Agent 🔄 NEXT
- Multi-modal response system
- Intent classification engine
- System introspection capabilities
- Dynamic visualization generation
- Proactive insights and suggestions

### Phase 3: Web Search & Context Intelligence 📋
- Web search API integration
- Information extraction and summarization
- Smart context management
- Knowledge base building
- Cross-domain knowledge linking

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