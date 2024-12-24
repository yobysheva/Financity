<script setup>
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
<div class="modal" style="top: 35%; width: 50%; min-height: 40%; height: auto;overflow: visible;">
  <div class="container modal-container" style="width: 100%; min-height: 100%;  align-items: center; justify-content: center; position: relative; padding: 15px;">
    <div class="column" style="width: 100%; align-items: center;">
      <div class="row" style="width: 80%;  text-align: center; margin-top: 5%;">
      <h3>Это какой-то вопрос на очень важную тему, дайте свой ответ</h3>
    </div>
      <textarea class="input-custom" style="min-height: 60%; width: 80%;" placeholder="Введите свой ответ или проговорите его вслух"></textarea>
    <div class="row buttons" style="width: 80%; text-align: center;">
      <button class="button-33" role="button" style="font-size: 24px; font-weight: bold;">+</button>
      <button class="button-33" role="button" style="font-size: 24px; font-weight: bold;">-</button>
    </div>
    </div>
  </div>
</div>
  <div class="overlay"></div>
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