let button = document.getElementsByTagName('button');
let product = document.getElementsByClassName('1');
let l = 0;
let product_page = 5;
let current_page = 1;
let movePer = 1020;
let maxMove = 3040;
let touchendX = 0;
let end = 0;


function checkDirection() {
    //console.log(touchstartX)
    console.log(end);
    l = end + ankara - touchstartX;
    console.log(l);
    for(const i of product)
        {
            if (l < 0){
                i.style.left =  l*2 + 'px';
            }
            else {
                i.style.left = 0 + 'pc';
            }
        }
  }

let mobile_view = window.matchMedia("(max-width: 768px)");
if (mobile_view.matches)
{
    element = document.getElementsByClassName("products")[0];
    //var bb = document.getElementById("products");

    element.addEventListener("touchstart", (e) => {
    touchstartX = e.changedTouches[0].screenX;
    //console.log(touchstartX);
    });

    element.addEventListener("touchend", (e) => {
    touchendX = e.changedTouches[0].screenX;
    end = end + (touchendX -  touchstartX);
    if (end > 0){
        end = 0;
    }
    });

    element.addEventListener("touchmove", (e) => {
        ankara = e.changedTouches[0].screenX;
        //console.log(ankara);
        checkDirection();
        });
    movePer = 1020;
    maxMove = 3040;
}


let right_mover = (a)=>{
    //console.log("dqsno")
    if (a == 0 || a == 1 ){
        //console.log(a)
        product = document.getElementsByClassName('1');
        //product_page = Math.ceil(product.length/4);
    }
    if (a == 2 || a == 3 ){
        //console.log(a)
        product = document.getElementsByClassName('2');
        //product_page = Math.ceil(product.length/4);
    }
    //console.log(current_page);
    //console.log(product_page);
    if (current_page < product_page) {
        current_page = current_page + 1;
        l = l + movePer;
    
        if (current_page == 1){ l = 0; }
        
        for(const i of product)
        {
              
            //console.log("messi");
            if (l > maxMove) {
                //console.log("moover");
                l = l - movePer;}
            i.style.left = '-' + 100 + 'px';
        }
}
}
let left_mover = (a)=>{
    if (a == 0 || a == 1 ){
        console.log(a);
        product = document.getElementsByClassName('1');
    }
    l = l - movePer;
    if (a == 2 || a == 3 ){
        console.log(a);
        product = document.getElementsByClassName('2');
    }
    if (current_page != 1){
    current_page = current_page - 1;
}
    if (l<=0){l = 0;}
    for(const i of product){
        if (product_page>1){
            i.style.left = '-' + l + 'px';
        }
    }
}
button[1].onclick = ()=>{right_mover(1);}
button[0].onclick = ()=>{left_mover(0);}
//button[3].onclick = ()=>{right_mover(3);}
//button[2].onclick = ()=>{left_mover(2);}
