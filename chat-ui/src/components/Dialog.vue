<template>
        <div class="dialog">
            <div class="input">
                <textarea name="inputtext" cols='50' rows='3' v-model="form.textarea"></textarea>
                <div>
                    <input v-model="schedMessMarker" type="checkbox" name="schedMessMarker" id="schedMessMarker">
                    <label for="schedMessMarker">Scheduled Message</label>
                </div>
                <div>
                    <button class="button" type='submit' @click="sendMess">Send Message</button>
                </div>
                <div>
                    <input v-if="sched" v-model="datetime" type="datetime-local">
                </div>
            </div>
            <div >
                <p>Total pages: {{totalPages}}</p>
                <ul class="hr">
                    <li v-for="p in totalPages" v-bind:key="p" @click="changePage(p)">
                        {{p}}
                    </li>
                </ul>
            </div>
            <div>{{status}}</div>
            <div v-for="mess in messages.slice().reverse()" v-bind:key="mess.id">
                <div class="message">
                    <h4>User: {{mess.user.username}}</h4>
                    <p >Date: {{parseDate(mess.date)}}</p>
                    <p >Time: {{parseTime(mess.date)}}</p>
                    <span>Text: {{mess.text}}</span>
                </div>
            </div>
        </div>
</template>

<script>
import $ from 'jquery'
export default {
  name: 'Dialog',
  props: {id: ''},
  data () {
    return {
      status: 'disconect',
      allMessages: [],
      messages: [],
      form: {
        textarea: ''
      },
      scheduledMessage: [],
      schedMessMarker: '',
      datetime: '',
      page: 1,
      total: 0,
      chatSocket: '',
      user: ''
    }
  },
  computed: {
    sched () {
      if (this.schedMessMarker) {
        return true
      }
    },
    totalPages () {
      return Math.ceil(this.allMessages.length / 5)
    }
  },
  created () {
    $.ajaxSetup({
      headers: {'Authorization': 'Token ' + sessionStorage.getItem('auth_token')}
    })
    this.connect()
  },
  methods: {
    connect () {
      this.chatSocket = new WebSocket(
        'ws:' + '127.0.0.1:8000/ws/chat/' + this.id)
      this.chatSocket.onopen = () => {
        this.status = 'connected'
        this.chatSocket.onmessage = (e) => {
          const data = JSON.parse(e.data)
          this.allMessages.push(data.message)
          this.messagesPerPage(this.totalPages)
        }
      }
    },
    changePage (page) {
      this.page = page
      this.messagesPerPage(page)
    },
    messagesPerPage (page) {
      this.messages = this.allMessages.slice(page * 5 - 5, page * 5)
    },
    parseDate (datetime) {
      var newdate = new Date(datetime)
      var date = newdate.toLocaleDateString()
      return date
    },
    parseTime (datetime) {
      var newdate = new Date(datetime)
      var time = newdate.toLocaleTimeString()
      return time
    },
    sendMess () {
      if (this.schedMessMarker) {
        if (this.datetime !== '') {
          if (this.form.textarea === '') {
            alert('Message cant be empty')
          } else {
            alert('Sorry, postponing messages is not available yet')
            // this.chatSocket.send(JSON.stringify({
            //   'chat': this.id, 'text': this.form.textarea, 'token': sessionStorage.getItem('auth_token'), 'datetime': this.datetime
            // }))
            // this.form.textarea = ''
          }
        } else {
          alert('Enter date and time')
        }
      } else {
        if (this.form.textarea === '') {
          alert('Message cant be empty')
        } else {
          this.chatSocket.send(JSON.stringify({
            'chat': this.id, 'text': this.form.textarea, 'token': sessionStorage.getItem('auth_token'), 'datetime': ''
          }))
          this.form.textarea = ''
        }
      }
    }
  }
}
</script>

<style>
    .dialog {
        width: 100%;
        height: 100%;
        border: 1px solid #000;
    }
    .message {
        text-align: left;
        width: 100%;
        height: 100%;
        border: 1px solid #000;
    }
    .button {
        width: 100px;
        height: 30px;
        margin-left: 50px;
    }
    ul.hr {
        margin: 0;
        padding: 4px;
   }
    ul.hr li{
        display: inline-block;
        margin-right: 5px;
        border: 1px solid #000;
        padding: 3px;
        cursor: pointer;
    }
</style>
