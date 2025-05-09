<script setup>
import {defineProps, defineEmits, onMounted, onUnmounted, defineExpose, computed, watch} from 'vue';
import {ref} from 'vue';
import {authService} from "@/services/auth";
import store from "@/store";
import radioSound from "@/assets/sound/radioBtn.mp3";
import clickSound from "@/assets/sound/click.wav";
import hoverSound from "@/assets/sound/hover2.wav";

const props = defineProps({
  questionId: Number,
  caseTitle: String,
  questionType: Number,
  visible: Boolean,
  color: String,
  isMyTurn: Boolean,
  soundOn: Boolean
});

const isMyTurn = ref(props.isMyTurn);
const questionType = ref(props.questionType);

const emit = defineEmits(['close', 'update-balance', 'plus', 'minus', 'setVotingTimer']);
const answerText = ref("Ваше действие будет иметь последствия");

const close = () => {
  emit('close');
  answerTextVisible.value = false;
};

const handleKeyDown = (event) => {
  if (event.key === 'Escape') {
    close();
  }
};

const radioAudio = new Audio(radioSound);
const clickAudio = new Audio(clickSound);
const hoverAudio = new Audio(hoverSound);
clickAudio.volume = 0.1
hoverAudio.volume = 0.1
radioAudio.volume = 0.6

const buttonClickSound = () => {
  if(props.soundOn){
    clickAudio.play()
  }
}
const buttonHoverSound = () => {
  if(props.soundOn) {
    hoverAudio.play()
  }
}
const radioButtonClickSound = () => {
  if(props.soundOn) {
    radioAudio.play()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});

let answerTextVisible = ref(false);

const modalStyles = computed(() => ({
  top: "35%",
  width: "70%",
  minHeight: "30%",
  maxHeight: "90%",
  height: "80%",
  overflow: "visible",
  position: "fixed",
  left: "50%",
  transform: "translate(-50%, -35%)",
  zIndex: 1000,
  padding: 0,
}));

const containerStyles = computed(() => ({
  backgroundColor: props.color || "white",
  width: "100%",
  height: "100%",
  padding: "16px",
  overflowY: "auto",
 msOverflowStyle: "none",
  scrollbarWidth: "none",
  boxSizing: "border-box",
  position: "relative",
}));

const contentStyles = computed(() => ({
  padding: "16px",
  display: "flex",
  flexDirection: "column",
  justifyContent: "flex-start",
  alignItems: "center",
  gap: "2%",
  width: "100%",
  boxSizing: "border-box",
  position: "relative",
}));


let question = ref({
  text : "",
});

let stopAnswering = ref(false)
let didIVote = ref(false)
let timeBeforeClose = ref(10)
const answers = ref([]);
let votes_pluses = ref(0)
let votes_minuses = ref(0)

function update_variables() {
    didIVote.value = false
    stopAnswering.value = false
    timeBeforeClose.value = 10
}
function vote_minus() {
  buttonClickSound();
    if (stopAnswering.value && !didIVote.value) {
        votes_minuses.value++
        didIVote.value = true
        emit('minus')
    }
}

function vote_plus() {
  buttonClickSound();
    if (stopAnswering.value && !didIVote.value) {
        didIVote.value = true
        emit('plus')
    }
}

function get_votes() {
    return {
        "pluses": votes_pluses.value,
        "minuses": votes_minuses.value
    }
}

onMounted(() => {
  const textarea = document.querySelector('.input-custom');
  const container = document.querySelector('.modal-container');

  if (textarea && container) {
    textarea.addEventListener('input', function () {
      this.style.height = 'auto'; // Сбрасываем высоту текстового поля
      this.style.height = this.scrollHeight + 'px'; // Устанавливаем высоту равной высоте содержимого

      // Увеличиваем высоту контейнера в зависимости от высоты текстового поля
      container.style.minHeight = this.scrollHeight + 140 + 'px'; // Добавьте отступ для упаковки
    });
  }
});

function setTextInTextArea(text) {
  const textarea = document.querySelector('.input-custom');
  if (textarea)
  textarea.value = text
}

function getTextInTextArea() {
  return document.querySelector('.input-custom')?.value
}

