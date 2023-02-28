let button = document.getElementsByTagName('button');
let product = document.getElementsByClassName('1');
let l = 0;
let product_page = 5;
let current_page = 1;
let movePer = 1020;
let maxMove = 3040;

let mobile_view = window.matchMedia("(max-width: 768px)");
if (mobile_view.matches)
{
    movePer = 1020;
    maxMove = 3040;
}
let right_mover = (a)=>{
    if (a == 0 || a == 1 ){
        console.log(a)
        product = document.getElementsByClassName('1');
        //product_page = Math.ceil(product.length/4);
    }
    if (a == 2 || a == 3 ){
        console.log(a)
        product = document.getElementsByClassName('2');
        //product_page = Math.ceil(product.length/4);
    }
    if (current_page < product_page) {
        current_page = current_page + 1;
        l = l + movePer;
        if (current_page == 1){ l = 0; }

        for(const i of product)
        {
            if (l > maxMove) {l = l - movePer;}
            i.style.left = '-' + l + 'px';
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
button[3].onclick = ()=>{right_mover(3);}
button[2].onclick = ()=>{left_mover(2);}
