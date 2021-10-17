
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function errorTag(selector, msg){
    if (selector == null){
        return
    }else{
        return document.querySelector(selector).innerHTML = msg
    }
}

function checkName(fullname, selector=null){
    var input_state = false
    if (!fullname.split(' ').length >= 2 <= 3) {
        input_state = true
    }else{
        msg = 'Only two or three names seperated by space'
    }
    if(selector != null && input_state == false){
        errorTag(selector, msg)
    }
    return input_state
}

function checkContact(contact, selector=null){

    const emel = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    //const numb = '[+,0-9]'
    var input_state = false
    if (!contact.match(emel)) {
        msg = 'Only email or phone number is allowed'
    }else{
        input_state = true
    }
    if(selector != null && input_state == false){
        errorTag(selector, msg)
    }
    return input_state
}

function checkAge(age, selector){
    var input_state = false
    if (!age === new Date()) {
        msg = 'Invalid age'
    }else{
        input_state = true
    }
    if(selector != null && input_state == false){
        errorTag(selector, msg)
    }
    return input_state
}

function checkPwd(paswd, selector=null){
    var weak = '[+,0-9]'
    var input_state = false
    if (paswd.length < 6) {
        msg = 'password is too short; at least six(6) characters'
    }else if(paswd.match(weak)){
        msg = 'password is weak'
        input_state = true
    }else{
        input_state = true
    }
    if(selector != null && input_state == false){
        errorTag(selector, msg)
    }
    return input_state
}

function checkPwdMatch(paswd, vpaswd, selector=null){
    
    var input_state = false
    if (!paswd==vpaswd) {
        msg = 'password must match'
    }else if(paswd==vpaswd){
        input_state = true
    }
    if(selector != null && input_state == false){
        errorTag(selector, msg)
    }
    return input_state
} 

function sendForm(event, callback) {
    const myForm = event.target
    const myFormData = new FormData(myForm)
    const url = myForm.getAttribute("action")
    const method = myForm.getAttribute("method")
    const xhr = new XMLHttpRequest()
    const responseType = "json"
    const token = getCookie("token")
    xhr.responseType = responseType
    xhr.open(method, url)
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("X-CSRFToken", token)
    xhr.withCredentials = true
    xhr.onload = function() {
        if (xhr.status === 201) {
            myForm.reset()
            callback(xhr.status, xhr.response)
        } else{
            return xhr.status
        }
    }
    xhr.onerror = function() {
        return 500
    }
    xhr.send(myFormData)
    return xhr.onload()
}

const fname = document.getElementById("fname")
fname.addEventListener("onchange", (event)=>{
    checkName(event.target.value, '#fname + div.err')
})

const cont = document.getElementById("cont")
cont.addEventListener("onchange", (event)=>{
    checkContact(event.target.value, '#cont + div.err')
})

//const dob = document.getElementById("dob")
//dob.addEventListener("onchange", (event)=>{
//    checkAge(event.target.value, '#dob + div.err')
//})

const paswd = document.getElementById("paswd")
paswd.addEventListener("oninput", (event)=>{
    checkPwd(event.target.value, '#paswd + div.err')
})

const vpaswd = document.getElementById("vpaswd")
vpaswd.addEventListener("onchange", (event)=>{
    checkPwdMatch(event.target.value, paswd.target.value, '#vpaswd + div.err')
})

document.getElementById("regForm").addEventListener("submit", (event)=>{
    event.preventDefault()
    const errors = [
        checkName(fname.value, '#fname + div.err'), checkContact(cont.value, '#cont + div.err'),
        checkPwdMatch(paswd.value, vpaswd.value, '#vpaswd + div.err')
    ]
    var i = errors.length;
    while(i--){
        if(errors[i]===false){
            alert("please check the form for errors")
            return false;
        }
    }
    sendForm(event, (status, response) => {
        if (status === 201){
            window.location.href = "http://127.0.0.1:5000/Registry"
            Ferror.innerHtml = ''
            Derror.innerHTML = ''
            Perror.innerHTML = ''
            Verror.innerHTML = ''
        } else {
            alert("An error occured please try again")
        }
    })
})

document.getElementById("loga").addEventListener("submit", (event)=>{
    event.preventDefault();
    sendForm(event,(status, response) => {
        if (status === 201){
            window.location.href = "/Registry/reg"
        } else if(status >= 400 && status < 502){
            window.location.href = "/Profiles/Basics"
        }else{
            console.log(status)
            console.log(response)
            alert("Internal server error. Try again later")
        }
    });
})

