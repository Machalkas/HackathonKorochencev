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
                $('#result_form').html(x["error"]["name"]["0"])
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
    let send={
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

function update(team_id, element_id){
    let send={
        action:"request",
        team:team_id
    }
    $.ajax({
    headers: { "X-CSRFToken": token },
    url: '/team/manageteam',
    method: 'get',
    dataType: 'json',
    data:send,
    success: function(data){
        // console.log(data);
        let element=document.getElementById(element_id);
        Increase(Number(data["score"]),element_id,Number(element.innerHTML));
    }
    });
    setTimeout(update,1000,team_id,element_id);
}