function getIdOfActiveRadioButton() {
    let rates = document.getElementsByName('answer');
    if (rates.length === 0) return;
    for(let i = 0; i < rates.length; i++){
        if (rates[i].checked){
            return i
        }
    }
    return -1
}

function setTimerThenClose() {
    stopAnswering.value = true
  if(timeBeforeClose.value === 10) {
    buttonClickSound();
  }
    if (timeBeforeClose.value-- > 0) {
        setTimeout(setTimerThenClose, 1000)
    }
    else {
        stopAnswering.value = false
        timeBeforeClose.value = 10
        close()
    }
}

function setVotingTimer() {
  if(timeBeforeClose.value === 10) {
    buttonClickSound();
  }
    stopAnswering.value = true
    if (timeBeforeClose.value-- > 0) {
        setTimeout(setVotingTimer, 1000)
    }
    else {
        stopAnswering.value = false
        timeBeforeClose.value = 10
    }
}

async function addAnswer() {
  buttonClickSound();
  let rates = document.getElementsByName('answer');
  for (let ans of rates) {
    if (ans.checked) {
      let answerId = ans.value;
      let response = await authService.addActionAnswer(store.state.playerID, answerId);
      answerText.value = response.data['text'];
      answerTextVisible.value = true;
      let newBalance = response.data['balance'];
      emit('update-balance', newBalance, store.state.playerID);
    }
  }
}

function setActiveRadioButtonForId(id) {
  // radioButtonClickSound();
    let rates = document.getElementsByName('answer');
    if (Number(id) === -1 || rates.length === 0) return;
    for(let i = 0; i < rates.length; i++){
        rates[i].checked = false
    }
    rates[id].checked = true
}

let typeEvent = 0
async function getQuestion(id, type) {
  typeEvent = type
  sessionStorage.setItem('typeEvent', typeEvent.toString());
  try {
    if(type === 3){
      const response = await authService.getChance(id);
      question.value.text = response.data['text'];
      sessionStorage.setItem('eventText', response.data['text']);
      return;
    }
    const response = await authService.getQuestion(id);
    question.value.text = response.data['text'];
    sessionStorage.setItem('eventText', response.data['text']);
    // question.value.type = response.data['type'];
    if(type === 2){
      const response1 = await authService.getAnswers(id);
      answers.value = [];
      for(const answer of response1.data){
        answers.value.push(answer);
      }
      sessionStorage.setItem('answerForEvent', JSON.stringify(answers.value));
    }
  } catch (error) {
        console.error(error);
  }
}

let flag = false
if (!question.value.text) {
  flag = true
}

watch(() => props.isMyTurn, (newVal) => {
  isMyTurn.value = newVal;
});
watch(() => props.questionType, (newVal) => {
  questionType.value = newVal;
});

if(flag) {
  isMyTurn.value = sessionStorage.getItem("myTurn") === "true";
  question.value.text = sessionStorage.getItem("eventText");
  questionType.value = parseInt(sessionStorage.getItem("typeEvent"));
  if (questionType.value === 2) {
    answers.value = JSON.parse(sessionStorage.getItem("answerForEvent"));
  }
}



defineExpose({
    getQuestion ,
    setTextInTextArea ,
    getTextInTextArea ,
    getIdOfActiveRadioButton ,
    setActiveRadioButtonForId ,
    get_votes,
    update_variables,
    setVotingTimer
});
</script>

