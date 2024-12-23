<script setup>
</script>

<template>
<div class="row">
  <p>1</p>
  <div class="photo"></div>
  <p>Имя пользователя</p>
  <p>Все, кто любит роблокс, присоединяйтесь к моей игре!!!</p>
</div>
</template>

<style scoped>
.row{
  padding: 5px;
}

.photo{
  width: 40px;
  height: 40px;
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

.photo:focus {
  outline: none;
  border-color: rgba(44, 187, 99, .6);
  box-shadow: rgba(44, 187, 99, .35) 0 0 5px;
}

.photo::placeholder {
  color: #aaa;
  opacity: 0.8;
}

.photo:hover {
  //background-color: rgba(100, 255, 200, .9);
  outline: none;
  border-color: rgba(44, 187, 99, .6);
  box-shadow: rgba(44, 187, 99, .35) 0 0 5px;
}

p{
  font-size: 10px;
  font-weight: bold;
  margin: 15px;
}

.pr{
  font-weight: bold;
  text-align: left;
  justify-content: center;
}

</style>