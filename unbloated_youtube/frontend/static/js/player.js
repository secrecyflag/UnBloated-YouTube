/* This file will handle all the requirements needed-
 * for the player to work properly.
 * He is currently only used for properly playing audio and video sources
 * together.
 */
var volume = document.getElementById("volume_slider");
var video = document.getElementById("mainvideo");
var audio = document.getElementById("mainaudio");
audio.volume = 0.2;
volume.addEventListener("mousemove", (e)=> {  // volume slider
    audio.volume = e.target.value;            
})
video.addEventListener("pause", (e)=> {  // if the video is paused
    audio.pause();
})
video.addEventListener("play", (e)=> {  // if the video is on, then:
    audio.play();
})
video.addEventListener("seeked", (e)=> {  // if the user changed the position in video, update also in the audio element
    audio.currentTime = video.currentTime;
})
video.addEventListener("waiting", (e)=> {  // if the video needs to buffer
    audio.currentTime = video.currentTime;
})

