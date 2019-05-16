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
      <h1>Signup</h1>
      <input class="input" v-model="username" type="text" placeholder="Nom de compte">
      <input class="input" v-model="password" type="password" placeholder="Mot de passe">
      <input
        class="input"
        v-model="confirmPassword"
        type="password"
        placeholder="Confirmation du mot de passe"
      >
      <a @click="signup" class="btn btn-primary">Creer</a>
      <h3 style="font-size:20px;margin-top:10px;">
        Tu as deja un compte?
        <router-link class="link" to="/login">Login</router-link>
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
      urlRegister: "",
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
      confirmPassword: ""
    };
  },
  methods: {
    async signup() {
      if (this.password == this.confirmPassword) {
        let res = await axios.post(this.urlRegister, {
          username: this.username,
          password: this.password
        });
        if (res.data.message == "account created") {
          this.$router.push("/login");
        }
      } else {
        console.log("Les mot de passes ne correspondent pas");
      }
    }
  },
  mounted() {
    if (window.location.href.includes("localhost")) {
      this.urlRegister = "http://localhost:5000/register";
    } else if (window.location.href.includes("192.168")) {
      this.urlRegister = "http://192.168.0.127:5000/register/";
    } else {
      this.urlRegister = "https://nos-server.now.sh/register/";
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
  }
};
</script>

<style lang="scss">
@import "../css/style.min.css";
</style>