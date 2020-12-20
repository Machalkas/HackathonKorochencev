var xhr = new XMLHttpRequest();
var ID, TEAM;
function getScore(team=TEAM,id=ID) {
    ID=id;
    TEAM=team;
    xhr.open("GET", "/team/score?team=" + team, false);
    xhr.send();
}
xhr.onload = function() {
    if (xhr.readyState != 4) return;
  
    // button.innerHTML = 'Готово!';
  
    if (xhr.status != 200) {
    //   alert(xhr.status + ': ' + xhr.statusText);
    } else {
    //   alert(xhr.responseText);
    p=document.getElementById(ID);
    n=Number(xhr.responseText);
    Increase(n,ID,Number(p.innerHTML));
    setTimeout(getScore,60000);
    }
  
  }