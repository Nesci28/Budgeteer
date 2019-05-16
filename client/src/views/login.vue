<template>
  <div>
    <v-avatar class="icon" size="110px">
      <v-icon
        size="80px"
        :style="{ color: 'rgb(172, 172, 172)', verticalAlign: 'middle' }"
      >fa fa-user-secret</v-icon>
    </v-avatar>

    <div
      class="box"
      v-bind:class="{ 
          blurWallpaper1: wallpaper1, 
          blurWallpaper2: wallpaper2,
          blurWallpaper3: wallpaper3,
          blurWallpaper4: wallpaper4,
          blurWallpaper5: wallpaper5,
          blurWallpaper6: wallpaper6,
          blurWallpaper7: wallpaper7,
        }"
    >
      <h1>Login</h1>
      <input class="input" v-model="username" type="text" placeholder="Username">
      <input class="input" v-model="password" type="password" placeholder="Password">
      <a @click="login" class="btn btn-primary">Login</a>
      <h3 style="font-size:20px;margin-top:10px;">
        Pas de compte?
        <router-link class="link" to="/signup">Signup</router-link>
      </h3>
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
      background: null,
      wallpaper1: false,
      wallpaper2: false,
      wallpaper3: false,
      wallpaper4: false,
      wallpaper5: false,
      wallpaper6: false,
      wallpaper7: false,
      username: "",
      password: "",
      urlLogin: ""
    };
  },
  methods: {
    async login() {
      if (this.username && this.password) {
        let res = await axios.post(this.urlLogin, {
          username: this.username.toString(),
          password: this.password.toString()
        });
        if (res.data.message == "logged in") {
          this.$store.state.loggedIn = true;
          this.$router.push("/account");
        }
      } else {
        console.log("Informations manquantes dans la forme");
      }
    },
    async checkLogin() {
      let res = await axios.get(this.urlLogin);
      if (res.data.message == "logged in") {
        this.$store.state.loggedIn = true;
        this.$router.push("/account");
      }
    }
  },
  mounted() {
    if (window.location.href.includes("localhost")) {
      this.urlLogin = "http://localhost:5000/login";
    } else if (window.location.href.includes("192.168")) {
      this.urlLogin = "http://192.168.0.127:5000/login/";
    } else {
      this.urlLogin = "https://nos-server.now.sh/login/";
    }
    if (!localStorage["background"]) {
      localStorage["background"] = "wallpaper1.jpg";
    }
    if (
      window.location.hostname == "localhost" ||
      window.location.hostname == "127.0.0.1"
    ) {
      this.isAdmin = true;
    }
    this.background = require(`../assets/${localStorage["background"]}`);
    switch (localStorage["background"]) {
      case "wallpaper1.jpg":
        this.wallpaper1 = true;
        break;
      case "wallpaper2.jpg":
        this.wallpaper2 = true;
        break;
      case "wallpaper3.jpg":
        this.wallpaper3 = true;
        break;
      case "wallpaper4.jpg":
        this.wallpaper4 = true;
        break;
      case "wallpaper5.jpg":
        this.wallpaper5 = true;
        break;
      case "wallpaper6.jpg":
        this.wallpaper6 = true;
        break;
      case "wallpaper7.jpg":
        this.wallpaper7 = true;
        break;
    }
    this.checkLogin();
  }
};
</script>

<style lang="scss">
@import "../css/style.min.css";
</style>