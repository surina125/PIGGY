<template>
  <div>
    <h1>블라블라</h1>
    <h3>예금</h3>
    <DepositChart/>
    <h3>적금</h3>
    <SavingChart/>
    <h3>주택담보대출</h3>
    <LoanChart/>
  </div>
</template>

<script setup>
import DepositChart from './Reco1Chart.vue/DepositChart.vue'
import SavingChart from './Reco1Chart.vue/SavingChart.vue'
import LoanChart from './Reco1Chart.vue/LoanChart.vue'

</script>

<style  scoped>

</style>