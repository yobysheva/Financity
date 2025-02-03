<script setup>
// import ChatComponent from "@/views/ChatComponent.vue"
import Player from "@/views/user/Player.vue";
// import Fields from "@/views/Fields.vue";
  import Question from "@/views/Question.vue";
  import Rules from "@/views/children/Rules.vue"
  // import Chance from "@/views/children/Chance.vue";
  import { authService } from "@/services/auth";
// import QuizQuestion from "@/views/QuizQuestion.vue";
import {nextTick, onBeforeUnmount, ref} from 'vue';
// import { getCurrentInstance } from 'vue';
import store from "@/store";
import routes from "../router/index.js";
import clickSound from "@/assets/sound/click.wav";
import hoverSound from "@/assets/sound/hover2.wav";
import modalSound from "@/assets/sound/modal.mp3";
import jumpSound from "@/assets/sound/jump.mp3"
import spinSound from "@/assets/sound/spin.wav"
import messageSound from "@/assets/sound/message.wav"
import moneySound from "@/assets/sound/money.mp3"

import soundOnImg from "@/assets/sound_on.png"
import soundOfImg from "@/assets/sound_of.png"
import song from "@/assets/sound/game_compress2.wav";

let images = ref([
  require('@/assets/av1.png'),
  require('@/assets/av2.png'),
  require('@/assets/av3.png'),
  require('@/assets/av4.png'),
  require('@/assets/av5.png'),
  require('@/assets/av6.png')
]);

let votes = ref({
  "pluses": 0,
  "minuses": 0
})

let soundOn = ref(true);
let soundButtonLabel = ref(soundOnImg);

const clickAudio = new Audio(clickSound);
const hoverAudio = new Audio(hoverSound);
const modalAudio = new Audio(modalSound);
const jumpAudio = new Audio(jumpSound);
const spinAudio = new Audio(spinSound);
const messageAudio = new Audio(messageSound);
const moneyAudio = new Audio(moneySound);

clickAudio.volume = 0.1
hoverAudio.volume = 0.1
modalAudio.volume = 0.1
spinAudio.volume = 0.05
messageAudio.volume = 0.9


// const buttonClickSound = () => {
//   clickAudio.play()
// }
// const buttonHoverSound = () => {
//   hoverAudio.play()
// }
// const modalShowSound = () => {
//   modalAudio.play()
// }
// const jumpingSound = () => {
//   jumpAudio.play()
// }
// const spinDiceSound = () => {
//   spinAudio.play()
// }
// const messageDelieveredSound = () => {
//   messageAudio.play()
// }



function makeSound(sound){
  if(soundOn.value){
    sound.play();
  }
}
const audio = new Audio(song)
audio.volume = 0.35
audio.loop = true

      const playMelody = () => {
      if (soundOn.value) {
        audio.play()
      }
    }

      const disableOrEnableSound = () => {
        soundOn.value = !soundOn.value
        soundButtonLabel = soundOn.value ? soundOnImg : soundOfImg
        makeSound(clickAudio)
        if (soundOn.value) {
          playMelody()
        } else {
          audio.pause()
        }
      }
      playMelody()

    const disableSound = () => {
        soundOn.value = false
        audio.pause()
    }

  //   const handleVisibilityChange = () => {
  //   if (document.hidden) {
  //     audio.pause();
  //     audio.currentTime = 0;
  //   }else {
  //     if (soundOn.value) {
  //       playMelody();
  //     }
  //   }
  // };

  // document.addEventListener('visibilitychange', handleVisibilityChange);

  onBeforeUnmount(() => {
    disableSound();
    // document.removeEventListener('visibilitychange', handleVisibilityChange);
  });

