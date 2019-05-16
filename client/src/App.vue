<template>
  <div id="app">
    <div class="dark-overlay">
      <div class="toolbar" id="toolbar" v-if="this.$store.state.loggedIn">
        <ul>
          <li class="icon">
            <a href="/#/settings">
              <v-icon :style="{ color: 'white', verticalAlign: 'middle' }">fa fa-cog</v-icon>
            </a>
            <ul>
              <li>
                <a @click="logOut" class="pointer">Quitter</a>
              </li>
            </ul>
          </li>
          <li>
            <a href="/income">Revenus</a>
            <ul>
              <li>
                <a href="/income/passive">Config</a>
              </li>
              <li>
                <a href="/income/ajouter">Ajouter</a>
              </li>
              <li>
                <a href="/income/visuel">Visuel</a>
              </li>
            </ul>
          </li>
          <li>
            <a href="/outcome">Depenses</a>
            <ul>
              <li>
                <a href="/outcome/passive">Config</a>
              </li>
              <li>
                <a href="/outcome/ajouter">Ajouter</a>
              </li>
              <li>
                <a href="/outcome/visuel">Visuel</a>
              </li>
            </ul>
          </li>
          <li>
            <a href="/dettes">Dettes</a>
            <ul>
              <li>
                <a href="/dettes/config">Config</a>
              </li>
              <li>
                <a href="/dettes/ajouter">Ajouter</a>
              </li>
              <li>
                <a href="/dettes/visuel">Visuel</a>
              </li>
            </ul>
          </li>
          <li>
            <a href="/charts">Graphiques</a>
          </li>
          <li class="icon">
            <a>
              <v-icon
                id="toolbarArrow"
                @click="eventToolbar"
                v-if="hideMenu"
                :style="{ color: 'white', verticalAlign: 'middle' }"
              >fa fa-arrow-right</v-icon>
            </a>
            <a>
              <v-icon
                id="toolbarArrow"
                @click="eventToolbar"
                v-if="!hideMenu"
                :style="{ color: 'white', verticalAlign: 'middle' }"
              >fa fa-arrow-left</v-icon>
            </a>
          </li>
        </ul>
      </div>

      <div class="toolbar" id="toolbar" v-if="!this.$store.state.loggedIn">
        <ul>
          <li class="icon">
            <a href="/#/settings">
              <v-icon :style="{ color: 'white', verticalAlign: 'middle' }">fa fa-cog</v-icon>
            </a>
          </li>
          <li>
            <a href="/#/">Budgeteer</a>
          </li>
          <li>
            <a href="/about">A propos</a>
            <ul>
              <li>
                <a href="/aboutMe">Moi</a>
              </li>
              <li>
                <a href="/aboutBudgeteer">Budgeteer</a>
              </li>
            </ul>
          </li>
          <li class="icon">
            <a>
              <v-icon
                id="toolbarArrow"
                @click="eventToolbar"
                v-if="hideMenu"
                :style="{ color: 'white', verticalAlign: 'middle' }"
              >fa fa-arrow-right</v-icon>
            </a>
            <a>
              <v-icon
                id="toolbarArrow"
                @click="eventToolbar"
                v-if="!hideMenu"
                :style="{ color: 'white', verticalAlign: 'middle' }"
              >fa fa-arrow-left</v-icon>
            </a>
          </li>
        </ul>
      </div>

      <div style="clear:both;"></div>
      <div id="routes">
        <transition name="fade" mode="out-in">
          <router-view/>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
const axios = require("axios");
axios.defaults.withCredentials = true;
axios.defaults.headers = {
  "Content-Type": "application/json"
};

export default {
  data() {
    return {
      urlLogin: "",
      urlLogout: "",
      hideMenu: false,
      loggedIn: false,
      background: null
    };
  },
  methods: {
    async checkLogin() {
      let res = await axios.get(this.urlLogin);
      if (res.data.message == "logged in") {
        this.$store.state.loggedIn = true;
        this.$router.push("/account");
      }
    },
    async logOut() {
      let res = await axios.get(this.urlLogout);
      if (res.data.message == "logged out") {
        this.$store.state.loggedIn = false;
        this.$router.push("/");
      }
    },
    eventToolbar(event) {
      let toolbarElement = document.getElementById("toolbar");
      let toolbarArrowElement = document.getElementById("toolbarArrow");
      let screenWidth = window.innerWidth;
      toolbarElement.className = "toolbar";
      let variant = "";
      if (!this.$store.state.loggedIn) variant = "loggedOut";
      if (event.clientX >= 156) {
        if (screenWidth > 939) {
          toolbarElement.classList.add(`slide-left${variant}`);
        }
        if (screenWidth < 939 && screenWidth >= 789) {
          toolbarElement.classList.add(`slide-left${variant}939`);
        }
        if (screenWidth < 789 && screenWidth >= 639) {
          toolbarElement.classList.add(`slide-left${variant}789`);
        }
        if (screenWidth < 639 && screenWidth >= 489) {
          toolbarElement.classList.add(`slide-left${variant}639`);
        }
        if (screenWidth < 489 && screenWidth >= 339) {
          toolbarElement.classList.add(`slide-left${variant}489`);
        }
        toolbarArrowElement.classList.remove("fa-arrow-left");
        toolbarArrowElement.classList.add("fa-arrow-right");
      } else if (event.clientX <= 155) {
        if (screenWidth > 939) {
          toolbarElement.classList.add(`slide-right${variant}`);
        }
        if (screenWidth < 939 && screenWidth >= 789) {
          toolbarElement.classList.add(`slide-right${variant}939`);
        }
        if (screenWidth < 789 && screenWidth >= 639) {
          toolbarElement.classList.add(`slide-right${variant}789`);
        }
        if (screenWidth < 639 && screenWidth >= 489) {
          toolbarElement.classList.add(`slide-right${variant}639`);
        }
        if (screenWidth < 489 && screenWidth >= 339) {
          toolbarElement.classList.add(`slide-right${variant}489`);
        }
        toolbarArrowElement.classList.remove("fa-arrow-right");
        toolbarArrowElement.classList.add("fa-arrow-left");
      }
    }
  },
  mounted() {
    if (window.location.href.includes("localhost")) {
      this.urlLogin = "http://localhost:5000/login";
      this.urlLogout = "http://localhost:5000/logout";
    } else if (window.location.href.includes("192.168")) {
      this.urlLogin = "http://192.168.0.127:5000/login/";
      this.urlLogout = "http://192.168.0.127:5000/logout/";
    } else {
      this.urlLogin = "https://nos-server.now.sh/login/";
      this.urlLogout = "https://nos-server.now.sh/logout/";
    }
    if (!localStorage["background"]) {
      localStorage["background"] = "wallpaper1.jpg";
    }
    this.background = require(`./assets/${localStorage["background"]}`);
    const backgoungElement = document.getElementById("app");
    backgoungElement.style.background = `url(${
      this.background
    }) no-repeat center center/cover`;
    this.checkLogin();
  }
};
</script>

<style lang="css">
@import url("https://fonts.googleapis.com/css?family=Anonymous+Pro");
@import "./css/style.min.css";
@import "../node_modules/animate.css/animate.min.css";
#app {
  font-family: "Anonymous Pro", monospace;
  font-variant: small-caps;
  position: relative;
  height: 100vh;
  width: 100vw;
  /* background: url("./assets/wallpaper1.jpg") no-repeat center center/cover; */
  background-attachment: fixed;
  z-index: 1;
}
</style>
