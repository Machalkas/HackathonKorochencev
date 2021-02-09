let months = {0:"января", 1:"февраля", 2:"марта", 3:"апреля", 4:"мая", 5:"июня", 6:"июля", 7:"августа", 8:"сентября", 9:"октября", 10:"ноября", 11:"декабря"};

function createSolutions(solutions){
    let m = document.getElementById("main");
    let cards = "";
    if(solutions.length==0){
        document.getElementById("solution-h1").innerHTML="Пусто...";
        m.innerHTML='<img src="'+img_empty+'" alt="пусто..." style="width: 60%; margin-top: 3%; margin-bottom: 2%;">\n<p class="lead">Сейчас нет никаких решений</p>';
    }else{
        document.getElementById("solution-h1").innerHTML="Решения";
        for (let i=0; i<solutions.length; i++){
            solutions[i]['task']="Задание: "+solutions[i]['task'];
            if(solutions[i]['task'].length>=483){
                solutions[i]['task']=solutions[i]['task'].slice(0,483)+"..."
            }
            let valuated="";
            if (solutions[i]['score']==null){
                solutions[i]['score']=0;
            }else{
                valuated="<h6 class='valuated'>оценено</h6>";
            }
            let d=new Date(solutions[i]['created']);
            let h=d.getHours();
            let m=d.getMinutes();
            if(d.getHours()<10){
                h="0"+d.getHours();
            }
            if(d.getMinutes()<10){
                m="0"+d.getMinutes();
            }
            let date=d.getDate()+' '+months[d.getMonth()]+' '+d.getFullYear()+' '+h+":"+m;
            cards+='<a class="a-card" href="view/'+solutions[i]["pk"]+'">\n<div class="card bg-light mb-4">\n<div class="card-header"><h5>'+solutions[i]["team"]+'</h5>'+valuated+'</div>\n<div class="card-body">\n<p>'+solutions[i]['task']+'</p>\n</div>\n<div class="card-footer">\n<p class="card-footer-text card-deadline">загружено<p>\n<p class="card-footer-text card-datetime">'+date+'<p><p class="card-footer-text card-organisation">Балл: '+solutions[i]['score']+' из '+solutions[i]['max-score']+'</p>\n</div>\n</div>\n</a>\n';
        }
        m.innerHTML=cards;
    }    
}
function getSolutions() {
    let send={"action":"get-solutions"}
    $.ajax({
        url: '/tasks/managetasks',
        method: 'get',
        dataType: 'json',
        data: send,
        success: function (data) {
            createSolutions(data["solutions"]);
        },
        error: function () {
            console.log("Ошибка подключения к серверу");
        }
    });
    setTimeout(getSolutions, 60000);
}
getSolutions();