let players = ref([])
if (store.state.playerID !== '') {
    localStorage.setItem('player_id', JSON.stringify(store.state.playerID))
    localStorage.setItem('game_id', JSON.stringify(store.state.gameID))
}
else {
    const PID = JSON.parse(localStorage.getItem("player_id"))
    const GID = JSON.parse(localStorage.getItem("game_id"))
    store.dispatch("updatePlayerID", PID)
    store.dispatch("updateGameID", GID)
}
players.value = []
let current_player_index = 0
let shine = ref([])
let isGameStarted = ref(false)
let isGameEnded = ref(false)
let need_to_share_text_answer = false
let need_to_share_radio_button_answer = false
let isMyTurn = ref(false)
let winner = ref(false)
let scipPlayer = ref([])

const playerComponent = ref([])
const balanceChange = ref([])

authService.getInfoAboutGame(
      store.state.gameID
).then((response) => {
    players.value = response.data['players'];
    players.value.forEach(
        function() {
          dotStyleMassive.value.push({
              width: "auto",
              height: "8%",
              position: "absolute",
              left: `${positions[0][0]}%`,
              top: `${positions[0][1]}%`,
              transition: "all 0.3s ease"
            });
            currentIndexMassive.value.push(0);
            totalSumMassive.value.push(0);
            shine.value.push(false);
            balanceChange.value.push('');
            playerComponent.value.push(null);
            scipPlayer.value.push(false);
        }
    )
    isMyTurn.value = (players.value.length === 1)
})

let newMessage = ref("")

let rulesVisible = ref(false)

function showRules() {
  makeSound(modalAudio);
  rulesVisible.value = !rulesVisible.value;
}

async function sendStartGame() {
  makeSound(clickAudio);
  if (players.value.length < 2) return

  gameSocket.send(
      JSON.stringify({
        'type': 'start_game',
        'info': {}
      })
  )

  await authService.updateGameStatus(
      {
        "game_id": store.state.gameID,
        "status": "started"
      }
  )
}

function startGame() {
    isGameStarted.value = true
}

// if(!props.userType){
  // let sessionID = props.sessionId;

let global_id = 0;
const positions = [
  [5.3, 8], [14.3, 8], [25.5, 8], [36.7, 8], [47, 9], [56.7, 8], [67.7, 8],
  [79, 8], [89, 8], [88.3, 22], [88.3, 35.5], [88.3, 56], [88.3, 69],
  [88.3, 83], [78.7, 83], [67.7, 83], [56.7, 83], [47.3, 84], [37.3, 84],
  [26.3, 84], [15.3, 84], [4.3, 86], [5.3, 70], [5.3, 56], [5.3, 36],
  [5.3, 22]
];

// const dotStyle = ref({
//   width: "auto",
//   height: "8%",
//   position: "absolute",
//   left: `${positions[0][0]}%`,
//   top: `${positions[0][1]}%`,
//   transition: "all 0.3s ease"
// });

const dotStyleMassive = ref([{
  width: "auto",
  height: "8%",
  position: "absolute",
  left: `${positions[0][0]}%`,
  top: `${positions[0][1]}%`,
  transition: "all 0.3s ease"
}]);

// const dotVisible = ref(true);
const result = ref("");
const diceStyle = ref({});
// const totalSum = ref(0);
let totalSumMassive = ref([0]);
let currentIndexMassive = ref([0]);
const lastRoll = ref(null);
let lastX = ref(0);
let lastY = ref(0);

const isSpinDisabled = ref(false);
const spinButtonLabel = ref("Крутить");
let spinTimer = null;

const modalVisible = ref(false);

const modalTitle = ref("");
// const modalQuestion = ref("");
const modalQuestionId = ref(0);
// const modalChanceId = ref(0);
const modalQuestionType = ref(1);

const questionComponent = ref(null);


