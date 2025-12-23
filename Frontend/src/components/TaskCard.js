import React from 'react';

const TaskCard = ({ task, onEdit, onDelete, onToggleComplete }) => {
  const getPriorityLabel = (priority) => {
    const labels = {
      1: 'Very Low',
      2: 'Low',
      3: 'Medium',
      4: 'High',
      5: 'Critical',
    };
    return labels[priority] || 'Unknown';
  };

  return (
    <div className={`task-card ${task.complete ? 'completed' : ''}`}>
      <div className="task-header">
        <h3>{task.title}</h3>
        <span className={`priority-badge priority-${task.priority}`}>
          {getPriorityLabel(task.priority)}
        </span>
      </div>
      
      <p className="task-description">{task.description}</p>
      
      <div className="task-actions">
        <button
          className={task.complete ? 'incomplete-btn' : 'complete-btn'}
          onClick={() => onToggleComplete(task)}
        >
          {task.complete ? 'Mark Incomplete' : 'Mark Complete'}
        </button>
        <button className="edit-btn" onClick={() => onEdit(task)}>
          Edit
        </button>
        <button className="delete-btn" onClick={() => onDelete(task.id)}>
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskCard;
