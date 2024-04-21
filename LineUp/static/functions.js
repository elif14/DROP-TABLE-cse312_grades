let socket = null
function initWS() {
    socket = io.connect('http://localhost:8080', {
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
        clearOnDutyTAList();
        TAsOnDuty(TAOnDutyList);
        addNames(TAOnDutyList);
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
    let ta = ""
    for (let singleChar of chatMessage){
        if (singleChar != " " || singleChar !="'" || singleChar != ":" || singleChar != "[" || singleChar != "]"){
            ta += singleChar;
        }
    }
}

function addNames(taNames){
    const currElem = document.getElementById("ta_names")
    for (let i = 0; i < taNames.length ; i++ ){
        const currTA = taNames[i];
        let newArr = name.split('(')
        const newDiv = document.createElement("div");
        newDiv.className = "container";

        const newImageDiv = document.createElement("div");
        const newImage = new Image ();
        newImage.src = "LineUp/static/" + currTA + ".jpg"
        newImageDiv.appendChild(newImage);
        
        const newTextDiv = document.createElement("div");
        newTextDiv.className = "text";
        const newElem = document.createElement("h3")
        const newName = document.createTextNode(name)
        newElem.appendChild(newName)
        newTextDiv.appendChild(newElem);
        
        newDiv.append(newImageDiv, newTextDiv);

        document.body.insertBefore(newDiv, currElem);
        //document.body.insertBefore(newElem, newImage)
    }
}

function display_ta(taName) {
    const profile_img = document.getElementById(taName + "ta_profile");
    let newName = taName.split(':')
    console.log(newName)
    let newerName = newName[0].split('[')[1]
    profile_img.src = "LineUp/static/"+ newerName + ".jpg";
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
