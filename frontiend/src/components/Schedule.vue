<template>
    <div class="schedule-wrapper">

      <div class="navigation-box">
        <button @click="prevWeek">❮</button>
        <span class="date-range">{{ dateRange }}</span>
        <button @click="nextWeek">❯</button>
      </div>
  

      <div class="schedule-container">
        <div
          v-for="({ key, label }, idx) in dayList"
          :key="key"
          class="day-box"
        >
          <h3>{{ label }}</h3>
          <ul v-if="processedSchedule[key].length">
            <li
              v-for="(lesson, i) in processedSchedule[key]"
              :key="i"
            >
              {{ lesson.time_start }} - {{ lesson.time_end }} {{ lesson.subject }}
            </li>
          </ul>
          <p v-else class="no-classes">No classes</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import api from '@/services/api';

  const TEACHER_ROLE = 1;
  const STUDENT_ROLE = 2;

  export default {
    name: 'SchedulePage',
    data() {
      return {
        userRole: null,
        weekNumber: 1,
        schedule: {},
        dayList: [
          { key: 'monday', label: 'Mon' },
          { key: 'tuesday', label: 'Tue' },
          { key: 'wednesday', label: 'Wed' },
          { key: 'thursday', label: 'Thu' },
          { key: 'friday', label: 'Fri' },
          { key: 'saturday', label: 'Sat' }
        ]
      }
    },
    computed: {
      processedSchedule() {
        const result = {};
        this.dayList.forEach(({ key }) => {
          const items = this.schedule[key];
          result[key] = Array.isArray(items) ? items.flat() : [];
        });
        return result;
      },
      dateRange() {
        const { date_start: start, date_end: end } = this.schedule;
        return start && end ? `${start} - ${end}` : `Week ${this.weekNumber}`;
      }
    },
    async created() {
      await this.fetchRole();
      await this.fetchSchedule();
    },

    methods: {
      async fetchRole() {
        try {
          const res = await api.get('/users/get_me');
          if (res.status !== 200) throw new Error(`Error ${res.status}`);
          this.userRole = res.data.role;
        } catch (err) {
          console.error('Failed to fetch role:', err);
        }
      },
      async fetchSchedule() {
        try {
          let url = '';
          if (this.userRole === TEACHER_ROLE) {
            url = `/teachers/schedules/${this.weekNumber}`;
          } else {
            url = `/schedule/get_for_current_student/${this.weekNumber}`;
          }

          const response = await api.get(url);
          if (response.status !== 200) throw new Error(`Error ${response.status}`);
          this.schedule = response.data;
        } catch (err) {
          console.error('Failed to fetch schedule:', err);
          this.schedule = {};
        }
      },
      prevWeek() {
        if (this.weekNumber <= 1) {
          alert('This is the first week');
          return;
        }
        this.weekNumber--;
        this.fetchSchedule();
      },
      nextWeek() {
        if (this.weekNumber >= 4) {
          alert('This is the last week');
          return;
        }
        this.weekNumber++;
        this.fetchSchedule();
      }
    },
    mounted() {
      this.fetchSchedule();
    }
  }
  </script>
  
  <style scoped>
  .schedule-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
    /* overflow: hidden; */
    overflow-x: auto;
    min-width: 400px;
  }
  .navigation-box {
    flex: none;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 8px;
    background: #79b9f5;
    border-bottom: 10px solid #ffffff;
  }
  .navigation-box button {
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
  }
  .date-range {
    font-weight: bold;
  }
  .schedule-container {
    flex: 1;
    

    overflow-y: auto;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: auto;
    gap: 16px;
    padding: 16px;
    box-sizing: border-box;
  }

  .day-box {
    background: #f5f5f5;
    border: 1px solid #ddd;
    padding: 12px;
    display: flex;
    flex-direction: column;
  }


  .day-box h3 {
    text-align: center;
    margin: 0 0 8px;
  }
  .day-box ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
    overflow-y: auto;
  }
  .day-box li {
    text-align: left;
    word-break: break-word;
  }
  .no-classes {
    margin: auto;
    text-align: center;
    color: #777777;
  }
  </style>