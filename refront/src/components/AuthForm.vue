<template>
  <div class="auth-form-container">
    <form @submit.prevent="handleFormSubmit">
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" v-model="username">
      <br>
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" v-model="password">
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
      <button class="submit-button">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
import { useRoute } from 'vue-router';

const route = useRoute();
const store = useAuthStore();

const username = ref('');
const password = ref('');
const password2 = ref('');
const email = ref('')
const annual_income = ref('')
const property = ref('')
const main_bank = ref('')
const saving_propensity = ref('')
const age = ref('')
const nickname = ref('')

const isSignUpRoute = route.name === 'signup';

const handleFormSubmit = () => {
  if (isSignUpRoute) {
    store.signUp(
      username.value, 
      password.value, 
      password2.value, 
      age.value , 
      nickname.value, 
      email.value, 
      annual_income.value, 
      property.value, 
      main_bank.value, 
      saving_propensity.value);
  } else {
    store.logIn(username.value, password.value);
  }
};
</script>

<style scoped>
.auth-form-container {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

label {
  font-weight: bold;
}

input {
  width: calc(100% - 16px);
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

button.submit-button {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button.submit-button:hover {
  background-color: #0056b3;
}
</style>
