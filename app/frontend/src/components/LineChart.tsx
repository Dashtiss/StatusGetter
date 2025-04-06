import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

type LineChartProps = {
  selectedMetrics: string[];
  data: any;
};

const LineChart: React.FC<LineChartProps> = ({ selectedMetrics, data }) => {
  if (!data) {
    return <div>Loading...</div>;
  }

  const chartData = {
    labels: Array.isArray(Object.values(data)[0])
      ? (Object.values(data)[0] as any[]).map((entry: any) => entry.timestamp)
      : [],
    datasets: selectedMetrics.map((metric, index) => {
      const metricData = Array.isArray(data[metric]) ? data[metric] : [];
      return {
        label: metric,
        data: metricData.map((entry: any) => entry.value),
        borderColor: `hsl(${index * 120}, 70%, 50%)`,
        backgroundColor: `hsl(${index * 120}, 70%, 70%)`,
        yAxisID: metric === 'Chunks' ? 'y1' : 'y',
      };
    }),
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Server Metrics Over Time',
      },
    },
    scales: {
      y: {
        type: 'linear' as const,
        display: true,
        position: 'left' as const,
        ticks: {
          callback: function (value: number | string) {
            return value.toLocaleString(); // Format large numbers
          },
          stepSize: 0.5, // Ensure the smallest distance between Y values is 0.5
        },
      },
      y1: {
        type: 'linear' as const,
        display: true,
        position: 'right' as const,
        grid: {
          drawOnChartArea: false, // Prevent grid lines from overlapping
        },
        ticks: {
          callback: function (value: number | string) {
            return value.toLocaleString(); // Format large numbers
          },
          stepSize: 0.5, // Ensure the smallest distance between Y1 values is 0.5
        },
      },
    },
  };

  return (
    <div style={{ width: '100%', height: '70vh' }}>
      <Line options={options} data={chartData} />
    </div>
  );
};

export default LineChart;