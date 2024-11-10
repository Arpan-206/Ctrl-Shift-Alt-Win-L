import axios from 'axios';

const api = axios.create({
  baseURL: 'https://watermelon-bpwf.onrender.com',
});

export default api;