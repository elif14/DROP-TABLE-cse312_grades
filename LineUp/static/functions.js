
function ta_display(){

    const request = new XMLHttpRequest();
    request.open("GET", '/ta_display');
    request.send();
    request.onload = () => {
        if(request.readyState == 4 && request.status == 200){
            const response = request.response
            let data_needed = JSON.parse(response)
            let needed_name = ""
            let new_arr = []
            for (let single_char of data_needed){
                if (single_char == ' ' || single_char == ']'){
                    new_arr.push(needed_name)
                    needed_name = ""
                }
                else if (single_char !== '['
                    && single_char !== '"'
                    && single_char !== ','){
                    needed_name += single_char
                }
            }
            let all_names = ""
            for (const name of new_arr){
                const singleName = name + " "
                all_names += singleName
            }
            console.log(all_names)
            document.getElementById("ta_names").innerHTML = all_names
        }
    }
}

function dequeue(item){//funciton to dequeue student, this is called by onclick button
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    request.open("POST", "/dequeue_student" + item.name);//appends the name of tudnet to dequeue
    request.send();
}