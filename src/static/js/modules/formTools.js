
$('#spnCharLeft').css('display', 'none');
var maxLimit = 100;
$(document).ready(function () {
    $('#<%= txtComments.ClientID %>').keyup(function () {
        var lengthCount = this.value.length;              
        if (lengthCount > maxLimit) {
            this.value = this.value.substring(0, maxLimit);
            var charactersLeft = maxLimit - lengthCount + 1;                   
        }
        else {                   
            var charactersLeft = maxLimit - lengthCount;                   
        }
        $('#spnCharLeft').css('display', 'block');
        $('#spnCharLeft').text(charactersLeft + ' Characters left');
    });
});

function errorTag(selector, msg){
    if (selector === null){
        return
    }else{
        return document.querySelector(selector).innerHTML = msg
    }
}

export function checkName(fullname, selector=null){

    if (!fullname.split(' ').length >= 2 <= 3) {
        msg = 'Only two or three names seperated by space'
        input_state = false
    }else{
        input_state = true
    }
    if(selector != null){
        errorTag(selector, msg)
    }
    return input_state
}

export function checkContact(contact, selector=null){

    const emel = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    const numb = '[+,0-9]'

    if (!contact.match(numb) || !contact.match(emel)) {
        msg = 'Only email or phone number is allowed'
        input_state = false
    }else{
        input_state = true
    }
    if(selector != null){
        errorTag(selector, msg)
    }
    return input_state
}

export function checkAge(age, selector){

    if (!age === new Date()) {
        msg = 'Invalid age'
        input_state = false
    }else{
        input_state = true
    }
    if(selector != null){
        errorTag(selector, msg)
    }
    return input_state
}

export function checkPwd(paswd, selector=null){
    var weak = '[+,0-9]'
    if (paswd.value.length < 6) {
        msg = 'password is too short; at least six(6) characters'
        input_state = false
    }else if(paswd.match(weak)){
        msg = 'password is weak'
        input_state = false
    }else{
        input_state = true
    }
    if(selector != null){
        errorTag(selector, msg)
    }
    return input_state
}

export function checkPwdMatch(paswd, vpaswd, selector=null){

    if (!paswd===vpaswd) {
        msg = 'password must match'
        input_state = false
    }else{
        input_state = true
    }
    if(selector != null){
        errorTag(selector, msg)
    }
    return input_state
}

export function sendForm(event) {
    const req_status
    const myForm = event.target
    const myFormData = new FormData(myForm)
    const url = myForm.getAttribute("action")
    const method = myForm.getAttribute("method")
    const xhr = new XMLHttpRequest()
    const responseType = "json"
    xhr.responseType = responseType
    xhr.open(method, url)
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.onload = function() {
        if (xhr.status === 201) {
            myForm.reset()
        } else req_status = xhr.status
    }
    xhr.onerror = function() {
        req_status = "An error occurred. Please try again later."
    }
    if(xhr.send(myFormData)){
        req_status = true
    }
    return req_status
}
