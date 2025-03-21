import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';

const apiService = {
  getToken() {
    return localStorage.getItem('token');
  },

  getAuthHeaders() {
    return {
      headers: { Authorization: `Bearer ${this.getToken()}` }
    };
  },

  async fetchItems() {
    try {
      const response = await axios.get(`${API_URL}items/`, this.getAuthHeaders());
      return response.data;
    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
      throw error;
    }
  },

  async deleteItem(id) {
    try {
      await axios.delete(`${API_URL}items/${id}/`, this.getAuthHeaders());
      return id;
    } catch (error) {
      console.error('Ошибка удаления:', error);
      throw error;
    }
  },

  async login(username, password) {
    try {
      const response = await axios.post(`${API_URL}login/`, { username, password });
      localStorage.setItem('token', response.data.access);
      const userResponse = await axios.get(`${API_URL}user/`, this.getAuthHeaders());
      localStorage.setItem('user', JSON.stringify(userResponse.data));
      return userResponse.data;
    } catch (error) {
      console.error('Ошибка авторизации:', error);
      throw error;
    }
  },

  async register(userData) {
    try {
      const response = await axios.post(`${API_URL}register/`, userData);
      return response.status === 201;
    } catch (error) {
      console.error('Ошибка регистрации:', error);
      throw error;
    }
  },

  getUser() {
    const storedUser = localStorage.getItem('user');
    return storedUser ? JSON.parse(storedUser) : null;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
};

export default apiService;