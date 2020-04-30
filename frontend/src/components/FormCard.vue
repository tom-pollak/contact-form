<template>
  <router-link
    class="event-link"
    :to="{ name: 'form-detail', params: { id: form.id } }"
  >
    <div class="event-card -shadow">
      <span class="eyebrow" v-if="form.confirmed">Passed</span>
      <span v-else>Last submisson not recieved</span>
      <h4>{{ form.name }}</h4>
      <p>Last submitted: {{ form.last_submitted }}</p>
      <p>{{ form.url }}</p>
      <p>Active {{ form.active }}</p>
    </div>
  </router-link>
</template>

<script>
export default {
  props: {
    form: Object
  }
}
</script>

<style scoped>
.event-card {
  padding: 20px;
  margin-bottom: 24px;
  transition: all 0.2s linear;
  cursor: pointer;
}
.event-card:hover {
  transform: scale(1.01);
  box-shadow: 0 3px 12px 0 rgba(0, 0, 0, 0.2), 0 1px 15px 0 rgba(0, 0, 0, 0.19);
}
.event-card > .title {
  margin: 0;
}
.event-link {
  color: black;
  text-decoration: none;
  font-weight: 100;
}
</style>
