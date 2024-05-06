let socket = null
function initWS() {
    socket = io.connect('wss://wonwoojeong.com/', {
        transports: ['websocket']
    });

    socket.on('connect', function() {
        initialTimer();
        console.log('connected to websocket');
        socket.emit('ClientTAChat');
        socket.emit('populateOnDuty');
        socket.emit('populateQueue');
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
        startTimer();
    });

    socket.on('TAOnDutyReceive', function(TAOnDutyList) {
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

function initialTimer() {
    const timerHTML = document.getElementById("timer");
    let cooldown;
    if (localStorage.getItem("timer2")){
        cooldown = localStorage.getItem("timer2");
    }
    else{
        cooldown = 4;
    }
    timerHTML.innerText = "Please wait " + String(cooldown) + " seconds before joining the queue";
    const timer = setInterval(function() {
        cooldown -= 1;
        localStorage.setItem("timer2", cooldown);
        timerHTML.innerText = "Please wait " + String(cooldown) + " seconds before joining the queue";
        if (cooldown === 0) {
            timerHTML.innerText = "";
            localStorage.removeItem("timer2");
            clearInterval(timer);
        }
    }, 1000);
}

function startTimer() {
    const timerHTML = document.getElementById("timer");
    let cooldown;
    if (localStorage.getItem("timer")){
        cooldown = localStorage.getItem("timer");
    }
    else{
        cooldown = 4;
    }
    timerHTML.innerText = "A student has just joined the queue. Please wait " + String(cooldown) + " seconds.";
    const timer = setInterval(function() {
        cooldown -= 1;
        localStorage.setItem("timer", cooldown);
        timerHTML.innerText = "A student has just joined the queue. Please wait " + String(cooldown) + " seconds.";
        if (cooldown === 0) {
            timerHTML.innerText = "";
            localStorage.removeItem("timer");
            clearInterval(timer);
        }
    }, 1000);
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
    if (localStorage.getItem("timer2")){
        initialTimer();
    }
    else if (localStorage.getItem("timer")){
        startTimer();
    }
    initWS();
}