<template>
  <div>
    <!-- 탭 -->
    <ul class="nav">
      <li class="nav-item">
        <RouterLink class="nav-link" aria-current="page" :to="{name: 'deposit'}">예금</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink class="nav-link" :to="{name: 'savings'}">적금</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink class="nav-link" :to="{name: 'loan'}">대출</RouterLink>
      </li>
    </ul>

    <!-- 메인 -->
    <RouterView />
    
  </div>
</template>

<script setup>

</script>

<style scoped>

</style>