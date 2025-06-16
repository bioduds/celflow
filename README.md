# SelFlow - Self-Creating AI Operating System

**The first AI system that creates specialized agents from your behavior patterns.**

SelFlow is a revolutionary AI operating system layer that observes your computer usage, learns behavioral patterns, and autonomously creates specialized AI agents tailored to your workflow. The system combines advanced machine learning with a beautiful desktop interface to provide intelligent assistance that evolves with your needs.

## 🚀 New: Desktop Application

SelFlow now features a **stunning Tauri-based desktop application** with professional data visualization and real-time analytics:

- 🖥️ **Beautiful Desktop UI** - Modern glass morphism design with neural-themed aesthetics
- 📊 **Advanced Analytics Dashboard** - Real-time visualization of 130K+ events and patterns
- 🤖 **Agent Architecture Display** - Visual representation of specialized AI agents
- 📈 **Pattern Evolution Timeline** - Track confidence and stability metrics over time
- 🎯 **AI Recommendations** - Priority-based suggestions with implementation roadmaps
- ⚡ **High Performance** - 5-12MB footprint vs 150MB+ Electron alternatives

### Desktop App Quick Start

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Tauri CLI
cargo install tauri-cli@^2.0

# Install Node.js dependencies
npm install

# Launch the desktop application
npm run tauri:dev
```

## 🧬 How It Works

SelFlow operates through a unique **embryo-to-agent evolution process**:

1. **Silent Observation** - The system monitors your computer activity (file operations, app usage, etc.)
2. **Advanced Pattern Detection** - ML algorithms with clustering analysis identify behavioral patterns
3. **Embryo Development** - Virtual "embryos" develop specialized intelligence based on detected patterns
4. **Agent Birth** - When embryos reach maturity, they become specialized AI agents
5. **Ecosystem Growth** - Agents coordinate to provide intelligent assistance

## ✨ Key Features

### Core Intelligence
- 🔒 **Privacy-First**: All processing happens locally on your machine
- 🧠 **Advanced ML Pipeline**: Pydantic models with sophisticated clustering algorithms
- 🤖 **Autonomous Agent Creation**: System creates agents without user intervention
- 🎯 **Specialized Intelligence**: Each agent develops unique capabilities based on real data

### Desktop Experience
- 🖥️ **Beautiful Desktop App**: Tauri-based application with React frontend
- 📊 **Real-Time Analytics**: Live visualization of system metrics and patterns
- 🎨 **Professional UI**: Glass morphism design with neural-themed color palette
- 📈 **Interactive Charts**: Comprehensive data visualization with D3.js and Recharts

### System Integration
- 🍎 **Native macOS Integration**: Beautiful system tray interface
- 🗣️ **Voice Interface**: Advanced speech recognition and synthesis
- 📡 **Real-Time Monitoring**: Live system status and performance metrics
- 🔧 **Enhanced Tray**: Multiple tray interfaces for different use cases

## 🏗️ Enhanced Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SelFlow Architecture                     │
├─────────────────────────────────────────────────────────────┤
│  🖥️ Tauri Desktop App (React + TypeScript Frontend)        │
│  🦀 Rust Backend (High-Performance Native Integration)      │
├─────────────────────────────────────────────────────────────┤
│  🧬 System Tray (macOS Menu Bar Integration)               │
│  🗣️ Voice Interface (Speech Recognition & Synthesis)       │
├─────────────────────────────────────────────────────────────┤
│  🤖 Agent Manager (Agent Lifecycle & Coordination)         │
│  🧠 Central AI Brain (Meta-Learning & Pattern Validation)  │
├─────────────────────────────────────────────────────────────┤
│  🥚 Embryo Pool (Developing Agent Intelligence)            │
│  📊 Advanced Analytics (Clustering & ML Pipeline)          │
├─────────────────────────────────────────────────────────────┤
│  🔍 Pattern Detector (Behavioral Analysis Engine)          │
│  🎯 Proactive Suggestions (AI-Powered Recommendations)     │
├─────────────────────────────────────────────────────────────┤
│  📡 Event Capture (System Activity Monitoring)             │
│  🌐 Web Dashboard (Browser-Based Analytics)                │
├─────────────────────────────────────────────────────────────┤
│  💾 SQLite Database (Event Storage & Pattern Data)         │
│  📋 Pydantic Models (Type-Safe Data Validation)            │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **macOS** (tested on macOS 14.3+)
- **Python 3.8+**
- **Node.js 18+** (for desktop app)
- **Rust 1.70+** (for Tauri desktop app)
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

# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements_pydantic.txt
pip install -r requirements_visual.txt

# Install Node.js dependencies for desktop app
npm install

# Install Rust and Tauri CLI (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install tauri-cli@^2.0

# Grant necessary permissions (follow prompts)
python app/system/permissions.py
```

