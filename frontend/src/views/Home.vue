<script>
import Rating from "@/views/children/Rating.vue";
import Profile from "@/views/user/Profile.vue";
import CurrentGames from "@/views/children/CurrentGames.vue";
import RequestGame from "@/views/RequestGame.vue";
import { authService } from "@/services/auth";
import store from "../store.js";
import { CometChat } from "@cometchat-pro/chat";

export default {
  components: {
    Rating,
    Profile,
    CurrentGames,
    RequestGame,
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
      incomingCall: false,
      ongoingCall: false
    };
  },

  created() {
    this.createSocket()
    this.getLoggedInUser();
    let globalContext = this;

    var listnerID = "UNIQUE_LISTENER_ID";
    CometChat.addCallListener(
      listnerID,
      new CometChat.CallListener({
        onIncomingCallReceived(call) {
          console.log("Incoming call:", call);
          globalContext.incomingCall = true;
          globalContext.session_id = call.sessionId;
        },

        onOutgoingCallAccepted(call) {
          console.log("Outgoing call accepted:", call);
          globalContext.ongoingCall = true;
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
                globalContext.ongoingCall = false;
                globalContext.incomingCall = false;
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
  },

  methods: {
    createSocket() {
      this.activeGamesSocket = new WebSocket(`ws://localhost:8000/ws/home/`);
      this.activeGamesSocket.onmessage = (event) => {
        let text_data = JSON.parse(event.data)
        console.log(text_data)
      }
    },

    sendMessageToSocket(gameId, playerId) {
      let data = {
        "player_id": playerId,
        "game_id": gameId
      }
      this.activeGamesSocket.send(
          JSON.stringify(
              data
          )
      )
    },

    getLoggedInUser() {
      CometChat.getLoggedinUser().then(
        cometUser => {
          this.user.username = cometUser.name;
          this.user.uid = cometUser.uid;
        },
        error => {
          // this.$router.push({ name: "login" });
          console.log(error);
        }
      );
    },

    addUserToGroup() {
      if (this.newUser) {
        this.groupUsers.push(this.newUser);
        this.newUser = '';
      }
    },

    makeGroup(gameId) {
      let GUID = gameId;
      let UID = this.user.username;
      console.log(UID);
      let groupName = gameId;
      let groupType = CometChat.GROUP_TYPE.PUBLIC;

      let group = new CometChat.Group(GUID, groupName, groupType);
      let members = [
        new CometChat.GroupMember(UID, CometChat.GROUP_MEMBER_SCOPE.PARTICIPANT)
      ];
      console.log(this.groupUsers)
      for(let user of this.groupUsers){
        members.push(new CometChat.GroupMember(user, CometChat.GROUP_MEMBER_SCOPE.PARTICIPANT))
      }

      return CometChat.createGroupWithMembers(group, members, []).then(
    (response) => {
      console.log("Group created successfully", response);
    },
    (error) => {
      console.log("Some error occurred while creating group", error);
      throw error; // Пробрасываем ошибку для обработки в makeNewGame
    }
  ).finally(() => {
    this.groupUsers = [];
  });
    },

    makeGroupCall(gameId) {
      const receiverID = gameId;
      const callType = CometChat.CALL_TYPE.AUDIO;
      const receiverType = CometChat.RECEIVER_TYPE.GROUP;

      const call = new CometChat.Call(receiverID, callType, receiverType);

      CometChat.initiateCall(call).then(
        (outGoingCall) => {
          console.log("Call initiated successfully:", outGoingCall);
        },
        (error) => {
          console.log("Call initialization failed with exception:", error);
        }
      );
      this.GameCreated = false;
    },

    addUsersToGame() {
      this.GameCreated = true;
    },

    async makeNewGame() {
    try {
    const response = await authService.createGame({
      username: store.state.username,
    });
    console.log(store.state.username, response.status)
    if (response.status === 200) {
      await store.dispatch("updateGameID", response.data.gameId);
      await store.dispatch("updatePlayerID", response.data.playerID);
      this.sendMessageToSocket(response.data.gameId, response.data.playerID)
      this.$router.push({ name: "Game", query: { id: store.state.gameID } });

      const groupId = String(response.data.gameId);

      try {
        await this.makeGroup(groupId);
        this.makeGroupCall(groupId);
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


//       startVideoChat() {
//       if (!this.receiver_id) this.error = true;
//       this.showSpinner = true;
//
//       var receiverID = this.receiver_id;
//       var callType = CometChat.CALL_TYPE.AUDIO;
//       var receiverType = CometChat.RECEIVER_TYPE.USER;
//
//       var call = new CometChat.Call(receiverID, callType, receiverType);
//
//       CometChat.initiateCall(call).then(
//         outGoingCall => {
//           this.showSpinner = false;
//           console.log("Call initiated successfully:", outGoingCall);
//           // perform action on success. Like show your calling screen.
//         },
//         error => {
//           console.log("Call initialization failed with exception:", error);
//         }
//       );
//     },


 acceptCall() {
      let globalContext = this;
      this.ongoingCall = true;
      this.incomingCall = false;
      var sessionID = this.session_id;
      CometChat.acceptCall(sessionID).then(
        call => {
          console.log("Call accepted successfully:", call);
          console.log("call accepted now....");
          // start the call using the startCall() method
          console.log(globalContext.ongoingCall);
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
                /* Notification received here if current ongoing call is ended. */
                console.log("Call ended:", call);
                globalContext.ongoingCall = false;
                globalContext.incomingCall = false;
                /* hiding/closing the call screen can be done here. */
              }
            })
          );
        },
        error => {
          console.log("Call acceptance failed with error", error);
          // handle exception
        }
      );
    },

    rejectCall() {
      var sessionID = this.session_id;
      var globalContext = this;
      var status = CometChat.CALL_STATUS.REJECTED;

      CometChat.rejectCall(sessionID, status).then(
        call => {
          console.log("Call rejected successfully", call);
          globalContext.incomingCall = false;
          globalContext.ongoingCall = false;
          globalContext.receiver_id = "";
        },
        error => {
          console.log("Call rejection failed with error:", error);
        }
      );
    }
  }
};

</script>

<template>
<!--  <AddUsersToGroup v-if="GameCreated" v-bind:group="group"/>-->
  <div class="add-users" v-if="GameCreated">
    <div class="modal" style="top: 35%; width: 50%; height: 60%; overflow: visible; padding: 15px;">
  <div class="container modal-container" style="opacity: 1; width: 100%; min-height: 100%; padding: 15px; align-items: center; justify-content: center;">
    <div class="column">
      <div class="column" style="justify-content: center;">
      <h3 style="width: 80%;">Вы пригласили в игру пользователей:</h3>
          <ul>
          <li v-for="user in  groupUsers" :key="user.id">{{ user }}</li>
          </ul>
    </div>
      <input id="add-user" v-model="newUser" class="input-custom" style="min-height: 20%; width: 80%;" placeholder="Введите уникальный id пользователей, которых хотите пригласить в игру">
    </div>
    <button class="button-33" role="button" @click="addUserToGroup">Пригласить</button>
    <button class="button-33" role="button" @click="makeNewGame">Начать игру</button>
  </div>
</div>
  <div class="overlay"></div>
  </div>
  <RequestGame v-if="IsGameRequested"/>

  <div class="outer-container">
<div class="container home-page" style="min-height: 95%; max-height: 95%;">
    <div class="column" style="width: 70%; height: 98%; max-height: 98%;">
      <Profile/>
      <div class="row game-row">
        <h3>Присоединись к этим играм!</h3>
      </div>
       <div v-if="incomingCall">
          <button class="btn btn-success" @click="acceptCall">Accept Call</button>
          <button class="btn btn-success" @click="rejectCall">Reject Call</button>
        </div>

        <div v-else-if="ongoingCall">
          <button class="btn btn-secondary"> Ongoing Call ... </button>
          <div id="callScreen"></div>
        </div>
      <CurrentGames v-if="!ongoingCall"/>
    </div>
    <div class="column" style="width: 25%; height: 98%; margin: 2.5%;">
      <button class="button-33" role="button" @click="addUsersToGame">Новая игра</button>
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

.column {
  justify-content: space-between;
}

.game-row {
  justify-content: center;
}

h3 {
  font-weight: bold;
}
</style>
