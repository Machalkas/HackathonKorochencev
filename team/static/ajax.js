$("#submit").click(function () {
    document.getElementById("submit").value = "Загрузка";
    $.ajax({
        url: '/team/manageteam',
        method: 'post',
        dataType: 'html',
        data: $("#form").serialize(),
        success: function (data) {
            // console.log(data);
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
                var x = JSON.parse(data);
                $('#result_form').html("")
                // console.log(x);
            }
            catch {
                $('#result_form').html("Ошибка подключения к серверу")
            }
            $('#error_name').html(x["errors"][0]);
            $('#error_description').html(x["errors"][1]);
            $('#error_link').html(x["errors"][2]);
        }
    });
    document.getElementById("submit").value = "Отправить";
});