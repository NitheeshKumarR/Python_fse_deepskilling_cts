import apiClient from './apiClient'

export async function getAllCourses() {
  return await apiClient.get('/courses')
}

export async function getCourseById(id) {
  return await apiClient.get(`/courses/${id}`)
}

export async function enrollStudent(studentId, courseId) {
  return await apiClient.post('/enrollments', {
    studentId,
    courseId
  })
}
