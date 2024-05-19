<template>
  <div class="auth-form-container">
    <form @submit.prevent="handleFormSubmit">
      <h2>{{ formTitle }}</h2>
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" v-model="username">
      <span v-if="errors.username" class="error">{{ errors.username }}</span>
      <br>
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" v-model="password">
      <span v-if="errors.password" class="error">{{ errors.password }}</span>
      <br>
      <div v-if="isSignUpRoute">
        <div>
          <label for="password2">Confirm Password:</label>
          <input type="password" id="password2" name="password2" v-model="password2">
        </div>
        <div>
          <label for="nickname">닉네임 : </label>
          <input type="text" v-model.trim="nickname" id="nickname">
        </div>
        <div>
          <label for="age">나이 : </label>
          <input type="text" v-model.trim="age" id="age">
        </div>
        <div>
          <label for="email">이메일 : </label>
          <input type="email" v-model.trim="email" id="email">
        </div>
        <div>
          <label for="annual_income">연봉 : </label>
          <input type="text" v-model.trim="annual_income" id="annual_income">
        </div>
        <div>
          <label for="property">자산 : </label>
          <input type="text" v-model.trim="property" id="property">
        </div>
        <div>
          <label for="main_bank">주거래 은행 : </label>
          <input type="text" v-model.trim="main_bank" id="main_bank">
        </div>
        <div>
          <label for="saving_propensity">저축 성향 :</label>
          <select v-model="saving_propensity" id="saving_propensity">
            <option value="알뜰형" selected>알뜰형</option>
            <option value="도전형">도전형</option>
            <option value="성실형">성실형</option>
          </select>
        </div>
        </div>
        <button class="submit-button">{{ buttonLabel }}</button>
      <span v-if="errorMessage" class="error">{{ errorMessage }}</span>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import { useRoute, useRouter } from 'vue-router';
import Swal from 'sweetalert2';

const route = useRoute();
const router = useRouter();
const store = useAuthStore();

const username = ref('');
const password = ref('');
const password2 = ref('');
const email = ref('');
const annual_income = ref('');
const property = ref('');
const main_bank = ref('');
const saving_propensity = ref('');
const age = ref('');
const nickname = ref('');

const errors = ref({});
const errorMessage = ref('');

const isSignUpRoute = route.name === 'signup';

const handleFormSubmit = () => {
  errors.value = {}; // 에러 초기화

  // 유효성 검사
  if (!username.value.trim()) {
    errors.value.username = 'Username is required';
  }
  if (!password.value.trim()) {
    errors.value.password = 'Password is required';
  }

  if (isSignUpRoute) {
    // 회원가입 시 추가적인 유효성 검사
    if (password.value !== password2.value) {
      errors.value.password2 = 'Passwords do not match';
    }
  }


  // 폼이 유효한지 확인
  if (Object.keys(errors.value).length === 0) {
    if (isSignUpRoute) {
      store.signUp(username.value, password.value, password2.value, age.value, nickname.value, email.value, annual_income.value, property.value, main_bank.value, saving_propensity.value)
        .then(() => {
        })
        .catch(error => {
          Swal.fire('회원가입에 실패했습니다', '', 'error')
          errorMessage.value = '회원가입에 실패했습니다.';
        });
    } else {
      store.logIn(username.value, password.value)
        .then(() => {
        })
        .catch(error => {
          Swal.fire('로그인에 실패했습니다', '', 'error')
          errorMessage.value = '로그인에 실패했습니다.';
        });
    }
  }
};

const formTitle = isSignUpRoute ? '회원가입' : '로그인';
const buttonLabel = isSignUpRoute ? '가입하기' : '로그인';

</script>


<style scoped>
.auth-form-container {
  background-color: #f8f9fa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

form {
  max-width: 300px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

input {
  width: calc(100% - 16px);
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.submit-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  font-size: 12px;
}
</style>