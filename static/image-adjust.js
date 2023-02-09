let img = document.getElementsByClassName('images');
for(const i of img){
    if (i.naturalWidth >= i.naturalHeight){
        i.style.width = '95%';
        i.style.height = 'fit-content';
    }
    if (i.naturalWidth < i.naturalHeight){
        i.style.height = '95%';
        i.style.width = 'fit-content';
    }
}
var rot = 180;
var content = document.getElementById("arrow");
var btn = document.getElementById("button");
if (btn){
btn.addEventListener("click", function() {
    console.log(content.style)
    console.log("2");
    //content.style = 'transform: rotate(' + rot + 'deg)';
    content.style.transform = 'rotate(' + rot + 'deg)';
    rot += 180;
});}
function changeMainImage(p1, p2){
    p1.src = p2.src;
    p1.style.width = p2.style.width;
    p1.style.height = p2.style.height;
    return;
}
imagBackround = document.getElementsByClassName('secondary-image-child');
let old = imagBackround[0];

function selectedImages(old, k, i) {
    console.log("click detected")
    console.log(k)
    k = k + 1;
    if (img[k]){
    old.style.borderColor   = '#F1F1FF';
    old = i;
    i.style.borderColor  = '#2F2FA2';
    changeMainImage(img[1], img[k]); 
    return;
}
};
/*
let n = 1
console.log(Array.from(imgBackground))
Array.from(imgBackground).forEach((item) => {
    item.addEventListener('click', function() {
        console.log("click detected");
        let k = n + 1;
        
        console.log(k);
        if (img[k]){
        old.style.borderColor   = '#F1F1FF';
        old = item;
        item.style.borderColor  = '#2F2FA2';
        img[1].src = img[k].src;
        img[1].style.width = img[k].style.width;
        img[1].style.height = img[k].style.height;
        return;
    }});
});
/*
imgBackground[1].addEventListener('click', selectedImages(old, k, item));
imgBackground[1].addEventListener('click', selectedImages(old, k, item));
imgBackground[1].addEventListener('click', selectedImages(old, k, item));*/
    /*
    i.addEventListener("click", function(){
        old.style.borderColor   = '#F1F1FF';
        old = i;
        i.style.borderColor  = '#2F2FA2';
        k = k + 1;
        changeMainImage(img[1], img[k]); });
}*/
imagBackround[0].addEventListener("click", function(){
    if (img[2]){
    old.style.borderColor   = '#F1F1FF';
    old = imagBackround[0];
    imagBackround[0].style.borderColor  = '#2F2FA2';
    changeMainImage(img[1], img[2])
}
});

imagBackround[1].addEventListener("click", function(){
    if (img[3]){
    old.style.borderColor   = '#F1F1FF';
    old = imagBackround[1];
    imagBackround[1].style.borderColor  = '#2F2FA2';
    
    changeMainImage(img[1], img[3]); }});
imagBackround[2].addEventListener("click", function(){ 
    if (img[4]){
    old.style.borderColor   = '#F1F1FF';
    old = imagBackround[2];
    imagBackround[2].style.borderColor  = '#2F2FA2';
    changeMainImage(img[1], img[4]); }});
imagBackround[3].addEventListener("click", function(){ 
    if (img[5]){
    old.style.borderColor   = '#F1F1FF';
    old = imagBackround[3];
    imagBackround[3].style.borderColor  = '#2F2FA2';
    changeMainImage(img[1], img[5]); }});

imagBackround[4].addEventListener("click", function(){ 
    console.log(img[4])
    if (img[6]){
    old.style.borderColor   = '#F1F1FF';
    old = imagBackround[4];
    imagBackround[4].style.borderColor  = '#2F2FA2';
    changeMainImage(img[1], img[7]); }});
imagBackround[5].addEventListener("click", function(){ 
    if (img[7]){
    old.style.borderColor   = '#F1F1FF';
    old = imagBackround[5];
    imagBackround[5].style.borderColor  = '#2F2FA2';
    changeMainImage(img[1], img[8]); }});
imagBackround[6].addEventListener("click", function(){
    if (img[8]){ 
    old.style.borderColor   = '#F1F1FF';
    old = imagBackround[6];
    imagBackround[6].style.borderColor  = '#2F2FA2';
    changeMainImage(img[1], img[9]); }});
imagBackround[7].addEventListener("click", function(){ 
    if (img[9]){ 
        old.style.borderColor   = '#F1F1FF';
        old = imagBackround[7];
        imagBackround[7].style.borderColor  = '#2F2FA2';
        changeMainImage(img[1], img[10]); }});
