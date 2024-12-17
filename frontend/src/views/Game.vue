<script setup>

import Player from "@/views/user/Player.vue";
// import Question from "@/views/Question.vue";
// import QuizQuestion from "@/views/QuizQuestion.vue";
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
</style>