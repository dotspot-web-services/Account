const fname = document.querySelector('[name="fname"]');
fname.addEventListener("onchange", (event) => {
  checkName(event.target.value, "#fname + div.err");
});

const cont = document.querySelector('[name="cont"]');
cont.addEventListener("onchange", (event) => {
  checkContact(event.target.value, "#cont + div.err");
});

//const dob = document.getElementById("dob")
//dob.addEventListener("onchange", (event)=>{
//    checkAge(event.target.value, '#dob + div.err')
//})

const paswd = document.querySelector('[name="dob"]');
paswd.addEventListener("oninput", (event) => {
  checkPwd(event.target.value, "#paswd + div.err");
});

const vpaswd = document.querySelector('[name="sx"]');
vpaswd.addEventListener("onchange", (event) => {
  checkPwdMatch(event.target.value, paswd.target.value, "#vpaswd + div.err");
});

function sendForm(event, callback) {
  const myForm = event.target;
  const myFormData = new FormData(myForm);
  const url = myForm.getAttribute("action");
  const method = myForm.getAttribute("method");
  const xhr = new XMLHttpRequest();
  const responseType = "json";
  const token = getCookie("token");
  xhr.responseType = responseType;
  xhr.open(method, url);
  xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest");
  xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhr.setRequestHeader("X-CSRFToken", token);
  xhr.withCredentials = true;
  xhr.onload = function () {
    if (xhr.status === 201) {
      myForm.reset();
      callback(xhr.status, xhr.response);
    } else {
      return xhr.status;
    }
  };
  xhr.onerror = function () {
    return 500;
  };
  xhr.send(myFormData);
  return xhr.onload();
}

const forms = Array.from(document.forms);
forms.forEach((form) => {
  if (form.elements["cont"]) {
    checkContact(form.elements["cont"].value, "#cont + div.err");
  }
  form.addEventListener("submit", (event) => {
    const myForm = event.target;
    event.preventDefault();
    switch (myForm.getAttribute("action")) {
      case "/Registry/reg":
        var errors = [
          checkName(form.elements["fname"].value, "#fname + div.err"),
          checkContact(form.elements["cont"].value, "#cont + div.err"),
        ];
        if (form.elements["dob"] != null) {
          errors.push(checkAge(form.elements["dob"].value, "#dob + div.err"));
        } else {
          errors.push(
            checkPwdMatch(
              form.elements["paswd"].value,
              form.elements["vpaswd"].value,
              "#vpaswd + div.err",
            ),
          );
        }
        var i = errors.length;
        while (i--) {
          if (errors[i] === false) {
            alert("please check the form for errors");
            return false;
          }
        }

        sendForm(event, (status, response) => {
          if (status === 201) {
            window.location.href = "/Accounts/";
          } else {
            alert("An error occured please try again");
          }
        });
        break;
      case "/Registry/login":
        sendForm(event, (status, response) => {
          if (status === 201) {
            window.location.href = "/Registry/reg";
          } else if (status >= 400 && status < 502) {
            window.location.href = "/Accounts/";
          } else {
            console.log(status);
            console.log(response);
            alert("Internal server error. Try again later");
          }
        });
        break;

      default:
        break;
    }
  });
});
