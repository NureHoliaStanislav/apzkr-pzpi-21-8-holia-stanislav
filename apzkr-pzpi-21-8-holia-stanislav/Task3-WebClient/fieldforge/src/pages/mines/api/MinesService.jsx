import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';
class MinesService {
    async getMines() {
        const token = localStorage.getItem('token');
        const response = await axios
            .get('/api/admin/list_mines', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
        const mines = response.data;
        return mines;
    }
    async deleteMine(mineUuid) {
        const token = localStorage.getItem('token');
        const response = await axios
            .delete(`/api/admin/delete_mine/${mineUuid}`, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
        const result = response.data;
        return result;
    }
    async addMine(mineData) {
        const token = localStorage.getItem('token');
        const response = await axios
            .post('/api/admin/add_mine', mineData, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
        const result = response.data;
        return result;
    }
}

const minesServiceInstance = new MinesService();

export default minesServiceInstance;