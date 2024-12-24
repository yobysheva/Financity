<script setup>
// import ChatComponent from "@/views/ChatComponent.vue"
import Player from "@/views/user/Player.vue";
// import Fields from "@/views/Fields.vue";
  import Question from "@/views/Question.vue";
  import Rules from "@/views/children/Rules.vue"
  import Chance from "@/views/children/Chance.vue";
// import QuizQuestion from "@/views/QuizQuestion.vue";
import {ref} from 'vue';
// import { getCurrentInstance } from 'vue';
import {CometChat} from "@cometchat-pro/chat";
import dotImage from '@/assets/dot.png';
const dotSrc = dotImage;

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

let loggedUser = ref({
  username: 'name',
  uid: 0,
});

let callInformation = ref({
      session_id: "",
      receiver_id: null,
      GameCreated: false,
      IsGameRequested: false,
      incomingCall: false,
      ongoingCall: false,
})

let newMessage = ref("")

let rulesVisible = ref(false)

function getLoggedInUser() {
      CometChat.getLoggedinUser().then(
        user => {
          loggedUser.value.username = user.name;
          loggedUser.value.uid = user.uid;
        },
        error => {
          this.$router.push({ name: "homepage" });
          console.log(error);
        }
      );
    }

getLoggedInUser();

function showRules() {
  rulesVisible.value = !rulesVisible.value;
}
//
// if(!props.userType){
  // let sessionID = props.sessionId;

// CometChat.acceptCall(props.sessionId).then(
//         call => {
//           console.log("Call accepted successfully:", call);
//           console.log("call accepted now....");
//           // start the call using the startCall() method
//           console.log(callInformation.value.ongoingCall);
//           CometChat.startCall(
//             call.sessionId,
//             document.getElementById("callScreen"),
//             new CometChat.OngoingCallListener({
//               onUserJoined: user => {
//                 /* Notification received here if another user joins the call. */
//                 console.log("User joined call:", user);
//                 /* this method can be use to display message or perform any actions if someone joining the call */
//               },
//               onUserLeft: user => {
//                 /* Notification received here if another user left the call. */
//                 console.log("User left call:", user);
//                 /* this method can be use to display message or perform any actions if someone leaving the call */
//               },
//               onCallEnded: call => {
//                 /* Notification received here if current ongoing call is ended. */
//                 console.log("Call ended:", call);
//                 callInformation.value.ongoingCall = false;
//                 callInformation.value.incomingCall = false;
//                 /* hiding/closing the call screen can be done here. */
//               }
//             })
//           );
//         },
//         error => {
//           console.log("Call acceptance failed with error", error);
//           // handle exception
//         }
//       );
// } else {
  // let globalContext = callInformation.value;
    var listnerID = loggedUser.value.username;
    CometChat.addCallListener(
      listnerID,
      new CometChat.CallListener({
        onIncomingCallReceived(call) {
          console.log("Incoming call:", call);
          callInformation.value.incomingCall = true;
          callInformation.value.session_id = call.sessionId;
        },

        onOutgoingCallAccepted(call) {
          console.log("Outgoing call accepted:", call);
          callInformation.value.ongoingCall = true;
          CometChat.startCall(
            call.sessionId,
            document.getElementById("callScreen"),
            new CometChat.OngoingCallListener({
              onUserJoined: user => {
                /* Notification received here if another user joins the call. */
                console.log("User joined call:", user);
                /* this method can be use to display message or perform any actions if someone joining the call */
              },
              onUserLeft: user => {
                /* Notification received here if another user left the call. */
                console.log("User left call:", user);
                /* this method can be use to display message or perform any actions if someone leaving the call */
              },
              onCallEnded: call => {
                callInformation.value.ongoingCall = false;
                callInformation.value.incomingCall = false;
                /* Notification received here if current ongoing call is ended. */
                console.log("Call ended:", call);
                /* hiding/closing the call screen can be done here. */
              }
            })
          );
          // Outgoing Call Accepted
        },
        onOutgoingCallRejected(call) {
          console.log("Outgoing call rejected:", call);
          this.incomingCall = false;
          this.ongoingCall = false;
          this.receiver_id = "";
          // Outgoing Call Rejected
        },
        onIncomingCallCancelled(call) {
          console.log("Incoming call calcelled:", call);
        }
      })
    );
// }


function leaveCall() {
  CometChat.endCall(callInformation.value.session_id).then(
      call => {
        console.log('call ended', call);
      }, error => {
        console.log('error', error);
      }
    );
}

