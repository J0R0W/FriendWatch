const video = document.getElementById("video");
const player = document.querySelector('.c-video');
const progressBar = player.querySelector('#videoProgressBar');
const seekBar = video
var lastSeeked = 0;
var blockSeekedEvent = false;
var seekingEventTriggered = false;
console.log(video)
video.addEventListener('play', videoPausePlayHandler, false);
video.addEventListener('pause', videoPausePlayHandler, false);
video.addEventListener('seeked', videoSeekPlayHandler, false);
//video.addEventListener('seeking', videoSeekPlayHandler, false);
progressBar.addEventListener('mousedown', mouseClickDown, false);
progressBar.addEventListener('mouseup', mouseClickUp, false);
var mouseDown = 0;
function mouseClickDown() {

  ++mouseDown;
  $("#hhh").text(mouseDown);
}
function mouseClickUp() {
    setTimeout(function(){ --mouseDown; $("#hhh").text(mouseDown);}, 200);

}

function videoPausePlayHandler(e) {
    if (e.type == 'play') {
        console.log("Play")
        $.ajax({
            url: '/videoStatus',
            data: {
                event: "play",
                time: video.currentTime,
                id: $("#hiddenCode").val()
            },
            type: 'POST',
            mimeType: 'application/json',
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        }).done(function (data) {
            if ((!data.error)) {
                if (data.updated) {
                    video.currentTime = data.time;
                }
            }
        });
    } else if (e.type == 'pause') {
        console.log("Pause")
        $.ajax({
            url: '/videoStatus',
            data: {
                event: "pause",
                time: video.currentTime,
                id: $("#hiddenCode").val()
            },
            type: 'POST',
            mimeType: 'application/json',
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}

function videoSeekPlayHandler(e) {
    console.log(e.type)
    //to avoid a loop we check if the Mouse is clicked and event is called by User and not by SeekedUpdate
    if(blockSeekedEvent)
    {
        blockSeekedEvent = false;
        return ;
    }
    //video.pause();
    if (true) {
        seekingEventTriggered = false;
        lastSeeked = performance.now();
        console.log("Seeked")
        $.ajax({
            url: '/videoStatus',
            data: {
                event: "seeked",
                time: video.currentTime,
                id: $("#hiddenCode").val()
            },
            type: 'POST',
            mimeType: 'application/json',
            success: function (response) {
                //console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        });
    }

}

setInterval(function () {
    $.ajax({
        url: '/updateVideo',
        data: {
            time: video.currentTime,
            id: $("#hiddenCode").val()
        },
        type: 'POST',
        mimeType: 'application/json',
        success: function (response) {
            //console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    }).done(function (data) {
        if ((!data.error)) {
            if (data.updated) {
                video.currentTime = data.time;
                blockSeekedEvent = true;
            }

            if (data.status == 'pause') {
                video.pause();
            } else if (data.status == 'play') {
                video.play();
            }
        }
    })
}, 1 * 1000);
