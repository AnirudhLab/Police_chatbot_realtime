import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

test('renders Police Chatbot title', () => {
  render(<App />);
  const title = screen.getByText(/Police Chatbot/i);
  expect(title).toBeInTheDocument();
});
