<script setup>

</script>

<template>
<div class="modal" style="top: 35%; width: 50%; min-height: 80%; overflow: visible;">
  <div class="container modal-container" style="width: 100%; min-height: 100%; padding: 20px; ">
    <div class="column">
      <div class="row">
      <div class="photo"></div>
      <h3 style="width: 80%;">Это какой-то тестовый вопрос на очень важную тему, дайте свой ответ</h3>
    </div>
      <div class="column">
        <label>
          <input type="radio" name="answer" value="1">
          Развернутый вариант ответа номер 1
        </label>
        <label>
          <input type="radio" name="answer" value="2">
          Развернутый вариант ответа номер 2
          Развернутый вариант ответа номер 2
          Развернутый вариант ответа номер 2
        </label>
        <label>
          <input type="radio" name="answer" value="3">
          Развернутый вариант ответа номер 3
        </label>
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
}

.column{
  align-items: center;
  justify-content: center;
}

.container{
  opacity: 1;
}

label{
  display: block;
  width: 100%;
  max-width: 400px;
}
</style>