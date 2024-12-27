import axios from 'axios';

const apiUrl = 'http://localhost:8000/api/';

export const authService = {
    register(userData) {
        return axios.post(`${apiUrl}user/register/`, userData);
    },
    login(userData) {
        return axios.post(`${apiUrl}user/login/`, userData);
    },
    createGame(userData) {
        return axios.post(`${apiUrl}gameApp/createGame/`, userData);
    },
    createPlayer(userData){
        return axios.post(`${apiUrl}gameApp/createPlayer/`, userData);
    },
    getData(username) {
        return axios.get(`${apiUrl}user/getData/`, {params : {username : username}});
    },
    updateData(userData) {
        return axios.put(`${apiUrl}user/updateData/`, userData);
    },
    getUsersStats(username){
        return axios.get(`${apiUrl}user/getStats/`, {params : {username : username}});
    },
    getQuestion(id){
        return axios.get(`${apiUrl}gameApp/getQuestion/`, {params: {id: id}})
    },
    getAnswers(id){
        return axios.get(`${apiUrl}gameApp/getAnswers/`, {params: {id: id}})
    },
    getRandomQuestion(category_id){
        return axios.get(`${apiUrl}gameApp/getRandomQuestion/`, {params: {category_id : category_id}})
    }
};