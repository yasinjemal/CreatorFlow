export default defineNuxtRouteMiddleware((to, from) => {
  const user = useUser()
  if (to.path !== '/' && !user.token) {
    // allow public routes; for demo we won't block
  }
})
