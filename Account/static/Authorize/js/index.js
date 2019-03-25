const el = document.querySelector(".pageWrapper");

var movementStrength = 15;
var height = movementStrength / $(window).height()
var width = movementStrength / $(window).width()

el.addEventListener("mousemove", (e) => {
	var pageX = e.pageX - ($(window).width() / 2);
    var pageY = e.pageY - ($(window).height() / 2);
    var newvalueX = width * pageX * -1 - 25;
    var newvalueY = height * pageY * -1 - 50;
  	el.style.setProperty('--x', newvalueX  + "px");
  	el.style.setProperty('--y', newvalueY + "px");
});

function sendForm() {
	let re = /^[a-zA-Z0-9]+$/;

	let responseContainer = document.getElementById("response")
	let login = document.getElementById("login").value
	let password = document.getElementById("password").value
	let token = document.getElementsByName("csrfmiddlewaretoken")[0].getAttribute("value")

	getErrorMessage = function(text) {
		return "<p class = 'error_msg'>" + text + "</p>";
	}

	if (login.length == 0 || password.length == 0) {
		responseContainer.innerHTML = getErrorMessage("Заполните все поля!");
	} else {
		const url = '/auth/login/';
		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", token);
				}
			}
		});
		$.ajax({
			type: "POST",
			url: url,
			data: {
				login: login,
				passwd: password,
			},
			success: (function(response) {
				if (!response['success']) {
					responseContainer.innerHTML = getErrorMessage(response['message']);
				}
				if (response['redirect']) {
					location.href = response['redirect'];
				}
			}),
		});
	}
}

$(document).keypress(function(event) {
	let sendFormButton = document.getElementById("sendFormButton")
	sendFormButton.press
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13'){
		sendFormButton.click()
    }
});