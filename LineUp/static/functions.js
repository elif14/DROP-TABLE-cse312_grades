function initWS() {
    var socket = io.connect('http://localhost:8080/', {
        transports: ['websocket']
    });

    socket.on('connect', function() {
        console.log('connected to websocket');
        clearTAChat();
        socket.emit('ClientTAChat');
    });

    socket.on('disconnect', function() {
        console.log('disconnected from websocket');
    });

    socket.on('TAChat', function(chat) {
        addMessageToChat(chat);
    });

    socket.on('connect_error', (error) => {
        console.log('Connection Error:', error);
    });

    const TAChatInput = document.getElementById('TA-chat');
    TAChatInput.addEventListener("keypress", function (event) {
        if (event.code === "Enter") {
            socket.emit('ReceiveTAChat', TAChatInput.value);
        }
    });

}

function clearTAChat() {
    const chatMessages = document.getElementById("TA-Announcements");
    chatMessages.innerHTML = "";
}

function addMessageToChat(chatJSON) {
    const chatMessages = document.getElementById("TA-Announcements");
    TA_chat = JSON.parse(chatJSON)
    for (let i = 0; i < TA_chat.length; i++) {
        const username = TA_chat[i].split(":")[0];
        const chatMessage = TA_chat[i].split(":")[1];
        chatMessages.innerHTML += "<div style='margin-top: 7px'><b>" + username + "</b>: " + chatMessage + "</div>";
    }
}

function ta_display(){
    initWS();

    const request = new XMLHttpRequest();
    request.open("GET", '/ta_display');
    request.send();
    let newArr = []
    request.onload = () => {
        if(request.readyState == 4 && request.status == 200){
            const response = request.response
            let dataNeeded = JSON.parse(response)
            let neededName = ""
            for (let singleChar of dataNeeded) {
                if (singleChar == ' ' || singleChar == ']') {
                    newArr.push(neededName)
                    neededName = ""
                } else if (singleChar !== '['
                    && singleChar !== '"'
                    && singleChar !== ',') {
                    neededName += singleChar
                }
            }
        }
        console.log(newArr)
        addNames(newArr)
    }
}

function dequeue(studentName){//funciton to dequeue student, this is called by onclick button
    const request = new XMLHttpRequest();
    const name = studentName
    console.log(name)
    const body = JSON.stringify({student_name: name});
    console.log(body)
    request.open("POST", "/dequeue_student");
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(body);
}

function dequeueChat(chatMessage){//funciton to dequeue student, this is called by onclick button
    const request = new XMLHttpRequest();
    console.log(chatMessage)
    const body = JSON.stringify({chat: chatMessage});
    console.log(body)
    request.open("POST", "/remove_TA_chat");
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(body);
}

function addNames(taNames){
    let elementNum = 3
    const currElem = document.getElementById("ta_names")
    for (const name of taNames){
        let newElemID = "h" + elementNum.toString()
        const newElem = document.createElement(newElemID)
        const newName = document.createTextNode(name)
        newElem.appendChild(newName)
        document.body.insertBefore(newElem, currElem)
    }
}