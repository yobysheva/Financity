<script setup>

</script>

<template>
<!--<div class="modal">-->
<!--  <div class="modal-content column">-->
    <div class="row">
      <div class="photo"></div>
      <div class="column pr">
        <p>Имя: Пользователь1234</p>
        <p>Уровень: 10</p>
        <p>Выиграно игр: 12/56</p>
        <p>Место в рейтинге: 5/187</p>
      </div>
    </div>
<!--  </div>-->

<!--</div>-->
<!--  <div class="overlay"></div>-->
</template>

<style scoped>
.photo{
  width: 200px;
  height: 200px;
  margin: 40px;
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

.photo:focus {
  outline: none;
  border-color: rgba(44, 187, 99, .6);
  box-shadow: rgba(44, 187, 99, .35) 0 0 5px;
}

.photo::placeholder {
  color: #aaa;
  opacity: 0.8;
}


p{
  font-size: 16px;
}

.pr{
  font-weight: bold;
  text-align: left;
  justify-content: center;
}

</style>