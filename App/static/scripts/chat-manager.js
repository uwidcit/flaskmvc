class ChatManager {

  constructor(url) {
    this.socketManager = new SocketManager(url);
  }


  async init() {
    $("#send-button").click(() => {
      const message = $("#message-text").val();
      this.socketManager.emit("message_send", { message, to: "John" });
    });


    try {
      this.socketManager.addCustomEventHandler("message_send", this.displayMessage);

      const result = await this.socketManager.connect();
    } catch (e) {
      console.log(e);
      alert("Connection Error");
    }
  }


  displayMessage(messageContext){
    const messageHTML = `<div>
                          <span class="from-user">${messageContext.from}:</span>
                          <span class="message">${messageContext.message}</span>
                        </div>`;
    $("#incoming-messages").append(messageHTML);
  }
}