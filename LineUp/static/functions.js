function initWS() {
    var socket = io.connect('ws://' + window.location.host + '/websocket');

    socket.on('open', function() {
        console.log('connected to websocket');
    });

    socket.on('closed', function() {
        console.log('No longer connected to websocket');
    });

    socket.on('TAChat', function(chat) {
        console.log('message: ', chat);
        addMessageToChat(chat);
    });
}


function updateTAChat() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearTAChat();
            const messages = JSON.parse(this.response);
            for (const message of messages) {
                addMessageToChat(message);
            }
        }
    }
    request.open("GET", "/TA-chat");
    request.send();
}

function clearTAChat() {
    const chatMessages = document.getElementById("TA-chat");
    chatMessages.innerHTML = "";
}

function addMessageToChat(chatJSON) {
    const chatMessages = document.getElementById("TA-chat");
    const username = chatJSON.username;
    const chatMessage = chatJSON.message;
    chatMessages.innerHTML += "<b>" + username + "</b>: " + chatMessage;
}

function ta_display(){
    initWS();
    updateTAChat();

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