<template>
  <main class="course-detail">
    <div v-if="loading" class="loading">Loading course details...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="course">
      <h2>{{ course.name }} ({{ course.code }})</h2>
      <p><strong>Credits:</strong> {{ course.credits }}</p>
      <p><strong>Description:</strong> {{ course.description }}</p>
      
      <div class="actions">
        <button @click="enrollAndRedirect" :disabled="store.loading">
          {{ store.loading ? 'Enrolling...' : 'Enroll' }}
        </button>
        <button @click="router.push('/courses')">Back to Courses</button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'
import { getCourseById } from '../api/courseApi'

const route = useRoute()
const router = useRouter()
const store = useEnrollmentStore()

const course = ref(null)
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  const courseId = Number(route.params.id)
  loading.value = true
  error.value = null
  try {
    course.value = await getCourseById(courseId)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})

async function enrollAndRedirect() {
  if (course.value) {
    try {
      await store.fetchAndEnroll(course.value.id)
      router.push('/profile')
    } catch (err) {
      console.error('Enrollment failed:', err)
    }
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
.loading {
  font-size: 1.2rem;
  color: #666;
}
.error {
  color: red;
  font-weight: bold;
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
button:hover:not(:disabled) {
  background-color: #3aa876;
}
button:disabled {
  background-color: #a0d8bf;
  cursor: not-allowed;
}
</style>
