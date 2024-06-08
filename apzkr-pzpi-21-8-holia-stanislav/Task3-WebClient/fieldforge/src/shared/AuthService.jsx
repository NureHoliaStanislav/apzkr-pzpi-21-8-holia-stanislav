import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
axios.defaults.baseURL = 'http://localhost:8000';
class AuthService {
  async login(credentials) {
  
    const response = await axios
      .post('/api/user/login', credentials);
    const token = response.data.user.token;
    if (typeof token === 'string') {
      localStorage.setItem('token', token);
      return jwtDecode(token);
    }
    throw new Error('Token is not a string');
  }

  logout() {
    localStorage.removeItem('token');
  }

  async signup(userDetails) {
    const response = await axios
      .post('/api/user/sign-up', userDetails);
    const token = response.data.user.token;
    if (typeof token === 'string') {
      localStorage.setItem('token', token);
      return jwtDecode(token);
    }
    throw new Error('Token is not a string');
  }

  async getCurrentUser() {
    try {
      const token = localStorage.getItem('token');
      const response = await axios
      .get('/api/user',{
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      const user = response.data.user;
      return user;
    } catch (ex) {
      return null;
    }
  }
}

const authServiceInstance = new AuthService();

export default authServiceInstance;