var delay=0;
var number=0;
function Increase(n,id){
    el=document.getElementById(id);
    el.innerHTML=number;
    number+=1;
    if(number<=n){
        if(n-number<35)if(delay<100) delay+=2;
        setTimeout(Increase,delay,n,id)
    }else{
        delay=1;
        number=0
    }
}