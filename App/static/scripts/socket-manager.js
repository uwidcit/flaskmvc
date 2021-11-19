class SocketManager {
    constructor(url) {
      this.socket = io(url, { autoConnect: false });
    }
  
    connect() {
      //auto connects
      console.log(this.socket);
      this.socket.on("disconnect", this.socket.connect);
  
      return new Promise((resolve, reject) => {
        try {
          this.socket.on("connect", (_) => {console.log("Connected"); resolve(true);});
          this.socket.open();
        } catch (e) {
          reject(e);
        }
      });
    }
  }
  