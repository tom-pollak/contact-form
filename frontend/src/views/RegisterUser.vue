<template>
  <div>
    <form @submit.prevent="register">
      <label for="email">
        Email:
      </label>
      <input v-model="email" type="email" name="email" value />

      <label for="password">
        Password:
      </label>
      <input v-model="password" type="password" name value />

      <button type="submit" name="button">
        Register
      </button>

      <ul>
        <li v-for="(error, index) in errors" :key="index">
          {{ error[0] }}
        </li>
      </ul>

      <router-link :to="{ name: 'login' }"
        >Already have an account? Login.</router-link
      >
    </form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      email: '',
      password: '',
      errors: null
    }
  },
  methods: {
    register() {
      return axios
        .post('//localhost:8000/users/', {
          email: this.email,
          password: this.password
        })
        .then(() => {
          this.$router.push({ name: 'login' })
        })
        .catch(err => {
          console.log(err.response.data)
          this.password = null
          this.errors = err.response.data
        })
    }
  }
}
</script>

<style scoped></style>
