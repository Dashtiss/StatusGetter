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
    labels: data.timestamps || [],
    datasets: selectedMetrics.map((metric, index) => {
      const metricKey = Object.keys(data).find(
        (key) => key.toLowerCase() === metric.toLowerCase()
      );
      return {
        label: metric,
        data: metricKey ? data[metricKey] : [],
        borderColor: `hsl(${index * 120}, 70%, 50%)`,
        backgroundColor: `hsl(${index * 120}, 70%, 70%)`,
      };
    }),
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Server Metrics Over Time',
      },
    },
  };

  return <Line options={options} data={chartData} />;
};

export default LineChart;