### Running SelFlow

#### Option 1: Desktop Application (Recommended)
```bash
# Launch the beautiful desktop application
npm run tauri:dev

# Or build for production
npm run tauri:build
```

#### Option 2: Traditional System Tray
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
```

#### Option 3: Visual Analytics Mode
```bash
# Run with enhanced visual analytics
python run_visual_selflow.py
```

### System Interfaces

#### Desktop Application
The new Tauri desktop app provides:
- **System Overview** - Real-time metrics and event distribution
- **Clustering Results** - Algorithm performance and consensus analysis
- **Pattern Evolution** - Timeline charts showing pattern development
- **AI Recommendations** - Priority-based suggestions with implementation phases

#### System Tray Interface
Multiple tray options available:
- **Standard Tray** - Basic system control and monitoring
- **Enhanced Tray** - Advanced analytics and agent management
- **Analysis Tray** - Deep pattern analysis and clustering insights

#### Voice Interface
```bash
# Enable voice commands and responses
python app/system/voice_interface.py
```

## 🧠 Advanced Components

### Machine Learning Pipeline
- **Advanced Clustering Engine**: Sophisticated algorithms for pattern detection
- **Pydantic Models**: Type-safe data validation and serialization
- **Meta-Learning System**: Learns how to learn from user patterns
- **Pattern Validator**: Ensures pattern quality and relevance

### Data Analytics
- **130K+ Events Processing**: Handles large-scale behavioral data
- **Real-Time Clustering**: Live pattern detection and analysis
- **Confidence Tracking**: Monitors pattern stability over time
- **Performance Metrics**: Comprehensive system health monitoring

### Agent Specializations
Based on actual data analysis, SelFlow creates two primary agent types:

- **GeneralFileAgent** (1M parameters, 95.2% of data)
  - Handles cache and state file operations
  - Optimizes file system performance
  - Manages temporary file cleanup

- **SystemAgent** (200K parameters, 4.8% of data)
  - Manages temporary file operations
  - Handles system-level optimizations
  - Coordinates with OS services

## 📊 Data Insights

Our analysis of real SelFlow data reveals:

- **99.4% File Operations** - Primarily cache, state, and temporary files
- **0.6% Application Events** - App launches, focus changes, system events
- **Heavy VS Code Usage** - Significant development environment activity
- **Browser Cache Operations** - Extensive web browser file management

This data-driven approach ensures agents are specialized for actual usage patterns, not assumptions.

## 🗂️ Enhanced Project Structure

```
selflow/
├── selflow-desktop/              # Tauri desktop application
│   ├── src-tauri/               # Rust backend
│   │   ├── src/lib.rs          # Python integration commands
│   │   └── tauri.conf.json     # App configuration
│   └── src/                    # React frontend
│       ├── components/         # UI components
│       ├── types/             # TypeScript definitions
│       └── utils/             # Utility functions
├── src/                        # React components (root level)
│   ├── App.tsx                # Main application
│   ├── components/            # Dashboard components
│   └── types/selflow.ts       # Type definitions
├── app/
│   ├── ai/                    # Advanced AI components
│   │   ├── central_brain.py   # Meta-learning system
│   │   ├── meta_learning_system.py
│   │   ├── pattern_validator.py
│   │   └── proactive_suggestion_engine.py
│   ├── analytics/             # ML and clustering
│   │   ├── advanced_clustering_engine.py
│   │   └── models.py          # Pydantic data models
│   ├── core/                  # Core system components
│   ├── system/                # System integration
│   │   ├── enhanced_tray.py   # Advanced tray interface
│   │   ├── voice_interface.py # Speech capabilities
│   │   └── macos_tray.py      # Standard tray
│   └── web/                   # Web dashboard
│       ├── dashboard.html     # Browser interface
│       └── dashboard_server.py
├── docs/                      # Comprehensive documentation
│   ├── architecture/          # System architecture docs
│   ├── guides/               # User and developer guides
│   ├── implementation/       # Implementation details
│   ├── planning/            # Project planning docs
│   └── testing/             # Testing documentation
├── data/                     # Data storage
├── logs/                     # System logs
├── config/                   # Configuration files
├── package.json             # Node.js dependencies
├── tailwind.config.js       # UI styling configuration
├── vite.config.ts          # Build configuration
└── requirements*.txt        # Python dependencies
```

## 🎯 Advanced Features

### Desktop Application Features
- **Glass Morphism Design** - Modern, professional interface
- **Neural Color Palette** - Custom theme optimized for data visualization
- **Interactive Charts** - Real-time data visualization with hover effects
- **Responsive Layout** - Adapts to different screen sizes
- **Type-Safe Communication** - React ↔ Rust ↔ Python integration

### AI Capabilities
- **Proactive Suggestions** - AI-generated recommendations for workflow optimization
- **Pattern Evolution Tracking** - Monitor how patterns change over time
- **Confidence Metrics** - Quantify pattern reliability and stability
- **Meta-Learning** - System learns how to improve its own learning

### System Integration
- **Cross-Platform Python Detection** - Automatically finds Python executables
- **State Management** - Persistent application state across sessions
- **Error Recovery** - Robust error handling and recovery mechanisms
- **Performance Monitoring** - Real-time system resource tracking

## 🛡️ Privacy & Security

SelFlow maintains its privacy-first approach:

### Local Processing
- **No Cloud Dependencies**: All processing happens on your machine
- **No Data Transmission**: Your data never leaves your computer
- **Offline Operation**: Works completely offline

### Enhanced Security
- **Type-Safe Data Handling**: Pydantic models ensure data integrity
- **Encrypted Storage**: All pattern data is encrypted
- **Sensitive Data Filtering**: Automatically filters passwords, keys, PII
- **Secure Desktop App**: Tauri provides native security features

## 🔧 Configuration

### Desktop App Configuration
The desktop app automatically detects and integrates with your Python environment.

### System Configuration (`config/default.yaml`)
```yaml
embryo_pool:
  max_embryos: 15
  birth_threshold_mb: 0.001
  
