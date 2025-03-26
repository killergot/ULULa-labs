<template>
  <div class="container">

    <div class="form-wrapper">

      <h1 class="project-name">ULULa</h1>

      <a href="http://127.0.0.1:8000/auth/login_oauth" class="oauth-button">
         Login with OAuth
      </a>

      <form @submit.prevent="handleSubmit">
      <input checked id="signin" name="action" type="radio" value="signin" v-model="action">
      <label for="signin">Sign in</label>
      <input id="signup" name="action" type="radio" value="signup" v-model="action">
      <label for="signup">Sign up</label>
      <input id="reset" name="action" type="radio" value="reset" v-model="action">
      <label for="reset">Reset</label>
      
      <div id="wrapper" :style="{ height: wrapperHeight + 'px' }">
          <div id="arrow" :style="{ left: arrowPosition + 'px' }"></div>
          
          <transition-group name="fade" tag="div" class="input-group">
            <input
              v-if="showEmail" key="email" id="email" placeholder="Email" type="text" v-model="email"
              />

            <input
              v-if="showPassword" key="password" id="pass" placeholder="Password" type="password" v-model="password"
            />

            <input
              v-if="showRepeatPassword" key="repeatPassword" id="repass" placeholder="Repeat password" type="password" v-model="repeatPassword"
            />

            <select
              v-if="showRoleSelect" key="role" v-model="selectedRole" class="role-select"
            >
              <option disabled value="">Select role</option>
              <option v-for="role in roles" :key="role">{{ role }}</option>
            </select>
          </transition-group>
      </div>

      <button type="submit">
          <span :style="{ transform: buttonTextPosition }">
          Reset password
          <br>
          Sign in
          <br>
          Sign up
          </span>
      </button>
      </form>
      <div id="hint">Click on the tabs</div>
  </div>


  <div v-if="showTwoFactor" class="modal-overlay">
    <div class="modal">
      <span class="close-button" @click="cancelTwoFactor">&times;</span>
      <p class="message-text">Enter code, please</p>
      <input type="text" v-model="twoFactorCode" placeholder="123456" maxlength="6"/>
      <button @click="verifyTwoFactorCode">Enter</button>
    </div>
  </div>

  
  <div v-if="showMessage" class="modal-overlay">
      <div class="modal">
        <span class="close-button" @click="closeMessage">&times;</span>
        <p class="message-text">{{ messageText }}</p>
      </div>
    </div>

</div>
</template>


