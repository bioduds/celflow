"""
CelFlow AI API Server
FastAPI server that exposes the Central AI Brain through REST endpoints
for the Tauri desktop application and other frontends.
"""

import logging
import yaml
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Add the backend path to sys.path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.ai.central_brain import CentralAIBrain, create_central_brain
from app.core.central_integration import CentralIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global AI system instance
central_brain: Optional[CentralAIBrain] = None
central_integration: Optional[CentralIntegration] = None

# Request/Response Models
class ChatMessage(BaseModel):
    message: str
    context_type: str = "chat"
    session_id: Optional[str] = None
    request_visualization: Optional[bool] = False

class VisualizationData(BaseModel):
    type: str  # 'chart', 'plot', 'table', 'graph', 'text', 'code'
    title: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    message: str
    response_time: float
    interaction_id: int
    agent_info: Dict[str, Any]
    visualization: Optional[VisualizationData] = None
    error: Optional[str] = None

class SystemStatus(BaseModel):
    status: str
    uptime: float
    model_name: str
    agents_active: int
    interaction_count: int
    health_status: Dict[str, Any]

class BlobCommand(BaseModel):
    command: str
    parameters: Optional[Dict[str, Any]] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events for the FastAPI app"""
    global central_brain, central_integration
    
    # Startup
    logger.info("🚀 Starting CelFlow AI API Server...")
    
    try:
        # Load configuration
        config = load_config()
        
        # Initialize Central AI Brain
        central_brain = await create_central_brain(config)
        if not central_brain:
            logger.error("Failed to create Central AI Brain")
            raise Exception("AI system initialization failed")
        
        # Initialize Central Integration
        central_integration = CentralIntegration(config)
        await central_integration.initialize()
        
        logger.info("✅ CelFlow AI API Server started successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to start AI API Server: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down CelFlow AI API Server...")
    if central_brain:
        await central_brain.stop()
    logger.info("✅ AI API Server shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="CelFlow AI API",
    description="API server for CelFlow Central AI Brain",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420", 
        "http://127.0.0.1:1420", 
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "tauri://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_config() -> Dict[str, Any]:
    """Load CelFlow configuration"""
    try:
        # Load AI config
        with open('config/ai_config.yaml', 'r') as f:
            ai_config = yaml.safe_load(f)
        
        # Load default config
        with open('config/default.yaml', 'r') as f:
            default_config = yaml.safe_load(f)
        
        # Merge configurations
        config = {**default_config, **ai_config}
        
        # Set up AI brain config
        config['ai_brain'] = {
            'model_name': ai_config['model']['model_name'],
            'base_url': 'http://localhost:11434',
            'temperature': ai_config['model']['temperature'],
            'max_tokens': ai_config['model']['max_tokens'],
            'context_window': ai_config['model']['context_window'],
            'timeout': 30
        }
        
        return config
        
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        # Fallback config
        return {
            'ai_brain': {
                'model_name': 'gemma3:4b',
                'base_url': 'http://localhost:11434',
                'temperature': 0.7,
                'max_tokens': 2048,
                'context_window': 8192,
                'timeout': 30
            }
        }

@app.get("/")
async def root():
    """API root endpoint"""
    return {"message": "CelFlow AI API Server", "status": "running"}

@app.get("/health", response_model=SystemStatus)
async def health_check():
    """Get system health status"""
    if not central_brain:
        raise HTTPException(status_code=503, detail="AI system not initialized")
    
    try:
        health_status = await central_brain.get_health_status()
        uptime = (datetime.now() - central_brain.startup_time).total_seconds() if central_brain.startup_time else 0
        
        return SystemStatus(
            status="healthy" if health_status.get("central_brain_running", False) else "unhealthy",
            uptime=uptime,
            model_name=health_status.get("ollama_model", "unknown"),
            agents_active=5,  # Number of active agents
            interaction_count=central_brain.interaction_count,
            health_status=health_status
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(message: ChatMessage):
    """Chat with the AI system"""
    if not central_brain:
        raise HTTPException(status_code=503, detail="AI system not initialized")
    
    try:
        start_time = datetime.now()
        
        # Process message through Central AI Brain
        result = await central_brain.chat_with_user_interface_agent(
            message.message,
            context={"session_id": message.session_id}
        )
        
        response_time = (datetime.now() - start_time).total_seconds()
        
        # Generate visualization if requested or if message contains visualization keywords
        visualization = None
        if (message.request_visualization or 
            any(keyword in message.message.lower() for keyword in ['plot', 'chart', 'graph', 'table', 'analyze', 'show', 'visualize'])):
            visualization = await generate_visualization(message.message, result.get("message", ""))
        
        if result.get("success", False):
            return ChatResponse(
                success=True,
                message=result.get("message", ""),
                response_time=response_time,
                interaction_id=result.get("interaction_id", 0),
                agent_info={
                    "agent": result.get("agent", "central_brain"),
                    "context_used": result.get("context_used", False)
                },
                visualization=visualization
            )
        else:
            return ChatResponse(
                success=False,
                message=result.get("message", "Sorry, I encountered an error."),
                response_time=response_time,
                interaction_id=0,
                agent_info={"agent": "error_handler"},
                visualization=visualization,
                error=result.get("error", "Unknown error")
            )
            
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return ChatResponse(
            success=False,
            message="I apologize, but I'm experiencing technical difficulties. Please try again.",
            response_time=0.0,
            interaction_id=0,
            agent_info={"agent": "error_handler"},
            error=str(e)
        )

@app.post("/blob-command")
async def process_blob_command(command: BlobCommand):
    """Process blob creature commands"""
    if not central_brain:
        raise HTTPException(status_code=503, detail="AI system not initialized")
    
    try:
        # Use the AI to interpret blob commands
        system_prompt = """You are controlling an animated blob creature in a desktop application.
        
        The user will give you commands to control the blob's appearance and behavior.
        Respond with a JSON object containing specific blob control parameters.
        
        Available blob properties:
        - mood: "happy", "sad", "excited", "sleeping", "thinking", "dancing"
        - color: any CSS color (hex, rgb, or named colors)
        - size: number between 0.5 and 2.0 (scale factor)
        - position: "center", "left", "right", "top", "bottom"
        - animation: "bounce", "pulse", "wiggle", "spin", "float"
        
        Examples:
        - "make it happy" -> {"mood": "happy"}
        - "turn it red" -> {"color": "#ff0000"}
        - "make it bigger" -> {"size": 1.5}
        - "move to the left" -> {"position": "left"}
        - "make it dance" -> {"mood": "dancing", "animation": "bounce"}
        
        Respond ONLY with valid JSON containing the blob control parameters."""
        
        result = await central_brain.ollama_client.generate_response(
            prompt=f"User command: {command.command}",
            system_prompt=system_prompt
        )
        
        # Try to parse the AI response as JSON
        try:
            import json
            blob_params = json.loads(result.strip())
            return {"success": True, "blob_params": blob_params, "ai_response": result}
        except json.JSONDecodeError:
            # Fallback parsing for non-JSON responses
            blob_params = parse_blob_command_fallback(command.command)
            return {"success": True, "blob_params": blob_params, "ai_response": result}
            
    except Exception as e:
        logger.error(f"Blob command error: {e}")
        return {"success": False, "error": str(e)}

async def generate_visualization(user_message: str, ai_response: str) -> Optional[VisualizationData]:
    """Generate visualization data based on user request and AI response"""
    try:
        # Check if user is asking for specific visualization types
        message_lower = user_message.lower()
        
        if any(keyword in message_lower for keyword in ['chart', 'bar chart', 'pie chart']):
            return VisualizationData(
                type="chart",
                title="Sample Chart",
                data={
                    "labels": ["A", "B", "C", "D"],
                    "values": [10, 25, 15, 30],
                    "chart_type": "bar"
                },
                config={"color_scheme": "blue"}
            )
        
        elif any(keyword in message_lower for keyword in ['plot', 'line plot', 'scatter', 'sine', 'wave']):
            import numpy as np
            x = np.linspace(0, 10, 100).tolist()
            y = np.sin(x).tolist() if 'sine' in message_lower else [i**2 for i in range(len(x))]
            
            return VisualizationData(
                type="plot",
                title="Mathematical Plot",
                data={
                    "x": x[:20],  # Limit data for demo
                    "y": y[:20],
                    "plot_type": "line"
                },
                config={"color": "green", "line_width": 2}
            )
        
        elif any(keyword in message_lower for keyword in ['table', 'data table', 'dataset']):
            return VisualizationData(
                type="table",
                title="Sample Data Table",
                data={
                    "headers": ["Name", "Value", "Category"],
                    "rows": [
                        ["Item A", 100, "Type 1"],
                        ["Item B", 250, "Type 2"],
                        ["Item C", 150, "Type 1"],
                        ["Item D", 300, "Type 3"]
                    ]
                }
            )
        
        elif any(keyword in message_lower for keyword in ['code', 'algorithm', 'function']):
            code_content = """# Sample Python function
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Generate first 10 Fibonacci numbers
fib_sequence = [fibonacci(i) for i in range(10)]
print(fib_sequence)
# Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"""
            
            return VisualizationData(
                type="code",
                title="Python Code Example",
                content=code_content
            )
        
        elif any(keyword in message_lower for keyword in ['analyze', 'analysis', 'summary']):
            return VisualizationData(
                type="text",
                title="AI Analysis Result",
                content=f"Analysis of your request:\n\n{ai_response}\n\nKey insights:\n• Data processing completed\n• Patterns identified\n• Recommendations generated"
            )
        
        # Default visualization for general requests
        if any(keyword in message_lower for keyword in ['show', 'display', 'visualize', 'generate']):
            return VisualizationData(
                type="chart",
                title="Generated Visualization",
                data={
                    "labels": ["Data Point 1", "Data Point 2", "Data Point 3"],
                    "values": [45, 78, 32],
                    "chart_type": "bar"
                },
                config={"color_scheme": "purple"}
            )
        
        return None
        
    except Exception as e:
        logger.error(f"Visualization generation error: {e}")
        return VisualizationData(
            type="text",
            title="Visualization Error",
            content=f"Sorry, I encountered an error generating the visualization: {str(e)}"
        )

