<template>
  <div class="chatbot" v-if="isVisible">
    <div class="chatbot-header">
      <button class="close-button" @click="closeChat">X</button>
    </div>
    <div class="chat-area">
      <div v-for="(chat, index) in chats" :key="index" :class="['chat', chat.type + '-chat']">
        <div class="message">{{ chat.message }}</div>
      </div>
    </div>
    <input
      type="text"
      v-model="userInput"
      @keyup.enter="sendMessage"
      class="chat-input"
      placeholder="Type a message..."
    />
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue';
import axios from 'axios';

const props = defineProps({
  isVisible: Boolean,
});

const emit = defineEmits(['close-chat']);
const chats = ref([]);
const userInput = ref('');
const oldMsg = ref('');

const OPEN_API_URL = 'https://api.openai.com/v1/chat/completions';
const API_KEY = 'sk-proj-2y5MeZ5AwEShg3zqkkbET3BlbkFJMURTlOkcUQlACUtQ8OdU';

const addChat = async (type, message) => {
  chats.value.push({ type, message });
  await nextTick(() => {
    const chatArea = document.querySelector('.chat-area');
    chatArea.scrollTop = chatArea.scrollHeight;
  });
};

const sendMessage = async () => {
  const userMsg = userInput.value;
  if (!userMsg) return;

  addChat('send', userMsg);
  userInput.value = '';

  const messages = [
    { role: 'user', content: userMsg },
    { role: 'system', content: oldMsg.value },
  ];

  try {
    const response = await axios.post(OPEN_API_URL, {
      model: 'gpt-3.5-turbo',
      messages,
    }, {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    });

    const responseMessage = response.data.choices[0].message.content;
    addChat('receive', responseMessage);
    oldMsg.value = responseMessage;
  } catch (error) {
    console.error(error.response.data);
  }
};

const closeChat = () => {
  emit('close-chat');
};
</script>

<style scoped>
.chatbot {
  position: fixed;
  bottom: 80px;
  right: 70px;
  width: 320px;
  height: 400px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: transform 0.3s ease-in-out;
}

.chatbot-header {
  display: flex;
  justify-content: flex-end;
  padding: 10px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.close-button {
  background-color: transparent;
  border: none;
  font-size: 16px;
  cursor: pointer;
}

.chat-area {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}

.chat-input {
  border-top: 1px solid #ccc;
  padding: 10px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  outline: none;
  font-size: 14px;
}

.chat {
  display: flex;
  margin: 10px 0;
}

.send-chat {
  justify-content: flex-end;
}

.receive-chat {
  justify-content: flex-start;
}

.message {
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.4;
  position: relative;
}

.send-chat .message {
  background-color: #dcf8c6;
  color: #000;
  border-top-right-radius: 0;
}

.receive-chat .message {
  background-color: #f1f0f0;
  color: #000;
  border-top-left-radius: 0;
}
</style>
