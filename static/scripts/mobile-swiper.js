// Start of swipe effect
let touchstartX = 0;
let touchendX = 0;

function checkDirection() {
  if (touchendX < touchstartX)
    document.getElementsByClassName("button-alert")[0].click();
  if (touchendX > touchstartX)
    document.getElementsByClassName("button-alert")[1].click();
}

var bb = document.getElementById("products");

bb.addEventListener("touchstart", (e) => {
  touchstartX = e.changedTouches[0].screenX;
  console.log(touchstartX)
});

bb.addEventListener("touchend", (e) => {
  touchendX = e.changedTouches[0].screenX;
  console.log(touchendX)
  checkDirection();
});