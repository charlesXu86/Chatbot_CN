<template>
   <div class="chat-room">
    <div class="chat-header">
      <mu-appbar title='聊天'>
        <mu-icon-button icon="chevron_left" slot="left" @click="goback" />
        <mu-icon-button icon="expand_more" slot="right"/>
      </mu-appbar>
    </div>
    <!-- 聊天内容区域 -->
    <div class="chat-content">
      <div v-for="obj in getMsgHistoryInfo" :key="obj.id">
        <other-msg v-if="obj.username!=name" :name="obj.username" :msg="obj.msg"
                  :avatar="avatar" :mytime="obj.gentime">
        </other-msg>
        <my-msg v-if="obj.username==name" :name="obj.username" :msg="obj.msg"
                :avatar="avatar" :mytime="obj.gentime">
        </my-msg>
      </div>
      <div v-for="obj in getInfo" :key="obj.id">
        <other-msg v-if="obj.username!=name" :name="obj.username" :msg="obj.msg"
                  :avatar="avatar" :mytime="obj.gentime">
        </other-msg>
        <my-msg v-if="obj.username==name" :name="obj.username" :msg="obj.msg"
                :avatar="avatar" :mytime="obj.gentime">
        </my-msg>
      </div>
    </div>
    <!-- 输入区域 -->
    <div class="bottom">
      <div class="chat-input">
        <div class="msg-input" @keyup.enter="send">
          <input type="text" v-model="chatMsg">
        </div>
        <mu-raised-button label='发送' class="send-button" primary fullWidth backgroundColor='grey900' @click="send" />
      </div>
    </div>
  </div>
</template>

<script>
import faker from 'faker'
import { mapGetters } from 'vuex'
import MyMsg from '../../components/myMsg'
import OtherMsg from '../../components/otherMsg'
import { getUserName } from '@/utils/localStorage'

export default{
  data () {
    return {
      name: '',
      chatMsg: '',
      container: {},
      avatar: faker.image.avatar()
    }
  },
  created () {
    const username = getUserName()
    if (!username) {
      // 防止未登录
      this.$router.push({path: '/login'})
    }
    this.name = username
    this.$store.dispatch('SetWebSocket', new WebSocket('ws://localhost:9090/chat/'))
  },
  mounted () {
    this.container = document.querySelector('.chat-content')
    const that = this
    // 初始化新的对话信息
    this.$store.dispatch('SetChatMsg')
    // 加载历史对话信息
    this.$store.dispatch('GetMessHistory')
    // 自动滚动到底部
    setTimeout(() => {
      this.$nextTick(() => {
        this.container.scrollTop = 10000
      })
    }, 1000)
    this.getSocket.onmessage = (message) => {
      let receivedMsg = JSON.parse(message.data)
      console.log(receivedMsg)
      const now = new Date()
      const msgData = {
        'username': receivedMsg.username,
        'msg': receivedMsg.msg,
        'gentime': now.toISOString()
      }
      that.$store.dispatch('AddChatMsg', msgData)
    }
  },
  methods: {
    goback () {
      // 返回时断开连接
      this.$store.dispatch('SetWebSocket', null)
      this.$router.goBack()
    },
    send () {
      const now = new Date()
      const msgData = {
        'username': this.name,
        'msg': this.chatMsg,
        'gentime': now.toISOString()
      }
      this.$store.dispatch('AddMessHistory', msgData)
      this.getSocket.send(JSON.stringify(msgData))
      this.chatMsg = ''
    },
    scrollToBottom () {
      let container = document.querySelector('.chat-content')
      let scrollHeight = container.scrollHeight
      container.scrollTop = scrollHeight
    }
  },
  computed: {
    ...mapGetters([
      'getSocket',
      'getUsers',
      'getInfo',
      'getMsgHistoryInfo'
    ])
  },
  updated () {
    this.scrollToBottom()
  },
  components: {
    'my-msg': MyMsg,
    'other-msg': OtherMsg
  }
}
</script>

<style scoped>
.mu-appbar {
  text-align: center;
  background-color: rgba(0,0,0,.78);
}
.chat-content {
  width: 100%;
  height: 500px;
  overflow: scroll;
  background: #ffffff;
}
.chat-header {
  position: fixed;
  height: 50px;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1;
}
.bottom {
  position: fixed;
  width: 100%;
  height: 90px;
  bottom: 0;
  left: 0;
  z-index: 1;
  background: #eeeff3;
}
.chat-input {
  width: 100%;
}
.msg-input {
  background: #eeeff3;
  padding: 4px;
}
input {
  width: 100%;
  height: 42px;
  box-sizing: border-box;
  border: 1px solid #8c8c96;
  color: #333333;
  font-size: 18px;
  padding-left: 5px;
}
.mu-raised-button {
  margin-top: 0;
}
.send-button {
  height: 42px;
  margin-top: 0;
}
</style>
