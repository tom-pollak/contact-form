<template>
  <div class="home">
    <h1>This is the home page</h1>
    <div v-if="!loggedIn">
      <router-link :to="{ name: 'login' }">Login</router-link> |
      <router-link :to="{ name: 'register' }">Register</router-link>
    </div>
  </div>
</template>

<script>
import { authComputed } from '@/store/helpers.js'
export default {
  computed: {
    ...authComputed
  }
}
</script>
