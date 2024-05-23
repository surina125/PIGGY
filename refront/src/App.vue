<template>
  <div id="app">
    <header>
      <AppNav />
    </header>

    <main class="main-content">
      <RouterView />
    </main>

    <!-- 챗봇 -->
    <ChatIcon @toggle-chat="toggleChat" />
    <Chatbot :isVisible="isChatVisible" @close-chat="toggleChat" />
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
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
/* 
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
} */

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  font-family: 'Noto Sans KR', sans-serif;
}

.main-content {
  flex: 1;
  width: 100%;
  padding-top: 80px;
  background: #f1f5ff; /* 원하는 배경색으로 설정 */
}
</style>
