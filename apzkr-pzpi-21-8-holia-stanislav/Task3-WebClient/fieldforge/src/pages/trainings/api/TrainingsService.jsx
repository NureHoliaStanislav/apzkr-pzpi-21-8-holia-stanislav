import axios from 'axios';
axios.defaults.baseURL = 'http://localhost:8000';

class TrainingsService {
  async getTrainings() {
    const token = localStorage.getItem('token');
    const response = await axios
      .get('/api/user/trainings',{
        headers: {
          'Authorization': `Token ${token}`
        }
      });
    const user = response.data;
    return user;
  }
}
const trainingsServiceInstance = new TrainingsService();

export default trainingsServiceInstance;