agent_manager:
  max_agents: 20
  specializations:
    - GeneralFileAgent
    - SystemAgent
  
clustering:
  algorithms:
    - kmeans
    - dbscan
    - hierarchical
  consensus_threshold: 0.8
  
analytics:
  confidence_tracking: true
  pattern_evolution: true
  real_time_updates: true
```

## 🚨 Troubleshooting

### Desktop App Issues

**App won't start:**
```bash
# Check Rust installation
rustc --version

# Check Node.js dependencies
npm install

# Check Tauri CLI
cargo install tauri-cli@^2.0
```

**Python integration issues:**
```bash
# Verify Python environment
which python3
python3 --version

# Check Python dependencies
pip install -r requirements_pydantic.txt
```

### System Issues

**Traditional troubleshooting still applies:**
```bash
# Check system status
./launch_selflow.sh status

# View logs
./launch_selflow.sh logs

# Restart system
./launch_selflow.sh restart
```

## 🛣️ Roadmap

### Current Status ✅
- ✅ Tauri desktop application with React frontend
- ✅ Advanced clustering engine with Pydantic models
- ✅ Real-time data visualization and analytics
- ✅ Type-safe Rust ↔ Python integration
- ✅ Professional UI with glass morphism design
- ✅ Voice interface and enhanced tray options
- ✅ Comprehensive documentation structure

### Next Phase 🚧
- 🚧 Real-time Python data integration in desktop app
- 🚧 Advanced agent communication protocols
- 🚧 Cross-platform desktop app support (Windows, Linux)
- 🚧 Plugin system for custom agent types
- 🚧 Enhanced voice command recognition

### Future Vision 🔮
- 🔮 Natural language agent interaction
- 🔮 Multi-device synchronization
- 🔮 Advanced AI model integration (LLMs)
- 🔮 Marketplace for community agents
- 🔮 Enterprise deployment options

## 🤝 Contributing

We welcome contributions to both the Python backend and Tauri frontend:

### Development Setup
```bash
# Clone and setup
git clone https://github.com/bioduds/selflow.git
cd selflow

# Python environment
python3 -m venv selflow_env
source selflow_env/bin/activate
pip install -r requirements.txt
pip install -r requirements_pydantic.txt

# Node.js environment
npm install

# Rust environment
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install tauri-cli@^2.0

# Start development
npm run tauri:dev
```

### Areas for Contribution
1. **Desktop App Features** - Enhance the React/Tauri interface
2. **ML Algorithms** - Improve clustering and pattern detection
3. **Agent Specializations** - Create new agent types
4. **Documentation** - Improve guides and examples
5. **Testing** - Add comprehensive test coverage

## 📄 License

SelFlow is released under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built with ❤️ for the future of human-AI collaboration
- Powered by **Tauri** for high-performance desktop applications
- Enhanced with **Pydantic** for type-safe data handling
- Visualized with **React**, **D3.js**, and **Recharts**
- Inspired by biological evolution and emergent intelligence
- Thanks to the open-source community for foundational tools

---

**SelFlow - Where AI Creates Itself** 🧬✨

*Now with a beautiful desktop experience that makes AI evolution visible and interactive.* 