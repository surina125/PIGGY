<template>
  <div class="recommend1-page">
    <h3>내 정보 기반으로 추천받기</h3>

    <div class="reco1-page">
      <h3>예금</h3>
      <DepositChart/>

      <h3>적금</h3>
      <SavingChart/>
      
      <h3>주택담보대출</h3>
      <LoanChart/>
    </div>
  </div>
</template>

<script setup>
import DepositChart from './Reco1Chart/DepositChart.vue'
import SavingChart from './Reco1Chart/SavingChart.vue'
import LoanChart from './Reco1Chart/LoanChart.vue'

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

.recommend1-page {
  padding: 30px 100px;
  font-family: 'Roboto', sans-serif;
  color: #333;
  height: 100%;
  margin-bottom: 50px;
}

.reco1-page {
  width: 100%;
  height: 100%;
}

h3 {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 10px;
}

.reco1-page h3 {
  margin-top: 40px;
}

.recommend1-page div {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

</style>
