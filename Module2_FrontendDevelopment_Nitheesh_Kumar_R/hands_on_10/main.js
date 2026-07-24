import { createApp, reactive } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Create a global state for the error boundary (Step 150)
export const globalState = reactive({
  hasError: false,
  errorMessage: ''
})

const app = createApp(App)

// Global Error Handler (Step 150)
app.config.errorHandler = (err, instance, info) => {
  console.error('Global Error Caught:', err)
  console.error('Component Info:', info)
  
  // Show fallback UI
  globalState.hasError = true
  globalState.errorMessage = err.message || 'An unexpected error occurred.'
}

app.use(createPinia())
app.use(router)

app.mount('#app')
