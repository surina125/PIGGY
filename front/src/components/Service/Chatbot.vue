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
      placeholder="메시지를 입력하세요..."
    />
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import axios from 'axios';
import { useDepositStore } from '@/stores/deposit';
import { useLoanStore } from '@/stores/loan';
import { useSavingStore } from '@/stores/saving';

const depositStore = useDepositStore();
const loanStore = useLoanStore();
const savingStore = useSavingStore();

const props = defineProps({
  isVisible: Boolean,
});

const emit = defineEmits(['close-chat']);
const chats = ref([]);
const userInput = ref('');
const context = ref([]);
const selectedProductType = ref('');
const selectedInsuranceCompany = ref('');

const OPEN_API_URL = 'https://api.openai.com/v1/chat/completions';
const API_KEY = import.meta.env.VITE_APP_OPEN_AI_KEY

const addChat = async (type, message) => {
  chats.value.push({ type, message });
  await nextTick(() => {
    const chatArea = document.querySelector('.chat-area');
    chatArea.scrollTop = chatArea.scrollHeight;
  });
};

const extractInsuranceCompany = (message) => {
  const words = message.split(' ');
  for (const word of words) {
    if (word.includes('보험')) {
      return word.split('보험')[0] + '보험';
    }
  }
  return '';
};

const getTopLoanProduct = (company) => {
  const filteredLoans = loanStore.loans.filter(loan => loan.kor_co_nm.includes(company));
  const topLoan = filteredLoans.reduce((max, loan) => (loan.like_user.length > max.like_user.length ? loan : max), filteredLoans[0]);

  if (topLoan) {
    const details = `
      상품명: ${topLoan.fin_prdt_nm}
      가입 방법: ${topLoan.join_way}
      중도상환 수수료: ${topLoan.erly_rpay_fee}
      연체 이자율: ${topLoan.dly_rate}
      대출 한도: ${topLoan.loan_lmt}
    `;
    return { 
      message: `${company}에서 가장 인기가 많은 대출 상품은 "${topLoan.fin_prdt_nm}"입니다.`,
      details: details
    };
  } else {
    return { message: `${company}에서 추천할 수 있는 대출 상품이 없습니다.`, details: '' };
  }
};

const getTopDepositOrSavingProduct = (type, bank) => {
  let products = [];
  if (type === '예금') {
    products = depositStore.deposits;
  } else if (type === '적금') {
    products = savingStore.savings;
  }

  const filteredProducts = products.filter(product => product.kor_co_nm.includes(bank));
  const topProduct = filteredProducts.reduce((max, product) => (product.like_user.length > max.like_user.length ? product : max), filteredProducts[0]);

  if (topProduct) {
    const details = `
      상품명: ${topProduct.fin_prdt_nm}
      가입 방법: ${topProduct.join_way}
      만기 후 이자: ${topProduct.mtrt_int}
      특이 조건: ${topProduct.spcl_cnd}
      가입 가능 대상: ${topProduct.join_member}
      기타 정보: ${topProduct.etc_note}
    `;
    return { 
      message: `${bank}에서 가장 인기가 많은 ${type} 상품은 "${topProduct.fin_prdt_nm}"입니다.`,
      details: details
    };
  } else {
    return { message: `${bank}에서 추천할 수 있는 ${type} 상품이 없습니다.`, details: '' };
  }
};

const sendMessage = async () => {
  const userMsg = userInput.value;
  if (!userMsg) return;

  addChat('send', userMsg);
  userInput.value = '';

  context.value.push({ role: 'user', content: userMsg });

  if (userMsg.includes('추천')) {
    if (userMsg.includes('예금')) {
      selectedProductType.value = '예금';
      addChat('receive', '선호하는 은행이 있나요? 은행 이름을 입력해 주세요.');
    } else if (userMsg.includes('적금')) {
      selectedProductType.value = '적금';
      addChat('receive', '선호하는 은행이 있나요? 은행 이름을 입력해 주세요.');
    } else if (userMsg.includes('대출')) {
      selectedProductType.value = '대출';
      addChat('receive', '선호하는 보험사가 있나요? 보험사 이름을 입력해 주세요.');
    } else {
      addChat('receive', '어떤 금융 상품을 추천받고 싶으신가요? 예금, 적금, 대출 중에 선택해 주세요.');
      return;
    }
  } else if (selectedProductType.value && selectedProductType.value !== '대출') {
    const bank = userMsg.split(' ').find(word => word.includes('은행'));
    if (bank) {
      const bankName = bank.split('은행')[0] + '은행';
      const { message, details } = getTopDepositOrSavingProduct(selectedProductType.value, bankName);
      addChat('receive', message);
      addChat('receive', details);
    } else {
      addChat('receive', '유효한 은행 이름을 입력해 주세요.');
    }
  } else if (selectedProductType.value === '대출' && !selectedInsuranceCompany.value) {
    selectedInsuranceCompany.value = extractInsuranceCompany(userMsg);
    if (selectedInsuranceCompany.value) {
      const { message, details } = getTopLoanProduct(selectedInsuranceCompany.value);
      addChat('receive', message);
      addChat('receive', details);
    } else {
      addChat('receive', '유효한 보험사 이름을 입력해 주세요.');
    }
  } else {
    const prompt = [
      { role: 'system', content: "당신은 금융상품 추천 챗봇입니다. 사용자가 입력한 메시지에 따라 적절한 금융상품을 추천하세요." },
      ...context.value,
    ];

    try {
      const response = await axios.post(OPEN_API_URL, {
        model: 'gpt-4o',
        messages: prompt,
      }, {
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          'Content-Type': 'application/json',
        },
      });

      const responseMessage = response.data.choices[0].message.content;
      addChat('receive', responseMessage);
      context.value.push({ role: 'assistant', content: responseMessage });
    } catch (error) {
      console.error(error.response.data);
    }
  }
};

const closeChat = () => {
  emit('close-chat');
};
</script>

<style scoped>
.chatbot {
  position: fixed;
  bottom: 60px;
  right: 70px;
  width: 600px;
  height: 550px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: transform 0.3s ease-in-out;
  z-index: 101;
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
  font-size: 20px;
  cursor: pointer;
}

.chat-area {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}

.chat-input {
  border-top: 1px solid #ccc;
  padding: 15px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  outline: none;
  font-size: 18px;
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
  padding: 15px;
  border-radius: 10px;
  font-size: 18px;
  line-height: 1.6;
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
