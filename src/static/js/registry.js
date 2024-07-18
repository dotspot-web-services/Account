function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function errorTag(selector, msg) {
  if (selector == null) {
    return;
  } else {
    return (document.querySelector(selector).innerHTML = msg);
  }
}

function checkName(fullname, selector = null, mini, max) {
  var input_state = false;
  if (!fullname.split(" ").length >= mini <= max) {
    input_state = true;
  } else {
    var msg = "name exceeds" + max + "or less than" + mini;
  }
  if (selector != null && input_state == false) {
    errorTag(selector, msg);
  }
  return input_state;
}

function checkContact(contact, selector = null, typ = null) {
  const emel =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  //const numb = '[+,0-9]'
  var input_state = false;
  if (typ === "email") {
    if (!contact.match(emel)) {
      var msg = "Only email or phone number is allowed";
    } else {
      input_state = true;
    }
  } else if (typ === "phone") {
    if (!contact.match(emel)) {
      var msg = "Only email or phone number is allowed";
    } else {
      input_state = true;
    }
  } else if (!contact.match(emel)) {
    var msg = "Only email or phone number is allowed";
  } else {
    input_state = true;
  }
  if (selector != null && input_state == false) {
    errorTag(selector, msg);
  }
  return input_state;
}

function checkAge(age, selector) {
  var input_state = false;
  if (age === new Date()) {
    var msg = "Invalid age";
  } else {
    input_state = true;
  }
  if (selector != null && input_state == false) {
    errorTag(selector, msg);
  }
  return input_state;
}

function checkYear(year, selector) {
  var input_state = false;
  if (!year < 1930 > new Date()) {
    var msg = "Invalid age";
  } else {
    input_state = true;
  }
  if (selector != null && input_state == false) {
    errorTag(selector, msg);
  }
  return input_state;
}

function checkPwd(paswd, selector = null) {
  var weak = "[+,0-9]";
  var input_state = false;
  if (paswd.length < 6) {
    var msg = "password is too short; at least six(6) characters";
  } else if (paswd.match(weak)) {
    msg = "password is weak";
    input_state = true;
  } else {
    input_state = true;
  }
  if (selector != null && input_state == false) {
    errorTag(selector, msg);
  }
  return input_state;
}

function checkRadio(rad) {
  var input_state = false;
  if (rad === null) {
    input_state = false;
  } else {
    input_state = true;
  }
  return input_state;
}

function checkPwdMatch(paswd, vpaswd, selector = null) {
  var input_state = false;
  if (!paswd == vpaswd) {
    var msg = "password must match";
  } else if (paswd == vpaswd) {
    input_state = true;
  }
  if (selector != null && input_state == false) {
    errorTag(selector, msg);
  }
  return input_state;
}

function sendForm(event, callback) {
  const myForm = event.target;
  const csrf_token = "{{ csrf_token() }}";
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
  xhr.setRequestHeader("X-ReqToken", token);
  xhr.setRequestHeader("X-CSRFToken", csrf_token);
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

if (document.querySelector("cont") || document.querySelector("emel")) {
  let contact =
    document.querySelector("cont") || document.querySelector("emel");
  contact.addEventListener("valueChange", () => {
    const xhr = new XMLHttpRequest();
    const responseType = "json";
    xhr.responseType = responseType;
    xhr.open("get", "/Registry/login");
    xhr.onload = function () {
      if (xhr.status === 201) {
        console.log(xhr.response);
      } else {
        return xhr.status;
      }
    };
    xhr.onerror = function () {
      return 500;
    };
    xhr.send(myFormData);
    return xhr.onload();
  });
}

if (document.getElementById("logForm") || document.getElementById("loga")) {
  let loga =
    document.getElementById("logForm") || document.getElementById("loga");
  console.log(loga);
  loga.addEventListener("submit", (event) => {
    event.preventDefault();
    sendForm(event, (status, response) => {
      if (status === 201) {
        window.location.href = "http://127.0.0.1:5000/";
      } else if (status === 401) {
        alert(response);
        return;
      } else {
        alert("Internal server error. Try again later");
        return;
      }
    });
  });
}

if (document.getElementById("regForm")) {
  const form = document.forms["regForm"];
  document.getElementById("regForm").addEventListener("submit", (event) => {
    event.preventDefault();
    let final = false;
    var errors = [
      checkName(form.elements["fname"].value, "#fname + div.alert", 2, 3),
      checkContact(form.elements["cont"].value, "#cont + div.alert"),
    ];
    if (form.elements["dob"] != null) {
      final = true;
      errors.push(checkAge(form.elements["dob"].value, "#dob + div.alert"));
    } else {
      errors.push(
        checkPwdMatch(
          form.elements["paswd"].value,
          form.elements["vpaswd"].value,
          "#vpaswd + div.alert",
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
        if (final === true) {
          window.location.href = "/Profiles/";
        } else {
          window.location.href = "/Accounts/";
        }
      } else if (status === 401) {
        alert(response);
        response;
      } else {
        alert("An error occured please try again");
        return;
      }
    });
  });
}

if (document.getElementById("proForm")) {
  const form = document.forms["proForm"];
  document.getElementById("proForm").addEventListener("submit", (event) => {
    event.preventDefault();
    var errors = [
      checkName(form.elements["dspln"].value, "dspln + div.alert", 1, 3),
      checkName(form.elements["plc"].value, "plc + div.alert", 1, 10),
      checkYear(form.elements["strt"].value, "strt + div.alert"),
    ];
    if (form.elements["ttl"] != null) {
      errors.push(
        checkName(form.elements["ttl"].value, "ttl + div.alert", 1, 1),
      );
    } else if (form.elements["emel"] != null) {
      errors.push(checkContact(form.elements["emel"].value), "typ + div.alert");
    } else if (form.elements["typ"] != null) {
      errors.push(checkRadio(form.elements["typ"].value));
    }
    var i = errors.length;
    while (i--) {
      if (errors[i] === false) {
        alert("please check the form for errors");
        return false;
      }
    }

    sendForm(event, (status, response) => {
      let next = document.querySelector("#right-btn");
      if (status === 201) {
        if (next) {
          window.location.href = next.getAttribute("href");
        } else {
          window.location.href = "/procfile";
        }
      } else if (status === 401) {
        alert(response);
        return;
      } else {
        alert("An error occured please try again");
        return;
      }
    });
  });
}
