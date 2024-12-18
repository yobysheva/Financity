<script setup>

import Player from "@/views/user/Player.vue";
// import Question from "@/views/Question.vue";
// import QuizQuestion from "@/views/QuizQuestion.vue";
import { ref } from 'vue';

   const result = ref('');
   const diceStyle = ref({});

   const spinDice = () => {
       let rnd = Math.floor(Math.random() * 6 + 1);
       let x, y;

       switch (rnd) {
           case 1:
               x = 720;
               y = 810;
               break;
           case 6:
               x = 720;
               y = 990;
               break;
           default:
               x = 720 + (6 - rnd) * 90;
               y = 900;
               break;
       }

       diceStyle.value = {
           transform: `translateZ(-100px) rotateY(${x}deg) rotateX(${y}deg)`,
       };

       // Обновление результата
       result.value = `Выпало: ${rnd}`;
   };
</script>

<template>
<!--  <QuizQuestion/>-->
<div class="outer-container">
<div class="transparent-container game-page" style="min-height: 98%; max-height: 98%; min-width: 96%; max-width: 96%;">
  <div class="row" style="height: 100%; width: 100%;">
    <div class="column" style="height: 100%; width: 20%;">
      <Player/>
      <Player/>
      <Player/>
      <Player/>
      <Player/>
    </div>
    <div class="column" style="height: 100%; width: 45%; margin-left: 5%;">
      <div class="container" style="width: 100%; height: 100%;">
        <img src="../assets/financity.png" style="width: 100%; height: 100%">
        <div class="panel">
    <div class="dice" :style="diceStyle">
        <div class="side one">
            <span class="dot"></span>
        </div>
        <div class="side two">
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
        <div class="side three">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
        </div>
        <div class="side four">
            <div class="kolona">
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
            <div class="kolona">
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        </div>
        <div class="side five">
            <div class="kolona">
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
            <div class="kolona">
                <span class="dot"></span>
            </div>
            <div class="kolona">
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        </div>
        <div class="side six">
            <div class="kolona">
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
            <div class="kolona">
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
            <div class="kolona">
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        </div>
    </div>
</div>

    <button id="spin" @click="spinDice">Крутить</button>
    <div id="result">{{ result }}</div>
    <div class="dice" :style="diceStyle"></div>
    </div>
    </div>
  <div class="column" style="width: 25%; height: 95%; margin-left: 5%;">
    <div class="container" style="width: 100%; height: 100%">
      <p>Тут должен быть чат</p>
      <p>Он будет высотой во весь экран</p>
    </div>
    </div>
  </div>
</div>
</div>
</template>

<style scoped>
.outer-container {
  opacity: 0.9;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  max-height: 100vh;
  width: 100%;
  box-sizing: border-box;
}
.row {
  flex-wrap: wrap;
}
.dice {
  border-radius: 10px;
    height: 66.67px;
    width: 66.67px;
    position: relative;
    transform-style: preserve-3d;
    transform: translateZ(-100px) rotateY(-45deg) rotateX(-45deg);
    transition: transform 1s;
}

.panel {
    border-radius: 10px;
    width: 66.67px;
    height: 66.67px;
    perspective: 400px;
    position: absolute;
    left: 46.7%;
    top: 35.5%;
    transform: translate(-50%, -50%);
}

.dot {
    display: block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin: 1.33px;
    background-color: #7cedc1;
}

.side {
    position: absolute;
    background-color: #a2bbf7;
    width: 66.67px;
    height: 66.67px;
    border-radius: 10px;
    line-height: 66.67px;
}

.one {
  border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    transform: rotateX(-90deg) translateZ(33.33px);
    z-index: 1;
}

.two {
  border-radius: 10px;
    display: flex;
    justify-content: space-between;
    transform: rotateY(180deg) translateZ(33.33px);
    z-index: 2;
}

.two .dot:nth-of-type(2) {
  border-radius: 10px;
    align-self: flex-end;
}

.three {
  border-radius: 10px;
    display: flex;
    justify-content: space-between;
    transform: rotateY(90deg) translateZ(33.33px);
    z-index: 3;
}

.three .dot:nth-of-type(2) {
  border-radius: 10px;
    align-self: center;
}

.three .dot:nth-of-type(3) {
  border-radius: 10px;
    align-self: flex-end;
}

.four {
  border-radius: 10px;
    z-index: 4;
    transform: rotateY(0deg) translateZ(33.33px);
}

.four,
.six {
  border-radius: 10px;
    display: flex;
    justify-content: space-between;
}

.four .kolona,
.six .kolona {
  border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.five {
  border-radius: 10px;
    display: flex;
    justify-content: space-between;
    transform: rotateY(-90deg) translateZ(33.33px);
    z-index: 5;
}

.five .kolona {
  border-radius: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.five .kolona:nth-of-type(2) {
  border-radius: 10px;
    justify-content: center;
}

.six {
  border-radius: 10px;
    transform: rotateX(90deg) translateZ(33.33px);
    z-index: 6;
}
</style>