<template>
  <div>
    <Hexagon v-if="loading"></Hexagon>
    <div class="configBox">
      <div class="item" v-for="event in events" :key="event[0]">
        <ul style="text-align: center;">
          <li>{{event[1]}}</li>
          <li>{{event[2]}}</li>
          <li>{{event[3]}}</li>
          <li>{{event[4]}}</li>
          <a
            @click="remove(event)"
            class="btn btn-danger"
            style="float: right; margin-top:3px;margin-right: 5px;"
          >-</a>
        </ul>
      </div>
    </div>
    <div v-if="!loading" class="configBox">
      <div class="itemConfig">
        <ul>
          <li>
            <select id="frequence" style="background-color:transparent;" v-model="frequence">
              <option disabled value>Freq.</option>
              <option>Mensuel</option>
              <option>Bi-hebdo</option>
              <option>Hebdo</option>
            </select>
          </li>
          <li v-if="frequence">
            <select
              id="day"
              v-if="frequence == 'Mensuel'"
              v-model="day"
              style="background-color:transparent;"
            >
              <option disabled value>Jour</option>
              <option v-for="number in 31" :key="number">{{number}}</option>
            </select>
            <select
              id="day"
              v-if="frequence == 'Bi-hebdo'"
              v-model="day"
              style="background-color:transparent;"
            >
              <option disabled value>Jour</option>
              <option v-for="number in daysBi" :key="number">{{number}}</option>
            </select>
            <select
              id="day"
              v-if="frequence == 'Hebdo'"
              v-model="day"
              style="background-color:transparent;"
            >
              <option disabled value>Jour</option>
              <option v-for="number in days" :key="number">{{number}}</option>
            </select>
          </li>
          <li v-if="day">
            <input
              id="commentaire"
              type="text"
              v-model="commentaire"
              placeholder="Commentaire"
              style="background-color:transparent; width: 100%;"
            >
          </li>
          <li v-if="commentaire">
            <input
              id="montant"
              style="width: 100%; background-color:transparent;"
              type="text"
              v-model="montant"
              placeholder="Montant"
              onkeypress="return event.charCode == 46 || (event.charCode >= 48 && event.charCode <= 57)"
            >
          </li>
          <a
            v-if="montant"
            @click="add"
            class="btn btn-success"
            style="float: right; margin-top:3px;margin-right: 5px;"
          >+</a>
        </ul>
      </div>
    </div>
    <a v-if="events.toString() != startEvents.toString()" class="btn btn-primary">Sauvergarder</a>
  </div>
</template>

<script>
const axios = require("axios");
axios.defaults.withCredentials = true;
axios.defaults.headers = {
  "Content-Type": "application/json"
};
import { Hexagon } from "vue-loading-spinner";

export default {
  components: {
    Hexagon
  },
  data() {
    return {
      loading: true,
      urlConfig: "",
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
      daysBi: [
        "Dimanche",
        "Lundi",
        "Mardi",
        "Mercredi",
        "Jeudi",
        "Vendredi",
        "Samedi",
        "Dimanche (2)",
        "Lundi (2)",
        "Mardi (2)",
        "Mercredi (2)",
        "Jeudi (2)",
        "Vendredi (2)",
        "Samedi (2)"
      ],
      commentaire: "",
      montant: "",
      events: [],
      startEvents: []
    };
  },
  methods: {
    add() {
      console.log("add");
      let frequenceElement = document.getElementById("frequence");
      if (!this.frequence && frequenceElement) {
        frequenceElement.style.border = "solid 1px red";
        return;
      }
      let dayElement = document.getElementById("day");
      if (!this.day && dayElement) {
        dayElement.style.border = "solid 1px red";
        return;
      }
      let commentaireElement = document.getElementById("commentaire");
      if (!this.commentaire && commentaireElement) {
        commentaireElement.style.border = "solid 1px red";
        return;
      }
      let montantElement = document.getElementById("montant");
      if (!this.montant && montantElement) {
        montantElement.style.border = "solid 1px red";
        return;
      }
      this.events.push([
        this.events.length,
        this.frequence,
        this.day,
        this.commentaire,
        this.montant
      ]);
    },
    remove(event) {
      let id = this.events.indexOf(event);
      this.events = this.events.filter(function(item) {
        return item !== event;
      });
    },
    pushToDb() {
      axios.post(this.urlConfig, {
        transaction: this.events
      });
    }
  },
  async mounted() {
    if (window.location.href.includes("localhost")) {
      this.urlConfig = "http://localhost:5000/config/outcome";
    } else if (window.location.href.includes("192.168")) {
      this.urlConfig = "http://192.168.0.127:5000/config/outcome";
    } else {
      this.urlConfig = "https://nos-server.now.sh/config/outcome";
    }
    this.events = await axios.get(this.urlConfig);
    this.events = this.events.data.message;
    this.startEvents = this.events;
    this.loading = false;
  },
  created() {
    window.addEventListener("keypress", e => {
      if (e.keyCode == 13) this.add();
    });
  },
  beforeRouteUpdate(to, from, next) {
    this.pushToDb();
  },
  beforeDestroy() {
    this.pushToDb();
  }
};
</script>

<style lang="scss">
</style>