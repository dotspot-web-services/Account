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

function sendForm(event, callback) {
  const addr = event.target;
  const myFormData = new FormData(addr);
  const url = addr.getAttribute("href");
  const method = "GET";
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

function display() {
  var togl = document.getElementById("toggler");
  if (togl.style.display === "none") {
    togl.style.display = "block";
    document.getElementById("limlit").classList.remove("show");
  } else {
    togl.style.display = "none";
    document.getElementById("limlit").classList.add("show");
  }
  return;
}

//if(document.getElementById("hider")){
//    document.getElementById("hider").addEventListener("click", display)
//}

if (document.getElementById("srcha")) {
  const srch_form = document.getElementById("srcha");
  srch_form.elements["srch-inp"].addEventListener("focus", display);
}
if (document.getElementById("srcha")) {
  const srch_form = document.getElementById("srcha");
  srch_form.elements["srch-inp"].addEventListener("blur", display);
}

$(document).click(function () {
  alert("me");
});
$(".myDiv").click(function (e) {
  e.stopPropagation(); // This is the preferred method.
  return false; // This should not be used unless you do not want
  // any click events registering inside the div
});

function getAddress(latitude, longitude) {
  $.ajax(
    "https://maps.googleapis.com/maps/api/geocode/json?latlng=" +
      latitude +
      "," +
      longitude +
      "&key=" +
      GOOGLE_MAP_KEY,
  ).then(
    function success(response) {
      console.log("User's Address Data is ", response);
    },
    function fail(status) {
      console.log("Request failed.  Returned status of", status);
    },
  );
}
if ("geolocation" in navigator) {
  // check if geolocation is supported/enabled on current browser
  navigator.geolocation.getCurrentPosition(
    function success(position) {
      // for when getting location is a success
      console.log(
        "latitude",
        position.coords.latitude,
        "longitude",
        position.coords.longitude,
      );
      getAddress(position.coords.latitude, position.coords.longitude);
    },
    function error(error_message) {
      // for when getting location results in an error
      console.error(
        "An error has occured while retrieving location",
        error_message,
      );
      ipLookUp();
    },
  );
} else {
  // geolocation is not supported
  // get your location some other way
  console.log("geolocation is not enabled on this browser");
  ipLookUp();
}
