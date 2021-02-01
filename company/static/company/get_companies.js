function createCompanies(companies){
    let m = document.getElementById("main");
    let cards = "";
    if(companies.length==0 && complited.length==0){
        document.getElementById("tasks").innerHTML="Пусто...";
        m.innerHTML='<img src="'+img_empty+'" alt="пусто..." style="width: 60%; margin-top: 3%; margin-bottom: 2%;">\n<p class="lead">Сейчас нет никаких заданий</p>\n<p class="lead">Заходи позже</p>';
    }
    else{
        for (let i=0; i<companies.length; i++){
            let des="";
            // for(let j=0; j<companies["description"].length-2; j++){
            //     if(companies["description"].slice(j,j+2)!="\n")
            // }
            if(companies[i]['description'].length>=270){
                companies[i]['description']=companies[i]['description'].slice(0,267)+"..."
            }
            let count=companies[i]["tasks"]+"";
            let n=parseInt(count.slice(count.length-1), 10);
            // let n=count*0.1;
            if(n==0 ||n>=5){
                count = count+" кейсов"
            }
            else if(n==1){
                count = count+" кейс"
            }
            else if(n<=4){
                count = count+" кейса"
            }
            cards+='<a class="a-card" href="'+companies[i]["pk"]+'">\n<div class="card bg-light mb-4">\n<div class="card-header"><h5>'+companies[i]["name"]+'</h5></div>\n<div class="card-body" style="height: 10em;">\n<p>'+companies[i]["description"]+'</p>\n</div><div class="card-footer"><p>'+count+'</p></div>\n</div>\n</a>\n';
        }
        m.innerHTML=cards;
    }    
}
function getCompanies() {
    let send={"action":"get-companies"}
    $.ajax({
        url: '/company/managecompany',
        method: 'get',
        dataType: 'json',
        data: send,
        success: function (data) {
            createCompanies(data["companies"]);
        },
        error: function () {
            console.log("Ошибка подключения к серверу");
        }
    });
    setTimeout(getCompanies, 60000);
}
getCompanies();