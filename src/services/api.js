import axios from 'axios';

const api = axios.create({
  baseURL: 'https://ai-video-editor-backend.onrender.com',  // Backend URL
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});

export default api;
