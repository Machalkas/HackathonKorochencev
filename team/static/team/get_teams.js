let m = document.getElementById("main");
function createTeams(teams){
    let cards="";
    if(teams.length==0){
        document.getElementById("teams").innerHTML="Нет команд";
        m.innerHTML='<img src="'+img_empty_street+'" alt="пусто..." style="width: 60%; margin-top: 3%; margin-bottom: 2%;">\n<p class="lead">Ни одна команда не зарегистрировалась 😢</p>';
    }else{
        for(let i=0; i<teams.length; i++){
            cards+='<a class="a-card" href="/team/'+teams[i]["name"]+'">\n<div class="card bg-light mb-4">\n<div class="card-header"><h5>'+teams[i]["name"]+'</h5></div>\n<div class="card-body">\n<p>Счет '+teams[i]['score']+'</p>\n</div>\n</div>\n</a>\n';
        }
        m.innerHTML=cards;
    }
}
function getTeams() {
    let send={"action":"get-teams"}
    $.ajax({
        url: '/team/ajax',
        method: 'get',
        dataType: 'json',
        data: send,
        success: function (data) {
            createTeams(data["teams"]);
        },
        error: function () {
            console.log("Ошибка подключения к серверу");
        }
    });
    setTimeout(getTeams, 60000);
}
getTeams();