$("#submit").click(function () {
    document.getElementById("submit").value = "Загрузка";
    console.log($("#form").serialize());
    console.log($("#form"));
    $.ajax({
        url: '/team/manageteam',
        method: 'post',
        dataType: 'html',
        data: $("#form").serialize()+"&action=update",
        success: function (data) {
            console.log(data);
            console.log("-------");
            var x = JSON.parse(data);
            // console.log(x);
            $('#name').html(x["data"]["name"]);
            $('#description').html(x["data"]["description"]);
            $('#link').html(x["data"]["link"]);
            l_team = x["data"]["name"];
            l_desc = x["data"]["description"];
            l_link = x["data"]["link"];
            checkForm();
            $('#result_form').html("")
        },
        error: function (data) {
            // console.log(data);
            try {
                var x = JSON.parse(data["responseText"]);
                $('#result_form').html(x["error"])
                // console.log(x);
            }
            catch {
                $('#result_form').html("Ошибка подключения к серверу")
            }
        }
    });
    document.getElementById("submit").value = "Отправить";
});

function leaveTeam(pk) {
    var send={delete_user:pk};
    send={
        action:"delete-members",
        members:{0:pk}
    };
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: '/team/manageteam',
        method: 'post',
        dataType: 'json',
        data: send,
        success: function (data) {
            window.location="/";
        },
        error: function (data) {
            console.log("error");
        },
    });
}