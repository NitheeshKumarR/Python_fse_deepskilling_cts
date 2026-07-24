import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([])

  const totalCredits = computed(() => {
    return enrolledCourses.value.reduce((total, course) => total + course.credits, 0)
  })

  function enroll(course) {
    if (!enrolledCourses.value.find(c => c.id === course.id)) {
      enrolledCourses.value.push(course)
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter(c => c.id !== courseId)
  }

  return { enrolledCourses, totalCredits, enroll, unenroll }
})
