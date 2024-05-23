<template>
  <div
    ref="chatIcon"
    class="chat-icon"
    @mousedown="onMouseDown"
    @click="toggleChat"
    :style="{ top: `${position.y}px`, left: `${position.x}px` }"
  >
    <img src="@/assets/piggy.png" alt="Chat Icon" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const emit = defineEmits(['toggle-chat']);
// 돼지 처음 위치 조정함
const position = ref({ x: 1750, y: 800 });

let isDragging = false;
let offset = { x: 0, y: 0 };
const chatIcon = ref(null);

const onMouseDown = (event) => {
  isDragging = true;
  offset = {
    x: event.clientX - position.value.x,
    y: event.clientY - position.value.y,
  };
  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
};

const onMouseMove = (event) => {
  if (isDragging) {
    position.value = {
      x: event.clientX - offset.x,
      y: event.clientY - offset.y,
    };
  }
};

const onMouseUp = () => {
  isDragging = false;
  document.removeEventListener('mousemove', onMouseMove);
  document.removeEventListener('mouseup', onMouseUp);
};

const toggleChat = () => {
  if (!isDragging) {
    emit('toggle-chat');
  }
};

onUnmounted(() => {
  document.removeEventListener('mousemove', onMouseMove);
  document.removeEventListener('mouseup', onMouseUp);
});
</script>

<style scoped>
.chat-icon {
  position: fixed;
  cursor: pointer;
  width: 80px;
  height: 80px;
}
.chat-icon img {
  width: 100%;
  height: 100%;
}
</style>