<script>
export default {
data() {
  return {
    action: 'signin',
    email: '',
    password: '',
    repeatPassword: '',
    selectedRole: '',
    roles: ['User', 'Moderator', 'Admin'],
    baseHeights: {
      signin: 178,
      signup: 262 + 82, // + высота селекта
      reset: 94
    },
    arrowPositions: {
      signin: 32,
      signup: 137,
      reset: 404
    },
    showTwoFactor: false,
    twoFactorCode: '',

    showMessage: false,
    messageText: ''
  };
},
computed: {
  showEmail() {
    // Всегда показываем Email, включая режим Reset
    return this.action !== 'invalid_state';
  },
  showPassword() {
    return this.action === 'signin' || this.action === 'signup';
  },
  showRepeatPassword() {
    return this.action === 'signup';
  },
  showRoleSelect() {
    return this.action === 'signup';
  },
  wrapperHeight() {
    let height = this.baseHeights[this.action];
    // Корректировка высоты для Reset
    if (this.action === 'reset') height = 94;
    return height;
  },
    arrowPosition() {
      return this.arrowPositions[this.action];
    },
    buttonTextPosition() {
      const positions = {
        signin: 'translate3d(0,-72px,0)',
        signup: 'translate3d(0,-144px,0)',
        reset: 'translate3d(0,0,0)'
      };
      return positions[this.action];
    }
  },
  methods: {
async handleSubmit() {
  if (this.action === 'signin' && (!this.email || !this.password)) {
    this.messageText = 'The login and password fields should not be empty';
    this.showMessage = true;
    return;
  }

  if (this.action === 'signup' && (!this.email || !this.password || !this.selectedRole)) {
    this.messageText = 'All fields must be filled in';
    this.showMessage = true;
    return;
  }

  if (this.action === 'signup' && this.password !== this.repeatPassword) {
    this.messageText = 'Passwords do not match';
    this.showMessage = true;
    return;
  }

  const formData = {
    action: this.action,
    email: this.email,
    password: this.password,
    ...(this.action === 'signup' && {
      repeatPassword: this.repeatPassword,
      role: this.selectedRole
    })
  };

  console.log('Form submitted:', formData);

  this.isLoading = true;

  try {
    let url = 'http://127.0.0.1:8000/auth';
    let payload = {};
    var response = 0;
    if (this.action === 'signin') {
      url += '/login';
      payload = new URLSearchParams();
      payload.append("username", this.email);
      payload.append("password", this.password);
        response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: payload
      });
    }
    if (this.action === 'signup') {
      url += '/signup';
      payload = {
        email: this.email,
        password: this.password,
        role: this.selectedRole
      };
      response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
  }
    
    const data = await response.json();


    if (response.ok) {
      alert(`Success: ${data.message}`);

      // отображение окна ввода кода двухфакторной аутентификации, надо сделать работу с сервером
      this.showTwoFactor = true;

    } else {
      alert(`Error: ${data.message}`);

    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred while submitting the form.');
  } finally {
    this.isLoading = false;
  }
  },

  // обработка закрытия окна ввода кода двухфакторной аутентификации
  cancelTwoFactor() {
    this.showTwoFactor = false;
    this.twoFactorCode = '';
    this.messageText = 'Two-factor authentication failed';
    this.showMessage = true;
  },

  // проверка кода двухфакторной аутентификации (сделала для примера)
  verifyTwoFactorCode() {
    if (this.twoFactorCode === "123456") {
      this.showTwoFactor = false;
      this.twoFactorCode = '';
      this.messageText = 'Two-factor authentication passed!';
      this.showMessage = true;

    } else {
      this.messageText = 'Invalid code. Try again';
      this.showMessage = true;
    }
  },

  // обработка закрытия окна с сообщением
  closeMessage() {
      this.showMessage = false;
      this.messageText = '';
    }


}
};
</script>


<style scoped>

.container {
  position: relative;
  background-color: #007BA5;
  background-size: cover;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.project-name {
  color: #fff;
  font-size: 72px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
  font-family: 'Raleway', sans-serif;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.input-group {
overflow: hidden;
}

.fade-enter-active, .fade-leave-active {
transition: all 0.5s cubic-bezier(0.6, 0, 0.4, 1);
}

.fade-enter-from, .fade-leave-to {
opacity: 0;
max-height: 0;
margin-bottom: 0;
}

.fade-enter-to, .fade-leave-from {
opacity: 1;
max-height: 72px;
}


/* Обеспечиваем плавность для всех элементов */
#wrapper > * {
transition: 
  opacity 0.5s,
  max-height 0.5s,
  margin-bottom 0.5s;
overflow: hidden;
}

/* Исправляем отображение для Reset */
#reset:checked ~ #wrapper #email {
display: block;
opacity: 1;
}


