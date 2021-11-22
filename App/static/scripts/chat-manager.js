class ChatManager {

  constructor(url) {
    this.socketManager = new SocketManager(url);
  }


  async init() {
    $("#connect-btn").click(_ => {
      const user_id = $("#to-user").find("option:selected").val();

      if (user_id !== undefined) {
        this.socketManager.emit("join_room", { to: user_id });
      }
    });


    $("#send-button").click(() => {
      const user_id = $("#to-user").find("option:selected").val();
      const message = $("#message-text").val();
      
      if(user_id !== undefined && message !== undefined) {
        this.socketManager.emit("message_send", { message, to: user_id });
      }
      else {
        alert("Message or recipient is empty.")
      }
    });


    try {
      this.socketManager.addCustomEventHandler("message_send", this.displayMessage);
      this.socketManager.addCustomEventHandler("user_connect", this.displayMessage);
      this.socketManager.addCustomEventHandler("join_room", this.displayMessage);


      const result = await this.socketManager.connect();
    } catch (e) {
      console.log(e);
      alert("Connection Error");
    }
  }


  displayMessage(messageContext) {
    const messageHTML = `<div>
                          <span class="from-user">${messageContext.from}:</span>
                          <span class="message">${messageContext.message}</span>
                        </div>`;
    $("#incoming-messages").append(messageHTML);
  }
}