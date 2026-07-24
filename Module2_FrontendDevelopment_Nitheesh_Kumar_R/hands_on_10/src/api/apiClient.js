import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'

const apiClient = axios.create({
  baseURL: 'https://api.studentportal.com/v1',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor (Step 141)
apiClient.interceptors.request.use(
  (config) => {
    // Attach mock token
    config.headers.Authorization = 'Bearer MOCK_TOKEN_12345'
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor (Step 140)
apiClient.interceptors.response.use(
  (response) => {
    // Return response.data directly
    return response.data
  },
  (error) => {
    const customError = new Error(error.response?.data?.message || error.message || 'Unknown Error')
    customError.statusCode = error.response?.status || 500
    return Promise.reject(customError)
  }
)

// Setup Mock Adapter for testing
const mock = new MockAdapter(apiClient, { delayResponse: 500 })

const mockCourses = [
  { id: 1, name: 'Introduction to Web Development', code: 'CS101', credits: 3, grade: '', description: 'Learn the basics of HTML, CSS, and JS.' },
  { id: 2, name: 'Advanced JavaScript', code: 'CS201', credits: 4, grade: '', description: 'Deep dive into JS concepts and patterns.' },
  { id: 3, name: 'Vue.js Framework', code: 'CS301', credits: 3, grade: '', description: 'Building SPAs with Vue 3.' },
  { id: 4, name: 'Database Systems', code: 'CS202', credits: 4, grade: '', description: 'SQL and NoSQL databases.' },
  { id: 5, name: 'Software Engineering', code: 'CS401', credits: 3, grade: '', description: 'Software lifecycle and methodologies.' }
]

mock.onGet('/courses').reply(200, mockCourses)
mock.onGet(new RegExp('/courses/*')).reply((config) => {
  const id = parseInt(config.url.split('/').pop())
  const course = mockCourses.find(c => c.id === id)
  if (course) return [200, course]
  return [404, { message: 'Course not found' }]
})
mock.onPost('/enrollments').reply((config) => {
  const data = JSON.parse(config.data)
  return [201, { message: 'Successfully enrolled', ...data }]
})

export default apiClient
