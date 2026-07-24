<template>
  <main class="courses-view">
    <h2>Available Courses</h2>
    
    <div class="search-bar">
      <input 
        type="text" 
        v-model="searchTerm" 
        placeholder="Search courses..." 
      />
    </div>

    <div v-if="loading" class="loading">Loading courses...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="!loading && !error" class="course-list">
      <CourseCard 
        v-for="course in filteredCourses" 
        :key="course.id"
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
      >
        <button @click="handleEnroll(course.id)" :disabled="store.loading">
          {{ store.loading ? 'Enrolling...' : 'Enroll' }}
        </button>
        <button @click="router.push(`/courses/${course.id}`)">View Details</button>
      </CourseCard>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import CourseCard from '../components/CourseCard.vue'
import { useEnrollmentStore } from '../stores/enrollment'
import { getAllCourses } from '../api/courseApi'

const router = useRouter()
const store = useEnrollmentStore()

const courses = ref([])
const searchTerm = ref('')
const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  error.value = null
  try {
    courses.value = await getAllCourses()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})

const filteredCourses = computed(() => {
  return courses.value.filter(course => 
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    course.code.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

async function handleEnroll(courseId) {
  try {
    await store.fetchAndEnroll(courseId)
    // Optional: add a success toast here
  } catch (err) {
    console.error('Enrollment failed:', err)
  }
}
</script>

<style scoped>
.courses-view {
  padding: 2rem;
}
.search-bar {
  margin-bottom: 20px;
}
.search-bar input {
  padding: 8px;
  width: 100%;
  max-width: 400px;
  font-size: 16px;
}
.course-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
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
  padding: 8px 12px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover:not(:disabled) {
  background-color: #3aa876;
}
button:disabled {
  background-color: #a0d8bf;
  cursor: not-allowed;
}
</style>