const modalColor = ref("")
async function checkPositionAndShowModal (currentCoords){
  const stateCoords = [[14.3, 8], [25.5, 8], [36.7, 8], [5.3, 36], [5.3, 22]];
  const entertainmentCoords = [[56.7, 8], [67.7, 8], [79, 8], [88.3, 22], [88.3, 35.5]];
  const realEstateCoords = [[88.3, 56], [88.3, 69], [78.7, 83], [67.7, 83], [56.7, 83]];
  const allCasesCoords = [[37.3, 84], [26.3, 84], [15.3, 84], [5.3, 70], [5.3, 56]];
  const ChanceCoords = [[47, 9], [89, 8], [5.3, 8], [88.3, 83], [47.3, 84], [4.3, 86]];
  let category = null;
  if (stateCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    category = 1;
    modalColor.value = "#c4beee"; // Фиолетовый
  } else if (entertainmentCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    category = 2;
    modalColor.value = "#FFBBF8"; // Розовый
  } else if (realEstateCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    category = 3;
    modalColor.value = "#C8E3FE"; // Голубой
  } else if (allCasesCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    category = [1, 2, 3][Math.floor(Math.random() * 3)];
    modalColor.value = "#E7FC93"; // Желтый
  }else if (ChanceCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    // modalChance.value = chances[Math.floor(Math.random() * chances.length)];
    // setTimeout(() => {
    //   modalChanceVisible.value = true;
    // }, 500);
    modalColor.value = "white";
    modalTitle.value = `Шанс`;
    if (players.value[current_player_index].id === store.state.playerID){
      try {
    const response = await authService.getRandomChance();
    modalQuestionId.value = response.data['id'];
    modalQuestionType.value = 3;
    await questionComponent.value.getQuestion(response.data['id'], 3);
  } catch (error) {
        console.error(error);
  }
    await sendQuestion();
    setTimeout(() => {
        modalVisible.value = true;
    }, 500);
    return;
    }
  }
  if (players.value[current_player_index].id === store.state.playerID) {
    modalTitle.value = `Кейс: ${category === 1 ? "Государство" : category === 2 ? "Развлечения" : "Недвижимость"}`;
    try {
    const response = await authService.getRandomQuestion(category);
    modalQuestionId.value = response.data['id'];
    modalQuestionType.value = response.data['type'];
    await questionComponent.value.getQuestion(response.data['id'], response.data['type']);
    need_to_share_text_answer = response.data['type'] === 1
    need_to_share_radio_button_answer = response.data['type'] === 2
  } catch (error) {
        console.error(error);
  }
    await sendQuestion();
    setTimeout(() => {
        modalVisible.value = true;
    }, 500);
    setTimeout(textAnswerTranslate, 1000)
    setTimeout(radioButtonAnswerTranslate, 1000)
  }
  // isSpinDisabled.value = false;
}


async function openModalWithValues (title, questionId, questionType) {
  modalTitle.value = title
  modalQuestionId.value = questionId
  modalQuestionType.value = questionType
  await questionComponent.value?.getQuestion(questionId, questionType)
  setTimeout(() => {
    makeSound(modalAudio);
        modalVisible.value = true;
    }, 500);
}

async function endGame () {
  makeSound(moneyAudio)
    await authService.updateGameStatus({
        "game_id": store.state.gameID,
        "status": "finished"
    })

    winner.value = getWinner()
    isGameEnded.value = true
    if (winner.value)
    await authService.addWinToGameWinner({
        "player_id": winner.value.id,
        'secret': store.state.mySecret
    })
}

function redirectToHome(){
  makeSound(clickAudio);
  disableSound();
  routes.push({ name: "home" });
}

function checkToEnd() {
    for (let player in players.value) {
        if (players.value[player].balance <= 0) {
            return true
        }
    }
    return players.value.length <= 1
}

function checkPlayerLeave(id) {
    for (let i = 0; i < players.value.length; i++) {

        if (players.value[i].id === id) {
            return i
        }
    }
    return -1
}

function setVotingTimer() {
    gameSocket.send(
      JSON.stringify({
        'type': 'start_voting',
      })
  )
}

function getWinner() {
    let winner = 0
    let min = -1
    for (let i = 0; i < players.value.length; ++i) {
        if (players.value[i].balance >= min) {
            min = players.value[i].balance
            winner = i
        }
    }
    return players.value[winner]
}

