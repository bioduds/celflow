import React, { useEffect, useRef, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  RadialLinearScale,
  Filler
} from 'chart.js';
import { Line, Bar, Pie, Doughnut, Radar, Scatter } from 'react-chartjs-2';
import Plot from 'react-plotly.js';
import * as d3 from 'd3';
import ForceGraph2D from 'react-force-graph-2d';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  RadialLinearScale,
  Filler
);

interface VisualizationData {
  type: 'line' | 'bar' | 'pie' | 'doughnut' | 'radar' | 'scatter' | 'heatmap' | 'network' | 'd3_custom' | 'plotly' | 'system_dashboard' | 'chart' | 'plot' | 'table' | 'graph' | 'text' | 'code' | 'image';
  title?: string;
  data?: any;
  config?: any;
  content?: string;
  realTimeData?: boolean;
  updateInterval?: number;
}

interface VisualizationEngineProps {
  visualization: VisualizationData;
  className?: string;
  onDataUpdate?: (data: any) => void;
}

export const VisualizationEngine: React.FC<VisualizationEngineProps> = ({
  visualization,
  className = '',
  onDataUpdate
}) => {
  const [currentData, setCurrentData] = useState(visualization.data);
  const [isLoading, setIsLoading] = useState(false);
  const d3ContainerRef = useRef<HTMLDivElement>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Handle real-time data updates
  useEffect(() => {
    if (visualization.realTimeData && visualization.updateInterval) {
      intervalRef.current = setInterval(async () => {
        setIsLoading(true);
        try {
          // Fetch updated data from API
          const response = await fetch('http://127.0.0.1:8000/system-stats');
          if (response.ok) {
            const newData = await response.json();
            setCurrentData(newData);
            onDataUpdate?.(newData);
          }
        } catch (error) {
          console.error('Error updating real-time data:', error);
        } finally {
          setIsLoading(false);
        }
      }, visualization.updateInterval);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [visualization.realTimeData, visualization.updateInterval, onDataUpdate]);

  // D3.js custom visualization
  useEffect(() => {
    if (visualization.type === 'd3_custom' && d3ContainerRef.current && currentData) {
      renderD3Visualization();
    }
  }, [visualization.type, currentData]);

  const renderD3Visualization = () => {
    if (!d3ContainerRef.current || !currentData) return;

    const container = d3.select(d3ContainerRef.current);
    container.selectAll('*').remove(); // Clear previous render

    const width = 800;
    const height = 400;
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };

    const svg = container
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    // Example: Simple bar chart with D3
    if (currentData.type === 'bar') {
      const data = currentData.values || [];
      
      const xScale = d3.scaleBand()
        .domain(data.map((d: any) => d.label))
        .range([margin.left, width - margin.right])
        .padding(0.1);

      const yScale = d3.scaleLinear()
        .domain([0, d3.max(data, (d: any) => Number(d.value)) || 0])
        .range([height - margin.bottom, margin.top]);

      // Create bars
      svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', (d: any) => xScale(d.label) || 0)
        .attr('y', (d: any) => yScale(d.value))
        .attr('width', xScale.bandwidth())
        .attr('height', (d: any) => height - margin.bottom - yScale(d.value))
        .attr('fill', '#3b82f6')
        .attr('rx', 4);

      // Add axes
      svg.append('g')
        .attr('transform', `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(xScale));

      svg.append('g')
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(yScale));
    }
  };

  const getChartOptions = () => ({
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: !!visualization.title,
        text: visualization.title,
      },
    },
    scales: visualization.type !== 'pie' && visualization.type !== 'doughnut' ? {
      y: {
        beginAtZero: true,
      },
    } : undefined,
  });

  const renderVisualization = () => {
    if (!currentData) {
      return (
        <div className="flex items-center justify-center h-64 text-gray-500">
          No data available
        </div>
      );
    }

    switch (visualization.type) {
      case 'line':
        return (
          <div className="h-96">
            <Line data={currentData} options={getChartOptions()} />
          </div>
        );

      case 'bar':
        return (
          <div className="h-96">
            <Bar data={currentData} options={getChartOptions()} />
          </div>
        );

      case 'pie':
        return (
          <div className="h-96">
            <Pie data={currentData} options={getChartOptions()} />
          </div>
        );

      case 'doughnut':
        return (
          <div className="h-96">
            <Doughnut data={currentData} options={getChartOptions()} />
          </div>
        );

      case 'radar':
        return (
          <div className="h-96">
            <Radar data={currentData} options={getChartOptions()} />
          </div>
        );

      case 'scatter':
        return (
          <div className="h-96">
            <Scatter data={currentData} options={getChartOptions()} />
          </div>
        );

      case 'heatmap':
      case 'plotly':
        return (
          <div className="h-96">
            <Plot
              data={currentData.data || []}
              layout={{
                title: visualization.title,
                autosize: true,
                ...currentData.layout
              }}
              config={{
                responsive: true,
                displayModeBar: true,
                ...visualization.config
              }}
              style={{ width: '100%', height: '100%' }}
            />
          </div>
        );

      case 'network':
        return (
          <div className="h-96 border rounded-lg">
            <ForceGraph2D
              graphData={currentData}
              nodeAutoColorBy="group"
              nodeCanvasObject={(node: any, ctx: any, globalScale: number) => {
                const label = String(node.id || '');
                const fontSize = 12/globalScale;
                ctx.font = `${fontSize}px Sans-Serif`;
                const textWidth = ctx.measureText(label).width;
                const bckgDimensions = [textWidth, fontSize].map((n: number) => n + fontSize * 0.2);

                ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
                const nodeX = node.x || 0;
                const nodeY = node.y || 0;
                ctx.fillRect(nodeX - bckgDimensions[0] / 2, nodeY - bckgDimensions[1] / 2, bckgDimensions[0], bckgDimensions[1]);

                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = node.color || '#000000';
                ctx.fillText(label, nodeX, nodeY);
              }}
              linkDirectionalParticles={2}
              width={800}
              height={400}
            />
          </div>
        );

      case 'd3_custom':
        return (
          <div className="h-96 border rounded-lg">
            <div ref={d3ContainerRef} className="w-full h-full" />
          </div>
        );

      case 'system_dashboard':
        return (
          <div className="grid grid-cols-2 gap-4 h-96">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-blue-800">CPU Usage</h3>
              <div className="text-2xl font-bold text-blue-600">
                {currentData.cpu_usage || 'N/A'}%
              </div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="font-semibold text-green-800">Memory</h3>
              <div className="text-2xl font-bold text-green-600">
                {currentData.memory_usage || 'N/A'}%
              </div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <h3 className="font-semibold text-purple-800">Active Agents</h3>
              <div className="text-2xl font-bold text-purple-600">
                {currentData.agents_active || 0}
              </div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <h3 className="font-semibold text-orange-800">Interactions</h3>
              <div className="text-2xl font-bold text-orange-600">
                {currentData.interaction_count || 0}
              </div>
            </div>
          </div>
        );

      case 'image':
        // Handle base64 encoded images or direct image URLs
        const imageSrc = visualization.content || currentData;
        console.log('Image visualization:', { type: visualization.type, hasContent: !!visualization.content, hasData: !!currentData });
        console.log('Image src preview:', imageSrc?.substring(0, 100) + '...');
        
        // Check if it's a data URL
        if (imageSrc && imageSrc.startsWith('data:image')) {
          return (
            <div className="flex items-center justify-center">
              <img 
                src={imageSrc} 
                alt={visualization.title || 'Generated visualization'}
                className="max-w-full h-auto rounded-lg shadow-md"
                style={{ maxHeight: '600px' }}
                onError={(e) => {
                  console.error('Image failed to load:', e);
                  // Fallback to showing error message
                  const target = e.target as HTMLImageElement;
                  target.style.display = 'none';
                  target.parentElement!.innerHTML = '<div class="text-red-400">Failed to load image</div>';
                }}
              />
            </div>
          );
        } else {
          // If it's not a proper data URL, show it as text for debugging
          return (
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-600">
              <h3 className="text-lg font-semibold text-red-400 mb-4">Image Data Error</h3>
              <div className="text-gray-300 text-xs overflow-auto">
                <pre>{imageSrc?.substring(0, 500)}...</pre>
              </div>
            </div>
          );
        }

      default:
        return (
          <div className="flex items-center justify-center h-64 text-gray-500">
            <div className="text-center">
              <p>Unsupported visualization type: {visualization.type}</p>
              <pre className="mt-2 text-xs bg-gray-100 p-2 rounded">
                {JSON.stringify(currentData, null, 2)}
              </pre>
            </div>
          </div>
        );
    }
  };

  return (
    <div className={`bg-white rounded-lg shadow-lg p-6 ${className}`}>
      {visualization.title && (
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-800">
            {visualization.title}
          </h2>
          {isLoading && (
            <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-blue-500"></div>
          )}
        </div>
      )}
      
      <div className="relative">
        {renderVisualization()}
      </div>
      
      {visualization.content && visualization.type !== 'image' && (
        <div className="mt-4 p-3 bg-gray-50 rounded text-sm">
          <pre className="whitespace-pre-wrap">{visualization.content}</pre>
        </div>
      )}
    </div>
  );
};

export default VisualizationEngine; 