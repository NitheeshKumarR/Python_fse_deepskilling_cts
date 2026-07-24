import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { enrollStudent, getCourseById } from '../api/courseApi'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([])
  const loading = ref(false)
  const error = ref(null)

  const totalCredits = computed(() => {
    return enrolledCourses.value.reduce((total, course) => total + course.credits, 0)
  })

  // Basic synchronous enroll for testing or when course is already known
  function enroll(course) {
    if (!enrolledCourses.value.find(c => c.id === course.id)) {
      enrolledCourses.value.push(course)
    }
  }

  // Advanced async action (Step 149)
  async function fetchAndEnroll(courseId) {
    loading.value = true
    error.value = null
    try {
      // API call to enroll
      await enrollStudent(1, courseId) // Hardcoded studentId = 1
      // Fetch the full course details
      const course = await getCourseById(courseId)
      
      // Update state
      if (!enrolledCourses.value.find(c => c.id === course.id)) {
        enrolledCourses.value.push(course)
      }
    } catch (err) {
      error.value = err.message
      throw err // Rethrow to let components handle it if needed
    } finally {
      loading.value = false
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter(c => c.id !== courseId)
  }

  function $reset() {
    enrolledCourses.value = []
    loading.value = false
    error.value = null
  }

  return { enrolledCourses, totalCredits, loading, error, enroll, fetchAndEnroll, unenroll, $reset }
})
