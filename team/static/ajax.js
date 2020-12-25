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
        console.log(data);
        let element=document.getElementById(element_id);
        Increase(Number(data["score"]),element_id,Number(element.innerHTML));
        updateMembers(data["members"]);
    },
    error:function(){
        console.log("Ошибка подключения к серверу")
    }
    });
    setTimeout(update,60000,team_id,element_id);
}

function updateMembers(members){
    let div=document.getElementById('members');
    let data="";
    for (let i=0; i<members.length; i++){
        data+='<div class="row mb-3">\n<div class="col-1 themed-grid-col">\n';
        if (members[i]['is_lider']==true){
            data+='<svg width="1.3em" height="1.3em"\nviewBox="0 0 16 16" class="bi bi-star-fill" fill="gold" xmlns="http://www.w3.org/2000/svg"\nstyle="margin-left:100%">\n<path\nd="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.283.95l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />\n</svg>\n';
        }
        data+='</div>\n<div class="col-3 themed-grid-col">'+members[i]["first_name"]+' '+members[i]["last_name"]+'</div>\n<div class="col-3 themed-grid-col"><a href="mailto:'+members[i]["email"]+'">'+members[i]["email"]+'</a></div>\n<div class="col-3 themed-grid-col">'+members[i]["specialization"]+'</div>\n</div>';
    }
    div.innerHTML=data;
 }