<template>
  <main class="profile-view">
    <h2>Student Profile</h2>
    
    <div class="summary">
      <h3>Enrollment Summary</h3>
      <p><strong>Total Enrolled Courses:</strong> {{ store.enrolledCourses.length }}</p>
      <p><strong>Total Credits:</strong> {{ store.totalCredits }}</p>
    </div>

    <div v-if="store.enrolledCourses.length > 0" class="enrolled-list">
      <h3>Enrolled Courses</h3>
      <ul>
        <li v-for="course in store.enrolledCourses" :key="course.id">
          <strong>{{ course.name }}</strong> ({{ course.code }}) - {{ course.credits }} credits
          <button class="unenroll-btn" @click="store.unenroll(course.id)">Unenroll</button>
        </li>
      </ul>
    </div>
    <div v-else class="empty-state">
      <p>You are not enrolled in any courses yet.</p>
      <button @click="router.push('/courses')">Browse Courses</button>
    </div>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const router = useRouter()
const store = useEnrollmentStore()
</script>

<style scoped>
.profile-view {
  padding: 2rem;
}
.summary {
  background-color: #f0f8ff;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.enrolled-list ul {
  list-style-type: none;
  padding: 0;
}
.enrolled-list li {
  padding: 10px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.unenroll-btn {
  background-color: #ff4757;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}
.unenroll-btn:hover {
  background-color: #ff6b81;
}
button {
  padding: 8px 15px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #3aa876;
}
</style>
