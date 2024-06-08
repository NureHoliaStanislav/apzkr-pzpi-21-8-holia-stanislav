import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';
class ProfileService {
  async getProfile(credentials) {
    const token = localStorage.getItem('token');
    const response = await axios
      .get('/api/user',{
        headers: {
          'Authorization': `Token ${token}`
        }
      });
    const user = response.data.user;
    return user;
  }
}

const profileServiceInstance = new ProfileService();

export default profileServiceInstance;