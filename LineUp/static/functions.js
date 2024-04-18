function initWS() {
    var socket = io.connect('ws://localhost:8080', {
        transports: ['websocket']
    });



    socket.on('connect', function() {
        clearTAChat();
        socket.emit('TA-chat');
        console.log('connected to websocket');
    });

    socket.on('disconnect', function() {
        console.log('No longer connected to websocket');
    });

    socket.on('TA-chat', function(chat) {
        console.log('message: ', chat);
        addMessageToChat(chat);
    });

    socket.on('connect_error', (error) => {
        console.log('xxxxConnection Error:', error);
    });

    socket.on('connect_error', (error) => {
        console.log('xxxxConnection Error:', error);
    });
}

function clearTAChat() {
    const chatMessages = document.getElementById("TA-Announcements");
    chatMessages.innerHTML = "";
}

function addMessageToChat(chatJSON) {
    const chatMessages = document.getElementById("TA-Announcements");
    const username = chatJSON.username;
    const chatMessage = chatJSON.message;
    chatMessages.innerHTML += "<b>" + username + "</b>: " + chatMessage;
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