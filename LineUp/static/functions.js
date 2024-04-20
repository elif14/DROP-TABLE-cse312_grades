
function ta_display(){

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
    let ta = ""
    for (let singleChar of chatMessage){
        if (singleChar != " " || singleChar !="'" || singleChar != ":" || singleChar != "[" || singleChar != "]"){
            ta += singleChar;
        }
    }
}

function addNames(taNames){
    const currElem = document.getElementById("ta_names")
    for (const name of taNames){
        let newArr = name.split('(')
        const newDiv = document.createElement("div");
        newDiv.className = "container";

        const newImageDiv = document.createElement("div");
        const newImage = new Image ();
        newImage.src = "LineUp/static/" + newArr[0] + ".jpg"
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
