import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',  // Backend URL
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});

export default api;
