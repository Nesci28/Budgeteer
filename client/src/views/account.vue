<template>
  <div class="calendar">
    <vue-cal
      :disable-views="['years', 'year', 'week', 'day']"
      default-view="month"
      events-on-month-view="short"
      :events="events"
      class="vuecal--blue-theme"
      :todayButton="true"
      @view-change="logEvents($event)"
    ></vue-cal>
  </div>
</template>

<script>
import VueCal from "vue-cal";
import "vue-cal/dist/vuecal.css";
const axios = require("axios");
axios.defaults.withCredentials = true;
axios.defaults.headers = {
  "Content-Type": "application/json"
};

export default {
  components: { VueCal },
  data() {
    return {
      budget: null,
      monthBudget: null,
      events: [],
      months: {
        "1": "janvier",
        "2": "fevrier",
        "3": "mars",
        "4": "avril",
        "5": "mai",
        "6": "juin",
        "7": "juillet",
        "8": "aout",
        "9": "septembre",
        "10": "octobre",
        "11": "novembre",
        "12": "decembre"
      }
    };
  },
  methods: {
    logEvents(event) {
      let year = event.startDate.getFullYear();
      let month = event.startDate.getMonth() + 1;
      this.getMonthBudget(year, month);
    },
    getYear() {
      let today = new Date();
      return today.getFullYear();
    },
    getMonth() {
      let today = new Date();
      return today.getMonth();
    },
    getMonthBudget(year, month) {
      this.events = [];
      let monthToString = this.months[month.toString()];
      this.monthBudget = this.budget[monthToString];
      let days = Object.keys(this.monthBudget);
      days.forEach(day => {
        let budgetDay = this.monthBudget[day];
        if (budgetDay.length > 0) {
          let budgetDayKeys = Object.keys(budgetDay);
          budgetDayKeys.forEach(tx => {
            tx = budgetDay[tx];

            if (Object.values(budgetDay[0])[0] > 0) {
              var moneyClass = "income";
            } else {
              var moneyClass = "outcome";
            }
            this.events.push({
              start: `${year}-${month
                .toString()
                .padStart(2, "0")}-${day.padStart(2, "0")}`,
              end: `${year}-${month.toString().padStart(2, "0")}-${day.padStart(
                2,
                "0"
              )}`,
              title: Object.keys(tx)[0] + " " + Object.values(tx)[0],
              content: Object.values(tx)[0],
              class: moneyClass
            });
          });
        }
      });
      console.log(this.events);
    }
  },
  async mounted() {
    if (window.location.href.includes("localhost")) {
      this.urlBudget = `http://localhost:5000/account/${this.getYear()}`;
    } else if (window.location.href.includes("192.168")) {
      this.urlBudget = `http://192.168.0.127:5000/account/${this.getYear()}`;
    } else {
      this.urlBudget = `https://nos-server.now.sh/login/${this.getYear()}`;
    }
    this.budget = await axios.get(this.urlBudget);
    this.budget = this.budget.data.message;
    this.getMonthBudget(this.getYear(), this.getMonth() + 1);
  }
};
</script>

<style lang='scss'>
</style>