async function closeModal(){
    if (modalQuestionType.value === 1) {
      if(isMyTurn.value){
        const response = await authService.voteHandler(players.value[current_player_index].id, votes.value.pluses, votes.value.minuses, store.state.mySecret);
        players.value[current_player_index].balance = response.data['balance'];
      }
      votes.value = {
          "pluses": 0,
          "minuses": 0
      }
    }

    modalVisible.value = false;
    // modalChanceVisible.value = false;
    sendCloseQuestion();
}


const moveDot = (targetIndex) => {
  const steps = [];
  if (targetIndex > currentIndexMassive.value[current_player_index]) {
    for (let i = currentIndexMassive.value[current_player_index] + 1; i <= targetIndex; i++) {
      steps.push(i);
    }
  } else {
    for (let i = currentIndexMassive.value[current_player_index] + 1; i < positions.length; i++) {
      steps.push(i);
    }
    for (let i = 0; i <= targetIndex; i++) {
      steps.push(i);
    }
  }

  let stepIndex = 0;
  const moveNext = () => {
    makeSound(jumpAudio);
    if (stepIndex < steps.length) {
      const [leftPercent, topPercent] = positions[steps[stepIndex]];
      dotStyleMassive.value[current_player_index].left = `${leftPercent}%`;
      dotStyleMassive.value[current_player_index].top = `${topPercent}%`;
      currentIndexMassive.value[current_player_index] = steps[stepIndex];
      stepIndex++;

      if (stepIndex === steps.length) {
        const [currentX, currentY] = positions[currentIndexMassive.value[current_player_index]];
        checkPositionAndShowModal([currentX, currentY]);
      }
      else setTimeout(moveNext, 300);
    }
  };
  moveNext();
};

const chatContainer = ref(null);

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTo({
      top: chatContainer.value.scrollHeight,
      behavior: 'smooth',
    });
  }
};

const messages = ref([
])

const gameId = new URLSearchParams(window.location.search).get('id');
const chatSocket = new WebSocket(`ws://localhost:8200/ws/chat/${gameId}/`);
chatSocket.onmessage = function (event) {
  makeSound(messageAudio);
    let data = JSON.parse(event.data)
    messages.value.push({
      id: global_id += 1,
      username: data["username"],
      msg: data["message"].toString()
    })
  nextTick(() => {
        scrollToBottom();
      });
}

function sendMessage() {
    const input = newMessage.value
    newMessage.value = ""
  if(!input) return
    chatSocket.send(JSON.stringify({
        "message": input,
        "username": store.state.username
      }))
}

const answerSocket = new WebSocket(`ws://localhost:8200/ws/game_answer/${gameId}/`);
answerSocket.onmessage = (event) => {
    let text_data = JSON.parse(event.data);
    text_data = text_data["info"];
    let type = text_data['type']
    let content = text_data['content']
    switch (type) {
        case 'change_text_answer':
            if (players[current_player_index] === store.state.playerID) break
            // eslint-disable-next-line no-case-declarations
            let text = content['text']
            questionComponent.value?.setTextInTextArea(text)
            break;
        case 'radio_button_answer':
            if (players[current_player_index] === store.state.playerID) break
            // eslint-disable-next-line no-case-declarations
            let button_id = content['button_id']
            questionComponent.value?.setActiveRadioButtonForId(button_id)
            break;
        case 'vote':
            if (players.value[current_player_index].id !== store.state.playerID) {
                break
            }
            // eslint-disable-next-line no-case-declarations
            let type_ = content["vote"]
            votes.value[type_]++

    }
}

function textAnswerTranslate() {
    if (!need_to_share_text_answer) return;
    const input1 = questionComponent.value?.getTextInTextArea()
    answerSocket.send(JSON.stringify({
        "type": "textAnswer",
        "text": input1,
    }))

    setTimeout(
        textAnswerTranslate
    , 1000)
}

function radioButtonAnswerTranslate() {
    if (!need_to_share_radio_button_answer) return;
    const input = questionComponent.value?.getIdOfActiveRadioButton()
    if (input)
    answerSocket.send(JSON.stringify({
        "type": "radioButtonAnswer",
        "button_id": input.toString()
    }))

    setTimeout(
        radioButtonAnswerTranslate
    , 1000)
}

