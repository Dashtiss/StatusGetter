import React, { useState, useEffect } from 'react';
import LineChart from './components/LineChart';
import './App.css';

const App: React.FC = () => {
  const [selectedMetrics, setSelectedMetrics] = useState<string[]>(['TPS', 'Chunks', 'Players']);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const toggleMetric = (metric: string) => {
    setSelectedMetrics((prev) =>
      prev.includes(metric)
        ? prev.filter((m) => m !== metric)
        : [...prev, metric]
    );
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/data');
        if (!response.ok) {
          throw new Error('Failed to fetch data from API');
        }
        const result = await response.json();

        // Transform the data to match the expected format for the chart
        const transformedData: Record<string, any[]> = {};
        result.data.forEach((server: any) => {
          server.metrics.forEach((metric: any) => {
            if (!transformedData[metric.metric_name]) {
              transformedData[metric.metric_name] = [];
            }
            transformedData[metric.metric_name].push({
              timestamp: metric.timestamp,
              value: metric.value,
            });
          });
        });

        setData(transformedData);
      } catch (err) {
        setError('Cannot connect to API');
        // Adding placeholder data for demonstration purposes
        setData({
          TPS: [
            { timestamp: '2023-10-01T12:00:00Z', value: 10 },
            { timestamp: '2023-10-01T12:30:00Z', value: 20 },
          ],
          Chunks: [
            { timestamp: '2023-10-01T12:00:00Z', value: 100 },
            { timestamp: '2023-10-01T12:30:00Z', value: 200 },
          ],
          Players: [
            { timestamp: '2023-10-01T12:00:00Z', value: 5 },
            { timestamp: '2023-10-01T12:30:00Z', value: 10 },
          ],
        });
      }
    };

    fetchData();

    const interval = setInterval(fetchData, 30000); // Fetch data every 30 seconds
    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, []);

  return (
    <div className="App">
      <h1>Server Metrics</h1>
      {error && <p className="error">{error}</p>}
      <div className="metrics-toggle">
        {['TPS', 'Chunks', 'Players', 'CPU_Usage', 'Memory_Usage'].map((metric) => (
          <button
            key={metric}
            onClick={() => toggleMetric(metric)}
            className={selectedMetrics.includes(metric) ? 'active' : ''}
          >
            {metric}
          </button>
        ))}
      </div>
      {data && (
        <LineChart data={data} selectedMetrics={selectedMetrics} />
      )}
    </div>
  );
};

export default App;
