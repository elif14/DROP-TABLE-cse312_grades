let socket = null
function initWS() {
    socket = io.connect('https://wonwoojeong.com/', {
        transports: ['websocket']
    });

    socket.on('connect', function() {
        console.log('connected to websocket');
        socket.emit('ClientTAChat');
        socket.emit('populateOnDuty');
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

    socket.on('TAOnDutyReceive', function(TAOnDutyList) {
        console.log(TAOnDutyList);
        console.log("test");
        clearOnDutyTAList();
        TAsOnDuty(TAOnDutyList);
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

    const onDutyButton = document.getElementById('on-duty-button');
    onDutyButton.addEventListener("click", function (event) {
        socket.emit('TAOnDuty');
    });

    const offDutyButton = document.getElementById('off-duty-button');
    offDutyButton.addEventListener("click", function (event) {
        socket.emit('TAOffDuty');
    });

}

function TAsOnDuty(TAOnDutyList) {
    const TAsOnDutyHTML = document.getElementById("ta_names");
    let TAsOnDuty = JSON.parse(TAOnDutyList)
    for (let i = 0; i < TAsOnDuty.length; i++) {
        const TA = TAsOnDuty[i];
        TAsOnDutyHTML.innerHTML += "<div style='margin-top: 7px'><b>" + TA + "</div>";
    }
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

function clearOnDutyTAList() {
    const OnDutyTAList = document.getElementById("ta_names");
    OnDutyTAList.innerHTML = "";
}


function clearStudentQueue() {
    const studentQueue = document.getElementById("student-enqueue");
    studentQueue.innerHTML = "";
}

// function randInt(min, max) {
//     min = Math.ceil(min);
//     max = Math.floor(max);
//     return Math.floor(Math.random() * (max - min + 1)) + min;
//   }

function addMessageToChat(chatJSON) {
    const chatMessages = document.getElementById("TA-Announcements");
    let TA_chat = JSON.parse(chatJSON)
    for (let i = 0; i < TA_chat.length; i++) {
        const username = TA_chat[i].split(":")[0];
        const username2 = TA_chat[i].split(":")[0] + "?" + String(i);
        const chatMessage = TA_chat[i].split(":")[1];
        chatMessages.innerHTML += "<div style='margin-top: 7px'><button onclick='dequeueTA(\"" + username2 + "\")'>X</button><b>" + username + "</b>: " + chatMessage + "</div>";
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

function onLoadFunction(){
    initWS();
}