function sendPlus() {
  // makeSound(clickAudio);
    answerSocket.send(JSON.stringify(
        {
          "type": "vote",
          "vote": "pluses"
        }
    ))
}

function sendMinus() {
  // makeSound(clickAudio);
    answerSocket.send(JSON.stringify(
        {
          "type": "vote",
          "vote": "minuses"
        }
    ))
}

const gameSocket = new WebSocket(`ws://localhost:8200/ws/game/${gameId}/${store.state.playerID}/`);
gameSocket.onmessage = async (event) => {
    let text_data = JSON.parse(event.data);
    text_data = text_data["info"];
    let info = text_data["info"];
    let type = text_data['type'];
    players.value.forEach((player, index) => {
            shine.value[index] = player.id === players.value[current_player_index].id;
          });
    isMyTurn.value = (players.value[current_player_index].id === store.state.playerID);
    switch (type) {
        case "on_turn_start":
          // eslint-disable-next-line no-case-declarations
            const turn_count = info["turn_count"];
            console.log("on_turn_start")
            // totalSum.value += turn_count;
            makeSound(spinAudio);
            if(totalSumMassive.value[current_player_index] % 26 + turn_count >= 26){
              let response = "";
              if (isMyTurn.value){
                response = await authService.changeBalance(players.value[current_player_index].id, store.state.mySecret);
              }
              else{
                response = await authService.checkBalance(players.value[current_player_index].id);
              }
              players.value[current_player_index].balance = response.data['balance'];
              playerComponent.value[current_player_index].makeBalanceChanceVisible();
              balanceChange.value[current_player_index] = response.data['result'];
            }
            totalSumMassive.value[current_player_index] += turn_count;
            spin(turn_count);
            break;
        case "on_question_open":
          makeSound(modalAudio);
          // eslint-disable-next-line no-case-declarations
            const title = info["title"]
          // eslint-disable-next-line no-case-declarations
            const questionId = info["questionId"]
          // eslint-disable-next-line no-case-declarations
            const questionType = info["questionType"]
            scipPlayer.value[current_player_index] = info["scip"]
            if (players.value[current_player_index].id !== store.state.playerID) {
                openModalWithValues(
                    title, questionId, questionType
                )
            }
            break;
        case "on_question_close":
          makeSound(modalAudio);
            if (checkToEnd()) {
                await endGame()
                return
            }
            need_to_share_text_answer = false
            need_to_share_radio_button_answer = false
            players.value[info['player_index']].balance = info['balance'];
            current_player_index = (current_player_index + 1) % players.value.length;
            // eslint-disable-next-line no-case-declarations
            let scip = true;
            while (scip) {
              // eslint-disable-next-line no-case-declarations
              // const response = await authService.checkScip(players.value[current_player_index].id);

              if(scipPlayer.value[current_player_index]){
                scipPlayer.value[current_player_index] = false;
                current_player_index = (current_player_index + 1) % players.value.length;
              }
              else{
                scip = false;
              }
            }
            questionComponent.value.update_variables()

            players.value.forEach((player, index) => {
              shine.value[index] = player.id === players.value[current_player_index].id;
            });

            isMyTurn.value = (players.value[current_player_index].id === store.state.playerID);
            modalVisible.value = false;
            isSpinDisabled.value = false;
            break;

        case "notification_about_connect_to_game":
            if (Number(info['id']) === store.state.playerID) break;
            players.value.push(info);
            dotStyleMassive.value.push({
              width: "auto",
              height: "8%",
              position: "absolute",
              left: `${positions[0][0]}%`,
              top: `${positions[0][1]}%`,
              transition: "all 0.3s ease"
            });
            currentIndexMassive.value.push(0);
            totalSumMassive.value.push(0);
            balanceChange.value.push('');
            playerComponent.value.push(null);
            scipPlayer.value.push(false);
            break;
        case "start_game":
            startGame()
            break

        case "player_leaving":
            if (Number(info['player_id']) === store.state.playerID) return;
            // eslint-disable-next-line no-case-declarations
            let index = checkPlayerLeave(Number(info['player_id']))
            if (index !== -1) {
              players.value.splice(index, 1)
              dotStyleMassive.value.splice(index, 1)
              currentIndexMassive.value.splice(index, 1)
              totalSumMassive.value.splice(index, 1)
              balanceChange.value.splice(index, 1)
              playerComponent.value.splice(index, 1)
              scipPlayer.value.splice(index, 1)
            }
             if (checkToEnd()) {
                await endGame()
                return
            }
            break;
        case "start_voting":
            if (players.value[current_player_index].id === store.state.playerID) break;
            questionComponent.value.setVotingTimer()
    }
};

