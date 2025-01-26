import {createStore} from 'vuex'

const store = createStore({
    state () {
        return {
            username: '',
            gameID: '',
            playerID: '',
            photo: 0,
        }
    },
    mutations: {
        setUsername(state, username) {
            state.username = username
        },

        setPhoto(state, photo) {
            state.photo = photo
        },

        setDefault(state) {
            state.username = ""
            state.record = 0
        },

        setGameID(state, gameID) {
            state.gameID = gameID;
        },

        setPlayerID(state, playerID) {
            state.playerID = playerID;
        }
    },

    actions: {
        updateUsername({ commit }, username) {
            commit('setUsername', username);
        },

        updatePhoto({ commit }, photo) {
            commit('setPhoto', photo);
        },

        logout({commit}) {
            commit("setDefault")
        },

        updateGameID({commit}, gameID) {
            commit("setGameID", gameID);
        },

        updatePlayerID({commit}, playerID) {
            commit("setPlayerID", playerID);
        }
    },


})

export default store;