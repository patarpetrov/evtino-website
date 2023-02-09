let button = document.getElementsByTagName('button');
let product = document.getElementsByClassName('secondary-image-child');
let product_page = Math.ceil(product.length/4);
let l = 0;
let current_page = 1;
let movePer = 550;
let maxMove = 1000;
let leftRight = 1;
//left = 0
//right = 1 
let mobile_view = window.matchMedia("(max-width: 768px)");
if (mobile_view.matches)
{
    movePer = 50.36;
    maxMove = 504;
}
let right_mover = ()=>{
    if (leftRight == 1){
    console.log("right");
    if (current_page < product_page) {
        current_page = current_page + 1;
        l = l + movePer;
        if (product == 1){ l = 0; }

        for(const i of product)
        {
            
            if (l > maxMove) {l = l - movePer;}
            i.style.left = '-' + l + '%';
        }
        leftRight = 0;
    }
    }
    else {
        console.log("call left");
        left_mover();
    }   

}
let left_mover = ()=>{
    console.log("function starts")
    if (current_page != 1){
    current_page = current_page - 1;
}
    l = l - movePer;
    if (l<=0){l = 0;}
    for(const i of product){
        if (product_page>1){
            i.style.left = '-' + l + '%';
            leftRight = 1;
        }
    }
}
if (button[0]){
button[0].onclick = ()=>{right_mover();}}

