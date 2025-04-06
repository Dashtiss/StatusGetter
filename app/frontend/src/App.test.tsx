import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('renders Server Metrics heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/Server Metrics/i);
  expect(headingElement).toBeInTheDocument();
});

test('renders a button and handles click event', () => {
  render(<App />);
  const buttonElement = screen.getByRole('button', { name: /Fetch Data/i });
  expect(buttonElement).toBeInTheDocument();
  fireEvent.click(buttonElement);
  const loadingElement = screen.getByText(/Loading.../i);
  expect(loadingElement).toBeInTheDocument();
});

test('displays error message on API failure', async () => {
  render(<App />);
  const errorElement = await screen.findByText(/Failed to fetch data/i);
  expect(errorElement).toBeInTheDocument();
});
