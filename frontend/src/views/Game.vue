<script setup>

import Player from "@/views/user/Player.vue";
// import Fields from "@/views/Fields.vue";

// import Question from "@/views/Question.vue";
// import QuizQuestion from "@/views/QuizQuestion.vue";
</script>

<template>
<!--  <QuizQuestion/>-->
<div class="outer-container">
<div class="transparent-container game-page" style="min-height: 98%; max-height: 98%; min-width: 96%; max-width: 96%;">
  <div class="row" style="height: 100%; width: 100%;">
    <div class="column" style="height: 100%; width: 10%;">
      <Player/>
      <Player/>
      <Player/>
      <Player/>
      <Player/>
    </div>
    <div class="column" style="height: 100%; width: 65%; margin-left: 2%;">
      <div class="container" style="width: 100%; height: 100%; position: relative;">
        <img class="image" src="../assets/financity_pole.png" style="width: 100%; height: 100%">
<!--        <Fields/>-->
<!--        <img src="../assets/kletki.svg" style="position:absolute; top: 0px; left: 0px; width: 100%; height: 100%">-->
      </div>
  </div>
  <div class="column" style="width: 20%; height: 95%; margin-left: 2%;">
    <div class="row buttons">
      <button class="button-33" role="button">Выйти из игры</button>
      <button class="button-33" role="button">?</button>
    </div>
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
  height: 100%;
  //max-height: 100vh;
  //width: 100%;
  box-sizing: border-box;
  padding: 2% 1%;
}

.game-page{
  justify-content: center;
  align-items: center;
}

.row {
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
}

.button-33{
  font-size: 14px;
  margin: 10px;
}

.buttons{
  //gap: 5px;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
}

.transparent-container{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>