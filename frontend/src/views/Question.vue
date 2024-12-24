<script setup>

import { defineProps, defineEmits } from 'vue';

defineProps({
  caseTitle: String,
  questionText: String,
  visible: Boolean,
  color: String
});
const emit = defineEmits(['close']);

  document.addEventListener("DOMContentLoaded", function() {
    const textarea = document.querySelector('.input-custom');
    const container = document.querySelector('.modal-container');

    textarea.addEventListener('input', function() {
      this.style.height = 'auto'; // Сбрасываем высоту текстового поля
      this.style.height = this.scrollHeight + 'px'; // Устанавливаем высоту равной высоте содержимого

      // Увеличиваем высоту контейнера в зависимости от высоты текстового поля
      container.style.minHeight = (this.scrollHeight + 140) + 'px'; // Добавьте отступ для упаковки
    });
  });
</script>

<template>
<div v-if="visible" class="modal" :style="{
      top: '35%',
      width: '50%',
      minHeight: '40%',
      height: 'auto',
      overflow: 'visible'
    }">
  <div class="container modal-container" :style="{backgroundColor: color, width: '100%', minHeight: '100%'}">
    <div class="column">
      <div class="row">
        <h3 style="width: 400px;">{{ caseTitle }} </h3>
      <h3 style="width: 400px;">{{ questionText }} </h3>
    </div>
    </div>
    <button class="button-33" role="button" @click="emit('close')">Закрыть</button>
  </div>
</div>
  <div v-if="visible" class="overlay"></div>
</template>

<style scoped>
.photo{
  width: 50px;
  height: 50px;
  margin: 10px;
  background-color: white;
  border-radius: 10px;
  box-shadow: rgba(44, 187, 99, .1) 0 2px 4px, rgba(44, 187, 99, .05) 0 1px 2px;
  color: #333;
  /*font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;*/
  padding: 10px 15px;
  font-size: 16px;
  border: 2px solid rgba(44, 187, 99, .3);
  transition: all 250ms;
}

.modal{
  opacity: 0.9;
  padding: 5%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.column{
  align-items: center;
  justify-content: center;
}

.container{
  opacity: 1;
}

.buttons{
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
}

</style>