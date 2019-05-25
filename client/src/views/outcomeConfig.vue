<template>
  <div>
    <transition name="fade" mode="out-in"></transition>
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
          <li v-if="frequence" style="width:100px; padding-bottom: 7px;">
            <datepicker
              v-model="startDate"
              class="fullscreen-when-on-mobile"
              placeholder="Choisir Date"
            ></datepicker>
          </li>
          <li v-if="startDate">
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
          <li v-if="montant" style="float: right;">
            <a @click="add" class="btn btn-success">+</a>
          </li>
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
import Datepicker from "vuejs-datepicker";

export default {
  components: {
    Hexagon,
    Datepicker
  },
  data() {
    return {
      loading: true,
      urlConfig: "",
      frequence: "",
      day: null,
      days: {
        "1": "Dimanche",
        "2": "Lundi",
        "3": "Mardi",
        "4": "Mercredi",
        "5": "Jeudi",
        "6": "Vendredi",
        "7": "Samedi"
      },
      months: {
        Jan: "01",
        Feb: "02",
        Mar: "03",
        Apr: "04",
        May: "05",
        Jun: "06",
        Jul: "07",
        Aug: "08",
        Sep: "09",
        Oct: "10",
        Nov: "11",
        Dec: "12"
      },
      commentaire: "",
      montant: "",
      event: [],
      events: [],
      startEvents: [],
      checkboxDate: false,
      startDate: ""
    };
  },
  methods: {
    add() {
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
      if (this.frequence == "Bi-hebdo" || this.frequence == "Hebdo") {
        this.day = this.startDate.getDay() + 1;
        this.day = this.days[this.day];
      } else {
        this.day = this.startDate.toString().split(" ")[2];
      }
      this.startDate = this.startDate.toString().split(" ");
      this.startDate = [
        this.startDate[3].toString(),
        +this.months[this.startDate[1]],
        +this.startDate[2]
      ];
      this.event = [
        this.events.length,
        this.frequence,
        this.day,
        this.commentaire,
        this.montant,
        this.startDate
      ];
      this.events.push(this.event);
      axios.post(this.urlConfig, {
        type: "add",
        transaction: this.event
      });
    },
    remove(event) {
      let id = this.events.indexOf(event);
      this.events = this.events.filter(function(item) {
        return item !== event;
      });
      axios.post(this.urlConfig, {
        type: "remove",
        transaction: event
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
  }
};
</script>

<style lang="scss">
</style>