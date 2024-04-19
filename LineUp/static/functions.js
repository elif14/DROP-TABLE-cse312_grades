
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
}

function addNames(taNames){
    const currElem = document.getElementById("ta_names")
    for (const name of taNames){
        let newArr = name.split('(')
        const newImage = new Image ()
        const newElem = document.createElement("h3")
        const newName = document.createTextNode(name)
        newImage.src = "LineUp/static/" + newArr[0] + ".jpg"
        newElem.appendChild(newName)
        document.body.insertBefore(newImage, currElem)
        document.body.insertBefore(newElem, newImage)
    }
}

function ta_pic_display(taList){
    const profileDisplayElem = document.getElementById("ta-pics")
    for (const singleTa in taList){
        const newImage = new Image ()
        newElem.src = "LineUp/static/" + singleTa + ".jpg"
        document.body.insertBefore(newElem, profileDisplayElem)
    }
}
