video.addEventListener("timeupdate", function () {
   const played = video.currentTime;
   const duration = video.duration.toFixed(1);
   document.querySelector("#videoplayed").innerHTML = "Abgespielt bis " + played.toFixed(1);
   document.querySelector("#videoplayed").innerHTML += "Zeit bis Ende " + (duration - played).toFixed(1);
}, false);