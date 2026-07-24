<template>
  <main class="course-detail">
    <div v-if="course">
      <h2>{{ course.name }} ({{ course.code }})</h2>
      <p><strong>Credits:</strong> {{ course.credits }}</p>
      <p><strong>Description:</strong> {{ course.description }}</p>
      
      <div class="actions">
        <button @click="enrollAndRedirect">Enroll</button>
        <button @click="router.push('/courses')">Back to Courses</button>
      </div>
    </div>
    <div v-else>
      <p>Loading course details or course not found...</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const route = useRoute()
const router = useRouter()
const store = useEnrollmentStore()

const course = ref(null)

// In a real app, you'd fetch this from an API using the ID
const allCourses = [
  { id: 1, name: 'Introduction to Web Development', code: 'CS101', credits: 3, grade: '', description: 'Learn the basics of HTML, CSS, and JS.' },
  { id: 2, name: 'Advanced JavaScript', code: 'CS201', credits: 4, grade: '', description: 'Deep dive into JS concepts and patterns.' },
  { id: 3, name: 'Vue.js Framework', code: 'CS301', credits: 3, grade: '', description: 'Building SPAs with Vue 3.' },
  { id: 4, name: 'Database Systems', code: 'CS202', credits: 4, grade: '', description: 'SQL and NoSQL databases.' },
  { id: 5, name: 'Software Engineering', code: 'CS401', credits: 3, grade: '', description: 'Software lifecycle and methodologies.' }
]

onMounted(() => {
  const courseId = Number(route.params.id)
  course.value = allCourses.find(c => c.id === courseId)
})

function enrollAndRedirect() {
  if (course.value) {
    store.enroll(course.value)
    router.push('/profile')
  }
}
</script>

<style scoped>
.course-detail {
  padding: 2rem;
}
.actions {
  margin-top: 20px;
}
button {
  margin-right: 10px;
  padding: 10px 15px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}
button:hover {
  background-color: #3aa876;
}
</style>
