let months = {0:"января", 1:"февраля", 2:"марта", 3:"апреля", 4:"мая", 5:"июня", 6:"июля", 7:"августа", 8:"сентября", 9:"октября", 10:"ноября", 11:"декабря"};

function createTasks(active, complited){
    let m = document.getElementById("main");
    let cards = "";
    for (let i=0; i<active.length; i++){
        if(active[i]['task'].length>=483){
            active[i]['task']=active[i]['task'].slice(0,483)+"..."
        }
        let d=new Date(active[i]['deadline']);
        let h=d.getHours();
        let m=d.getMinutes();
        if(d.getHours()<10){
            h="0"+d.getHours();
        }
        if(d.getMinutes()<10){
            m="0"+d.getMinutes();
        }
        let date=d.getDate()+' '+months[d.getMonth()]+' '+d.getFullYear()+' '+h+":"+m;
        cards+='<a class="a-card" href="'+active[i]["pk"]+'">\n<div class="card bg-light mb-4">\n<div class="card-header"><h5>'+active[i]["title"]+'</h5></div>\n<div class="card-body">\n<p>'+active[i]['task']+'</p>\n</div>\n<div class="card-footer">\n<p class="card-footer-text card-deadline">дедлайн<p>\n<p class="card-footer-text card-datetime">'+date+'<p><p class="card-footer-text card-organisation">ПУПиПИП</p>\n</div>\n</div>\n</a>\n';
    }
    for (let i=0; i<complited.length; i++){
        if(complited[i]['task'].length>=483){
            complited[i]['task']=complited[i]['task'].slice(0,483)+"..."
        }
        let d=new Date(complited[i]['deadline']);
        let h=d.getHours();
        let m=d.getMinutes();
        if(d.getHours()<10){
            h="0"+d.getHours();
        }
        if(d.getMinutes()<10){
            m="0"+d.getMinutes();
        }
        let date=d.getDate()+' '+months[d.getMonth()]+' '+d.getFullYear()+' '+h+":"+m;
        cards+='<a class="a-card" href="'+complited[i]["pk"]+'">\n<div class="card bg-light mb-4">\n<div class="card-header card-color-complited"><h5>'+complited[i]["title"]+'</h5><h6 class="complited">завершено</h6></div>\n<div class="card-body card-color-complited">\n<p>'+complited[i]['task']+'</p>\n</div>\n<div class="card-footer card-color-complited">\n<p class="card-footer-text card-deadline">дедлайн<p>\n<p class="card-footer-text card-datetime">'+date+'<p><p class="card-footer-text card-organisation">ПУПиПИП</p>\n</div>\n</div>\n</a>\n';
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