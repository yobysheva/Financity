<script>
import Rating from "@/views/children/Rating.vue";
import Profile from "@/views/user/Profile.vue";
// import CurrentGames from "@/views/children/CurrentGames.vue";
import { authService } from "@/services/auth";
import store from "../store.js";
import clickSound from "@/assets/sound/click.wav";
import hoverSound from "@/assets/sound/hover2.wav";
import requestSound from "@/assets/sound/request.wav"
import soundOnImg from "@/assets/sound_on.png";
import soundOfImg from "@/assets/sound_of.png";
import song from "@/assets/sound/menu.mp3"
import {onBeforeUnmount, ref} from "vue";

export default {
  components: {
    Rating,
    Profile,
  },
  setup() {
    const soundOn = ref(true);
      const clickAudio = new Audio(clickSound);
      const hoverAudio = new Audio(hoverSound);
      const requestAudio = new Audio(requestSound);
      const audio = new Audio(song)
      audio.volume = 0.6
      audio.loop = true

      clickAudio.volume = 0.1
      hoverAudio.volume = 0.1
      requestAudio.volume = 0.3

      const buttonClickSound = () => {
        if(soundOn.value){
          clickAudio.play()
        }
      }
      const buttonHoverSound = () => {
        if(soundOn.value) {
          hoverAudio.play()
        }
      }

      const invitationSound = () => {
        if(soundOn.value) {
          requestAudio.play()
        }
      }

      const playMelody = () => {
      if (soundOn.value) {
        audio.play()
      }
    }

      const disableOrEnableSound = () => {
        soundOn.value = !soundOn.value
        buttonClickSound()
        if (soundOn.value) {
          playMelody()
        } else {
          audio.pause()
          audio.currentTime = 0
        }
      }
      playMelody()

    const disableSound = () => {
        soundOn.value = false
        audio.pause()
        audio.currentTime = 0
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

      return {buttonClickSound, buttonHoverSound, invitationSound, disableOrEnableSound, disableSound, soundOn, soundOnImg, soundOfImg}
  },
  data() {
    return {
      user: {
        username: 'name',
        uid: 0,
      },
      activeGamesSocket: false,
      session_id: "",
      receiver_id: null,
      groupUsers: [],
      newUser: '',
      GameCreated: false,
      IsGameRequested: false,
      incomingInvite: false,
      gameId: null,
      activeGame: [],
      senderName: '',
      images: [
        require('@/assets/av1.png'),
        require('@/assets/av2.png'),
        require('@/assets/av3.png'),
        require('@/assets/av4.png'),
        require('@/assets/av5.png'),
        require('@/assets/av6.png'),
      ],
    };
  },
  mounted() {
    window.addEventListener('keydown', this.handleKeyDown);
  },
  created() {
    this.createWaitingRequestSocket()
    this.createActiveGamesSocket()
    this.getLoggedInUser();
    this.getActiveGames();
  },

  methods: {
    createActiveGamesSocket() {
        this.activeGamesSocket = new WebSocket(`ws://localhost:8200/ws/home/`);
        this.activeGamesSocket.onmessage = (event) => {
        let text_data = JSON.parse(event.data)
        this.activeGame.push(text_data)
      }
    },

    sendMessageToActiveGamesSocket(gameId) {
      let data = {
        "game_id": gameId,
        "username": store.state.username,
      }
      this.activeGamesSocket.send(
          JSON.stringify(
              data
          )
      )
    },

    async getActiveGames() {
      try {
        const response = await authService.getActiveGames();
        for(let r in response.data) {
          this.activeGame.push(response.data[r]);
        }
      } catch (error) {
        if (error.response) {
          alert("Login failed: " + error.response.data || "Unknown error");
        } else if (error.request) {
          alert("No response from server. Please try again later.");
        } else {
          alert("Error setting up request: " + error.message);
        }
      }
    },

    createWaitingRequestSocket() {
      let username = store.state.username;
      this.waitingRequestSocket = new WebSocket(`ws://localhost:8200/ws/waiting_request/${username}/`);


      this.waitingRequestSocket.onmessage = async (event) => {
        let data = JSON.parse(event.data);
        if (data.type === "game_invitation") {
          this.invitationSound();
          await store.dispatch("updateGameID", data.game_id);
          this.senderName = data.sender;
          this.incomingInvite = true
        }
      }
      this.waitingRequestSocket.onerror = (error) => {
        console.error("WebSocket error:", error)
      }
    },
    sendWaitingRequestSocket(senderUsername, recipientUsername, gameID) {
      let sendRequestSocket = new WebSocket(`ws://localhost:8200/ws/waiting_request/${recipientUsername}/`);

      sendRequestSocket.onopen = () => {
        let data = {
          "sender": senderUsername,
          "game_id": gameID
        };
        sendRequestSocket.send(JSON.stringify(data));
        setTimeout(() => { sendRequestSocket.close(); }, 1000);
      };

      sendRequestSocket.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    },

    getLoggedInUser() {
      if(!store.state.username) {
        this.$router.push({ name: "login" });
      }
    },

    addUserToGroup() {
      this.buttonClickSound();
      if (this.newUser && this.groupUsers.length < 5) {
        this.groupUsers.push(this.newUser);
        this.newUser = '';
    } else if(this.groupUsers.length >= 5){
        alert('Максимальное число игорков: 6');
      }
    },

    addUsersToGame() {
      this.buttonClickSound();
      this.GameCreated = true;
    },

    sendInvitation(gameID) {
      this.buttonClickSound();
      let senderUser = store.state.username
      for (let user in this.groupUsers) {
        this.sendWaitingRequestSocket(senderUser, this.groupUsers[user], gameID)
      }
    },

    async makeNewGame() {
      this.buttonClickSound();
    try {
    const response = await authService.createGame({
      username: store.state.username,
    });
    if (response.status === 200) {
      await store.dispatch("updateGameID", response.data.gameId);
      await store.dispatch("updatePlayerID", response.data.playerID);
      this.sendMessageToActiveGamesSocket(response.data.gameId, response.data.playerID);
      this.$router.push({ name: "Game", query: { id: store.state.gameID } });
      this.gameId = String(response.data.gameId);
      try {
        this.sendInvitation(this.gameId);
        this.groupUsers = [];
        this.disableSound();
        this.$router.push({ name: "Game", query: { id: response.data.gameId} });
      } catch (error) {
        console.error("Failed to create group or initiate call:", error);
      }
    }
  } catch (error) {
    if (error.response) {
      alert("Login failed: " + error.response.data || "Unknown error");
    } else if (error.request) {
      alert("No response from server. Please try again later.");
    } else {
      alert("Error setting up request: " + error.message);
    }
  }
},
    closeModals() {
      this.buttonClickSound();
      this.GameCreated = false;
    },

    handleKeyDown(event) {
      if (event.key === 'Escape') {
        this.buttonClickSound();
        this.closeModals();
      }
    },

    async joinToGame(gameID) {
      this.buttonClickSound();
      const response = await authService.connectToGame({
        username: store.state.username,
        game_id: gameID,
      });
      if (response.status === 200) {
        await store.dispatch("updateGameID", response.data.gameId);
        await store.dispatch("updatePlayerID", response.data.playerID);
        this.disableSound();
        this.$router.push({name: "Game", query: {id: store.state.gameID}});
      }
    },

    async acceptInvite() {
      this.buttonClickSound();
      const response = await authService.connectToGame({
        username: store.state.username,
        game_id: store.state.gameID,
      });
      if (response.status === 200) {
        await store.dispatch("updatePlayerID", response.data.playerID);
        this.disableSound();
      this.$router.push({name: "Game", query: {id: store.state.gameID}});
      }
    },

    rejectInvite() {
      this.buttonClickSound();
      this.$router.push({ name: "home" });
      this.incomingInvite = false
    }
  }
};

</script>

<template>
  <div class="add-users" v-if="GameCreated">
    <div class="modal" style="top: 35%; min-height: 30%; width: 60%; height: auto;">
  <div class="container modal-container" style="opacity: 1; width: 100%; min-height: 100%; align-items: center; justify-content: center; position: relative;  overflow: auto;">
    <div class="column" style="width: 100%; align-items: center; justify-content: center;">
      <div class="column" style="justify-content: center;">
      <h1 style="text-align: center; margin-bottom: 15px; margin-top: 15px;">Вы пригласили в игру пользователей:</h1>
          <ul style="margin-bottom: 5px;">
          <h3 v-for="user in  groupUsers" :key="user.id">{{ user }}</h3>
          </ul>
    </div>
      <input id="add-user" v-model="newUser" class="input-custom" style="min-height: 20%; width: 80%;" placeholder="Введите уникальный id пользователей, которых хотите пригласить в игру">
    </div>
    <button class="button-33" role="button" @click="addUserToGroup" @mouseenter="buttonHoverSound">Пригласить</button>
    <button class="button-33" role="button" @click="makeNewGame" @mouseenter="buttonHoverSound">Начать игру</button>
  </div>
</div>
    <div v-if="GameCreated" class="overlay" @click="closeModals" id="overlay"></div>
  </div>


  <div class="outer-container">
<div class="container home-page" style="min-height: 95%; max-height: 95%;">
    <div class="column" style="width: 70%; height: 98%; max-height: 98%;">
      <Profile/>
      <div class="row game-row">
        <h3>Присоединись к этим играм!</h3>
      </div>
       <div v-if="incomingInvite">
         <div class="modal" style="top: 35%; width: 60%; min-height: 30%; height: auto; overflow: auto;">
            <div class="container modal-container" style="width: 100%; min-height: 100%; padding: 5%;  align-items: center; justify-content: center;">
                <h1>Приглашение в игру</h1>
                <div class="row" style=" align-items: center; justify-content: center;">
                <h3>{{this.senderName}} приглашает вас присоединиться к игре</h3>
              </div>
                <div class="row" style=" align-items: center; justify-content: center;">
                <button class="button-33" role="button" @click="acceptInvite" @mouseenter="buttonHoverSound">Принять приглашение</button>
                <button class="button-33" role="button" @click="rejectInvite" @mouseenter="buttonHoverSound">Отклонить приглашение</button>
                </div>
            </div>
          </div>
            <div class="overlay"></div>
        </div>


      <div class="container_games" style="overflow-y: scroll; overflow-x: hidden">
        <div v-for="game in this.activeGame"
             :key="game.game_id">
          <div class="row" style="justify-content: flex-start;">
          <div class="row" style="margin-left: 4%; margin-right: 4%;">
            <p>1</p>
            <div class="photo"><img :src="images[game.indexPhoto || 0]" alt="User Photo" /></div>
            </div>
            <div class="row" style="justify-content: space-between; padding: 10px;">
            <p>{{ game.username }}</p>
            <p>Создана игра: {{game.game_id}}</p>
          </div>
            <div style="justify-content: flex-end;">
              <button class="button-33" role="button" @click="joinToGame(game.game_id)" @mouseenter="buttonHoverSound">Присоединиться к игре</button>
            </div>
          </div>            
        </div>
      </div>
    </div>

    <div class="column" style="width: 25%; height: 98%; margin: 2.5%;">
      <div class="row" style="width: 100%; padding: 0px 5%;">
        <button class="button-33" style="flex-grow: 1;" role="button" @click="addUsersToGame" @mouseenter="buttonHoverSound">Новая игра</button>
        <button class="button-33" role="button" @click="disableOrEnableSound" @mouseenter="buttonHoverSound"><img :src="soundOn ? soundOnImg : soundOfImg" class="sound"></button>
      </div>
      <Rating/>
    </div>
  </div>
</div>
</template>

<style scoped>
input {
  margin: 15px 30px;
  padding: 10px 20px;
  font-size:14px;
}
@media (max-width: 1200px) {
  input {
    margin: 10px 26px;
    padding: 5px 17px;
    font-size:12px;
  }
}

@media (max-width: 900px) {
  input {
    margin: 8px 23px;
    padding: 3px 13px;
    font-size: 10px;
  }
}

@media (max-width: 770px) {
  input {
    margin: 5px 19px;
    padding: 3px 10px;
    font-size: 9px;
  }
}
.container_games{
  max-height: 50vh;
  min-height: 50vh;
  @media(max-height: 800px) {
    max-height: 45vh;
    min-height: 45vh;
  }
  @media(max-height: 600px) {
    max-height: 40vh;
    min-height: 40vh;
  }
}

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

.home-page {
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
p{
  font-size: 15px;
  margin: 13px;
  @media(max-width: 1200px) {
    font-size: 12px;
    margin: 8px;
  }
  @media(max-width: 900px) {
    font-size: 10px;
    margin: 6px;
  }
  @media(max-width: 770px) {
    font-size: 8px;
    margin: 4px;
  }
  font-weight: bold;
}

.column {
  justify-content: space-between;
}

.game-row {
  justify-content: center;
}

h3 {
  font-weight: bold;
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

.photo{
  width: 40px;
  height: 40px;
  margin: 10px;
  @media(max-width: 1200px) {
    width: 30px;
    height: 30px;
    margin: 8px;
  }
  @media(max-width: 900px) {
    width: 25px;
    height: 25px;
    margin: 6px;
  }
  @media(max-width: 770px) {
    width: 20px;
    height: 20px;
    margin: 5px;
  }
  background-color: white;
  border-radius: 10px;
  box-shadow: rgba(44, 187, 99, .1) 0 2px 4px, rgba(44, 187, 99, .05) 0 1px 2px;
  color: #333;
  /*font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;*/
  padding: 0;
  font-size: 16px;
  border: 2px solid rgba(44, 187, 99, .3);
  transition: all 250ms;
}

.photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
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

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  display: block;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 5;
}

.photo:hover {
  //background-color: rgba(100, 255, 200, .9);
  outline: none;
  border-color: rgba(44, 187, 99, .6);
  box-shadow: rgba(44, 187, 99, .35) 0 0 5px;
}
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: 5px 5px 5px -5px rgba(34, 60, 80, 0.2) inset;
  background-color: #a0c1c9;
  border-radius: 10px;
  margin-top: 15px;
  margin-bottom: 15px;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background: linear-gradient(180deg, rgba(185, 255, 185, .6), rgba(173, 255, 176, .6));
}

.button-33 {
    margin: 17px 13px;
    padding: 5px 17px;
    font-size: 14px;
}

@media (max-width: 1200px) {
  .button-33 {
    margin: 15px 10px;
    padding: 5px 15px;
    font-size: 12px;
  }
}

@media (max-width: 900px) {
  .button-33 {
    margin: 10px 7px;
    padding: 3px 10px;
    font-size: 10px;
  }
}

@media (max-width: 770px) {
  .button-33 {
    margin: 5px 5px;
    padding: 3px 7px;
    font-size: 8px;
  }
}
.sound{
  width: 16px;
  height: 16px;
}
@media (max-width: 1200px) {
  .sound{
  width: 14px;
  height: 14px;
}
}

@media (max-width: 900px) {
  .sound{
  width: 12px;
  height: 12px;
}
}

@media (max-width: 770px) {
  .sound{
  width: 10px;
  height: 10px;
}
}
</style>
