<template>
  <div>
    <transition name="fade" mode="out-in"></transition>
    <Hexagon v-if="loading"></Hexagon>
    <div v-if="!loading">
      <div class="budget">
        <select
          id="mois"
          style="margin-right:10px;height:20px;font-size: 16px;background-color:transparent;"
          v-model="currentMonth"
        >
          <option v-for="month in months" :key="month">{{month}}</option>
        </select>
        <select
          id="annee"
          style="margin-right:20px;height:20px;font-size: 16px;background-color:transparent;"
          v-model="currentYear"
        >
          <option v-for="year in years" :key="year">{{year}}</option>
        </select>
        <a @click="loadMonth(currentMonth, currentYear)" class="btn btn-primary">Go</a>
      </div>
      <div class="budgetBox">
        <div class="budgetItemAuto" v-for="budget in monthBudget" :key="budget.title">
          <h1
            style="text-transform: capitalize;font-size: 22px;margin-top: 10px;margin-bottom: 10px;"
          >{{budget.title}}</h1>
          <h1 style="width:100%; border-bottom:1px solid black;">{{budget.value}}</h1>
          <h3
            style="border-bottom: 1px dotted black;"
          >Dernier mois: {{ getLastMonthResult(budget.title) }}</h3>
          <h3>Tx du mois:</h3>
          <h3 v-for="tx in getMonthTx(budget.title)" :key="tx">{{ tx }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Hexagon } from "vue-loading-spinner";
const axios = require("axios");
axios.defaults.withCredentials = true;
axios.defaults.headers = {
  "Content-Type": "application/json"
};

export default {
  components: {
    Hexagon
  },
  data() {
    return {
      loading: true,
      urlBudget: "",
      budgets: null,
      monthBudget: null,
      mois: "",
      annee: "",
      currentMonth: null,
      currentMonthInt: null,
      currentYear: null,
      months: [
        "janvier",
        "fevrier",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "aout",
        "septembre",
        "octobre",
        "novembre",
        "decembre"
      ],
      years: [],
      semaines: []
    };
  },
  methods: {
    getCurrentMonth() {
      let date = new Date();
      this.currentMonthInt = date.getMonth();
      this.currentMonth = this.months[date.getMonth()];
    },
    getCurrentYear() {
      let date = new Date();
      this.currentYear = date.getFullYear();
      for (let i = 0; i < 3; i++) {
        this.years.push((this.currentYear + i).toString());
      }
    },
    getLastMonthResult(title) {
      for (let i = 0; i < this.budgets["last_month"].length; i++) {
        if (this.budgets["last_month"][i]["title"] == title) {
          return this.budgets["last_month"][i]["value"];
        }
      }
      return 0;
    },
    getMonthTx(title) {
      for (let i = 0; i < this.budgets["tx_month"].length; i++) {
        if (this.budgets["tx_month"][i]["title"] == title) {
          return this.budgets["tx_month"][i]["value"];
        }
      }
      return [0];
    },
    async loadMonth(month, year) {
      this.budgets = await axios.post(this.urlBudget, {
        month: this.months.indexOf(month),
        year: year
      });
      this.budgets = this.budgets.data.message;
      console.log(this.budgets);
      this.monthBudget = this.budgets["month_budget"];
    }
  },
  async mounted() {
    if (window.location.href.includes("localhost")) {
      this.urlBudget = "http://localhost:5000/budget";
    } else if (window.location.href.includes("192.168")) {
      this.urlBudget = "http://192.168.0.127:5000/budget";
    } else {
      this.urlBudget = "https://nos-server.now.sh/budget";
    }
    this.getCurrentMonth();
    this.getCurrentYear();
    this.budgets = await axios.post(this.urlBudget, {
      month: this.currentMonthInt,
      year: this.currentYear
    });
    this.budgets = this.budgets.data.message;
    this.monthBudget = this.budgets["month_budget"];
    this.loading = false;
  }
};
</script>

<style lang='scss'>
.budget {
  select {
    background-color: rgba(255, 255, 255, 0.5) !important;
    color: black;
  }
}
</style>