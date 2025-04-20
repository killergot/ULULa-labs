<template>
    <div class="sidebar" :class="{ collapsed: collapsed }">
    <button @click="$emit('toggle')">
        <span v-if="!collapsed">❮</span>
        <span v-else>❯</span>
      </button>
      <nav v-show="!collapsed" class="menu">
        <ul>
          <li v-for="item in items" :key="item.name">
            <router-link :to="item.link" >{{ item.name }}</router-link>
          </li>
        </ul>
      </nav>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SidebarMenu',
    data() {
      return {
        items: [
          { name: 'Home', link: '/' },
          { name: 'Profile', link: '/test' },
          { name: 'test2', link: '/test2' }
        ]
      }
    },
    props: {
      collapsed: {
        type: Boolean,
        default: false
      }
    },
  }
  </script>
  
  <style scoped>
  .sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  padding-top: 60px;
  left: 0;
  width: 200px;
  height: 100vh;
  background-color: #34495e;
  color: white;
  transition: width 0.3s ease;
  z-index: 1000;
}
  .sidebar.collapsed {
    width: 50px;
  }
  .toggle-btn {
    background: none;
    border: none;
    color: inherit;
    font-size: 1.2rem;
    padding: 1rem;
    cursor: pointer;
  }
  .menu {
    margin-top: 2rem;
  }
  .menu ul {
    list-style: none;
    padding: 0;
  }
  .menu li {
    margin: 1rem 0;
  }
  .menu a {
    color: inherit;
    text-decoration: none;
  }
  </style>