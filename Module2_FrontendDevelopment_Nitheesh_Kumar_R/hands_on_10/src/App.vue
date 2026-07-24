<script setup>
import { RouterView } from 'vue-router'
import Header from './components/Header.vue'
import { globalState } from './main'
</script>

<template>
  <div v-if="globalState.hasError" class="global-error-boundary">
    <h1>Something went wrong!</h1>
    <p>{{ globalState.errorMessage }}</p>
    <button @click="() => window.location.reload()">Reload Application</button>
  </div>
  <div v-else>
    <Header />
    <RouterView />
  </div>
</template>

<style>
/* Global styles */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.global-error-boundary {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #ffeaea;
  color: #d32f2f;
  text-align: center;
  padding: 2rem;
}
.global-error-boundary h1 {
  margin-bottom: 1rem;
}
.global-error-boundary button {
  margin-top: 1rem;
  padding: 10px 20px;
  background-color: #d32f2f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}
.global-error-boundary button:hover {
  background-color: #b71c1c;
}
</style>
