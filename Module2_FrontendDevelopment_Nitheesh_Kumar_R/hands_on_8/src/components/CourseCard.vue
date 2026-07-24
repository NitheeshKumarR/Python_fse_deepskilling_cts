<template>
  <div class="course-card">
    <h3>{{ name }} ({{ code }})</h3>
    <p>Credits: {{ credits }}</p>
    <p v-if="grade">Grade: {{ grade }}</p>
    <div class="actions">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: String,
  code: String,
  credits: Number,
  grade: String
});
</script>

<style scoped>
.course-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #f9f9f9;
}
.course-card h3 {
  margin-top: 0;
}
.actions {
  margin-top: 10px;
}
</style>
