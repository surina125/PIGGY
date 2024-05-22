import { ref } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import axios from 'axios';

export const useAuthStore = defineStore('auth', () => {
  const user = ref({})
  const router = useRouter()
  const token = ref('')
  const isAuthenticated = ref(false)
  const userData = ref(null)

  // 로그인한 유저 정보 저장하고, isAuthenticated 변경
  const getUserInfo = function () {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/accounts/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        userData.value = res.data
        isAuthenticated.value = true

      })
      .catch((err) => {
        console.log(err)
      })
  }


  // 회원가입
  const signUp = async function (username, password1, password2, age, nickname, email, annual_income, property, main_bank) {
    try {
      const response = await axios.post('http://127.0.0.1:8000/accounts/registration/', {
        username,
        password1,
        password2,
        age,
        nickname,
        email,
        annual_income,
        property,
        main_bank,
      })
      console.log('회원가입 성공!')
      const password = password1
      logIn(username, password)
    } catch (error) {
      console.log('Error:', error.response)
    }
  }

  // 로그인
  const logIn = async function (username, password) {
    try {
      const res = await axios.post('http://127.0.0.1:8000/accounts/login/', {
        username,
        password
      })
      console.log('로그인 성공!')
      token.value = res.data.key
      getUserInfo()
          
      router.push({ name: 'home' })
    } catch (error) {
      console.log('Error:', error.response)
    }
  }


  // 로그아웃
  const logOut = () => {
    token.value = "";
    isAuthenticated.value = false
    userData.value = null
    router.push({ name: "home" })
  };

  return { signUp, logIn, logOut, token, isAuthenticated, userData }
}, { persist: true })
