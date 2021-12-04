<template>
    <div>
        <div  class="chats">
                <div class="chat" v-for="mess in chats" v-bind:key="mess.id">
                    <h4 @click="openDialog(mess.id)">Chat Name: {{mess.chat_name}}</h4>
                    <h5>Creator: {{mess.creator.username}}</h5>
                </div>
        </div>
            <div>
                <button @click="addChat">Add New Chat</button>
                <button @click="closeChat">Close Current Chat</button>
            </div>
    </div>
</template>

<script>
import $ from 'jquery'
export default {
  name: 'Chat',
  data () {
    return {
      chats: ''
    }
  },
  created () {
    $.ajaxSetup({
      headers: {'Authorization': 'Token ' + sessionStorage.getItem('auth_token')}
    })
    this.loadChat()
  },
  methods: {
    loadChat () {
      $.ajax({
        url: 'http://localhost:8000/chat/',
        type: 'GET',
        success: (response) => {
          this.chats = response.data.data
        }
      })
    },
    openDialog (id) {
    //   this.$router.push({name: 'home', params: {id: id}})
      this.$emit('openDialog', id)
    },
    closeChat () {
      window.location = '/'
    },
    addChat () {
      $.ajax({
        url: 'http://localhost:8000/chat/',
        type: 'POST',
        success: (response) => {
          window.location = '/'
        },
        error: (response) => {
          alert(response.statusText)
        }
      })
    }
  }
}
</script>

<style>
.chats {
    display: flex;
    widows: 50%;
    height: 100%;
}
.chat {
    width: 50%;
    height: 100%;
    border: 1px solid;
}
 h4 {
     cursor: pointer;
 }
</style>
