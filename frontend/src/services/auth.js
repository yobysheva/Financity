import axios from 'axios';

const apiUrl = 'http://localhost:8000/api/user/';

export const authService = {
    register(userData) {
        return axios.post(`${apiUrl}register/`, userData);
    },
    login(userData) {
        return axios.post(`${apiUrl}login/`, userData);
    },
    getData(username) {
        return axios.get(`${apiUrl}getData/`, {params : {username : username}});
    },
    updateData(userData) {
        return axios.put(`${apiUrl}updateData/`, userData);
    },
    getUsersStats(username){
        return axios.get(`${apiUrl}getStats/`, {params : {username : username}});
    }
};