:focus { outline: none; }
::-webkit-input-placeholder { color: #DEDFDF; }
::-moz-placeholder { color: #DEDFDF; }
:-moz-placeholder { color: #DEDFDF; }
::-ms-input-placeholder { color: #DEDFDF; }

#wrapper {
  transition: all .5s cubic-bezier(.6,0,.4,1);
  overflow: hidden;
}

.role-select {
  background: #fff;
  border: none;
  border-radius: 8px;
  font-size: 27px;
  font-family: 'Raleway', sans-serif;
  height: 72px;
  width: 100%;
  margin-bottom: 10px;
  padding: 0 20px;
  appearance: none;
  color: #555;
}

.role-select:focus {
  outline: 2px solid #079BCF;
  outline-offset: -2px;
}

form {
  transition: all .3s ease;
  width: 450px;
  background: #ffffffcc;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  position: relative;
}


#wrapper, label, #arrow, button span { transition: all .5s cubic-bezier(.6,0,.4,1); }

#wrapper { overflow: hidden; }

#signin:checked ~ #wrapper { height: 178px; }
#signin:checked ~ #wrapper #arrow { left: 32px; }
#signin:checked ~ button span { transform: translate3d(0,-72px,0); }

#signup:checked ~ #wrapper { height: 262px; }
#signup:checked ~ #wrapper #arrow { left: 137px; }
#signup:checked ~ button span { transform: translate3d(0,-144px,0); }

#reset:checked ~ #wrapper { height: 94px; }
#reset:checked ~ #wrapper #arrow { left: 404px; }
#reset:checked ~ button span { transform: translate3d(0,0,0); }

/* Адаптация остальных стилей под динамическую высоту */
#signin:checked ~ #wrapper { height: v-bind(wrapperHeight + 'px'); }
#signup:checked ~ #wrapper { height: v-bind(wrapperHeight + 'px'); }
#reset:checked ~ #wrapper { height: v-bind(wrapperHeight + 'px'); }

input[type=radio] { display: none; }

label {
cursor: pointer;
display: inline-block;
font-size: 22px;
font-weight: 800;
opacity: .5;
margin-bottom: 30px;
text-transform: uppercase;
}
label:hover {
transition: all .3s cubic-bezier(.6,0,.4,1);
opacity: 1;
}
label[for="signin"] { margin-right: 20px; }
label[for="reset"] { float: right; }
input[type=radio]:checked + label { opacity: 1; }

input[type=text],
input[type=password] {
background: #fff;
border: none;
border-radius: 8px;
font-size: 27px;
font-family: 'Raleway', sans-serif;
height: 72px;
width: 99.5%;
margin-bottom: 10px;
opacity: 1;
text-indent: 20px;
transition: all .2s ease-in-out;
}

button {
background: #079BCF;
border: none;
border-radius: 8px;
color: #fff;
cursor: pointer;
font-family: 'Raleway', sans-serif;
font-size: 27px;
height: 72px;
width: 100%;
margin-bottom: 10px;
overflow: hidden;
transition: all .3s cubic-bezier(.6,0,.4,1);
}
button span {
display: block;
line-height: 72px;
position: relative;
top: -2px;
transform: translate3d(0,0,0);
}
button:hover {
background: #007BA5;
}

#arrow {
height: 0;
width: 0;
border-bottom: 10px solid #fff;
border-left: 10px solid transparent;
border-right: 10px solid transparent;
position: relative;
left: 32px;
}

#hint {
width: 100%;
text-align: center;
position: absolute;
bottom: 20px;
color: #fff;
}
.oauth-button {
position: absolute;
top: 20px;
right: 20px;
padding: 10px 20px;
background-color: #4285f4;
color: white;
text-decoration: none;
border-radius: 4px;
font-size: 14px;
transition: all 0.3s ease;
display: flex;
align-items: center;
gap: 8px;
}

.oauth-button:hover {
background-color: #357abd;
box-shadow: 0 2px 4px rgba(0,0,0,0.2);
transform: translateY(-1px);
}

.oauth-button:active {
transform: translateY(0);
}



.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); 
  backdrop-filter: blur(3px); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: #cff0f8;
  border-radius: 8px;
  padding: 20px;
  width: 300px;
  position: relative;
  text-align: center;
  opacity: 1;
}


.modal input[type="text"] {
  background: #fff;
  border: none;
  border-radius: 8px;
  font-size: 27px;
  font-family: 'Raleway', sans-serif;
  height: 72px;
  width: 100%;
  margin-bottom: 10px;
  opacity: 1;
  text-indent: 20px;
  transition: all .2s ease-in-out;
}


.modal button {
  background: #079BCF;
  border: none;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  font-family: 'Raleway', sans-serif;
  font-size: 27px;
  height: 72px;
  width: 100%;
  margin-bottom: 10px;
  overflow: hidden;
  transition: all .3s cubic-bezier(0.6, 0, 0.4, 1);
}

.modal button:hover {
  background: #007BA5;
}


.modal .close-button {
  color: #000000;
  position: absolute;
  top: 1px;
  right: 10px;
  cursor: pointer;
  font-size: 36px;
}



.message-text {
  font-size: 27px;
  font-family: 'Raleway', sans-serif;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: center;
}

</style>