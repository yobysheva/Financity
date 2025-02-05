<template>

  <div id="app">
    <router-view/>
  </div>
</template>


<script>
import { CometChat } from "@cometchat-pro/chat";

import "./App.css";

export default {
  data() {
    return {};
  },
  created() {
    this.initializeApp();
  },
  methods: {
    initializeApp() {

    }
  }
};
</script>