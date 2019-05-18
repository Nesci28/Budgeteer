<template>
  <div>
    <div class="configBox">
      <div class="item" v-for="event in events" :key="event">
        <ul>
          <li>{{event[0]}}</li>
          <li>{{event[1]}}</li>
          <li>{{event[2]}}</li>
          <li>{{event[3]}}</li>
          <li>
            <a>-</a>
          </li>
        </ul>
      </div>
    </div>
    <div class="configBox">
      <div class="item">
        <ul>
          <li>
            <select v-model="frequence">
              <option disabled value>Frequence</option>
              <option>Mensuel</option>
              <option>Bi-hebdomadaire</option>
              <option>Hebdomadaire</option>
            </select>
          </li>
          <li>
            <select v-if="frequence == 'Mensuel'" v-model="day">
              <option disabled value>Jour</option>
              <option v-for="number in 31" :key="number">{{number}}</option>
            </select>
            <select v-if="frequence == 'Bi-hebdomadaire'" v-model="day">
              <option disabled value>Jour</option>
              <option v-for="number in days" :key="number">{{number}}</option>
            </select>
            <select v-if="frequence == 'Hebdomadaire'" v-model="day">
              <option disabled value>Jour</option>
              <option v-for="number in days" :key="number">{{number}}</option>
            </select>
          </li>
          <li v-if="day">
            <input type="text" v-model="commentaire" alt="Commentaire">
          </li>
          <li v-if="commentaire">
            <input style="width: 75px;" type="number" v-model="montant" alt="Montant">
          </li>
          <li v-if="montant">
            <a class="btn btn-primary">+</a>
          </li>
        </ul>
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
      urlLogin: "",
      errorInfo: false,
      missingInfo: false,
      frequence: "",
      day: null,
      days: [
        "Dimanche",
        "Lundi",
        "Mardi",
        "Mercredi",
        "Jeudi",
        "Vendredi",
        "Samedi"
      ],
      commentaire: "",
      montant: 0,
      events: [
        ["Mensuel", 5, "Assurance Auto", 102.21],
        ["Mensuel", 4, "Internet", 99.54]
      ]
    };
  },
  methods: {
    add() {
      console.log("add");
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
  },
  created() {
    window.addEventListener("keypress", e => {
      if (e.keyCode == 13) this.add();
    });
  }
};
</script>

<style lang="scss">
.addBtn {
  position: relative;
  height: 30px;
  width: 100px;
  left: 50%;
  transform: translate(-50%, 0);
  margin-top: 20px;
  a {
    width: 100% !important;
    height: 100% !important;
    padding-right: 40px;
    padding-left: 40px;
    padding-top: 10px;
    padding-bottom: 10px;
  }
}
.item {
  height: 100%;
  top: 50%;
  ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    // background-color: rgba(255, 255, 255, 0.5);
    height: 100%;
    top: 50%;
  }

  li {
    float: left;
    margin: 10px;
    top: 50%;
    font-size: 18px;
  }

  a {
    padding: 5px;
    border: solid 1px purple;
    background-color: rgba(128, 0, 128, 0.5);
    font-size: 18px;
  }
}
.configBox {
  @media screen and (max-width: 794px) {
    display: inline-block;
  }
  display: flex;
  flex-wrap: wrap;
}
.item {
  flex: 1 0 40%;
  border: solid 3px black;
  background-color: rgba(255, 255, 255, 0.5);
  box-sizing: border-box;
  margin: 20px;
  height: 75px;
}
</style>