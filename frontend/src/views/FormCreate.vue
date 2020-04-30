<template>
  <div>
    <h1>Create Form</h1>
    <form @submit.prevent="formCreate">
      <label for="name">
        Name:
      </label>
      <input v-model="name" type="text" name="name" value />

      <label for="url">
        URL:
      </label>
      <input v-model="url" type="url" name="url" value />

      <label for="test-period">
        URL:
      </label>
      <select v-model="testPeriod" name="test-period" value>
        <option value="1">Daily</option>
        <option value="7">Weekly</option>
        <option value="30">Monthly</option>
      </select>

      <ul>
        <li v-for="(error, index) in errors" :key="index">
          {{ error[0] }}
        </li>
      </ul>

      <button type="submit" name="button">
        Submit
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      name: '',
      url: '',
      testPeriod: '',
      errors: null
    }
  },
  methods: {
    formCreate() {
      return axios
        .post('//localhost:8000/forms/', {
          name: this.name,
          url: this.url,
          test_period: this.testPeriod
        })
        .then(({ data }) => {
          console.log('form data:', data)
          this.$router.push({ name: 'dashboard' })
        })
        .catch(err => {
          console.log(err.response.data)
          this.errors = err.response.data
        })
    }
  }
}
</script>

<style scoped></style>
