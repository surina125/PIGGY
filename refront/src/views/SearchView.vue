<template>
  <div class="search-page mt-4 mb-3">
    <!-- 탭 -->
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <RouterLink class="nav-link" :class="{ active: isActive('deposit') }" aria-current="page" :to="{name: 'deposit'}">예금</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink class="nav-link" :class="{ active: isActive('savings') }" :to="{name: 'savings'}">적금</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink class="nav-link" :class="{ active: isActive('loan') }" :to="{name: 'loan'}">대출</RouterLink>
      </li>
    </ul>

    <!-- 메인 -->
    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();

const isActive = (name) => {
  return route.name === name;
};
</script>

<style scoped>
.search-page {
  padding-right: 100px;
  padding-left: 100px;
  padding-bottom: 100%;
}

.nav {
  display: flex;
  justify-content: center;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  margin-bottom: 20px;
  padding: 10px 0;
}

.nav-tabs .nav-item {
  margin: 0 15px;
}

.nav-tabs .nav-link {
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  background-color: transparent;
  border: none;
  transition: color 0.3s, background-color 0.3s;
}

.nav-tabs .nav-link:hover {
  color: #000;
  background-color: #e0e0e0;
  border-radius: 5px;
}

.nav-tabs .nav-link.active {
  color: #fff;
  background-color: #333;
  border-radius: 5px;
}

.main-content {
  padding: 20px;
  background-color: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
