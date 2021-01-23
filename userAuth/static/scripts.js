var test;
var login_result_form = document.getElementById("login_result_form");
$("#login_submit").click(function () {
    if (checkForm(document.forms["login_form"])) {
        $.ajax({
            url: '/auth/ajax',
            method: 'post',
            dataType: 'html',
            data: $("#login_form").serialize() + "&action=login",
            success: function (data) {
                test = data;
                data = JSON.parse(data);
                location = data["url"];
            },
            error: function (data) {
                data = JSON.parse(data["responseText"]);
                try {
                    login_result_form.innerHTML = data["error"]['email'][0];
                } catch {
                    login_result_form.innerHTML = data["error"];
                }
            }
        })
    }
    else {
        login_result_form.innerHTML = "Заполните все обязательные поля"
    }
});
function checkForm(form) {
    let is_valid = true;
    let elem_valid = [];
    elem_valid.length = form.elements.length;
    for (let i = 0; i < form.elements.length; i++) {
        let valid = true;
        form.elements[i].style = "";
        if (form.elements[i].required && form.elements[i].value == "") {
            form.elements[i].style = "background-color:rgba(248, 37, 37, 0.527);";
            valid = false;
            is_valid = false;
        }
        elem_valid[i] = valid;
    }
    return is_valid;
}