$("#submit").click(function () {
    $.ajax({
        url: '/team/manageteam',
        method: 'post',
        dataType: 'html',
        data: $("#form").serialize(),
        success: function (data) {
            // console.log(data);
            var x=JSON.parse(data);
            // console.log(x);
            $('#name').html(x["data"]["name"]);
            $('#description').html(x["data"]["description"]);
            $('#link').html(x["data"]["link"]);
            l_team=x["data"]["name"];
            l_desc=x["data"]["description"];
            l_link=x["data"]["link"];
            checkForm();
        },
        error: function(data){
            // console.log(data);
            var x=JSON.parse(data);
            // console.log(x);
            $('#error_name').html(x["errors"][0]);
            $('#error_description').html(x["errors"][1]);
            $('#error_link').html(x["errors"][2]);
        }
    });
});