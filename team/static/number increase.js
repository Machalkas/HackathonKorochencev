var delay=0;
var real=0;
function Increase(n,id,real=0){
    if(Math.abs(n-real)>=1000){
        var step=139;
        // console.log(step);
    }
    else if(Math.abs(n-real)>=100){
        var step=21;
        // console.log(step);
    }else{
        var step=1;
        // console.log(step);
    }
    if (real<n)real+=step;
    else if(real>n)real-=step;
    el=document.getElementById(id);
    el.innerHTML=real;
    if(real!=n){
        if(Math.abs(n-real)<30)if(delay<100) delay+=2;
        setTimeout(Increase,delay,n,id,real)
    }else{
        delay=0;
    }
}