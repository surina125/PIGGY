<template>
  <div class="container">
    <div class="box" @click="navigateTo('one')">
      <h2>Explore Page 1</h2>
      <p>Click here to see more details on Page 1</p>
    </div>
    <div class="box" @click="navigateTo('two')">
      <h2>Discover Page 2</h2>
      <p>Click here to see more details on Page 2</p>
    </div>
  </div>
  <div class="result-buttons">
    <button class="result-button" @click="navigateTo('recommendations1')">View Recommendations from Method 1</button>
    <button class="result-button" @click="navigateTo('deposit2')">View Recommendations from Method 2</button>
  </div>
  {{ authStore.userData }}
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const navigateTo = (page) => {
  router.push({ name: page, params: {username: authStore.userData.username} })
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 80vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.box {
  width: 300px;
  height: 300px;
  background-color: #007bff;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  text-align: center;
  padding: 20px;
  margin: 20px;
}

.box:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
}

h2 {
  margin: 0;
  font-size: 24px;
}

p {
  margin: 10px 0 0;
  font-size: 16px;
}

.result-buttons {
  display: flex;
  justify-content: space-around;
  padding: 20px;
}

.result-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.result-button:hover {
  background-color: #218838;
  transform: translateY(-5px);
}
</style>
