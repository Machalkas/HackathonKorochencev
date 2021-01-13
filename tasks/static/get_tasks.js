function createTasks(active, complited){
    let m = document.getElementById("main");
    let cards = "";
    for (let i=0; i<active.length; i++){
        if(active[i]['task'].length>=483){
            active[i]['task']=active[i]['task'].slice(0,483)+"..."
        }
        cards+='<div class="card bg-light mb-4" style="max-width: 30rem; margin-left: auto; margin-right: auto;">\n<div class="card-header"><h5>'+active[i]["title"]+'</h5></div>\n<div class="card-body">\n<p class="card-text">'+active[i]['task']+'</p>\n</div>\n</div>\n';
    }
    for (let i=0; i<complited.length; i++){
        if(complited[i]['task'].length>=483){
            complited[i]['task']=complited[i]['task'].slice(0,483)+"..."
        }
        cards+='<div class="card bg-light mb-4" style="max-width: 30rem; margin-left: auto; margin-right: auto;">\n<div class="card-header"><h5 class="card-title-complited">'+complited[i]["title"]+'</h5><h6 class="card-title-complited complited">завершено</h6></div>\n<div class="card-body">\n<p class="card-text card-title-complited">'+complited[i]['task']+'</p>\n</div>\n</div>\n';
    }
    m.innerHTML=cards;    
}
function getTasks() {
    let send={"action":"get-tasks"}
    $.ajax({
        url: '/tasks/managetasks',
        method: 'get',
        dataType: 'json',
        data: send,
        success: function (data) {
            createTasks(data["active"], data["complited"]);
        },
        error: function () {
            console.log("Ошибка подключения к серверу");
        }
    });
    setTimeout(getTasks, 60000);
}
getTasks();