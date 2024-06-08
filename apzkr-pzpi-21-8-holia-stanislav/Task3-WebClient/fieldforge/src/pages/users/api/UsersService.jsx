import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';
class UsersService {
  async getUsers() {
    const token = localStorage.getItem('token');
    const response = await axios
      .get('/api/admin/list_users', {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
    const users = response.data;
    return users;
  }
  async banUser(userId) {
    const token = localStorage.getItem('token');
    const response = await axios
      .delete(`/api/admin/${userId}/ban`, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
    const result = response.data;
    return result;
  }
}

const usersServiceInstance = new UsersService();

export default usersServiceInstance;