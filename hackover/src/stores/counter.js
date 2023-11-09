import { ref, computed } from 'vue'
import { defineStore } from 'pinia'


export const useUserStore = defineStore('user', () => {
  const user = ref({})
  const token = ref('')
  const setUser = (newUser) => {
    user.value = newUser
  }
  const setToken = (newToken) => {
    token.value = newToken
  }
  return { user, setUser, token, setToken }
})

