import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'


export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'

  const token = ref(null)
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()


  // 회원가입
  const signUp = function (payload) {
    // 1. 사용자 입력 데이터를 받아
    const { username, password1, password2 } = payload

    // 2. axios로 django에 요청을 보냄
    axios({
      method: 'post',
      url: `${API_URL}/accounts/registration/`,
      data: {
        username, password1, password2
      }
    })
     .then((response) => {
       console.log('회원가입 성공!')
       const password = password1
       logIn({ username, password })
     })
     .catch((error) => {
       console.log(error)
     })
  }


  // 로그인
  const logIn = function (payload) {
    // 1. 사용자 입력 데이터를 받아
    const { username, password } = payload
    // 2. axios로 django에 요청을 보냄
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((response) => {
        // 3. 로그인 성공 후 응답 받은 토큰을 저장
        token.value = response.data.key
        router.push({ name : 'home' })
      })
      .catch((error) => {
        console.log(error)
      })
  }


  // 커뮤니티(return에 만든 것 넣어주기)
  // const articles = ref([])

  // const getArticles = function () {
  //   axios({
  //     method: 'get',
  //     url: `${API_URL}/api/v1/articles/`,
  //     headers: {
  //       Authorization: `Token ${token.value}`
  //     }
  //   })
  //     .then(response => {
  //       articles.value = response.data
  //     })
  //     .catch(error => {
  //       console.log(error)
  //     })
  // }

  
  return { signUp, logIn, token, isLogin }
}, { persist: true })

