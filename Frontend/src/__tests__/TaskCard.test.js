import React from 'react';
import { render, screen } from '@testing-library/react';
import TaskCard from '../components/TaskCard';

describe('TaskCard Component', () => {
  const mockTask = {
    id: 1,
    title: 'Test Task',
    description: 'This is a test task',
    priority: 3,
    complete: false
  };

  const mockHandlers = {
    onEdit: jest.fn(),
    onDelete: jest.fn(),
    onToggleComplete: jest.fn()
  };

  test('renders task information', () => {
    render(<TaskCard task={mockTask} {...mockHandlers} />);
    
    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('This is a test task')).toBeInTheDocument();
    expect(screen.getByText('Medium')).toBeInTheDocument();
  });

  test('shows correct priority label', () => {
    const priorities = [
      { value: 1, label: 'Very Low' },
      { value: 2, label: 'Low' },
      { value: 3, label: 'Medium' },
      { value: 4, label: 'High' },
      { value: 5, label: 'Critical' }
    ];

    priorities.forEach(({ value, label }) => {
      const { rerender } = render(
        <TaskCard task={{ ...mockTask, priority: value }} {...mockHandlers} />
      );
      expect(screen.getByText(label)).toBeInTheDocument();
      rerender(<></>);
    });
  });

  test('renders action buttons', () => {
    render(<TaskCard task={mockTask} {...mockHandlers} />);
    
    expect(screen.getByText('Mark Complete')).toBeInTheDocument();
    expect(screen.getByText('Edit')).toBeInTheDocument();
    expect(screen.getByText('Delete')).toBeInTheDocument();
  });

  test('shows "Mark Incomplete" button for completed tasks', () => {
    const completedTask = { ...mockTask, complete: true };
    render(<TaskCard task={completedTask} {...mockHandlers} />);
    
    expect(screen.getByText('Mark Incomplete')).toBeInTheDocument();
  });

  test('applies completed class to completed tasks', () => {
    const completedTask = { ...mockTask, complete: true };
    const { container } = render(<TaskCard task={completedTask} {...mockHandlers} />);
    
    const taskCard = container.querySelector('.task-card');
    expect(taskCard).toHaveClass('completed');
  });
});
