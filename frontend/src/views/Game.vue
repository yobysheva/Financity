<script setup>
// import ChatComponent from "@/views/ChatComponent.vue"
import Player from "@/views/user/Player.vue";
// import Fields from "@/views/Fields.vue";
  import Question from "@/views/Question.vue";
  import Rules from "@/views/children/Rules.vue"
  // import Chance from "@/views/children/Chance.vue";
  import { authService } from "@/services/auth";
// import QuizQuestion from "@/views/QuizQuestion.vue";
import {onMounted, ref} from 'vue';
// import { getCurrentInstance } from 'vue';
import store from "@/store";
import routes from "../router/index.js";

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

// const props = defineProps({
//   id: {
//     type: String,
//     required: true
//   },
//   sessionId: {
//     type: String,
//     required: false
//   },
//   userType: {
//     type: Boolean,
//     required: true
//   }
// });

// let loggedUser = ref({
//   username: 'name',
//   uid: 0,
// });

let players = ref([])
onMounted(() => {
  players.value = []
})
let current_player_index = 0
let shine = ref([])
let isGameStarted = ref(false)
let isGameEnded = ref(false)
let need_to_share_text_answer = false
let need_to_share_radio_button_answer = false
let isMyTurn = ref(false)
let winner = ref(false)

// async function getProfession(){
//   await authService.getRandomProfession(store.state.playerID);
// }
//
// onMounted(() => {
//   getProfession();
// })

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
            shine.value.push(false)
        }
    )
    isMyTurn.value = (players.value.length === 1)
})


let newMessage = ref("")

let rulesVisible = ref(false)

function showRules() {
  rulesVisible.value = !rulesVisible.value;
}

async function sendStartGame() {
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
    modalColor.value = "#ADA1F6"; // Фиолетовый
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
  await questionComponent.value.getQuestion(questionId, questionType)
  setTimeout(() => {
        modalVisible.value = true;
    }, 500);
}

async function endGame () {
    await authService.updateGameStatus({
        "game_id": store.state.gameID,
        "status": "finished"
    })

    winner.value = getWinner()
    isGameEnded.value = true
    console.log(winner.value)
}