def parse_blob_command_fallback(command: str) -> Dict[str, Any]:
    """Fallback blob command parser if AI doesn't return valid JSON"""
    command_lower = command.lower()
    params = {}
    
    # Mood detection
    if "happy" in command_lower:
        params["mood"] = "happy"
    elif "sad" in command_lower:
        params["mood"] = "sad"
    elif "excited" in command_lower:
        params["mood"] = "excited"
    elif "sleep" in command_lower:
        params["mood"] = "sleeping"
    elif "think" in command_lower:
        params["mood"] = "thinking"
    elif "dance" in command_lower:
        params["mood"] = "dancing"
    
    # Color detection
    colors = {
        "red": "#ff0000", "blue": "#0000ff", "green": "#00ff00",
        "yellow": "#ffff00", "purple": "#800080", "orange": "#ffa500",
        "pink": "#ffc0cb", "white": "#ffffff", "black": "#000000"
    }
    for color_name, color_value in colors.items():
        if color_name in command_lower:
            params["color"] = color_value
            break
    
    # Size detection
    if "bigger" in command_lower or "larger" in command_lower:
        params["size"] = 1.5
    elif "smaller" in command_lower:
        params["size"] = 0.7
    
    # Position detection
    if "left" in command_lower:
        params["position"] = "left"
    elif "right" in command_lower:
        params["position"] = "right"
    elif "center" in command_lower:
        params["position"] = "center"
    
    return params

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Process message through AI
            if central_brain:
                result = await central_brain.chat_with_user_interface_agent(data)
                response = {
                    "type": "chat_response",
                    "message": result.get("message", ""),
                    "success": result.get("success", False),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                response = {
                    "type": "error",
                    "message": "AI system not available",
                    "success": False,
                    "timestamp": datetime.now().isoformat()
                }
            
            await manager.send_personal_message(str(response), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/agents")
async def get_agents():
    """Get information about active agents"""
    if not central_brain:
        raise HTTPException(status_code=503, detail="AI system not initialized")
    
    agents = {
        "user_interface": {
            "name": "User Interface Agent",
            "status": "active" if central_brain.user_interface else "inactive",
            "description": "Natural language processing and user interaction"
        },
        "agent_orchestrator": {
            "name": "Agent Orchestrator", 
            "status": "active" if central_brain.agent_orchestrator else "inactive",
            "description": "Coordinates multiple agents for complex tasks"
        },
        "system_controller": {
            "name": "System Controller",
            "status": "active" if central_brain.system_controller else "inactive", 
            "description": "Translates user commands to system actions"
        },
        "embryo_trainer": {
            "name": "Embryo Trainer",
            "status": "active" if central_brain.embryo_trainer else "inactive",
            "description": "Intelligent training and validation of embryos"
        },
        "pattern_validator": {
            "name": "Pattern Validator",
            "status": "active" if central_brain.pattern_validator else "inactive",
            "description": "Ensures pattern classification coherence"
        }
    }
    
    return {"agents": agents, "total_agents": len(agents)}

if __name__ == "__main__":
    uvicorn.run(
        "ai_api_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 