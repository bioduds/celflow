import React, { useState, useEffect, useRef } from "react";
import "./index.css";

// Types
interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  visualization?: VisualizationData;
}

interface VisualizationData {
  type: 'chart' | 'plot' | 'table' | 'graph' | 'text' | 'code';
  title?: string;
  data?: any;
  config?: any;
  content?: string;
}

interface ChatResponse {
  success: boolean;
  message: string;
  response_time: number;
  interaction_id: number;
  agent_info: {
    agent: string;
    context_used: boolean;
  };
  visualization?: VisualizationData;
  error?: string;
}

interface SystemStatus {
  status: string;
  uptime: number;
  model_name: string;
  agents_active: number;
  interaction_count: number;
  health_status: any;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [aiStatus, setAiStatus] = useState<SystemStatus | null>(null);
  const [currentVisualization, setCurrentVisualization] = useState<VisualizationData | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const visualizationRef = useRef<HTMLDivElement>(null);

  // API base URL
  const API_BASE = 'http://127.0.0.1:8000';

  // Check AI system health on startup
  useEffect(() => {
    checkAiHealth();
    const healthInterval = setInterval(checkAiHealth, 30000); // Check every 30 seconds
    return () => clearInterval(healthInterval);
  }, []);

  const checkAiHealth = async () => {
    try {
      const response = await fetch(`${API_BASE}/health`);
      if (response.ok) {
        const status: SystemStatus = await response.json();
        setAiStatus(status);
      } else {
        console.error('AI health check failed:', response.status);
        setAiStatus(null);
      }
    } catch (error) {
      console.error('AI health check error:', error);
      setAiStatus(null);
    }
  };

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    
    try {
      // Send message to AI with visualization context
      const chatResponse = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputText,
          context_type: 'visualization_chat',
          request_visualization: true
        })
      });
      
      if (chatResponse.ok) {
        const chatResult: ChatResponse = await chatResponse.json();
        
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: chatResult.success ? chatResult.message : 'Sorry, I encountered an error processing your message.',
          sender: 'ai',
          timestamp: new Date(),
          visualization: chatResult.visualization
        };
        
        setMessages(prev => [...prev, aiMessage]);
        
        // Update main visualization if provided
        if (chatResult.visualization) {
          setCurrentVisualization(chatResult.visualization);
        }
      } else {
        throw new Error('Chat API call failed');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: aiStatus ? 
          'Sorry, I encountered an error. Please try again.' : 
          'AI system is not available. Please make sure the CelFlow AI server is running.',
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const renderVisualization = (viz: VisualizationData) => {
    switch (viz.type) {
      case 'chart':
        return (
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-600">
            <h3 className="text-lg font-semibold text-blue-400 mb-4">{viz.title || 'Chart'}</h3>
            <div className="text-center text-gray-400 py-8">
              📊 Chart visualization would render here
              <br />
              <small className="text-xs">Data: {JSON.stringify(viz.data).substring(0, 100)}...</small>
            </div>
          </div>
        );
      case 'plot':
        return (
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-600">
            <h3 className="text-lg font-semibold text-green-400 mb-4">{viz.title || 'Plot'}</h3>
            <div className="text-center text-gray-400 py-8">
              📈 Plot visualization would render here
              <br />
              <small className="text-xs">Config: {JSON.stringify(viz.config).substring(0, 100)}...</small>
            </div>
          </div>
        );
      case 'table':
        return (
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-600">
            <h3 className="text-lg font-semibold text-purple-400 mb-4">{viz.title || 'Data Table'}</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-gray-300">
                <thead>
                  <tr className="border-b border-gray-600">
                    <th className="text-left p-2">Column 1</th>
                    <th className="text-left p-2">Column 2</th>
                    <th className="text-left p-2">Column 3</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-700">
                    <td className="p-2">Sample data</td>
                    <td className="p-2">would render</td>
                    <td className="p-2">here</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        );
      case 'code':
        return (
          <div className="bg-gray-900 rounded-lg p-6 border border-gray-600">
            <h3 className="text-lg font-semibold text-yellow-400 mb-4">{viz.title || 'Code Output'}</h3>
            <pre className="bg-black rounded p-4 text-green-400 text-sm overflow-x-auto">
              <code>{viz.content || 'Code output would appear here'}</code>
            </pre>
          </div>
        );
      case 'text':
        return (
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-600">
            <h3 className="text-lg font-semibold text-cyan-400 mb-4">{viz.title || 'Analysis Result'}</h3>
            <div className="text-gray-300 whitespace-pre-wrap">
              {viz.content || 'Text analysis would appear here'}
            </div>
          </div>
        );
      default:
        return (
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-600">
            <h3 className="text-lg font-semibold text-gray-400 mb-4">Visualization</h3>
            <div className="text-center text-gray-500 py-8">
              🔮 AI-generated visualization will appear here
            </div>
          </div>
        );
    }
  };

  // Main UI
  return (
    <div className="h-screen bg-gray-900 text-white flex">
      {/* Left side - Chat interface (1/3) */}
      <div className="w-96 bg-gray-800 border-r border-gray-700 flex flex-col">
        {/* Chat header */}
        <div className="p-4 border-b border-gray-700">
          <h2 className="text-xl font-bold text-blue-400">CelFlow AI Chat</h2>
          <p className="text-sm text-gray-400">
            Ask Gemma 3:4b to analyze data and create visualizations
          </p>
          
          {/* AI System status */}
          <div className="mt-3 bg-black/30 rounded-lg p-2">
            <div className="text-xs">
              <div className="text-blue-400 font-semibold">AI Status</div>
              {aiStatus ? (
                <>
                  <div>Model: <span className="text-cyan-400">{aiStatus.model_name}</span></div>
                  <div>Status: <span className="text-green-400">{aiStatus.status}</span></div>
                  <div>Agents: <span className="text-purple-400">{aiStatus.agents_active}</span></div>
                </>
              ) : (
                <div className="text-red-400">Offline</div>
              )}
            </div>
          </div>
        </div>
        
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-8">
              <p>🧠 Welcome to CelFlow AI!</p>
              <p className="text-sm mt-2">Ask me to:</p>
              <div className="text-xs mt-2 space-y-1 text-left">
                <p>• "Plot a sine wave"</p>
                <p>• "Create a bar chart of sales data"</p>
                <p>• "Analyze this dataset"</p>
                <p>• "Show me a scatter plot"</p>
                <p>• "Generate random data visualization"</p>
              </div>
            </div>
          )}
          
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs px-4 py-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-gray-100'
                }`}
              >
                <p className="text-sm">{message.text}</p>
                {message.visualization && (
                  <div className="mt-2 text-xs text-blue-300">
                    📊 Visualization: {message.visualization.type}
                  </div>
                )}
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-700 text-gray-100 max-w-xs px-4 py-2 rounded-lg">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-400"></div>
                  <p className="text-sm">Gemma 3:4b is analyzing...</p>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input area */}
        <div className="p-4 border-t border-gray-700">
          <div className="flex space-x-2">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask for data analysis or visualization..."
              className="flex-1 bg-gray-700 text-white px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputText.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-4 py-2 rounded-lg transition-colors text-sm"
            >
              Send
            </button>
          </div>
        </div>
      </div>
      
      {/* Right side - Dynamic Visualization Stage (2/3) */}
      <div className="flex-1 bg-gradient-to-br from-gray-800 to-gray-900 flex flex-col">
        {/* Stage header */}
        <div className="p-4 border-b border-gray-700">
          <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600">
            CelFlow AI Visualization Stage
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Powered by Gemma 3:4b • Dynamic data analysis and visualization
          </p>
        </div>
        
        {/* Main visualization area */}
        <div className="flex-1 p-6 overflow-auto" ref={visualizationRef}>
          {currentVisualization ? (
            renderVisualization(currentVisualization)
          ) : (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl mb-4">🧠</div>
                <h2 className="text-2xl font-bold text-gray-400 mb-2">Ready for AI Analysis</h2>
                <p className="text-gray-500 mb-6">Ask Gemma 3:4b to create visualizations, analyze data, or generate insights</p>
                
                <div className="grid grid-cols-2 gap-4 max-w-md mx-auto text-left">
                  <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600">
                    <div className="text-blue-400 font-semibold mb-2">📊 Charts & Graphs</div>
                    <p className="text-xs text-gray-400">Bar charts, line plots, scatter plots, histograms</p>
                  </div>
                  <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600">
                    <div className="text-green-400 font-semibold mb-2">📈 Data Analysis</div>
                    <p className="text-xs text-gray-400">Statistical analysis, trends, correlations</p>
                  </div>
                  <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600">
                    <div className="text-purple-400 font-semibold mb-2">📋 Tables</div>
                    <p className="text-xs text-gray-400">Data tables, summaries, reports</p>
                  </div>
                  <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600">
                    <div className="text-yellow-400 font-semibold mb-2">💻 Code Output</div>
                    <p className="text-xs text-gray-400">Generated code, calculations, algorithms</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Stage footer with quick actions */}
        <div className="p-4 border-t border-gray-700 bg-gray-800/50">
          <div className="flex space-x-2 text-xs">
            <button 
              onClick={() => setInputText("Generate a sample chart")}
              className="bg-blue-600/20 hover:bg-blue-600/40 text-blue-400 px-3 py-1 rounded transition-colors"
            >
              📊 Sample Chart
            </button>
            <button 
              onClick={() => setInputText("Create random data analysis")}
              className="bg-green-600/20 hover:bg-green-600/40 text-green-400 px-3 py-1 rounded transition-colors"
            >
              📈 Random Analysis
            </button>
            <button 
              onClick={() => setInputText("Show me a data table")}
              className="bg-purple-600/20 hover:bg-purple-600/40 text-purple-400 px-3 py-1 rounded transition-colors"
            >
              📋 Data Table
            </button>
            <button 
              onClick={() => setCurrentVisualization(null)}
              className="bg-gray-600/20 hover:bg-gray-600/40 text-gray-400 px-3 py-1 rounded transition-colors ml-auto"
            >
              🗑️ Clear Stage
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 