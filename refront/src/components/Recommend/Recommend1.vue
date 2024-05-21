<template>
  <div class="container">
    <div class="card" v-for="(product, index) in products" :key="index">
      <div class="card-header">
        {{ product.name }}
      </div>
      <div class="card-body">
        <p>{{ product.description }}</p>
        <p>Interest Rate: {{ product.interestRate }}%</p>
        <p>Term: {{ product.term }} months</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Sample data for demonstration
const products = ref([
  { name: 'Savings Account A', description: 'High interest savings account.', interestRate: 1.5, term: 12 },
  { name: 'Savings Account B', description: 'Flexible savings account.', interestRate: 1.2, term: 6 },
  { name: 'Savings Account C', description: 'No minimum balance required.', interestRate: 1.0, term: 24 },
  { name: 'Savings Account D', description: 'Premium account with extra benefits.', interestRate: 2.0, term: 36 },
  { name: 'Savings Account E', description: 'Standard savings account.', interestRate: 1.3, term: 18 },
  { name: 'Savings Account F', description: 'Account with bonus interest.', interestRate: 1.8, term: 12 },
  { name: 'Savings Account G', description: 'Easy access savings account.', interestRate: 1.4, term: 9 },
  { name: 'Savings Account H', description: 'Long term savings account.', interestRate: 2.1, term: 48 },
  { name: 'Savings Account I', description: 'Young savers account.', interestRate: 1.6, term: 12 },
  { name: 'Savings Account J', description: 'Business savings account.', interestRate: 1.7, term: 12 }
]);
</script>

<style scoped>
.container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  background-color: #f0f4f8;
  padding: 20px;
}

.card {
  width: 250px;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.card-header {
  background-color: #4caf50;
  color: #fff;
  padding: 16px;
  font-size: 18px;
  font-weight: bold;
}

.card-body {
  padding: 16px;
  color: #333;
}

.card-body p {
  margin: 8px 0;
}
</style>
