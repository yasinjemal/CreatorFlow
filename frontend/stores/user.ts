import { defineStore } from 'pinia'

export const useUser = defineStore('user', {
  state: () => ({ token: '', email: '', name: '' }),
  actions: {
    set(auth: { token: string, user: { email: string, name: string } }) {
      this.token = auth.token
      this.email = auth.user.email
      this.name = auth.user.name
    },
    clear() { this.token=''; this.email=''; this.name='' }
  }
})
