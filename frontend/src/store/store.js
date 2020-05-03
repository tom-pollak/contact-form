import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null
  },
  mutations: {
    SET_USER_DATA(state, userData) {
      state.user = userData
      localStorage.setItem('user', JSON.stringify(userData))
      axios.defaults.headers.common[
        'Authorization'
      ] = `Bearer ${userData.access}`
    },
    CLEAR_USER_DATA() {
      localStorage.removeItem('user')
      location.reload()
    }
  },
  actions: {
    login({ commit }, credentials) {
      return axios
        .post('//localhost:8000/auth/jwt/create/', credentials)
        .then(({ data }) => {
          commit('SET_USER_DATA', data)
        })
    },
    logout({ commit }) {
      commit('CLEAR_USER_DATA')
    },
    refresh({ state, commit }) {
      if (state.user) {
        return axios
          .post('//localhost:8000/auth/jwt/refresh/', {
            refresh: state.user.refresh
          })
          .then(({ data }) => {
            commit('SET_USER_DATA', {
              access: data.access,
              refresh: state.user.refresh
            })
          })
      }
    }
  },
  getters: {
    loggedIn(state) {
      return !!state.user
    },
    accessToken(state) {
      return state.user.access
    }
  },
  modules: {}
})
