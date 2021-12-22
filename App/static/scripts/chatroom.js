async function main(){
    const serverUrl = "http://localhost:8080/";
    const chatManager = new ChatManager(serverUrl);

    await chatManager.init();
}

main();