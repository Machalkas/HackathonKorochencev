let months = {0:"января", 1:"февраля", 2:"марта", 3:"апреля", 4:"мая", 5:"июня", 6:"июля", 7:"августа", 8:"сентября", 9:"октября", 10:"ноября", 11:"декабря"};
function formDateTime(datetime){
    let d=new Date(datetime);
    let h=d.getHours();
    let m=d.getMinutes();
    if(d.getHours()<10){
        h="0"+d.getHours();
    }
    if(d.getMinutes()<10){
        m="0"+d.getMinutes();
    }
    return d.getDate()+' '+months[d.getMonth()]+' '+d.getFullYear()+' '+h+":"+m;
}