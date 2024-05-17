import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useDepositStore } from './deposit'


export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const user = ref({})
  const router = useRouter()
  const token = ref('')
  const isAuthenticated = ref(false)

  const signUp = function (username, password1, password2, age , nickname, email, annual_income, property, main_bank, saving_propensity) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/registration/`,
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
      .then(response => {
        console.log('회원가입 성공!')
        const password = password1
        logIn(username, password)
      })
      .catch(error => {
        console.log(error)
      })
      
  }

  const logIn = function (username, password) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username,
        password
      },
    })
      .then(res => {
        console.log('로그인 성공!')
        token.value = res.data.key
        isAuthenticated.value = true
        router.push({name: 'home'})
      })
      .catch(error => {
        console.log(error)
      })
    }

  return { API_URL, signUp, logIn, token, isAuthenticated, user }
}, { persist: true })

