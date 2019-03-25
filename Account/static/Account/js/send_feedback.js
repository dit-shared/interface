function sendFeedbackForm() {
    const url = '/account/feedback';
    let token = document.getElementsByName("csrfmiddlewaretoken")[0].getAttribute("value")

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        }
    });

    feedback_form = '<div class="row">' +
    '<form class="col s12">' +
      '<div class="row">' +
        '<div class="input-field col s6">' + 
          '<i class="material-icons prefix">title</i>' +
          '<input id="feedback_title" name="title" type="text" class="validate">' +
          '<label for="feedback_title">Заголовок</label>' +
        '</div>' + 
        '<div class="input-field col s6">' +
          '<i class="material-icons prefix">contact_mail</i>' +
          '<input id="feedback_mail" name="mail" type="text" class="validate">' +
          '<label for="feedback_mail">Ваша почта</label>' +
        '</div>' +
      '</div>' + 
    '</form>' +
  '</div>' +   
  '<div class="row">' +
  '<form class="col s12">' +
    '<div class="row">' +
      '<div class="input-field col s12">' +
        '<i class="material-icons prefix">message</i>' +
        '<textarea id="feedback_text" name = "text" class="materialize-textarea"></textarea>' +
        '<label for="feedback_text">Сообщение</label>' + 
      '</div>' +
    '</div>' +
  '</form>' +
  '</div>';

    swal({
        title: "Выполнить предсказание",
        html: feedback_form,
        icon: "info",
        showCancelButton: true,
        closeOnConfirm: false,
        showLoaderOnConfirm: true,
        button: {
            text: "Отправить",
            closeModal: false,
        },
    }).then(function (isConfirm) {
        if (!isConfirm.value) return;
        let title = document.getElementById("feedback_title").value
        let text = document.getElementById("feedback_text").value
        let mail = document.getElementById("feedback_mail").value
        console.log(token, title, text, mail)

        $.ajax({
            type: "POST",
            url: url,
            data: {
                title: title,
                text: text,
                mail: mail,
            },
            success: (function(response) {
                if (!response["success"]) {
                    swal("Ошибка!", "Похоже на сервере возникла ошибка", "error");
                } else {
                    swal("Выполнено", "Запрос отправлен." + response["message"], "success");
                }
            }),
        });
    });
}


$(document).keypress(function (event) {
    let sendFormButton = document.getElementById("predictFormButton")
    sendFormButton.press
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13') {
        sendFormButton.click()
    }
});
