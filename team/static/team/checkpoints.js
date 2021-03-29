var checkp;
var teams;
var solutions;
var checked;
var rating;

var row = '<div class="row mb-1" style="font-weight: bold;">';
var col = '<div class="col-sm">'
var end_div = '</div>';
var active_checkpoint=null;
var x=null;
function getCheckpoints(is_update=false) {
  $.ajax({
    // headers: {"X-CSRFToken": getCookie("csrftoken")},
    url: '/team/ajax',
    method: 'get',
    dataType: 'json',
    data: { "action": "checkpoint-get-teams" },
    success: function (data) {
      // notification("Успешно!");
      console.log(data);
      x=data;
      if(is_update){
        updateCheckpoints(data);
      }
      else{
      displayCheckpoints(data);
      }
    },
    error: function (data) {
      if(data.status==0){
        notification("Ошибка подключения к серверу", "red");
      }
      // else{
      //   notification(data.responseJSON.error, "red");
      // }
      console.log(data.responseJSON.error);
    },
  });
  // setTimeout(getCheckpoints, 6000);
};
function displayCheckpoints(data) {
  checkp = data["checkpoints"];
  teams = data["teams"];
  solutions = data["solutions"];
  checked = data["checked"];
  rating = data["rating"];
  solutions.sort(function(a,b){//Сортируем список решений по дате(сначала новые)
    a=new Date(a.created)
    b=new Date(b.created)
    if ((a-b)>0){
      return -1
    }
    if ((a-b)<0){
      return 1
    }
    return 0
  });
  let sol_list="";
  for (i in checkp) {//перебираем все чекпоинты
    let t = "";
    for (j in teams) {//перебираем все команды
      t += row;
      t += col;
      t += '<a href="/team/' + teams[j].name + '" target="_blank">' + teams[j].name + '</a>';
      t+='<br><a class="text-dark collapsed" data-toggle="collapse" href="#team-solutions-'+teams[j].id+'_'+checkp[i].id+'" role="button" aria-expanded="false" aria-controls="team-solutions-'+teams[j].id+'_'+checkp[i].id+'"> Решения</a>'+end_div;
      if(solutions.find(item=>item.team==teams[j].id)==undefined){//проверяем есть ли у команды загруженные решения
        sol_list+='<div class="container collapse mt-3 mb-3" id="team-solutions-'+teams[j].id+'_'+checkp[i].id+'" style="background: gainsboro;">'+col+"<p>Пусто</p>"+end_div+end_div;
      }
      else{
        sol_list+='<div class="container collapse mt-3 mb-3" id="team-solutions-'+teams[j].id+'_'+checkp[i].id+'" style="background: gainsboro;">';
          let sl=solutions.filter(item=>item.team==teams[j].id);
          for(l in sl){
            sol_list+=row;
            if(sl[l].solution_file!=""){
              sol_list+=col+'<a href="/media/'+sl[l].solution_file+'" target="_blank">'+sl[l].solution_file.split("/")[1]+'</a>'+end_div;
            }
            else{
              sol_list+=col+'-'+end_div
            }
            if(sl[l].solution_link!=""){
              sol_list+=col+'<a href="'+sl[l].solution_link+'" target="_blank">Ссылка</a>'+end_div;
            }
            else{
              sol_list+=col+'-'+end_div;
            }
            sol_list+=col+parceTime(sl[l]["created"])+end_div;
            sol_list+=end_div;
          }
          sol_list+=end_div;
      }
      t+=col+'<a href="'+teams[j].link+'" target="_blank" class="btn btn-sm btn-blue">Подключится</a>'+ end_div;
      let chk=checked.find(index=>index.team==teams[j].id && index.checkpoint==checkp[i].id);//в checked смотрим проходила ли данная команда данный чекпоинт и записывем результат в chk
      if(chk!=undefined && chk.checkpoint==checkp[i].id){//если проходила то выводим счет и прочую инфу за чекпоинт 
        if(chk.score!=null){
          t+=col+'<p id="score-'+teams[j].id+'_'+checkp[i].id+'">счет:'+chk.score+'</p>'+end_div;
        }
        else{
        t+=col+'<p id="score-'+teams[j].id+'_'+checkp[i].id+'">-</p>'+end_div;
        }
        if(chk.is_came==true){
          t+=col+'<p id="is-came-'+teams[j].id+'_'+checkp[i].id+'">Пришла</p>'+end_div;
        }
        else if(chk.is_came==false && chk.is_came!=undefined){
          t+=col+'<p id="is-came-'+teams[j].id+'_'+checkp[i].id+'">Не пришла</p>'+end_div;
        }
        else{
          t+=col+'<p id="is-came-'+teams[j].id+'_'+checkp[i].id+'">-</p>'+end_div;
        }
      }
      else{
        t+=col+'<p id="score-'+teams[j].id+'_'+checkp[i].id+'">-</p>'+end_div+col+'<p id="is-came-'+teams[j].id+'_'+checkp[i].id+'">-</p>'+end_div;
      }
      evaluate_list='';//далее в переменную evaluate_list генерируем формы выставления баллов для команды
      if (isActive(checkp[i])){//но сначала проверим что чекпоинт активен
        t+=col+'<a class="collapsed btn btn-sm btn-primary" data-toggle="collapse" href="#team-evaluate-'+teams[j].id+'_'+checkp[i].id+'" role="button" aria-expanded="false" aria-controls="team-evaluate-'+teams[j].id+'_'+checkp[i].id+'">Оценить</a>'+end_div;
        if(checked.find(index=>index.team==teams[j].id && index.checkpoint==checkp[i].id)==undefined || checked.find(index=>index.team==teams[j].id && index.checkpoint==checkp[i].id).is_came==false){//проверяем пришла команда на чекпоинт или нет
        t+=col+'<a class="btn btn-sm btn-success" onclick="changeIsCame('+teams[j].id+','+checkp[i].id+')" id="btn-is-came-'+teams[j].id+'_'+checkp[i].id+'">Команда пришла</a>'+end_div;
        }else{
          t+=col+'<a class="btn btn-sm btn-danger" onclick="changeIsCame('+teams[j].id+','+checkp[i].id+')" id="btn-is-came-'+teams[j].id+'_'+checkp[i].id+'">Команда не пришла</a>'+end_div;
        }
        evaluate_list+='<div class="container collapse mt-3 mb-3" id="team-evaluate-'+teams[j].id+'_'+checkp[i].id+'" style="background: thistle;"><form method="post" class="form mt-3" id="evaluate-form-'+teams[j].id+'_'+checkp[i].id+'" onchange="checkForm('+teams[j].id+','+checkp[i].id+')">';
        for(r in rating){
          evaluate_list+='<label>'+rating[r].name+'</label><input type="number" class="form-control mt-1" style="max-width: 4em;margin-left: auto;margin-right: auto;" name="'+rating[r].id+'_'+teams[j].id+'_'+checkp[i].id+'"><p style="color: dimgray; font-size: small;">max '+rating[r].max+'</p>';
        }
        evaluate_list+='<p style="font-size:1.5em; color:red;">Итого</p><p style="font-size:1.8em; color:red;" id="total'+teams[j].id+'_'+checkp[i].id+'">0</p><div class="info" onclick="getInfo()">?</div>';
        evaluate_list+='<input type="button" value="Сохранить" class="btn btn-primary btn-blue mt-3 mb-3" required onclick="submitForm('+j+','+i+')"></form>'+end_div;
      }
      else{
        t+=col+end_div;
      }
      t+=end_div;
      t+=evaluate_list;
      t+=sol_list+"<hr>";
      sol_list="";
    }
    $("#checkpoint" + checkp[i].id).html(t);//выводим все что сгенерировали в чекпоинт
    if(isActive(checkp[i])){
      $("#div-checkpoint" + checkp[i].id).css({"border":"solid forestgreen","border-width":"2px", "border-radius":"10px"})//выделяем зеленой рамкой активный чекпоинт
    }
    else{
      $("#div-checkpoint" + checkp[i].id).css({"border":"solid grey","border-width":"2px", "border-radius":"10px"})//и серой не активный
    }
  }
}

