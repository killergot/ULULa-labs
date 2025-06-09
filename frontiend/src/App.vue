<template>
  <div id="app" :class="{ 'menu-collapsed': isCollapsed }">
    <SidebarMenu
      v-if="showSidebar()"
      :collapsed="isCollapsed"
      @toggle="toggleSidebar"
    />


    <div class="content" :style="{ marginLeft: contentMargin(), marginRight: panelMargin() }">
      <router-view />
    </div>


    <ComponentSidebar
      v-if="['main','labWorksPage'].includes($route.name)"
      @toggle-panel="onPanelToggle"
    />
  </div>
</template>

<script>
import SidebarMenu      from './components/SidebarMenu.vue'
import ComponentSidebar from './components/ComponentsSidebar.vue'

export default {
  name: 'App',
  components: { SidebarMenu, ComponentSidebar },
  data() {
    return {
      isCollapsed: false,
      panelCollapsed: true,
      hiddenSidebarRoutes: ['/login']
    }
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    onPanelToggle(collapsed) {
      this.panelCollapsed = collapsed;
    },
    showSidebar() {
      return !this.hiddenSidebarRoutes.includes(this.$route.path);
    },
    contentMargin() {
      if (!this.showSidebar()) return '0px';
      return this.isCollapsed ? '50px' : '200px';
    },
    panelMargin() {
      return this.panelCollapsed ? '0px' : '33.33vw';
    }
  },

  watch: {
    '$route.name'(newVal) {
      if (newVal !== 'main') {
        this.panelCollapsed = true;
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;

  height: 100vh;
  overflow: hidden;
}

.content {
  transition: margin 0.3s ease;
  height: 100%;
  overflow-y: auto;
}
</style>