function sendCloseQuestion() {
    const info = {
        "type": "on_question_close",
        "info": {
            "player_index": current_player_index,
            "result": false,
            "balance": players.value[current_player_index].balance
        }
    }
    gameSocket.send(JSON.stringify(
        info
    ))
}

async function sendQuestion() {
  let scip = false
  if(modalQuestionType.value === 3){
    let response = await authService.addActionChance(store.state.playerID, modalQuestionId.value)
    players.value[current_player_index].balance = response.data['balance']
    scipPlayer.value[current_player_index] = response.data['scip']
    scip = response.data['scip']
  }
  const info = {
    "type": "on_question_open",
    "info": {
      "title": modalTitle.value,
      "questionId": modalQuestionId.value,
      "questionType": modalQuestionType.value,
      "scip": scip
    }
  }
  gameSocket.send(JSON.stringify(
      info
  ))
}

function sendTurnCount(turn_count) {
    const info = {
        "type": "on_turn_start",
        "info": {
          "turn_count": turn_count,
        }
    }
    gameSocket.send(JSON.stringify(
        info
    ))
}


const generateAndSpin = () => {
  let rnd = Math.floor(Math.random() * 6 + 1);
  sendTurnCount(rnd);
};

function leaveCall() {
  const info = {
      "type": "player_leaving",
      "info": {
          "player_id": store.state.playerID
      }
  }
  gameSocket.send(JSON.stringify(
        info
    ))
  routes.push({ name: "home" });
  disableSound();
}

function spin(rnd) {
  isSpinDisabled.value = true;
  let x, y;

  if (lastRoll.value === rnd) {
    x = lastX.value + 360;
    y = lastY.value + 360;
  } else {
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
  }

  diceStyle.value = {
    transform: `translateZ(-100px) rotateY(${x}deg) rotateX(${y}deg)`
  };

  lastX.value = x;
  lastY.value = y;
  lastRoll.value = rnd;

  setTimeout(() => {
    let targetIndex = totalSumMassive.value[current_player_index] % 26;
    if (targetIndex < 0) targetIndex += 26;
    moveDot(targetIndex);
  }, 1200);

  result.value = `Выпало: ${rnd}`;
  isSpinDisabled.value = true;
  spinButtonLabel.value = "Крутить";
}


const manualSpin = () => {
  clearTimeout(spinTimer);
  if (players.value[current_player_index].id === store.state.playerID)
    generateAndSpin();
};

function isMyMessage(message) {
  return message.username === store.state.username;
}


const handleUpdateBalance = (newBalance, player_id) => {
  players.value.forEach((element) => {
    if (element.id === player_id) {
      element.balance = newBalance;
    }
  });
};


</script>

<template>
  <Rules v-if="rulesVisible" @close="showRules"/>
<div v-if="isGameEnded" class="modal" style="width: 50%; height: 50%">
  <div class="container" style="width: 100%; height: 100%;">
  <h1 style="margin-top: 30px;">Победитель: игрок {{winner.name}}</h1>
  <h3>Победитель накопил наибольший капитал размером {{winner.balance}}₽</h3>
  <button class="button-33" style="margin-bottom: 30px;" @click="redirectToHome" @mouseenter="makeSound(hoverAudio)">Вернуться в меню</button>
  </div>
