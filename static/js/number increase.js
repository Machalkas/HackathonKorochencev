var delay=0;
// var real=0;
function Increase(n,id,real=0){
    if (real<n)real+=1;
    else if(real>n)real-=1;
    el=document.getElementById(id);
    el.innerHTML=real;
    if(real!=n){
        if(n-real<35)if(delay<100) delay+=2;
        setTimeout(Increase,delay,n,id,real)
    }else{
        delay=0;
    }
}