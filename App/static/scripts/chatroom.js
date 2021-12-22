async function main(){
    const serverUrl = "/:8080";
    const chatManager = new ChatManager(serverUrl);

    await chatManager.init();
}

main();