function parceTime(time){
let x=time.split("T")[0].split("-")
return x[2]+"."+x[1]+"."+x[0]+" "+time.split("T")[1].split(".")[0];
}
function isActive(cp){
let now=new Date();
let s=new Date(cp.start_date);
let e=new Date(cp.end_date);

if(now-s>=0 && now-e<=0){
  active_checkpoint=cp.id;
  return true;
}
else{
  return false;
}
}
function wait(){
if(active_checkpoint==null){
 setTimeout(wait,10); 
}
else{
  $("#checkpoint" + active_checkpoint).attr("class","container collapse show");
}
}
function checkForm(t,c){
let form=$("#evaluate-form-"+t+"_"+c);
let count=0;
for(let i in rating){
  let inpt=form.find("input[name="+rating[i].id+"_"+t+"_"+c+"]")
  if(inpt.val()!=null){
  if (inpt.val()>rating[i].max){
    inpt.val(rating[i].max);
  }
  else if (inpt.val()<0){
    inpt.val(0);
  }
  count+=Number(inpt.val())+(Number(inpt.val())*rating[i].cof);
}
}
$("#total"+t+"_"+c).text(count);
return count;
}
function submitForm(t,c){
let count=checkForm(teams[t].id,checkp[c].id);
console.log(teams[t].name);
console.log(checkp[c].title);
showModal("Загрузка решения","Вы уверены, что хотите отправить "+count+" баллов команде "+teams[t].name+" за чекпоинт "+checkp[c].title+"?", '<button type="button" class="btn btn-secondary btn-green header-join" data-dismiss="modal" id="modal-cancel" onclick="sendForm('+t+','+c+')">Подтвердить</button><button type="button" class="btn btn-primary btn-red header-logout"  data-dismiss="modal" id="modal-submit" onclick="">Отмена</button>');
}
function sendForm(t,c){
let send={"action":"checkpoint-send-form", "team":teams[t].id, "checkpoint":checkp[c].id, "score":checkForm(teams[t].id,checkp[c].id)};
$.ajax({
    headers: {"X-CSRFToken": getCookie("csrftoken")},
    url: '/team/ajax',
    method: 'post',
    dataType: 'json',
    data: send,
    success: function (data) {
      notification("Успешно!");
      console.log(data);
      x=data;
      getCheckpoints(true);
    },
    error: function (data) {
      if(data.status==0){
        notification("Ошибка подключения к серверу", "red");
      }
      else{
        notification(data.responseJSON.error, "red");
      }
      console.log(data.responseJSON.error);
      getCheckpoints(true);
    },
  });
}
function getInfo(){
$("#div-info").fadeIn(100);
}
function changeIsCame(t,c){
let btn=$("#btn-is-came-"+t+"_"+c);
let send={action:"isCame", team:t, checkpoint:c}
if(btn.hasClass("btn-success")){
  send.is_came=true;
  btn.toggleClass("btn-success");
}
else if(btn.hasClass("btn-danger")){
  send.is_came=false;
  btn.toggleClass("btn-danger");
}
else{
  alert("Подождите");
  return ;
}
btn.toggleClass("btn-warning");
btn.text("Загрузка");
$.ajax({
    headers: {"X-CSRFToken": getCookie("csrftoken")},
    url: '/team/ajax',
    method: 'post',
    dataType: 'json',
    data: send,
    success: function (data) {
      notification("Успешно!");
      console.log(data);
      x=data;
      btn.toggleClass("btn-warning");
      console.log(data["is_came"])
      if(data["is_came"]){
        btn.toggleClass("btn-danger");
        btn.text("Команда не пришла");
      }
      else{
        btn.toggleClass("btn-success");
        btn.text("Команда пришла");
      }
      getCheckpoints(true);
    },
    error: function (data) {
      if(data.status==0){
        notification("Ошибка подключения к серверу", "red");
      }
      else{
        notification(data.responseJSON.error, "red");
      }
      btn.text("Ошибка")
      console.log(data.responseJSON.error);
      getCheckpoints(true);
    },
  });
}
function updateCheckpoints(data){
console.log("update")
checkp = data["checkpoints"];
teams = data["teams"];
solutions = data["solutions"];
checked = data["checked"];
rating = data["rating"];
sol_list="";
for (i in checkp) {
    for (j in teams) {
      //обновляем решения
      if(solutions.find(item=>item.team==teams[j].id)==undefined){
        sol_list=col+"<p>Пусто</p>"+end_div;
      }
      else{
          sol_list="";
          let sl=solutions.filter(item=>item.team==teams[j].id);
          for(l in sl){
            sol_list+=row;
            if(sl[l].solution_file!=""){
              sol_list+=col+'<a href="/media/'+sl[l].solution_file+'" target="_blank">'+sl[l].solution_file.split("/")[1]+'</a>'+end_div;
            }
            else{
              sol_list+=col+'-'+end_div
            }
            if(sl[l].solution_link!=""){
              sol_list+=col+'<a href="'+sl[l].solution_link+'" target="_blank">Ссылка</a>'+end_div;
            }
            else{
              sol_list+=col+'-'+end_div;
            }
            sol_list+=col+parceTime(sl[l]["created"])+end_div;
            sol_list+=end_div;
          }
          sol_list+=end_div;
      }
      $("#team-solutions-"+teams[j].id+"_"+checkp[i].id).html(sol_list);
      
      //обновляем счет, статус и кнопку 
      let score=$("#score-"+teams[j].id+"_"+checkp[i].id);
      let is_came=$("#is-came-"+teams[j].id+"_"+checkp[i].id);
      let btn=$("#btn-is-came-"+teams[j].id+"_"+checkp[i].id);
      let chk=checked.find(index=>index.team==teams[j].id && index.checkpoint==checkp[i].id);//в checked смотрим проходила ли данная команда данный чекпоинт и записывем результат в chk
      if(chk!=undefined && chk.checkpoint==checkp[i].id){//если проходила то выводим счет и прочую инфу за чекпоинт 
        if(chk.score!=null){
          score.text('счет:'+chk.score);
        }
        else{
          score.text('-');
        }
        if(chk.is_came==true){
          is_came.text("Пришла");
          btn.removeClass("btn-success");
          btn.addClass("btn-danger");
          btn.text("Команда не пришла");
        }
        else if(chk.is_came==false && chk.is_came!=undefined){
          is_came.text("Не пришла");
          btn.removeClass("btn-danger");  
          btn.addClass("btn-success");
          btn.text("Команда пришла");             
        }
        else{
          is_came.text("-");
          btn.removeClass("btn-danger"); 
          btn.addClass("btn-success");
          btn.text("Команда пришла");
        }
      }
      else{
        is_came.text("-");
        score.text('-');
        btn.removeClass("btn-danger"); 
        btn.addClass("btn-success");
        btn.text("Команда пришла");
      }
    }
  }
}

function update(){
  // console.log(checkp.find(item=>item.id==active_checkpoint));
  if(checkp!=undefined && isActive(checkp.find(item=>item.id==active_checkpoint))==false){
    window.location.reload();
  }
  console.log("not now");
}

wait();
getCheckpoints();
setInterval(getCheckpoints, 60000, true);
update();
setInterval(update, 1000);