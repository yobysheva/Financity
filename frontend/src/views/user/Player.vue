<script setup>
import {defineProps} from 'vue';
defineProps({
  jobName: String,
  jobPayment: Number,
  av: String
});

</script>

<template>
<div class="player-container" style="height: 10%;">
  <div class="column">
    <div class="photo" ><img :src="av" style="width: 100%; /* Заполняет ширину блока */
  height: auto; /* Сохраняет пропорции изображения */
  display: block; "/></div>
<!--        <p>Пользователь1234</p>-->
        <p>Профессия: {{jobName}}</p>
        <p>{{jobPayment}}₽</p>
  </div>
</div>
</template>

<style scoped>
.player-container{
  background-color: white;
  border-radius: 30px;
  box-shadow: rgba(44, 187, 99, .1) 0 2px 4px, rgba(44, 187, 99, .05) 0 1px 2px;
  color: #333;
  padding: 5px;
  /*margin: 20px;*/
  font-size: 8px;
  border: 2px solid rgba(44, 187, 99, .3);
  /*display: flex;*/
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 10%;
  margin: 10px;
}

.column{
  align-items: center;
  justify-content: center;
}

.photo{
  width: 45px;
  height: 45px;
  margin: 5px;
  background-color: white;
  border-radius: 10px;
  box-shadow: rgba(44, 187, 99, .1) 0 2px 4px, rgba(44, 187, 99, .05) 0 1px 2px;
  color: #333;
  /*font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;*/
  padding: 0px 0px;
  font-size: 16px;
  border: 2px solid rgba(44, 187, 99, .3);
  transition: all 250ms;
  position: relative;
  overflow: hidden;
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
  outline: none;
  border-color: rgba(44, 187, 99, .6);
  box-shadow: rgba(44, 187, 99, .35) 0 0 5px;
}

p{
  font-size: 8px;
  margin: 5px;
  font-weight: bold;
}

</style>