import axios from 'axios';

const apiUrl = 'http://localhost:8000/api/';

export const authService = {
    register(userData) {
        return axios.post(`${apiUrl}user/register/`, userData);
    },
    login(userData) {
        return axios.post(`${apiUrl}user/login/`, userData);
    },
    getInfoAboutGame(gameId) {
        return axios.get(`${apiUrl}gameApp/getInfoAboutGame/`, {params : {gameId: gameId}});
    },
    connectToGame(userData){
        return axios.post(`${apiUrl}gameApp/connectToGame/`, userData);
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
    updatePhoto(userData){
        return axios.put(`${apiUrl}user/updatePhoto/`, userData);
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
    },
    getChance(id){
        return axios.get(`${apiUrl}gameApp/getChance/`, {params: {id: id}})
    },
    getRandomChance(){
        return axios.get(`${apiUrl}gameApp/getRandomChance/`)
    },
    getActiveGames() {
      return axios.get(`${apiUrl}gameApp/getActiveGames/`)
    },
    getRandomProfession(player_id){
        return axios.get(`${apiUrl}gameApp/getRandomProfession/`, {params: {player_id: player_id}})
    },
    changePlayer(player_id, profession){
        return axios.get(`${apiUrl}gameApp/changePlayer/`,{params: {player_id: player_id, profession: profession}})
    },
    addActionAnswer(player_id, answer_id){
        return axios.get(`${apiUrl}gameApp/addActionAnswer/`, {params: {player_id: player_id, answer_id: answer_id}})
    },
    addActionChance(player_id, chance_id){
        return axios.get(`${apiUrl}gameApp/addActionChance/`, {params: {player_id: player_id, chance_id: chance_id}})
    },
    checkScip(player_id){
      return axios.get(`${apiUrl}gameApp/checkScip/`, {params: {player_id: player_id}})
    },
    changeBalance(player_id){
      return axios.get(`${apiUrl}gameApp/changeBalance/`, {params: {player_id: player_id}})
    },
    getAnswerOutcome(answer_id){
        return axios.get(`${apiUrl}gameApp/getAnswerOutcome/`, {params: {answer_id: answer_id}})
    },
};