let global_id = 0;
const positions = [
  [6.3, 9], [15.3, 9], [26.3, 9], [37.3, 9], [47.3, 9], [56.7, 9], [67.7, 9],
  [78.7, 9], [88.3, 9], [88.3, 23], [88.3, 36], [88.3, 56], [88.3, 69],
  [88.3, 83], [78.7, 83], [67.7, 83], [56.7, 83], [47.3, 83], [37.3, 83],
  [26.3, 83], [15.3, 83], [5.3, 85], [6.3, 69], [6.3, 56], [6.3, 36],
  [6.3, 23]
];

const dotStyle = ref({
  width: "20px",
  height: "20px",
  position: "absolute",
  left: `${positions[0][0]}%`,
  top: `${positions[0][1]}%`,
  transition: "all 0.3s ease"
});

const dotVisible = ref(true);
const result = ref("");
const diceStyle = ref({});
const totalSum = ref(0);
const currentIndex = ref(0);
const lastRoll = ref(null);
const lastX = ref(0);
const lastY = ref(0);

const isSpinDisabled = ref(true);
const spinButtonLabel = ref("Крутить");
let spinTimer = null;

const questions = {
  state: ["Вопрос 1 (Государство)", "Вопрос 2 (Государство)", "Вопрос 3 (Государство)"],
  entertainment: ["Вопрос 1 (Развлечения)", "Вопрос 2 (Развлечения)", "Вопрос 3 (Развлечения)"],
  realEstate: ["Вопрос 1 (Недвижимость)", "Вопрос 2 (Недвижимость)", "Вопрос 3 (Недвижимость)"]
};
const chances = ["chance1", "chance2", "chanse3"]
const modalVisible = ref(false);
const modalTitle = ref("");
const modalQuestion = ref("");
const modalChance = ref("");
const modalChanceVisible = ref(false);

const getRandomQuestion = (category) => {
  const caseQuestions = questions[category];
  return caseQuestions[Math.floor(Math.random() * caseQuestions.length)];
};
const modalColor = ref("")
const checkPositionAndShowModal = (currentCoords) => {
  const stateCoords = [[15.3, 9], [26.3, 9], [37.3, 9], [6.3, 36], [6.3, 23]];
  const entertainmentCoords = [[56.7, 9], [67.7, 9], [78.7, 9], [88.3, 23], [88.3, 36]];
  const realEstateCoords = [[88.3, 56], [88.3, 69], [78.7, 83], [67.7, 83], [56.7, 83]];
  const allCasesCoords = [[37.3, 83], [26.3, 83], [15.3, 83], [6.3, 69], [6.3, 56]];
  const ChanceCoords = [[47.3, 9], [88.3, 9], [88.3, 83], [47.3, 83], [5.3, 85]];
  let category = null;

  if (stateCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    category = "state";
    modalColor.value = "#ADA1F6"; // Фиолетовый
  } else if (entertainmentCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    category = "entertainment";
    modalColor.value = "#FFBBF8"; // Розовый
  } else if (realEstateCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    category = "realEstate";
    modalColor.value = "#C8E3FE"; // Голубой
  } else if (allCasesCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    category = ["state", "entertainment", "realEstate"][Math.floor(Math.random() * 3)];
    modalColor.value = "#E7FC93"; // Желтый
  }else if (ChanceCoords.some(([x, y]) => x === currentCoords[0] && y === currentCoords[1])) {
    modalChance.value = chances[Math.floor(Math.random() * chances.length)];
    setTimeout(() => {
      modalChanceVisible.value = true;
    }, 500);
  }

  if (category) {
    modalTitle.value = `Кейс: ${category === "state" ? "Государство" : category === "entertainment" ? "Развлечения" : "Недвижимость"}`;
    modalQuestion.value = getRandomQuestion(category);
     setTimeout(() => {
          modalVisible.value = true;
        }, 500);
  }
};
const closeModal = () => {
  modalVisible.value = false;
  modalChanceVisible.value = false;
};
const moveDot = (targetIndex) => {
  const steps = [];
  if (targetIndex > currentIndex.value) {
    for (let i = currentIndex.value + 1; i <= targetIndex; i++) {
      steps.push(i);
    }
  } else {
    for (let i = currentIndex.value + 1; i < positions.length; i++) {
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
      dotStyle.value.left = `${leftPercent}%`;
      dotStyle.value.top = `${topPercent}%`;
      currentIndex.value = steps[stepIndex];
      stepIndex++;

      if (stepIndex === steps.length) {
        const [currentX, currentY] = positions[currentIndex.value];
        checkPositionAndShowModal([currentX, currentY]);
      }

      setTimeout(moveNext, 300);
    }
  };

  moveNext();
};


const messages = ref([
])

