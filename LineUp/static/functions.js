const info = []

function display_ta_name(e){
    e.preventDefault();
    var ta = document.getElementById("ta_name").value;
    info.push(ta);
    var name = document.createElement("h2");
    name.innerHTML = name;
    document.body.appendChild(name);
}