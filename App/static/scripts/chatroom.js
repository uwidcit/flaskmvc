async function main(){
    const serverUrl = "https://8080-scarlet-dolphin-dvpmbcot.ws-us17.gitpod.io";
    const chatManager = new ChatManager(serverUrl);

    await chatManager.init();
}

main();