</div>
    <div class="overlay" v-if="isGameEnded" @click="redirectToHome" @mouseenter="makeSound(hoverAudio)"></div>
<div class="outer-container">
<div class="transparent-container game-page" style="min-height: 98%; max-height: 98%; min-width: 100%; max-width: 100%; width: 100%;">
  <div class="row" style="height: 100%; width: 100%;">
    <div class="column" style="height: 85%; width: 13%; padding: 5px;">
      <Player v-for="(player, index) in players"
              :ref="(el) => (playerComponent[index] = el)"
             :key="index"
              :name = player.name
              :jobName = player.profession
              :balance = player.balance
              :jobPayment = player.salary
              :av="images[index]"
              :shine="shine[index]"
              :balanceChange="balanceChange[index]"
      />
    </div>
    <div class="column" style="height: 100%; width: 60%; margin-left: 2%; padding: 5px;">
        <button
      class="button-33"
      :hidden="isGameStarted"
      :disabled="!isMyTurn"
      @click="sendStartGame"
        @mouseenter="makeSound(hoverAudio)">
      Начать игру
    </button>
      <div class="container" style="width: 100%; height: 100%; position: relative">
        <img class="image" src="../assets/financity_pole.png" style="width: 100%; height: 100%">
         <img
             v-for="(player, index) in players"
             :key="index"
            :src="images[index]"
            :style="dotStyleMassive[index]"
            alt="dot"
          />
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
    </div>
<!--    <button v-if="isMyTurn" class="button-33" @click="startTurn">Сделать ход</button>-->
    <button
      class="button-33"
      :disabled="!isMyTurn || isSpinDisabled || !isGameStarted || isGameEnded"
      @click="manualSpin">
      {{ spinButtonLabel }}
    </button>
      <Question ref="questionComponent"
                @update-balance="handleUpdateBalance"
                :questionId="modalQuestionId"
                :questionType="modalQuestionType"
                :caseTitle="modalTitle"
                :visible="modalVisible"
                :color="modalColor"
                :isMyTurn="isMyTurn"
                :soundOn="soundOn"
                @setVotingTimer="setVotingTimer"
                @close="closeModal"
                @minus="sendMinus"
                @plus="sendPlus"
                :answerTextVisible="false"/>
    </div>
  <div class="column" style="width: 22%; min-height: 95vh; height: 95%; max-height: 95vh; margin-left: 2%;  padding: 1%;">
    <div class="row buttons">
      <button class="button-33" role="button" @click="leaveCall" @mouseenter="makeSound(hoverAudio)">Выйти из игры</button>
      <button class="button-33" role="button" @click="disableOrEnableSound" @mouseenter="makeSound(hoverAudio)"><img :src="soundButtonLabel" class="sound"></button>
      <button class="button-33" role="button" @click="showRules" @mouseenter="makeSound(hoverAudio)">?</button>
    </div>
    <div class="container" style="padding: 3px; min-height: 82vh; max-height:82%; display:flex; flex-direction:column; align-items:center; justify-content: end; position: relative;">
    <div class="column message-container"
         id="messageContainer"
         ref="chatContainer"
         style="
    -ms-overflow-style: none;
      scrollbar-width: none;
      align-items:center;
      justify-content:center;
      max-height: 58vh;
      height: 88%;
      width: 100%;
      padding: 0px;
      overflow-y: scroll;
      font-size: 12px;
      display: flex;
      flex-direction: column;
      min-width: 90%
      "
    :style="{
      'mask-image': 'linear-gradient(to top, black 0%, black 20%, black 80%, transparent 100%)',
      '-webkit-mask-image': 'linear-gradient(to top, black 0%, black 20%, black 80%, transparent 100%)'
    }">
        <div v-for="message in messages"
             :key="message.id"
             :class="{'my-message': isMyMessage(message), 'other-message': !isMyMessage(message)}"
             class="message">
          <span v-if="!isMyMessage(message)">{{ message.username }}:</span> {{ message.msg }}
      </div>
    </div>
    <input class="input-custom" id="123" v-model="newMessage" style="width: 90%;" @keydown.enter="sendMessage">
    <button class="button-33" role="button" @click="sendMessage" @mouseenter="makeSound(hoverAudio)" style="width: 90%; margin-bottom: 15px;">
      send message
    </button>
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
  box-sizing: border-box;
  padding: 2% 1%;
}

