import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Server Metrics heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/Server Metrics/i);
  expect(headingElement).toBeInTheDocument();
});
