import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders time tracker app', () => {
  render(<App />);
  const titleElement = screen.getByText(/Time Tracker/i);
  expect(titleElement).toBeInTheDocument();
});