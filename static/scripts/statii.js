/*var div = document.getElementsByClassName('homepage-statii-content');
console.log(typeof div[0]);

for(const statii in div)
{
    statii.style.display="none";
}
*/
var div = document.getElementsByClassName('homepage-statii-content');
div[0].style.display ="grid";
function statii1(number){
    for (var i=0;i<div.length;i+=1){
        div[i].style.display = 'none';
      }
    div[number].style.display = "grid";
}