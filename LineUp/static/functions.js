let socket = null
function initWS() {
    socket = io.connect('https://wonwoojeong.com/', {
        transports: ['websocket']
    });

    socket.on('connect', function() {
        console.log('connected to websocket');
        socket.emit('ClientTAChat');
        socket.emit('populateStudentQueue');
    });

    socket.on('disconnect', function() {
        console.log('disconnected from websocket');
    });

    socket.on('TAChat', function(chat) {
        clearTAChat();
        addMessageToChat(chat);
    });

    socket.on('TAChatReceive', function(chat) {
        addMessageToChat(chat);
    });

    socket.on('studentQueue', function(student) {
        clearStudentQueue();
        addStudentToQueue(student);
    });

    socket.on('studentQueue2', function(student) {
        addStudentToQueue(student);
    });

    socket.on('connect_error', (error) => {
        console.log('Connection                                                                                                                                                                                                                                                                                                                                                             Error:', error);
    });

    const TAChatInput = document.getElementById('TA-chat');
    TAChatInput.addEventListener("keypress", function (event) {
        if (event.code === "Enter") {
            let TAChat = TAChatInput.value;
            TAChatInput.value = "";
            socket.emit('ReceiveTAChat', TAChat);
        }
    });

    const StudentEnqueue = document.getElementById('student-queue');
    StudentEnqueue.addEventListener("keypress", function (event) {
        if (event.code === "Enter") {
            let Student = StudentEnqueue.value;
            StudentEnqueue.value = "";
            socket.emit('StudentQueue', Student);
        }
    });

}

function dequeueStudent(id) {
    socket.emit('StudentDequeue', id);
}

function dequeueTA(id) {
    socket.emit('TADequeue', id);
}

function clearTAChat() {
    const chatMessages = document.getElementById("TA-Announcements");
    chatMessages.innerHTML = "";
}

function clearStudentQueue() {
    const studentQueue = document.getElementById("student-enqueue");
    studentQueue.innerHTML = "";
}

function randInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

function addMessageToChat(chatJSON) {
    const chatMessages = document.getElementById("TA-Announcements");
    let TA_chat = JSON.parse(chatJSON)
    for (let i = 0; i < TA_chat.length; i++) {
        const username = TA_chat[i].split(":")[0];
        const username2 = TA_chat[i].split(":")[0] + "?";
        const chatMessage = TA_chat[i].split(":")[1];
        let html = `<div style='margin-top: 7px'><button onclick='dequeueTA("${username}?${i}")'>X</button><b>${username}</b>: ${chatMessage}</div>`;
        chatMessages.innerHTML += html;
    }
}

function addStudentToQueue(student) {
    const Queue = document.getElementById("student-enqueue");
    let students = JSON.parse(student)
    for (let i = 0; i < students.length; i++) {
        const username = students[i];
        Queue.innerHTML += "<div style='margin-top: 7px'><button onclick='dequeueStudent(" + i + ")'>X</button><b>" + username + "</b></div>";
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