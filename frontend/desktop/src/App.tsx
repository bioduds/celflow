import React, { useState, useEffect, useRef } from "react";
import "./index.css";

// Mock data types
interface SystemMetrics {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: {
    total: number;
    used: number;
    free: number;
  };
  events_per_second: number;
}

// Blob state types
interface BlobState {
  mood: 'happy' | 'sad' | 'excited' | 'sleeping' | 'thinking' | 'dancing';
  color: string;
  size: number;
  position: { x: number; y: number };
  message: string;
}

// Message types
interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

function App() {
  const [showSimpleUI, setShowSimpleUI] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: "Hello! I'm CelFlow AI. Meet Cel, your blob companion! Try saying 'make Cel happy' or 'make Cel dance'!", sender: 'ai', timestamp: new Date() }
  ]);
  const [inputText, setInputText] = useState('');
  const [blobState, setBlobState] = useState<BlobState>({
    mood: 'happy',
    color: '#667eea',
    size: 200,
    position: { x: 50, y: 50 },
    message: "Hi! I'm Cel!"
  });
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>();
  const timeRef = useRef<number>(0);

  // Mock system metrics
  const systemMetrics: SystemMetrics = {
    cpu_usage: 12.5,
    memory_usage: 1024.5,
    disk_usage: {
      total: 512000,
      used: 128000,
      free: 384000
    },
    events_per_second: 42.5
  };

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Animate the blob
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const animate = () => {
      timeRef.current += 0.01;
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Calculate blob center
      const centerX = (canvas.width * blobState.position.x) / 100;
      const centerY = (canvas.height * blobState.position.y) / 100;
      
      // Draw blob with animated shape
      ctx.fillStyle = blobState.color;
      ctx.beginPath();
      
      const points = 8;
      for (let i = 0; i < points; i++) {
        const angle = (i / points) * Math.PI * 2;
        let radius = blobState.size;
        
        // Add mood-based animations
        switch (blobState.mood) {
          case 'dancing':
            radius += Math.sin(timeRef.current * 5 + i) * 20;
            break;
          case 'excited':
            radius += Math.sin(timeRef.current * 10 + i) * 10;
            break;
          case 'sleeping':
            radius += Math.sin(timeRef.current * 0.5) * 5;
            break;
          case 'thinking':
            radius += Math.sin(timeRef.current * 2 + i * 0.5) * 15;
            break;
          case 'sad':
            radius -= 20;
            break;
          default:
            radius += Math.sin(timeRef.current * 2 + i) * 10;
        }
        
        const x = centerX + Math.cos(angle) * radius;
        const y = centerY + Math.sin(angle) * radius;
        
        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.quadraticCurveTo(
            centerX + Math.cos(angle - Math.PI / points) * radius * 1.5,
            centerY + Math.sin(angle - Math.PI / points) * radius * 1.5,
            x, y
          );
        }
      }
      
      ctx.closePath();
      ctx.fill();
      
      // Draw eyes
      const eyeSize = blobState.mood === 'sleeping' ? 2 : 10;
      const eyeY = centerY - 20;
      
      ctx.fillStyle = 'white';
      ctx.beginPath();
      ctx.arc(centerX - 30, eyeY, eyeSize, 0, Math.PI * 2);
      ctx.arc(centerX + 30, eyeY, eyeSize, 0, Math.PI * 2);
      ctx.fill();
      
      if (blobState.mood !== 'sleeping') {
        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.arc(centerX - 30, eyeY, 5, 0, Math.PI * 2);
        ctx.arc(centerX + 30, eyeY, 5, 0, Math.PI * 2);
        ctx.fill();
      }
      
      // Draw mouth based on mood
      ctx.strokeStyle = 'white';
      ctx.lineWidth = 3;
      ctx.beginPath();
      
      switch (blobState.mood) {
        case 'happy':
        case 'dancing':
        case 'excited':
          ctx.arc(centerX, centerY + 10, 30, 0.2 * Math.PI, 0.8 * Math.PI);
          break;
        case 'sad':
          ctx.arc(centerX, centerY + 40, 30, 1.2 * Math.PI, 1.8 * Math.PI);
          break;
        case 'thinking':
          ctx.moveTo(centerX - 20, centerY + 20);
          ctx.lineTo(centerX + 20, centerY + 20);
          break;
      }
      ctx.stroke();
      
      // Draw message
      ctx.fillStyle = blobState.color;
      ctx.font = '20px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(blobState.message, centerX, canvas.height - 50);
      
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [blobState]);

  // Process AI commands
  const processCommand = (text: string) => {
    const lowerText = text.toLowerCase();
    let response = "";
    let newBlobState = { ...blobState };
    
    if (lowerText.includes('happy')) {
      newBlobState.mood = 'happy';
      newBlobState.message = "Yay! I'm happy!";
      response = "I've made Cel happy! Look at that smile!";
    } else if (lowerText.includes('sad')) {
      newBlobState.mood = 'sad';
      newBlobState.message = "Aww, I'm sad...";
      response = "Oh no, Cel is sad now. Maybe try cheering them up?";
    } else if (lowerText.includes('dance') || lowerText.includes('dancing')) {
      newBlobState.mood = 'dancing';
      newBlobState.message = "Let's dance!";
      response = "Cel is dancing! Look at those moves!";
    } else if (lowerText.includes('sleep')) {
      newBlobState.mood = 'sleeping';
      newBlobState.message = "Zzz...";
      response = "Shh... Cel is sleeping now.";
    } else if (lowerText.includes('think')) {
      newBlobState.mood = 'thinking';
      newBlobState.message = "Hmm...";
      response = "Cel is deep in thought...";
    } else if (lowerText.includes('excited')) {
      newBlobState.mood = 'excited';
      newBlobState.message = "Woohoo!";
      response = "Cel is super excited!";
    } else if (lowerText.includes('big')) {
      newBlobState.size = Math.min(300, newBlobState.size + 50);
      newBlobState.message = "I'm growing!";
      response = "Cel is getting bigger!";
    } else if (lowerText.includes('small')) {
      newBlobState.size = Math.max(100, newBlobState.size - 50);
      newBlobState.message = "I'm shrinking!";
      response = "Cel is getting smaller!";
    } else if (lowerText.includes('red')) {
      newBlobState.color = '#ef4444';
      response = "Cel is now red!";
    } else if (lowerText.includes('blue')) {
      newBlobState.color = '#3b82f6';
      response = "Cel is now blue!";
    } else if (lowerText.includes('green')) {
      newBlobState.color = '#10b981';
      response = "Cel is now green!";
    } else if (lowerText.includes('purple')) {
      newBlobState.color = '#8b5cf6';
      response = "Cel is now purple!";
    } else if (lowerText.includes('move') && lowerText.includes('left')) {
      newBlobState.position.x = Math.max(20, newBlobState.position.x - 20);
      response = "Moving Cel to the left!";
    } else if (lowerText.includes('move') && lowerText.includes('right')) {
      newBlobState.position.x = Math.min(80, newBlobState.position.x + 20);
      response = "Moving Cel to the right!";
    } else if (lowerText.includes('move') && lowerText.includes('up')) {
      newBlobState.position.y = Math.max(20, newBlobState.position.y - 20);
      response = "Moving Cel up!";
    } else if (lowerText.includes('move') && lowerText.includes('down')) {
      newBlobState.position.y = Math.min(80, newBlobState.position.y + 20);
      response = "Moving Cel down!";
    } else {
      response = "I can control Cel! Try commands like: 'make Cel happy', 'make Cel dance', 'make Cel big', 'turn Cel red', 'move Cel left', etc.";
    }
    
    setBlobState(newBlobState);
    return response;
  };

  const handleSendMessage = () => {
    if (!inputText.trim()) return;
    
    // Add user message
    const userMessage: Message = {
      id: messages.length + 1,
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };
    
    // Process command and get AI response
    const aiResponse = processCommand(inputText);
    
    const aiMessage: Message = {
      id: messages.length + 2,
      text: aiResponse,
      sender: 'ai',
      timestamp: new Date()
    };
    
    setMessages([...messages, userMessage, aiMessage]);
    setInputText('');
  };

  // Simple test component
  const SimpleTestComponent = () => (
    <div style={{ 
      width: '100vw', 
      height: '100vh', 
      backgroundColor: 'blue', 
      color: 'white',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      fontSize: '24px',
      padding: '20px',
      boxSizing: 'border-box'
    }}>
      <h1 style={{ marginBottom: '20px' }}>CelFlow Basic Test</h1>
      <p>If you can see this blue screen with text, React is working!</p>
      <div style={{ 
        backgroundColor: 'white', 
        color: 'blue', 
        padding: '20px', 
        borderRadius: '10px',
        marginTop: '20px',
        maxWidth: '80%',
        textAlign: 'center'
      }}>
        This is a simplified test to check rendering
      </div>
      <button 
        onClick={() => setShowSimpleUI(false)}
        style={{
          marginTop: '20px',
          padding: '10px 20px',
          backgroundColor: 'white',
          color: 'blue',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
      >
        Show Main UI
      </button>
    </div>
  );

  // Basic system overview component
  const BasicSystemOverview = ({ metrics }: { metrics: SystemMetrics }) => (
    <div className="glass-panel rounded-lg p-6 shadow-lg">
      <h2 className="text-2xl font-bold mb-4 text-neural-800">System Overview</h2>
      <div className="space-y-4">
        <div className="flex justify-between">
          <span className="text-neural-600">CPU Usage:</span>
          <span className="font-mono">{metrics.cpu_usage.toFixed(1)}%</span>
        </div>
        <div className="flex justify-between">
          <span className="text-neural-600">Memory Usage:</span>
          <span className="font-mono">{metrics.memory_usage.toFixed(1)} MB</span>
        </div>
        <div className="flex justify-between">
          <span className="text-neural-600">Disk Free:</span>
          <span className="font-mono">{(metrics.disk_usage.free / 1024).toFixed(1)} GB</span>
        </div>
        <div className="flex justify-between">
          <span className="text-neural-600">Events/Second:</span>
          <span className="font-mono">{metrics.events_per_second.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );

  // If showing simple UI
  if (showSimpleUI) {
    return <SimpleTestComponent />;
  }

  // Main UI
  return (
    <div className="h-screen flex bg-gradient-to-br from-gray-900 to-gray-800">
      {/* Left 2/3: Blob creature */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="relative w-full h-full max-w-4xl max-h-4xl">
          <canvas 
            ref={canvasRef}
            width={800}
            height={800}
            className="w-full h-full"
          />
        </div>
      </div>
      
      {/* Right 1/3: Chat interface */}
      <div className="w-96 bg-gray-800 border-l border-gray-700 flex flex-col">
        <div className="p-4 border-b border-gray-700">
          <h2 className="text-xl font-bold text-white">CelFlow AI Chat</h2>
          <p className="text-sm text-gray-400">Chat with me to control Cel!</p>
        </div>
        
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-white'
                }`}
              >
                <p className="text-sm">{message.text}</p>
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input */}
        <div className="p-4 border-t border-gray-700">
          <div className="flex space-x-2">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type a command..."
              className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleSendMessage}
              className="bg-blue-600 text-white rounded-lg px-4 py-2 hover:bg-blue-700 transition-colors"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 