.game-page{
  justify-content: center;
  align-items: center;
}

.column {
  padding: 15px;
}

.row {
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
}

.button-33{
  font-size: 14px;
  margin: 15px 7px;
}
.sound{
  width: 16px;
  height: 16px;
}
@media (max-width: 1200px) {
  .button-33 {
    margin: 10px 4px;
    padding: 5px 13px;
    font-size: 12px;
  }
  .sound{
  width: 14px;
  height: 14px;
}
}

@media (max-width: 900px) {
  .button-33 {
    margin: 7px 3px;
    padding: 3px 10px;
    font-size: 10px;
  }
  .sound{
  width: 12px;
  height: 12px;
}
}

@media (max-width: 770px) {
  .button-33 {
    margin: 5px 3px;
    padding: 3px 8px;
    font-size: 8px;
  }
  .sound{
  width: 10px;
  height: 10px;
}
}

.buttons{
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
    left: 50.7%;
    top: 50%;
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

.games{
  overflow-y: scroll;
  max-height: 45vh;
}

.six {
  border-radius: 10px;
    transform: rotateX(90deg) translateZ(33.33px);
    z-index: 6;
}
.button-33 {
  cursor: pointer;
}

.button-33:disabled {
  cursor: not-allowed;
}

.message {
  word-break: break-word;
  margin: 7px 3px;
  padding: 15px;
  border-radius: 10px;
  max-width: 100%;
  min-width: 100%;
  transition: opacity 0.3s ease;
}

@media (max-width: 1200px) {
  .message {
    margin: 5px 3px;
    padding: 10px;
    font-size:11px;
  }
}

@media (max-width: 900px) {
  .message {
    margin: 5px 3px;
    padding: 8px;
    font-size: 10px;
  }
}

@media (max-width: 770px) {
  .message {
    margin: 4px 3px;
    padding: 7px;
    font-size: 8px;
  }
}

.message-container {
  position: relative;
  overflow-y: scroll;
}

/* Для более плавного эффекта можно добавить псевдоэлемент */
.message-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 33%;
  background: linear-gradient(
    to bottom,
    rgba(255,255,255,1) 0%,
    rgba(255,255,255,0) 100%
  );
  pointer-events: none;
}

.my-message {
  background-color: #d1f7d6;
  align-self: flex-end;
  text-align: right;
  margin-left: auto;
  margin-bottom: 10px;
}

.other-message {
  background-color: #f1f1f1;
  align-self: flex-start;
  text-align: left;
  margin-right: auto;
  margin-bottom: 10px;
}

input,
  .input-custom {
  margin: 15px;
  padding: 10px 20px;
  font-size:15px;
}

@media (max-width: 1200px) {
  input,
  .input-custom {
    margin: 10px 20px;
    padding: 5px 17px;
    font-size:12px;
  }
}

@media (max-width: 900px) {
  input,
  .input-custom {
    margin: 7px 13px;
    padding: 3px 13px;
    font-size: 10px;
  }
}

@media (max-width: 770px) {
  input,
  .input-custom{
    margin: 5px 10px;
    padding: 3px 10px;
    font-size: 9px;
  }
}


@media (max-width: 1200px) {
  h3 {
    font-size: 16px;
  }
}

@media (max-width: 900px) {
  h3 {
    font-size: 14px;
  }
}

@media (max-width: 770px) {
  h3 {
    font-size: 11px;
  }
}

h1 {
  font-weight: bold;
}

@media (max-width: 1200px) {
  h1 {
    font-size: 18px;
  }
}

@media (max-width: 900px) {
  h1 {
    font-size: 15px;
  }
}

@media (max-width: 770px) {
  h1 {
    font-size: 13px;
  }
}

</style>