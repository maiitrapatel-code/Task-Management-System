import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authAPI, tasksAPI } from '../services/api';
import TaskCard from '../components/TaskCard';
import TaskModal from '../components/TaskModal';

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const { username, logout } = useAuth();
  const navigate = useNavigate();

  // Fetch tasks on component mount
  useEffect(() => {
    console.log('Dashboard mounted, fetching tasks...');
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await tasksAPI.getAll();
      console.log('Tasks fetched:', data);
      setTasks(data);
      setError('');
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    console.log('Logging out user:', username);
    try {
      await authAPI.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      logout();
      navigate('/login');
    }
  };

  const handleAddTask = () => {
    console.log('Opening modal to add new task');
    setEditingTask(null);
    setShowModal(true);
  };

  const handleEditTask = (task) => {
    console.log('Editing task:', task);
    setEditingTask(task);
    setShowModal(true);
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      console.log('Deleting task with id:', taskId);
      try {
        await tasksAPI.delete(taskId);
        setTasks(tasks.filter((t) => t.id !== taskId));
        console.log('Task deleted successfully');
      } catch (err) {
        setError('Failed to delete task');
        console.error('Delete error:', err);
      }
    }
  };

  const handleToggleComplete = async (task) => {
    console.log('Toggling complete status for task:', task.id);
    try {
      await tasksAPI.update(task.id, {
        title: task.title,
        description: task.description,
        priority: task.priority,
        complete: !task.complete,
      });
      setTasks(
        tasks.map((t) =>
          t.id === task.id ? { ...t, complete: !t.complete } : t
        )
      );
      console.log('Task status updated');
    } catch (err) {
      setError('Failed to update task');
      console.error(err);
    }
  };

  const handleSaveTask = async (taskData) => {
    console.log('Saving task:', taskData);
    try {
      if (editingTask) {
        // Update existing task
        console.log('Updating existing task');
        await tasksAPI.update(editingTask.id, taskData);
        setTasks(
          tasks.map((t) =>
            t.id === editingTask.id ? { ...t, ...taskData } : t
          )
        );
      } else {
        // Create new task
        console.log('Creating new task');
        await tasksAPI.create(taskData);
        fetchTasks(); // Refresh tasks to get the new task with ID
      }
      setShowModal(false);
      setEditingTask(null);
    } catch (err) {
      console.error('Save task error:', err);
      throw err; // Let the modal handle the error
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingTask(null);
  };

  // Sort tasks: incomplete first, then by priority (high to low)
  const sortedTasks = [...tasks].sort((a, b) => {
    if (a.complete !== b.complete) {
      return a.complete ? 1 : -1;
    }
    return b.priority - a.priority;
  });

  console.log('Rendering dashboard with', tasks.length, 'tasks');

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <h1>📋 Task Manager</h1>
        <div className="navbar-right">
          <span>Welcome, {username}!</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-header">
          <h2>My Tasks ({tasks.length})</h2>
          <button className="add-task-btn" onClick={handleAddTask}>
            + Add New Task
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loading">Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div className="empty-state">
            <h3>No tasks yet!</h3>
            <p>Click "Add New Task" to create your first task.</p>
          </div>
        ) : (
          <div className="tasks-grid">
            {sortedTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={handleEditTask}
                onDelete={handleDeleteTask}
                onToggleComplete={handleToggleComplete}
              />
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <TaskModal
          task={editingTask}
          onSave={handleSaveTask}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
};

export default Dashboard;