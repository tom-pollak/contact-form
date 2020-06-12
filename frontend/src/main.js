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
        if (
          error.response.status === 401 &&
          !error.config.url.includes('//localhost:8000/auth/jwt/')
        ) {
          return this.$store
            .dispatch('refresh')
            .then(() => {
              //make another API call
              error.config.headers[
                'Authorization'
              ] = `Bearer ${this.$store.getters.accessToken}`
              error.config.baseURL = undefined //baseURL already present in URL
              return axios(error.config)
            })
            .catch(err => {
              console.log('response interceptor:', err)
              this.$store.dispatch('logout')
              return Promise.reject(error)
            })
        }
        return Promise.reject(error)
      }
    )
  },
  render: h => h(App)
}).$mount('#app')
