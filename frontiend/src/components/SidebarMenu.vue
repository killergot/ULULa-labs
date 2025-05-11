<template>
    <div class="sidebar" :class="{ collapsed: collapsed }">
    <button @click="$emit('toggle')">
        <span v-if="!collapsed">❮</span>
        <span v-else>❯</span>
      </button> 
      <div v-show="!collapsed">
        <nav class="menu">
            <ul>
            <li v-for="item in pages" :key="item.name">
                <router-link :to="item.link" >{{ item.name }}</router-link>
            </li>
            </ul>
        </nav>
        
        <hr class="divider">

        <div class="folders-section">
            <ul>
                <li v-for="item in folders" :key="item.name" class="folder-item">
                    <span class="folder-icon">📁</span>
                    <span class="folder-name">{{ item.name }}</span>
                </li>
            </ul>
                <button @click="addFolder" class="add-folder-btn">
                    + folder    
                </button>
            </div>
        </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SidebarMenu',
    data() {
      return {
        pages: [
          { name: 'Home', link: '/' },
          { name: 'my profile', link: '/userPage' },
          { name: 'registration', link: '/login' },
          { name: 'test', link: '/test' },
          { name: 'test2', link: '/test2' },
          
        ],
        folders: [
            { name: 'Личные' },
            { name: 'Рабочие' }
        ],
        counter: 1
      }
    },
    props: {
      collapsed: {
        type: Boolean,
        default: false
      }
    },
    methods: {
        addFolder() {
        this.folders.push({
            name: `Новая папка ${this.counter++}`
        })
        }
    }
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

  .divider {
  border: 0;
  border-top: 1px solid #46637f;
  margin: 1rem 0;
}

.folders-section {
  padding: 0 1rem;
}

.folder-item {
  display: flex;
  align-items: center;
  margin: 0.5rem 0;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.folder-item:hover {
  background-color: #40576b;
}

.folder-icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.folder-name {
  font-size: 0.9rem;
}

.add-folder-btn {
  width: 100%;
  padding: 0.5rem;
  margin-top: 1rem;
  background-color: #46637f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-folder-btn:hover {
  background-color: #567892;
}

button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 0.5rem;
}
  </style>