function checkToEnd() {
    for (let player in players.value) {
        if (player.balance <= 0) {
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
        console.log(votes.value);
      if(isMyTurn.value){
        const response = await authService.voteHandler(players.value[current_player_index].id, votes.value.pluses, votes.value.minuses);
        players.value[current_player_index].balance = response.data['balance'];
      }
       // вот это не удаляем это прикол реально!
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


const messages = ref([
])

const gameId = new URLSearchParams(window.location.search).get('id');
const chatSocket = new WebSocket(`ws://localhost:8000/ws/chat/${gameId}/`);
chatSocket.onmessage = function (event) {
    let data = JSON.parse(event.data)
    messages.value.push({
      id: global_id += 1,
      username: data["username"],
      msg: data["message"].toString()
    })
}

function sendMessage() {
    const input = newMessage.value
    newMessage.value = ""
    chatSocket.send(JSON.stringify({
        "message": input,
        "username": store.state.username
      }))
}

const answerSocket = new WebSocket(`ws://localhost:8000/ws/game_answer/${gameId}/`);
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
            // eslint-disable-next-line no-case-declarations
            let sa = content['stop_answering'] !== 'false'
            questionComponent.value.setTextInTextArea(text)
            questionComponent.value.set_stop_answering(sa)
            break;
        case 'radio_button_answer':
            if (players[current_player_index] === store.state.playerID) break
            // eslint-disable-next-line no-case-declarations
            let button_id = content['button_id']
            questionComponent.value.setActiveRadioButtonForId(button_id)
            break;
        case 'vote':
            if (players.value[current_player_index].id !== store.state.playerID) {
                break
            }
            // eslint-disable-next-line no-case-declarations
            let type_ = content["vote"]
            votes.value[type_]++
            console.log(votes.value)

    }
}

function textAnswerTranslate() {
    if (!need_to_share_text_answer) return;
    const input1 = questionComponent.value.getTextInTextArea()
    const input2 = questionComponent.value.get_stop_answering()
    answerSocket.send(JSON.stringify({
        "type": "textAnswer",
        "text": input1,
        "stop_answering": input2.toString()
    }))

    setTimeout(
        textAnswerTranslate
    , 1000)
}

function radioButtonAnswerTranslate() {
    if (!need_to_share_radio_button_answer) return;
    const input = questionComponent.value.getIdOfActiveRadioButton()
    answerSocket.send(JSON.stringify({
        "type": "radioButtonAnswer",
        "button_id": input.toString()
    }))

    setTimeout(
        radioButtonAnswerTranslate
    , 1000)
}

function sendPlus() {
    answerSocket.send(JSON.stringify(
        {
          "type": "vote",
          "vote": "pluses"
        }
    ))
}

function sendMinus() {
    answerSocket.send(JSON.stringify(
        {
          "type": "vote",
          "vote": "minuses"
        }
    ))
}

const gameSocket = new WebSocket(`ws://localhost:8000/ws/game/${gameId}/${store.state.playerID}/`);
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
            // totalSum.value += turn_count;
            if(isMyTurn.value && totalSumMassive.value[current_player_index] % 26 + turn_count >= 26){
              const response = await authService.changeBalance(players.value[current_player_index].id);
              players.value[current_player_index].balance = response.data['balance'];
            }
            totalSumMassive.value[current_player_index] += turn_count;
            spin(turn_count);
            break;
        case "on_question_open":
          // eslint-disable-next-line no-case-declarations
            const title = info["title"]
          // eslint-disable-next-line no-case-declarations
            const questionId = info["questionId"]
          // eslint-disable-next-line no-case-declarations
            const questionType = info["questionType"]
            if (players.value[current_player_index].id !== store.state.playerID) {
                openModalWithValues(
                    title, questionId, questionType
                )
            }
            break;
        case "on_question_close":
            if (checkToEnd()) {
                await endGame()
                return
            }

            need_to_share_text_answer = false
            need_to_share_radio_button_answer = false
            players.value[info["player_index"]].balance = info["balance"];
            current_player_index = (current_player_index + 1) % players.value.length;
            players.value.forEach((player, index) => {
              shine.value[index] = player.id === players.value[current_player_index].id;
            });
            // eslint-disable-next-line no-case-declarations
            let scip = true;
            while (scip) {
              // eslint-disable-next-line no-case-declarations
              const response = await authService.checkScip(players.value[current_player_index].id);
              if(response.data['scip']){
                current_player_index = (current_player_index + 1) % players.value.length;
                console.log("scip");
              }
              else{
                scip = false;
              }
            }
            questionComponent.value.update_variables()

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
            break;
        case "start_game":
            startGame()
            break

        case "player_living":
            // eslint-disable-next-line no-case-declarations
            let index = checkPlayerLeave(Number(info['player_id']))
            console.log(index, Number(info['player_id']))
            if (index !== -1) {
              console.log('DELETE')
              players.value.splice(index, 1)
            }
            console.log(players.value)
            break;
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
  const info = {
    "type": "on_question_open",
    "info": {
      "title": modalTitle.value,
      "questionId": modalQuestionId.value,
      "questionType": modalQuestionType.value,
    }
  }
  gameSocket.send(JSON.stringify(
      info
  ))
  if(modalQuestionType.value === 3){
    console.log("chance 3")
    let response = await authService.addActionChance(store.state.playerID, modalQuestionId.value)
    players.value[current_player_index].balance = response.data['balance']
  }
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
      "type": "player_living",
      "info": {
          "player_id": store.state.playerID
      }
  }
  gameSocket.send(JSON.stringify(
        info
    ))
  routes.push({ name: "home" });
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
   // spinButtonLabel.value = "Крутить ХАХАХАХАХ"
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

