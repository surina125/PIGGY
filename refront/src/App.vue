<template>
  <div id="app">
    <header>
      <AppNav />
    </header>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import AppNav from '@/components/Common/AppNav.vue'
</script>

<style scoped>
#app {
  width: 100vw;
  height: 100vh;
  padding-right: 100px;
  padding-left: 100px;
  background-color: #f1f5ff;
}

.main-content {
  padding-top: 80px; 
}
</style>
