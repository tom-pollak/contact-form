import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/store'
import axios from 'axios'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  created() {
    const userString = localStorage.getItem('user')
    if (userString) {
      const userData = JSON.parse(userString)
      this.$store.commit('SET_USER_DATA', userData)
    }
    axios.interceptors.response.use(
      response => response,
      error => {
        if (error.response.status === 401) {
          response = this.refreshToken()
          console.log(response)
          if (response.data.access) {
          }

          //this.$store.dispatch('logout')
        }
        return Promise.reject(error)
      }
    )
  },
  methods: {
    refreshToken() {
      return axios.get('//localhost:8000/auth/jwt/refresh/', {
        refresh: this.$store.getters.refreshToken
      })
    }
  },
  render: h => h(App)
}).$mount('#app')
