<template>
  <div>
    <form>
      <label for="comment">댓글</label>
      <input type="text" id="comment" v-model="comment"/>
      <button type="submit">댓글 생성</button>
    </form>
  </div>
</template>

<script setup>
import {ref} from 'vue'

const comment = ref('')
</script>

<style scoped>

</style>