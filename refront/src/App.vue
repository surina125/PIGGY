<template>
  <div>
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
.main-content {
  padding-top: 70px; /* Adjust this value according to the height of your fixed navbar */
}
</style>
