<template>
  <div>
    <form @submit.prevent="login">
      <label for="email">
        Email:
      </label>
      <input v-model="email" type="email" name="email" value />

      <label for="password">
        Password:
      </label>
      <input v-model="password" type="password" name value />

      <button type="submit" name="button">
        Login
      </button>

      <p>{{ error }}</p>
      <router-link :to="{ name: 'register' }"
        >Don't have an account? Register.</router-link
      >
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    login() {
      this.$store
        .dispatch('login', {
          email: this.email,
          password: this.password
        })
        .then(() => {
          this.$router.push({ name: 'dashboard' })
        })
        .catch(err => {
          this.password = null
          this.error = err.response.data.detail
        })
    }
  }
}
</script>

<style scoped></style>
