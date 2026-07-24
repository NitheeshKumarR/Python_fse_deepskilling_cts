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

    <div class="course-list">
      <CourseCard 
        v-for="course in filteredCourses" 
        :key="course.id"
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
      >
        <button @click="store.enroll(course)">Enroll</button>
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

const router = useRouter()
const store = useEnrollmentStore()

const courses = ref([])
const searchTerm = ref('')

onMounted(() => {
  courses.value = [
    { id: 1, name: 'Introduction to Web Development', code: 'CS101', credits: 3, grade: '', description: 'Learn the basics of HTML, CSS, and JS.' },
    { id: 2, name: 'Advanced JavaScript', code: 'CS201', credits: 4, grade: '', description: 'Deep dive into JS concepts and patterns.' },
    { id: 3, name: 'Vue.js Framework', code: 'CS301', credits: 3, grade: '', description: 'Building SPAs with Vue 3.' },
    { id: 4, name: 'Database Systems', code: 'CS202', credits: 4, grade: '', description: 'SQL and NoSQL databases.' },
    { id: 5, name: 'Software Engineering', code: 'CS401', credits: 3, grade: '', description: 'Software lifecycle and methodologies.' }
  ]
})

const filteredCourses = computed(() => {
  return courses.value.filter(course => 
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    course.code.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})
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
button {
  margin-right: 10px;
  padding: 8px 12px;
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
