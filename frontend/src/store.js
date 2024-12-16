import {createStore} from 'vuex'

const store = createStore({
    state () {
        return {
            username: ''
        }
    },
    mutations: {
        setUsername(state, username) {
            state.username = username
        },

        setDefault(state) {
            state.username = ""
            state.record = 0
        }
    },

    actions: {
        updateUsername({ commit }, username) {
            commit('setUsername', username);
        },

        logout({commit}) {
            commit("setDefault")
        },

    },


})

export default store;