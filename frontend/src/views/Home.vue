<script setup>
import Rating from "@/views/Rating.vue";
import Profile from "@/views/user/Profile.vue";
import CurrentGames from "@/views/CurrentGames.vue";
// import RequestGame from "@/views/RequestGame.vue";



</script>

<template>
<!--  <RequestGame />-->
  <div class="outer-container">
<div class="container home-page" style="min-height: 95%; max-height: 95%;">
    <div class="column" style="width: 70%; height: 95%; max-height: 95%;">
      <Profile/>
      <div class="row game-row">
        <h3>Присоединись к этим играм!</h3>
      </div>
      <CurrentGames/>
    </div>
    <div class="column" style="width: 20%; height: 95%; margin-right: 20px;">
      <button class="button-33" role="button">Новая игра</button>
      <Rating/>
    </div>
  </div>
</div>
</template>

<style scoped>
.outer-container {
  //opacity: 0.9;
  //display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  //max-height: 100vh;
  width: 100%;
  padding: 1%;
  box-sizing: border-box;
}

.home-page{
  opacity: 0.9;
  padding: 20px;
  min-width: 95%;
  min-height: 95%;
  max-height: 95%;
  background: #ffffff;
  align-self: center;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.column{
  justify-content: space-between;
}

.game-row{
  justify-content: center;
}

h3{
  font-weight: bold;
}
</style>