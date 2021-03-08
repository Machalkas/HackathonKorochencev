var form_result = document.getElementById("form_result");
$("#upload_task").click(function (e) {
    // e.preventDefault();
    $("#form_result").text("");
    let check_result = checkForm(document.forms["task_form"], 1024);
    if (check_result[0] && check_result[1]) {
        let x = $("#task_form")[0];
        var formData = new FormData(x);
        formData.append("action", "upload-task")
        $.ajax({
            url: '/tasks/managetasks',
            method: 'post',
            dataType: 'json',
            headers: { 'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value },
            data: formData,
            async: false,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                console.log(data["ok"]);
                document.getElementById("task_form").reset();
                $("#message_text").html("Задание <span style='font-weight: bold;'>" + data["ok"] + "</span> загружено");
                $("#message").fadeIn().delay(5000).fadeOut(2000);
            },
            error: function (data) {
                try {
                    data = JSON.parse(data["responseText"]);
                    // console.log(data);
                    let errors = "";
                    for (i in data["error"]) {
                        console.log(data["error"][i]);
                        // errors += '<p class="lead" style="font-size: 1em;">' + data["error"][i] + '</p>\n';
                    }
                    errors += '<p class="lead" style="font-size: 1em;">' + data["error"] + '</p>\n';
                    form_result.innerHTML = errors;
                }
                catch {
                    form_result.innerHTML = '<p class="lead" style="font-size: 1em;">Ошибка подключения к серверу</p>';
                }
            }
        })
    }
    else {
        let e = '';
        if (!check_result[0]) {
            e = '<p class="lead" style="font-size: 1em;">Заполните все обязательные поля</p>';
        }
        if (!check_result[1]) {
            e += '<p class="lead" style="font-size: 1em;">Файл слишком большой</p>';
        }
        form_result.innerHTML = e;
    }
});