// const startTurn = () => {
//   isSpinDisabled.value = false;
//   spinButtonLabel.value = "Крутить (3 сек)";
//   let countdown = 3;
//
//   const updateLabel = () => {
//     if (countdown > 0) {
//       spinButtonLabel.value = `Крутить (${countdown--} сек)`;
//       spinTimer = setTimeout(updateLabel, 1000);
//     } else {
//       if (players.value[current_player_index].id === store.state.playerID)
//       generateAndSpin();
//     }
//   };
//
//   updateLabel();
// };


// getLoggedInUser();
</script>

<template>
<!--  <QuizQuestion/>-->
  <Rules v-if="rulesVisible" @close="showRules"/>
<!--  <Question v-if="questionActive"/>-->
<div v-if="!isGameEnded" class="modal" style="width: 100%; height: 100%">
  {{winner.id}}
  {{winner.balance}}
</div>
<div class="outer-container">
<div class="transparent-container game-page" style="min-height: 98%; max-height: 98%; min-width: 100%; max-width: 100%; width: 100%;">
  <div class="row" style="height: 100%; width: 100%;">
    <div class="column" style="height: 85%; width: 13%; padding: 5px;">
      <Player v-for="(player, index) in players"
             :key="index"
              :name = player.name
              :jobName = player.profession
              :balance = player.balance
              :jobPayment = player.salary
              :av="images[index]"
              :shine="shine[index]"
      />
    </div>
    <div class="column" style="height: 100%; width: 60%; margin-left: 2%; padding: 5px;">
        <button
      class="button-33"
      :hidden="isGameStarted"
      :disabled="!isMyTurn"
      @click="sendStartGame">
      Начать игру
    </button>
      <div class="container" style="width: 100%; height: 100%; position: relative">
        <img class="image" src="../assets/financity_pole.png" style="width: 100%; height: 100%">
<!--        <Fields/>-->
<!--        <img src="../assets/kletki.svg" style="position:absolute; top: 0px; left: 0px; width: 100%; height: 100%">-->
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
      <Question ref="questionComponent" @update-balance="handleUpdateBalance" :questionId="modalQuestionId" :questionType="modalQuestionType" :caseTitle="modalTitle" :visible="modalVisible" :color="modalColor" :isMyTurn="isMyTurn" @close="closeModal" @minus="sendMinus" @plus="sendPlus" :answerTextVisible="false"/>
    </div>
  <div class="column" style="width: 22%; min-height: 95vh; height: 95%; margin-left: 2%;">
    <div class="row buttons">
      <button class="button-33" role="button" @click="leaveCall">Выйти из игры</button>
      <button class="button-33" role="button" @click="showRules">?</button>
    </div>
    <div class="container" style="padding: 5px; min-height: 82vh; max-height:82%; display:flex; flex-direction:column; align-items:center; justify-content: end; position: relative;">
    <div class="column message-container" id="messageContainer" style="
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
      "
    :style="{
      'mask-image': 'linear-gradient(to top, black 0%, black 20%, black 80%, transparent 100%)',
      '-webkit-mask-image': 'linear-gradient(to top, black 0%, black 20%, black 80%, transparent 100%)'
    }">
      <div style = "min-width: 90%">
        <div v-for="message in messages"
             :key="message.id"
             :class="{'my-message': isMyMessage(message), 'other-message': !isMyMessage(message)}"
             class="message">
          {{ message.username }}: {{ message.msg }}
        </div>
      </div>
    </div>
    <input class="input-custom" id="123" v-model="newMessage" style="width: 90%;" @keydown.enter="sendMessage">
    <button class="button-33" role="button" @click="sendMessage" style="width: 90%; margin-bottom: 15px;">
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
  margin: 10px;
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
  margin: 15px 0;
  padding: 15px;
  border-radius: 10px;
  max-width: 100%;
  min-width: 100%;
  transition: opacity 0.3s ease;
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


</style>