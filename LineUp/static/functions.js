
function ta_display(){
    const request = new XMLHttpRequest();
    request.open("GET", '/ta_display');
    request.send();
    request.onload = () => {
        if(request.readyState == 4 && request.status == 200){
            const response = request.response
            let data_needed = JSON.parse(response)
            console.log(data_needed)
            for (let single_ta of ta_names){
                document.getElementById("ta_names").innerHTML = single_ta
            }
        }
    }
}