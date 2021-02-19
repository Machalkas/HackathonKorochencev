var test;
var login_result_form = document.getElementById("login_result_form");
var singup_result_form = document.getElementById("singup_result_form");
var style="border-color:red;";
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
                let next=$.urlParam('next');
                if (next){
                    location=next
                }
                else{
                location = data["url"];
                }
            },
            error: function (data) {
                data = JSON.parse(data["responseText"]);
                console.log(data);
                let errors="";
                errors+='<p class="lead" style="font-size: 1em;">'+data["error"]+'</p>\n';
                login_result_form.innerHTML=errors;
                login_result_form.style=style;
            }
        })
    }
    else {
        login_result_form.innerHTML = "Заполните все обязательные поля"
        login_result_form.style=style;
    }
});
$("#singup_submit").click(function () {
    if (checkForm(document.forms["singup_form"])) {
        $.ajax({
            url: '/auth/ajax',
            method: 'post',
            dataType: 'html',
            data: $("#singup_form").serialize() + "&action=singup",
            success: function (data) {
                test = data;
                data = JSON.parse(data);
                let next=$.urlParam('next');
                if (next){
                    location=next
                }
                else{
                location = data["url"];
                }
            },
            error: function (data) {
                data = JSON.parse(data["responseText"]);
                console.log(data);
                let errors="";
                try{
                    for(let i of data["error"]['email']){
                        // console.log(i);
                        errors+='<p class="lead" style="font-size: 1em;">'+i+'</p>\n';
                    }
                }
                catch{}
                try{
                    for(let i of data["error"]['password2']){
                        // console.log(i);
                        errors+='<p class="lead" style="font-size: 1em;">'+i+'</p>\n';
                    }
                }
                catch{}
                singup_result_form.innerHTML=errors;
                singup_result_form.style=style;
            }
        })
    }
    else {
        singup_result_form.innerHTML = "Заполните все обязательные поля";
        singup_result_form.style=style;
    }
});

$.urlParam = function(name){
    try{
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	return results[1] || 0;
    }
    catch (TypeError){
        return null;
    }
}
// function checkForm(form) {
//     let is_valid = true;
//     let elem_valid = [];
//     elem_valid.length = form.elements.length;
//     for (let i = 0; i < form.elements.length; i++) {
//         let valid = true;
//         form.elements[i].style = "";
//         if (form.elements[i].required && form.elements[i].value == "") {
//             form.elements[i].style = "background-color:rgba(248, 37, 37, 0.527);";
//             valid = false;
//             is_valid = false;
//         }
//         elem_valid[i] = valid;
//     }
//     return is_valid;
// }