console.log(window.location.host)
const gameId = new URLSearchParams(window.location.search).get('id');
const chatSocket = new WebSocket(`ws://localhost:8000/ws/chat/${gameId}/`);
chatSocket.onmessage = function (event) {
    let data = JSON.parse(event.data)
    messages.value.push({
      id: global_id += 1,
      player_id: data["player_id"],
      msg: data["message"].toString()
    })

    console.log(messages)
}

function sendMessage() {
    const input = newMessage.value
    newMessage.value = ""
    chatSocket.send(JSON.stringify({
        "message": input,
        "player_id": loggedUser.value.uid
      }))
}


const gameSocket = new WebSocket(`ws://localhost:8000/ws/game/${gameId}/`);
gameSocket.onmessage = (event) => {
    let text_data = JSON.parse(event.data);
    let info = text_data["info"];
    let type = text_data['type'];
    console.log(type)
    switch (type) {
        case "turn":
            console.log("play_turn_animation")
          // eslint-disable-next-line no-case-declarations
            const turn_count = info["turn_count"];
            spin(turn_count);
            break;
    }
    console.log(info);
};

function sendGameInfo(turn_count) {
    const info = {
        "type": "turn",
        "info": {
          "turn_count": turn_count,
          // "player_id": player_id
        }
    }
    gameSocket.send(JSON.stringify(
        info
    ))
}


const generateAndSpin = () => {
  let rnd = Math.floor(Math.random() * 6 + 1);
  totalSum.value += rnd;
  sendGameInfo(rnd)
};
function spin(rnd) {
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
    let targetIndex = totalSum.value % 26;
    if (targetIndex < 0) targetIndex += 26;
    moveDot(targetIndex);
  }, 1200);

  result.value = `Выпало: ${rnd}`;
  isSpinDisabled.value = true;
  spinButtonLabel.value = "Крутить";
}

const manualSpin = () => {
  clearTimeout(spinTimer);
  generateAndSpin();
};

const startTurn = () => {
  isSpinDisabled.value = false;
  spinButtonLabel.value = "Крутить (3 сек)";
  let countdown = 3;

  const updateLabel = () => {
    if (countdown > 0) {
      spinButtonLabel.value = `Крутить (${countdown--} сек)`;
      spinTimer = setTimeout(updateLabel, 1000);
    } else {
      generateAndSpin();
    }
  };

  updateLabel();
};


// getLoggedInUser();
</script>

<template>
<!--  <QuizQuestion/>-->
  <Rules v-if="rulesVisible" @close="showRules"/>
  <Question v-if="questionActive"/>
  <div id="callScreen" style="position: absolute; width: 0px; height: 0px; overflow:hidden;"></div>
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
    <div class="column" style="height: 100%; width: 60%; margin-left: 2%;">
      <div class="container" style="width: 100%; height: 100%; position: relative">
        <img class="image" src="../assets/financity_pole.png" style="width: 100%; height: 100%">
<!--        <Fields/>-->
<!--        <img src="../assets/kletki.svg" style="position:absolute; top: 0px; left: 0px; width: 100%; height: 100%">-->
         <img
            v-if="dotVisible"
            :src="dotSrc"
            :style="dotStyle"
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
    <button class="button-33" @click="startTurn">Сделать ход</button>
    <button
      class="button-33"
      :disabled="isSpinDisabled"
      @click="manualSpin">
      {{ spinButtonLabel }}
    </button>
      <Question :caseTitle= modalTitle  :questionText=modalQuestion :visible="modalVisible" :color="modalColor" @close="closeModal" />
      <Chance  :questionText=modalChance :visible="modalChanceVisible" @close="closeModal" />
    </div>
  <div class="column" style="width: 20%; min-height: 95vh; height: 95%; margin-left: 2%;">
    <div class="row buttons">
      <button class="button-33" role="button" @click="leaveCall">Выйти из игры</button>
      <button class="button-33" role="button" @click="showRules">?</button>
    </div>
    <div class="container" style=" min-height: 80vh; max-height:80%; display:flex; flex-direction:column; align-items:center; justify-content: end; position: relative;">
    <div class="column" id="messageContainer" style="-ms-overflow-style: none;
      scrollbar-width: none; align-items:center; justify-content:center; max-height: 50vh; height: 80%; width: 90%; overflow-y: scroll; display: flex; flex-direction: column;">
      <div v-for="message in messages" v-bind:key="message.id" style=" align-items:center; justify-content:center; word-break: break-word;">
          {{ message.msg }}
      </div>
    </div>
    <input class="input-custom" id="123" v-model="newMessage" style="width: 80%;" @keydown.enter="sendMessage">
    <button class="button-33" role="button" @click="sendMessage" style="width: 80%;">
      send message
    </button>
</div>
    </div>
  </div>
</div>
</div>
  <div id="callScreen" style="position: absolute; width: 0px; height: 0px;"></div>
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
</style>