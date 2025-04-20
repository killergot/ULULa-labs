<template>
  <div id="app" :class="{ 'menu-collapsed': isCollapsed }">
    <SidebarMenu
      v-if="showSidebar()"
      :collapsed="isCollapsed" 
      @toggle="toggleSidebar" />
    <div class="content" :style="{ marginLeft: contentMargin() }">
      <div :class="{ 'content-collapsed': isCollapsed}">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import SidebarMenu from './components/SidebarMenu.vue'

export default {
  name: 'App',
  components: {
    SidebarMenu
  },
  data() {
    return {
      isCollapsed: false,
      hiddenSidebarRoutes: []
    }
  },
  methods: {
    toggleSidebar()  {
      this.isCollapsed = !this.isCollapsed
    },
    showSidebar() {
      return !this.hiddenSidebarRoutes.includes(this.$route.path);
    },
    contentMargin() {
      if (!this.showSidebar()) return '0px'
      return this.isCollapsed ? '50px' : '200px'
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}
.content {
  transition: margin-left 0.3s ease;
}
</style>