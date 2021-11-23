class SocketManager {
  reserved_events = [
    'connect', 
    'connect_error', 
    'connect_timeout',
    'error',
    'disconnect',
    'reconnect',
    'reconnect_attempt',
    'reconnecting',
    'reconnect_error',
    'reconnect_failed',
    'ping',
    'pong'
  ]


  constructor(url) {
    this.socket = io(url, { autoConnect: false });
  }


  connect() {
    // Enables socket auto connect
    this.socket.on("disconnect", this.socket.connect);

    return new Promise((resolve, reject) => {
      try {
        this.socket.on("connect", _ => resolve(true));
        this.socket.open();
      } catch (e) {
        reject(e);
      }
    });
  }


  addCustomEventHandler(event, callback){
    if(this.reserved_events.includes(event))throw 'RESERVED EVENT EXCEPTION'
    this.socket.on(event, callback);
  }

  addEventHandler(event, callback){
    if(!this.reserved_events.includes(event))throw 'UNKNOWN EVENT EXCEPTION';
    this.socket.on(event, callback)
  }

  emit(event, data){
    if(!this.socket.connected) throw 'SOCKET NOT CONNECTED EXCEPTION';
    this.socket.emit(event, data);
  }
}
