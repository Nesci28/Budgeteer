<template>
  <div>
    <Hexagon v-if="loading"></Hexagon>
    <div v-if="!loading" class="calendar">
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
  </div>
</template>

<script>
import { Hexagon } from 'vue-loading-spinner';
import VueCal from 'vue-cal';
import 'vue-cal/dist/vuecal.css';

const axios = require('axios');

axios.defaults.withCredentials = true;
axios.defaults.headers = {
  'Content-Type': 'application/json',
};

export default {
  components: { Hexagon, VueCal },
  data() {
    return {
      loading: true,
      budget: null,
      monthBudget: null,
      events: [],
      months: {
        1: 'janvier',
        2: 'fevrier',
        3: 'mars',
        4: 'avril',
        5: 'mai',
        6: 'juin',
        7: 'juillet',
        8: 'aout',
        9: 'septembre',
        10: 'octobre',
        11: 'novembre',
        12: 'decembre',
      },
    };
  },
  methods: {
    logEvents(event) {
      const year = event.startDate.getFullYear();
      const month = event.startDate.getMonth() + 1;
      this.getMonthBudget(year, month);
    },
    getYear() {
      const today = new Date();
      return today.getFullYear();
    },
    getMonth() {
      const today = new Date();
      return today.getMonth();
    },
    getMonthBudget(year, month) {
      this.events = [];
      const monthToString = this.months[month.toString()];
      this.monthBudget = this.budget[monthToString];
      const days = Object.keys(this.monthBudget);
      days.forEach((day) => {
        const budgetDay = this.monthBudget[day];
        if (budgetDay.length > 0) {
          const budgetDayKeys = Object.keys(budgetDay);
          budgetDayKeys.forEach((tx) => {
            tx = budgetDay[tx];
            console.log(tx);
            if (tx.hasOwnProperty('type')) {
              var moneyClass = 'depense';
            } else if (Object.values(tx)[1] > 0) {
              var moneyClass = 'income';
            } else {
              var moneyClass = 'outcome';
            }
            const value = moneyClass == 'budget'
              ? Object.values(tx)[2]
              : Object.values(tx)[1];
            this.events.push({
              start: `${year}-${month
                .toString()
                .padStart(2, '0')}-${day.padStart(2, '0')}`,
              end: `${year}-${month.toString().padStart(2, '0')}-${day.padStart(
                2,
                '0',
              )}`,
              title:
                `${[...Object.values(tx)[0]].splice(0, 9).join('')} ${value}`,
              content: `${Object.values(tx)[0]} ${value}`,
              class: moneyClass,
            });
          });
        }
      });
      console.log(this.events);
    },
  },
  async mounted() {
    this.urlBudget = `/api/v2/account/${this.getYear()}`;
    this.budget = await axios.get(this.urlBudget);
    this.budget = this.budget.data.message;
    await this.getMonthBudget(this.getYear(), this.getMonth() + 1);
    this.loading = false;
  },
};
</script>

<style lang='scss'>
</style>
