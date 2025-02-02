<script>
import store from "../../store.js";
import {authService} from "@/services/auth";
export default {
  computed: {
    store() {
      return store
    }
  },
  components: {

  },
  data() {
    return {
      usersStats: [],
      images: [
        require('@/assets/av1.png'),
        require('@/assets/av2.png'),
        require('@/assets/av3.png'),
        require('@/assets/av4.png'),
        require('@/assets/av5.png'),
        require('@/assets/av6.png'),
      ],
      interval: null,
    };
  },
  mounted() {
    this.getUsersStats();
  },
  methods: {
    updateUserGames(username, games, wins) {
      console.log(this.usersStats[0], games, wins)
      for (let i = 0; i < this.usersStats[0].length; i++) {
        if (this.usersStats[0][i].username === username) {
          this.usersStats[0][i].winGames = wins
          this.usersStats[0][i].countGames = games
          break
        }
      }
    },
    updateUserPhoto(username, new_photo_index) {
      for (let i = 0; i < this.usersStats[0].length; i++) {
        if (this.usersStats[0][i].username === username) {
          this.usersStats[0][i].indexPhoto = new_photo_index
          break
        }
      }
    },
    async getUsersStats() {
      try {
        const response = await authService.getUsersStats(store.state.username);
        this.usersStats[0] = response.data['user_data'];
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
  }
};
</script>

<template>
  <div class="container rating">
    <h3>Рейтинг</h3>
    <div class ="row" style="justify-content: center" v-for="user in this.usersStats[0]"
         :key="user.index">
      <p>{{ user.index }}</p>
      <div class="photo"><img :src="images[user.indexPhoto || 0]" alt="User Photo" /></div>
      <p><br>{{ user.username }} <br> Выиграно игр: {{user.winGames}}/{{user.countGames}}</p>
    </div>
  </div>
</template>

<style scoped>
.rating{
  overflow-y: scroll;
  height: 70vh;
  position: relative;
}
.row{
  padding: 5px;
}

@media (max-width: 1200px) {
  h3 {
    font-size: 14px;
  }
}

@media (max-width: 900px) {
  h3 {
    font-size: 11px;
  }
}

@media (max-width: 770px) {
  h3 {
    font-size: 9px;
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
  //background-color: rgba(100, 255, 200, .9);
  outline: none;
  border-color: rgba(44, 187, 99, .6);
  box-shadow: rgba(44, 187, 99, .35) 0 0 5px;
}

.photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

p{
  font-size: 14px;
  @media(max-width: 1200px) {
    font-size: 10px;
  }
  @media(max-width: 900px) {
    font-size: 8px;
  }
  @media(max-width: 770px) {
    font-size: 6px;
  }
  font-weight: bold;
}

.pr{
  font-weight: bold;
  text-align: left;
  justify-content: center;
}

</style>