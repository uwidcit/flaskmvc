class ChatManager {

  constructor(url) {
    this.socketManager = new SocketManager(url);
  }


  async init() {
    try {
      const result = await this.socketManager.connect();
      const socket = this.socketManager.socket;

      socket.on("my_response", (data) => {
        console.log(`connected: ${data.data}`);
      });
      
    } catch (e) {
      console.log(e);
      alert("Connection Error");
    }
  }

}