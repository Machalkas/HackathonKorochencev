$("#submit").click(function () {
    jQuery.ajax()({
        url: 'http://127.0.0.1:8000/team/manageteam',
        method: 'post',
        dataType: 'html',
        data: $("#form").serialize(),
        success: function (data) {
            $('#result_form').html(data);
        },
        error: function(response){
            $('#result_form').html("error");
        }
    });
});