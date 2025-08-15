import axios from 'axios'
export default defineNuxtPlugin((nuxtApp) => {
  const runtimeBase = useRuntimeConfig().public.apiBase
  // Derive a sensible default when accessing via non-localhost host/IP
  let baseURL = runtimeBase
  if (process.client) {
    const { protocol, hostname } = window.location
    // If runtime base is missing or points to localhost while we are on another host/IP,
    // point to the same host on port 8000
    if (!baseURL || /localhost/i.test(baseURL)) {
      baseURL = `${protocol}//${hostname}:8000`
    }
  }
  const api = axios.create({ baseURL })
  api.interceptors.request.use((config) => {
    const user = useUser()
    if (user.token) {
      config.headers = config.headers || {}
      config.headers['Authorization'] = `Bearer ${user.token}`
    }
    return config
  })
  return { provide: { api } }
})
