<template>
  <div>
    <input v-model="login" placeholder="Login" type="text"/>
    <input v-model="password" placeholder="Password" type="password"/>
    <button @click="setLogin">Login</button>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  name: 'Login',
  data () {
    return {
      login: '',
      password: ''
    }
  },
  methods: {
    setLogin () {
      $.ajax({
        url: 'http://127.0.0.1:8000/auth/token/login',
        type: 'POST',
        data: {
          username: this.login,
          password: this.password
        },
        success: (response) => {
          alert('Login success')
          sessionStorage.setItem('auth_token', response.data.attributes.auth_token)
          sessionStorage.setItem('username', this.login)
          this.$router.push({name: 'home'})
        },
        error: (response) => {
          if (response.status === 401) {
            alert('Incorrect Login or Password')
          } else if (response.status === 400) {
            alert('Incorrect Login or Password')
          }
        }
      })
    }
  }
}
</script>
