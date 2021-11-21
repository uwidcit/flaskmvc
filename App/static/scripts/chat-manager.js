class ChatManager {

  constructor(url) {
    this.socketManager = new SocketManager(url);
  }


  async init() {
    try {
      this.socketManager.addCustomEventHandler("response", data => console.log(`Data: ${data.data}`));      
      const result = await this.socketManager.connect();
    } catch (e) {
      console.log(e);
      alert("Connection Error");
    }
  }

}