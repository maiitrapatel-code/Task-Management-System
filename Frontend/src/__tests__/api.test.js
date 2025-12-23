// Mock axios before importing api
jest.mock('axios', () => {
  const mockApi = {
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn()
  };
  
  return {
    __esModule: true,
    default: {
      create: jest.fn(() => ({
        ...mockApi,
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() }
        }
      }))
    }
  };
});

import { authAPI, tasksAPI } from '../services/api';

describe('API Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('authAPI', () => {
    test('signup is defined and callable', () => {
      expect(typeof authAPI.signup).toBe('function');
    });

    test('login is defined and callable', () => {
      expect(typeof authAPI.login).toBe('function');
    });

    test('logout is defined and callable', () => {
      expect(typeof authAPI.logout).toBe('function');
    });
  });

  describe('tasksAPI', () => {
    test('getAll is defined and callable', () => {
      expect(typeof tasksAPI.getAll).toBe('function');
    });

    test('create is defined and callable', () => {
      expect(typeof tasksAPI.create).toBe('function');
    });

    test('update is defined and callable', () => {
      expect(typeof tasksAPI.update).toBe('function');
    });

    test('delete is defined and callable', () => {
      expect(typeof tasksAPI.delete).toBe('function');
    });
  });
});
