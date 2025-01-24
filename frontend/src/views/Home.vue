<script>
import Rating from "@/views/children/Rating.vue";
import Profile from "@/views/user/Profile.vue";
import CurrentGames from "@/views/children/CurrentGames.vue";
import { authService } from "@/services/auth";
import store from "../store.js";
import { CometChat } from "@cometchat-pro/chat";

export default {
  components: {
    Rating,
    Profile,
    CurrentGames,
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
      ongoingCall: false,
      gameId: null
    };
  },

  created() {
    this.createWaitingRequestSocket()
    this.createActiveGamesSocket()
    this.getLoggedInUser();
    // let globalContext = this;
    //
    // var listnerID = this.user.username;
    // CometChat.addCallListener(
    //   listnerID,
    //   new CometChat.CallListener({
    //     onIncomingCallReceived(call) {
    //       globalContext.incomingCall = true;
    //       globalContext.session_id = call.sessionId;
    //     },
    //
    //     onOutgoingCallAccepted(call) {
    //       globalContext.ongoingCall = true;
    //       call.setSessionId(this.gameId);
    //       CometChat.startCall(
    //         call.sessionId,
    //         document.getElementById("callScreen"),
    //         new CometChat.OngoingCallListener({
    //           onUserJoined: user => {
    //             /* Notification received here if another user joins the call. */
    //             /* this method can be use to display message or perform any actions if someone joining the call */
    //           },
    //           onUserLeft: user => {
    //             /* Notification received here if another user left the call. */
    //             /* this method can be use to display message or perform any actions if someone leaving the call */
    //           },
    //           onCallEnded: call => {
    //             globalContext.ongoingCall = false;
    //             globalContext.incomingCall = false;
    //             /* Notification received here if current ongoing call is ended. */
    //             /* hiding/closing the call screen can be done here. */
    //           }
    //         })
    //       );
    //       // Outgoing Call Accepted
    //     },
    //     onOutgoingCallRejected(call) {
    //       this.incomingCall = false;
    //       this.ongoingCall = false;
    //       this.receiver_id = "";
    //       // Outgoing Call Rejected
    //     },
    //     onIncomingCallCancelled(call) {
    //     }
    //   })
    // );
  },

  methods: {
    createActiveGamesSocket() {
        this.activeGamesSocket = new WebSocket(`ws://localhost:8000/ws/home/`);
        this.activeGamesSocket.onmessage = (event) => {
        let text_data = JSON.parse(event.data)
        console.log(text_data)
      }
    },

    sendMessageToActiveGamesSocket(gameId, playerId) {
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


    createWaitingRequestSocket() {
      let username = store.state.username;
      this.waitingRequestSocket = new WebSocket(`ws://localhost:8000/ws/waiting_request/${username}/`);


      this.waitingRequestSocket.onmessage = async (event) => {
        let data = JSON.parse(event.data);
        if (data.type === "game_invitation") {
          const response = await authService.connectToGame({
            username: store.state.username,
            game_id: data.game_id,
          });
          alert(`Вас пригласил ${data.sender_id} в игру ${data.game_id}`);
          if (response.status === 200) {
            await store.dispatch("updateGameID", response.data.gameId);
            await store.dispatch("updatePlayerID", response.data.playerID);
          this.$router.push({name: "Game", query: {id: data.game_id}});
        }
      }
      }
      this.waitingRequestSocket.onerror = (error) => {
        console.error("WebSocket error:", error)
      }
    },
    sendWaitingRequestSocket(senderUsername, recipientUsername, gameID) {
      let sendRequestSocket = new WebSocket(`ws://localhost:8000/ws/waiting_request/${recipientUsername}/`);

      sendRequestSocket.onopen = () => {
        let data = {
          "sender_id": senderUsername,
          "game_id": gameID
        };
        sendRequestSocket.send(JSON.stringify(data));
        // sendRequestSocket.close();
      };

      sendRequestSocket.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    },

    getLoggedInUser() {
      if(!store.state.username) {
        this.$router.push({ name: "login" });
        // return;
      }
      // CometChat.getLoggedinUser().then(
      //   cometUser => {
      //     this.user.username = cometUser.name;
      //     this.user.uid = cometUser.uid;
      //   },
      //   error => {
      //     // this.$router.push({ name: "login" });
      //     console.log(error);
      //   }
      // );
    },

    addUserToGroup() {
      if (this.newUser && this.groupUsers.length < 5) {
        this.groupUsers.push(this.newUser);
        this.newUser = '';
    } else if(this.groupUsers.length >= 5){
        alert('Максимальное число игорков: 6');
      }
    },

    makeGroup(gameId) {
      let GUID = gameId;
      let UID = this.user.username;
      let groupName = gameId;
      let groupType = CometChat.GROUP_TYPE.PUBLIC;

      let group = new CometChat.Group(GUID, groupName, groupType);
      let members = [
        new CometChat.GroupMember(UID, CometChat.GROUP_MEMBER_SCOPE.PARTICIPANT)
      ];
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
    // this.groupUsers = [];
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

    sendInvitation(gameID) {
      let senderUser = store.state.username
      for (let user in this.groupUsers) {
        this.sendWaitingRequestSocket(senderUser, this.groupUsers[user], gameID)
      }
    },

    async makeNewGame() {
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
      // const groupId = String(response.data.gameId);

      try {
        // await this.makeGroup(groupId);
        // this.makeGroupCall(groupId);
        this.sendInvitation(this.gameId);
        this.groupUsers = [];
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

    acceptCall() {
      // this.$router.push({ name: "Game", query: { id: groupId} });
      // let globalContext = this;
      // this.ongoingCall = true;
      // this.incomingCall = false;
      // var sessionID = this.session_id;
      // CometChat.acceptCall(sessionID).then(
      //    async call => {
      //     console.log("Call accepted successfully:", call);
      //     let group = call.getCallReceiver();
      //     let groupId = group.getGuid();
      //     const response = await authService.createPlayer({
      //       username: store.state.username,
      //       id: groupId,
      //     });
      //     store.state.playerID = response.data.playerID;
      //     this.$router.push({ name: "Game", query: { id: groupId} });
      //     console.log("call accepted now....");
      //     // start the call using the startCall() method
      //     console.log(globalContext.ongoingCall);
      //     console.log(this.sessionID);
      //     console.log(call.sessionId);
      //     CometChat.startCall(
      //       call.sessionId,
      //       document.getElementById("callScreen"),
      //       new CometChat.OngoingCallListener({
      //         onUserJoined: user => {
      //           /* Notification received here if another user joins the call. */
      //           console.log("User joined call:", user);
      //           /* this method can be use to display message or perform any actions if someone joining the call */
      //         },
      //         onUserLeft: user => {
      //           /* Notification received here if another user left the call. */
      //           console.log("User left call:", user);
      //           /* this method can be use to display message or perform any actions if someone leaving the call */
      //         },
      //         onCallEnded: call => {
      //           /* Notification received here if current ongoing call is ended. */
      //           console.log("Call ended:", call);
      //           globalContext.ongoingCall = false;
      //           globalContext.incomingCall = false;
      //           /* hiding/closing the call screen can be done here. */
      //         }
      //       })
      //     );
      //   },
      //   error => {
      //     console.log("Call acceptance failed with error", error);
      //     // handle exception
      //   }
      // );
    },

    rejectCall() {
      this.$router.push({ name: "home" });
      // var sessionID = this.session_id;
      // var globalContext = this;
      // var status = CometChat.CALL_STATUS.REJECTED;
      //
      // CometChat.rejectCall(sessionID, status).then(
      //   call => {
      //     console.log("Call rejected successfully", call);
      //     globalContext.incomingCall = false;
      //     globalContext.ongoingCall = false;
      //     globalContext.receiver_id = "";
      //   },
      //   error => {
      //     console.log("Call rejection failed with error:", error);
      //   }
      // );
    }
  }
};

</script>

<template>
  <div class="add-users" v-if="GameCreated">
    <div class="modal" style="top: 35%; width: 50%; height: 60%; overflow: visible; padding: 15px;">
  <div class="container modal-container" style="opacity: 1; width: 100%; min-height: 100%; padding: 15px; align-items: center; justify-content: center; position: relative;">
    <div class="column" style="width: 100%; align-items: center; justify-content: center;">
      <div class="column" style="justify-content: center;">
      <h3 style="text-align: center; margin-bottom: 15px; margin-top: 15px;">Вы пригласили в игру пользователей:</h3>
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


  <div class="outer-container">
<div class="container home-page" style="min-height: 95%; max-height: 95%;">
    <div class="column" style="width: 70%; height: 98%; max-height: 98%;">
      <Profile/>
      <div class="row game-row">
        <h3>Присоединись к этим играм!</h3>
      </div>
       <div v-if="incomingCall">
<!--          <button class="btn btn-success" @click="acceptCall">Accept Call</button>-->
<!--          <button class="btn btn-success" @click="rejectCall">Reject Call</button>-->
         <div class="modal" style="top: 35%; width: 60%; min-height: 30%; height: auto; overflow: visible;">
            <div class="container modal-container" style="width: 100%; min-height: 100%; padding: 5%;  align-items: center; justify-content: center;">
                <h3>Приглашение в игру</h3>
                <div class="row" style=" align-items: center; justify-content: center;">
                <p>Вас приглашают присоединиться к игре</p>
              </div>
                <div class="row" style=" align-items: center; justify-content: center;">
                <button class="button-33" role="button" @click="acceptCall">Принять приглашение</button>
                <button class="button-33" role="button" @click="rejectCall">Отклонить приглашение</button>
                </div>
            </div>
          </div>
            <div class="overlay"></div>
        </div>

<!--        <div v-else-if="ongoingCall">-->
<!--          <button class="btn btn-secondary"> Ongoing Call ... </button>-->
<!--        </div>-->

      <CurrentGames/>
      <div id="callScreen" style="position: absolute; width: 0px; height: 0px; overflow:hidden;"></div>
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
