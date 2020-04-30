<template>
  <div>
    <h1>{{ form.name }}</h1>
    <p>{{ form }}</p>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  props: ['id'],
  data() {
    return {
      form: {}
    }
  },
  created() {
    return axios
      .get('//localhost:8000/forms/' + this.id + '/')
      .then(response => {
        this.form = response.data
      })
      .catch(err => {
        console.log('error:', err.response)
      })
  }
}
</script>
