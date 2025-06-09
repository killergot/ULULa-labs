<template>
  <div>
    <div :class="['panel', { collapsed }]">
      <div class="header">
        <button @click="select('Schedule')">Schedule</button>
        <!-- <button @click="select('Calendar')">Calendar</button> -->
        
        <button v-if="isStudent" @click="select('Materials')">Materials</button>
        
        <button v-if="isTeacher" @click="select('TeacherSubjects')">Subjects</button>

        <button class="toggle" @click="toggle">❯</button>
      </div>
      <div class="body">
        <component :is="currentView"/>
      </div>
    </div>


    <button
      v-if="collapsed"
      class="expand-btn"
      @click="toggle"
      aria-label="Развернуть панель">❮</button>

  </div>
</template>

<script>
import api from '@/services/api';

import Schedule  from './Schedule.vue'
import Calendar  from './Calendar.vue'
import Materials from './Materials.vue'
import TeacherSubjects from './TeacherSubjects.vue'

const TEACHER_ROLE = 1;
const STUDENT_ROLE = 2;

export default {
  name: 'ComponentSidebar',
  components: { Schedule, Calendar, Materials,  TeacherSubjects},
  data() {
    return {
      collapsed: false,
      currentView: 'Schedule',
      userRole: null
    }
  },
  computed: {
    isStudent() {
      return this.userRole & STUDENT_ROLE;
    },
    isTeacher() {
      return this.userRole & TEACHER_ROLE;
    }
  },
  async created() {
    await this.fetchRole();
  },
  mounted() {
    this.$emit('toggle-panel', this.collapsed)
  },
  methods: {
    async fetchRole() {
      try {
        const response = await api.get('/users/get_me');
        if (response.status !== 200) throw new Error(`Error ${response.status}`);
        this.userRole = response.data.role;
      } catch (err) {
        console.error('Failed to fetch role:', err);
      }
    },
    toggle() {
      this.collapsed = !this.collapsed;
      this.$emit('toggle-panel', this.collapsed);
    },
    select(view) {
      if (view === 'Materials' && !this.isStudent) return;
      if (view === 'TeacherSubjects' && !this.isTeacher) return;
      this.currentView = view;
    }
  }
}
</script>

<style scoped>
.panel {
  position: fixed;
  top: 0;
  right: 0;
  display: grid;
  min-width: 400px;
  grid-template-rows: auto 1fr;
  width: 33.33vw;     
  height: 100vh;
  background: #ffffff;
  box-shadow: -2px 0 6px rgba(0,0,0,0.1);
  transform: translateX(0);
  transition: transform 0.3s ease;
  overflow: hidden;
  border-left: 0.5px solid #34495e;
}


.panel.collapsed {
  transform: translateX(100%);
}

.header {
  display: flex;
  align-items: center;
  padding: 8px;
  background: #34495e;

  position: relative;  


  justify-content: center;  

  height: 45px;
}


.panel.collapsed .header button:not(.toggle) {
  display: none;
}


.header .toggle {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  color: #ffffff;
}

.header button:not(.toggle) {
  margin: 0 4px;
  background: #46637f;
  color: #fff;
  border: none;
  padding: 4px 8px;
  border-radius: 5px;
  cursor: pointer;
}

.body {
  padding: 16px;
  overflow-y: auto;
}

.expand-btn {
  position: fixed;
  top: 8px;
  right: 18px;
  width: 32px;
  height: 32px;
  background: #46637f;
  border: none;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  font-size: 1.2em;
  cursor: pointer;
  transition: background 0.2s;
  color: #ffffff;
}

.expand-btn:hover {
  background: #e0e0e0;
}
</style>