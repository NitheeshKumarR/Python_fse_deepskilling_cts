<template>
  <header class="app-header">
    <nav>
      <RouterLink to="/">Home</RouterLink> |
      <RouterLink to="/courses">Courses</RouterLink> |
      <RouterLink to="/profile">Profile</RouterLink>
    </nav>
    <div class="enrollment-status">
      Enrolled Courses: {{ store.enrolledCourses.length }}
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #333;
  color: white;
}
.app-header a {
  color: white;
  text-decoration: none;
  margin-right: 10px;
}
.app-header a.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}
</style>
