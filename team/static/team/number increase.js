var delay=0;
var real=0;
function Increase(n,id,real=0){
    if(Math.abs(n-real)>=100000){
        var step=18432;
        // console.log(step);
    }
    else if(Math.abs(n-real)>=10000){
        var step=1243;
        // console.log(step);
    }
    else if(Math.abs(n-real)>=1000){
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
    if (real>=10000000){
        el.style.cssText="font-size:2.5em";
    }
    else if (real>=100000){
        el.style.cssText="font-size:3em";
    }
    else if (real>=10000){
        el.style.cssText="font-size:4em";
    }
    else{
        el.style.cssText="font-size:5em";
    }
    if(real!=n){
        if(Math.abs(n-real)<30)if(delay<100) delay+=2;
        setTimeout(Increase,delay,n,id,real)
    }else{
        delay=0;
    }
}