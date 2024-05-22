<template>
  <div class="chatbot" v-if="isVisible">
    <button class="close-button" @click="closeChat">X</button>
    <div class="chat-area">
      <div v-for="(chat, index) in chats" :key="index" :class="['chat', chat.type + '-chat']">
        {{ chat.message }}
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
import { ref, nextTick } from 'vue';
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
  right: 20px;
  width: 300px;
  height: 400px;
  border: 1px solid #ccc;
  background-color: #fff;
  display: flex;
  flex-direction: column;
}

.close-button {
  align-self: flex-end;
  margin: 10px;
  padding: 5px;
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
}

.chat {
  margin: 5px 0;
}

.send-chat {
  text-align: right;
}

.receive-chat {
  text-align: left;
}
</style>
