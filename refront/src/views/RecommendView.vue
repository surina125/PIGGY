<template>
  <div class="container">
    <div class="box" @click="navigateTo('recommendationBySimilarity')">
      <h2>Find Similar People</h2>
      <p>Discover products used by people like you in terms of age, assets, and salary.</p>
    </div>
    <div class="box" @click="navigateTo('recommendationBySurvey')">
      <h2>Answer Survey Questions</h2>
      <p>Choose your preferences and get tailored product recommendations.</p>
    </div>
  </div>
  <div class="result-buttons">
    <button class="result-button" @click="navigateTo('recommendationsFromSimilarity')">View Recommendations from Similar People</button>
    <button class="result-button" @click="navigateTo('recommendationsFromSurvey')">View Recommendations from Survey</button>
  </div>
  {{ authStore.userData }}
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRecommendStore } from '@/stores/recommend'
import { onMounted } from 'vue'

onMounted(() => {
  const recommendStore = useRecommendStore()
  recommendStore.reco1D = [] // Initialize empty array for recommendations
  recommendStore.reco1S = []
  recommendStore.reco1L = []
  recommendStore.reco1Result()
})

const authStore = useAuthStore()
const router = useRouter()

const navigateTo = (page) => {
  router.push({ name: page, params: { username: authStore.userData.username } })
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 80vh;
  background-color: #f1f5ff;
  padding: 20px;
}

.box {
  width: 300px;
  height: 300px;
  background-color: rgba(0, 123, 255, 0.8);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
  cursor: pointer;
  text-align: center;
  padding: 20px;
  margin: 20px;
}

.box:hover {
  background-color: rgba(0, 123, 255, 1);
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
