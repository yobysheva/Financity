<script setup>
import {defineExpose, defineProps, ref} from 'vue';
defineProps({
  name: String,
  jobName: String,
  jobPayment: Number,
  balance: Number,
  av: String,
  shine: Boolean,
  balanceChange: String
});
import moneySound from "@/assets/sound/money.mp3"

const moneyAudio = new Audio(moneySound);

const moneyMakeSound = () => {
  moneyAudio.volume = 0.3
  moneyAudio.play()
}

const balanceChanged = ref(false);
const visibleTimer = ref(5);

function makeBalanceChanceVisible(){
  balanceChanged.value = true
  if (visibleTimer.value === 5){
    moneyMakeSound();
  }
  console.log('Баланс изменился!')
    if (visibleTimer.value > 0) {
        // console.log(`${visibleTimer.value--} осталось`)
        visibleTimer.value--;
        setTimeout(makeBalanceChanceVisible, 1000)
    }
    else {
        balanceChanged.value = false
        visibleTimer.value = 5
    }
}
defineExpose({
    makeBalanceChanceVisible
});
</script>

<template>
<div class="player-container"
     :class="{ active: shine }"
      :style="{
      height: '10%',
      backgroundColor: shine ? '#defcea' : 'white'
    }">
  <div class="column">
    <div class="photo" ><img :src="av" style="width: 100%;
  height: auto;
  display: block; "/></div>
    <p>{{name}}</p>
        <p>{{jobName}} {{jobPayment}}₽</p>
    <p>Баланс: {{balance}}₽</p>
  </div>
  <div class="balance-change" v-if="balanceChanged">
    <div class="container">
      <p>{{balanceChange}}</p>
    </div>
  </div>
</div>
</template>

<style scoped>
.player-container{
  background-color: white;
  position: relative;
  border-radius: 30px;
  box-shadow: rgba(44, 187, 99, .1) 0 2px 4px, rgba(44, 187, 99, .05) 0 1px 2px;
  color: #333;
  padding: 1px;
  /*margin: 20px;*/
  font-size: 8px;
  border: 2px solid rgba(44, 187, 99, .3);
  /*display: flex;*/
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 10%;
  margin: 5px;
  @media(max-width: 1200px) {
    border-radius: 25px;
  }
  @media(max-width: 900px) {
    border-radius: 20px;
  }
  @media(max-width: 770px) {
    border-radius: 15px;
  }
}

.balance-change{
  position: absolute;
  top: 0px;
  left: 110%;
  z-index: 1000;
  opacity: 0.9;
}

.active{
  outline: none;
  border-color: rgba(44, 187, 99, .6);
  box-shadow: rgba(44, 187, 99, .35) 0 0 5px;
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
  @media(max-width: 1200px) {
    width: 30px;
    height: 30px;
    margin: 4px;
  }
  @media(max-width: 900px) {
    width: 20px;
    height: 20px;
    margin: 3px;
  }
  @media(max-width: 770px) {
    width: 15px;
    height: 15px;
    margin: 2px;
  }
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
p{
  font-size: 8px;
  margin: 5px;
  font-weight: bold;
  @media(max-width: 1200px) {
    font-size: 7px;
    margin: 3px;
  }
  @media(max-width: 900px) {
    font-size: 6px;
    margin: 2px;
  }
  @media(max-width: 770px) {
    font-size: 5px;
    margin: 2px;
  }
}

</style>