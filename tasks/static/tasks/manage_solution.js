var max_score = null, task = null, team = null;
$("#id_score").change(function () {
    if ($("#id_score")[0].value > max_score) {
        $("#id_score")[0].value = max_score;
    }
    if ($("#id_score")[0].value < 0) {
        $("#id_score")[0].value = 0;
    }
});

$("#upload_value").click(function () {
    $("#form_result").text("");
    $("#upload_value").attr("disabled", "");
    if (checkForm(document.forms["solution_form"])) {
    $.ajax({
        url: '/tasks/managetasks',
        method: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': document.getElementsByName("csrfmiddlewaretoken")[0].value },
        data: { "action": "upload-score", "solution": solution_id, "score": $("#id_score")[0].value },
        success: function (data) {
            console.log("success");
            $("#message_text").html("Оценка задания <span style='font-weight: bold;'>" + task + "</span><br>команды <span style='font-weight: bold;'>" + team + "</span> загружена");
            $("#message").fadeIn().delay(5000).fadeOut(2000);
            getSolution();
            $("#upload_value").attr("disabled", null);
        },
        error: function (data) {
            if (data.status == 0) {
                console.log("Ошибка подключения к серверу");
                $("#form_result").text("Ошибка подключения к серверу");
            }
            else {
                console.log(data.responseJSON["error"]);
                $("#form_result").text(data.responseJSON["error"]);
            }
            $("#upload_value").attr("disabled", null);
        }
    });
    }else{
        $("#form_result").text("Заполните все обязательные поля");
    }
});

function getSolution(solution = null) {
    $("#form_result").text("");
    $.ajax({
        url: '/tasks/managetasks',
        method: 'get',
        dataType: 'json',
        data: { "action": "get-solution", "solution": solution },
        success: function (data) {
            $("#upload_value").attr("disabled", null);
            if (data["url"] != null) {
                location = data["url"];
            }
            $("#task").text(data["task"]);
            $("#team").text("Команда " + data["team"]);
            $("#file").text(data["file"]);
            $("#file").attr("href", "/media/solutions/" + data["file"]);
            $("#upload").text(data["upload"]);
            $("#id_score")[0].value = data["score"];
            max_score = data["max-score"];
            team = data["team"];
            task = data["task"];
            solution_id = Number(data["solution-pk"])
        },
        error: function (data) {
            if (data.status == 0) {
                console.log("Ошибка подключения к серверу");
                $("#form_result").text("Ошибка подключения к серверу");
            }
            else {
                console.log(data.responseJSON["error"]);
                $("#form_result").text(data.responseJSON["error"]);
            }
        }
    });
}
getSolution(solution_id);