<template>
  <div v-if="visible && !answerTextVisible" class="modal" :style="modalStyles">
    <div class="container modal-container" :style="containerStyles">
      <div class="column" :style="contentStyles">
        <h1 style="margin-bottom: 16px;">{{ caseTitle }}</h1>
        <h3 style="margin-bottom: 16px;">{{ question.text }}</h3>
        <textarea
          v-if="questionType === 1"
          class="input-custom"
          :disabled="!isMyTurn || stopAnswering"
          style="min-height: 120px; height:40%; width: 100%; padding: 40px; margin-bottom: 16px;"
        ></textarea>
        <div v-if="questionType === 2" class="answers" style="justify-content: space-between;">
          <div
            class="radio-container column"
            style="gap:10px; margin-bottom: 8px; align-items: center; -ms-overflow-style: none; scrollbar-width: none;"
          >
            <label v-for="answer in answers"
            :key="answer.id" style="color:black; display: flex; align-items: center;" @click="radioButtonClickSound">
              <input type="radio" name="answer" :value="answer.id" :disabled="!isMyTurn" />
              <div class="radio-custom"></div>
              {{ answer.text }}
            </label>
          </div>
        </div>
        <button v-if="questionType === 2 && isMyTurn"
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="addAnswer"
        @mouseenter="buttonHoverSound"
      >
        Ответить
      </button>
      <button v-if="questionType === 3 && isMyTurn"
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="close"
        @mouseenter="buttonHoverSound"
      >
        Закрыть
      </button>
        <div class="row" v-if="questionType === 1 && !isMyTurn">
          <button
        class="button-33"
        role="button"
        :hidden="didIVote || !stopAnswering"
        style="margin-bottom: 16px;"
        @mouseenter="buttonHoverSound"
        @click="vote_plus"
      >
        +
      </button>
              <button
        class="button-33"
        role="button"
        :hidden="didIVote || !stopAnswering"
        style="margin-bottom: 16px;"
        @mouseenter="buttonHoverSound"
        @click="vote_minus"
      >
        -
      </button>
        </div>
        <button v-if="questionType === 1 && isMyTurn && !stopAnswering"
        class="button-33"
        role="button"
        :hidden="stopAnswering"
        style="margin-bottom: 16px;"
        @click="setTimerThenClose(); emit('setVotingTimer')"
        @mouseenter="buttonHoverSound"
      >
        Ответить
      </button>
        <h3 v-if="questionType === 1 && stopAnswering">{{timeBeforeClose}}</h3>
</div>
    </div>
  </div>
  <div v-if="visible && answerTextVisible" class="modal" :style="modalStyles">
    <div class="container modal-container" :style="containerStyles">
      <div class="column" style="justify-content: center; align-items: center; padding: 5%;" :style="contentStyles">
        <div v-if="questionType === 2">
          <h1>{{ answerText }}</h1>
        </div>
        <button v-if="isMyTurn"
        class="button-33"
        role="button"
        style="margin-bottom: 16px;"
        @click="close"
        @mouseenter="buttonHoverSound"
      >
        Закрыть
      </button>

      </div>
    </div>
  </div>
  <div v-if="visible" class="overlay"></div>
</template>

<style scoped>
.modal{
  opacity: 0.9;
  padding: 5%;
  display: flex;
  align-items: center;
  justify-content: center;
  max-height: 90vh;
  overflow-y: auto;
}

.column{
  align-items: center;
  justify-content: center;
}

.container{
  opacity: 1;
}

.buttons{
  flex-wrap: nowrap;
  align-items: center;
  justify-content: center;
}
h3{
  width: 80%;
}

input[type="radio"] {
    display: none;
}

.radio-container {
    display: flex;
    align-items: center;
    margin: 10px 0;
    cursor: pointer;
}

.radio-custom {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(44, 187, 99);
    border-radius: 10px;
    position: relative;
    margin-right: 10px;
    transition: background-color 0.3s, border-color 0.3s;
    flex-shrink: 0;
}

input[type="radio"]:checked + .radio-custom {
    background-color: rgba(44, 187, 99);
}

.radio-custom::after {
    content: '';
    width: 5px;
    height: 5px;
    background-color: white;
    border-radius: 10px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    transition: transform 0.3s;
}

input[type="radio"]:checked + .radio-custom::after {
    transform: translate(-50%, -50%) scale(1);
}

.radio-custom:hover {
    border-color: rgba(44, 187, 99);
}

input[type="radio"]:checked + .radio-custom:hover {
    background-color: rgba(44, 187, 99);
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

p{
  font-size: 16px;
  margin: 15px;
  @media(max-width: 1200px) {
    font-size: 14px;
    margin: 12px;
  }
  @media(max-width: 900px) {
    font-size: 12px;
    margin: 10px;
  }
  @media(max-width: 770px) {
    font-size: 10px;
    margin: 8px;
  }
  font-weight: bold;
}
</style>