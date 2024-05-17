import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'


export const useAuthStore = defineStore('auth', () => {
  const user = ref({})
  const router = useRouter()
  const token = ref('')
  const isAuthenticated = ref(false)

  const signUp = function (username, password1, password2, age , nickname, email, annual_income, property, main_bank, saving_propensity) {
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/registration/',
      data: {
        username,
        password1,
        password2, 
        age ,
        nickname, 
        email, 
        annual_income, 
        property, 
        main_bank, 
        saving_propensity
      }
    })
    .then(res => {
      const password = password1
      logIn(username, password)

    })
  }

  const logIn = function (username, password) {
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/login/',
      data: {
        username,
        password
      }
    })
      .then(res => {
        token.value = res.data.key
        isAuthenticated.value = true
        router.push({name: 'home'})
      })
    }

  return { signUp, logIn, token, isAuthenticated, user }
}, { persist: true })

