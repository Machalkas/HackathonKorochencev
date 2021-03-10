// let months = {0:"января", 1:"февраля", 2:"марта", 3:"апреля", 4:"мая", 5:"июня", 6:"июля", 7:"августа", 8:"сентября", 9:"октября", 10:"ноября", 11:"декабря"};

function createTasks(tasks){
    let m = document.getElementById("main");
    let cards = "";
    let selected=""
    if(tasks.length==0){
        document.getElementById("tasks").innerHTML="Пусто...";
        m.innerHTML='<img src="'+img_empty+'" alt="пусто..." style="width: 60%; margin-top: 3%; margin-bottom: 2%;">\n<p class="lead">Сейчас нет никаких заданий</p>\n<p class="lead">Заходи позже</p>';
    }else{
        tasks.sort(function(a,b){return b["selected"]-a["selected"]});
        document.getElementById("tasks").innerHTML="Задания";
        for (let i=0; i<tasks.length; i++){
            if(tasks[i]['task'].length>=483){
                tasks[i]['task']=tasks[i]['task'].slice(0,483)+"..."
            }
            if (tasks[i]['selected']){
                selected='style="border-color:forestgreen"';
            }
            else{
                selected="";
            }
            cards+='<a class="a-card" href="view/'+tasks[i]["pk"]+'">\n<div class="card bg-light mb-4" '+selected+'>\n<div class="card-header"><h5>'+tasks[i]["title"]+'</h5></div>\n<div class="card-body">\n<p>'+tasks[i]['task']+'</p>\n</div>\n<div class="card-footer">\n<p class="card-footer-text card-deadline"></p>\n<p class="card-footer-text card-datetime"></p><p class="card-footer-text card-score">Выбрано '+tasks[i]['teams']+' раз</p><p class="card-footer-text card-organisation">'+tasks[i]['company']+'</p>\n</div>\n</div>\n</a>\n';
        }
        m.innerHTML=cards;
    }    
}
function getTasks() {
    let send={"action":"get-tasks"}
    $.ajax({
        url: '/tasks/managetasks',
        method: 'get',
        dataType: 'json',
        data: send,
        success: function (data) {
            createTasks(data["tasks"]);
        },
        error: function () {
            console.log("Ошибка подключения к серверу");
        }
    });
    setTimeout(getTasks, 60000);
}
getTasks();