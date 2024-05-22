<template>
  <div id="app">
    <header>
      <AppNav />
    </header>

    <main class="main-content">
      <RouterView />

      <ChatIcon @toggle-chat="toggleChat" />
      <Chatbot :isVisible="isChatVisible" @close-chat="toggleChat" />
    </main>

  </div>
</template>

<script setup>
import AppNav from '@/components/Common/AppNav.vue'
import ChatIcon from '@/components/Service/ChatIcon.vue';
import Chatbot from '@/components/Service/Chatbot.vue';
import { ref } from 'vue'


const isChatVisible = ref(false);

const toggleChat = () => {
  isChatVisible.value = !isChatVisible.value;
};
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
