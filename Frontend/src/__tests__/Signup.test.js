import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Signup from '../pages/Signup';
import * as api from '../services/api';

// Mock the API
jest.mock('../services/api');

const MockedSignup = () => (
  <BrowserRouter>
    <Signup />
  </BrowserRouter>
);

describe('Signup Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders signup form', () => {
    render(<MockedSignup />);
    
    expect(screen.getByText('Create an Account')).toBeInTheDocument();
    expect(screen.getByLabelText('Username')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByLabelText('Confirm Password')).toBeInTheDocument();
  });

  test('shows error when passwords do not match', () => {
    render(<MockedSignup />);
    
    fireEvent.change(screen.getByLabelText('Username'), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' }
    });
    fireEvent.change(screen.getByLabelText('Confirm Password'), {
      target: { value: 'password456' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

    expect(screen.getByText(/Passwords do not match/i)).toBeInTheDocument();
  });

  test('shows error for short password', () => {
    render(<MockedSignup />);
    
    fireEvent.change(screen.getByLabelText('Username'), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: '12345' }
    });
    fireEvent.change(screen.getByLabelText('Confirm Password'), {
      target: { value: '12345' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

    expect(screen.getByText(/Password must be at least 6 characters/i)).toBeInTheDocument();
  });

  test('has link to login page', () => {
    render(<MockedSignup />);
    
    const loginLink = screen.getByText(/Login here/i);
    expect(loginLink).toBeInTheDocument();
    expect(loginLink.closest('a')).toHaveAttribute('href', '/login');
  });
});
