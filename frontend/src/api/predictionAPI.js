import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictionAPI = {
  predictAirQuality: async (data) => {
    try {
      const response = await api.post('/predict', data);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  getHealthStatus: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  getModelInfo: async () => {
    try {
      const response = await api.get('/model-info');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};
