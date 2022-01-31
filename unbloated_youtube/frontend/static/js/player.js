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
    console.log("pause")
    audio.pause();
    audio.currentTime = video.currentTime;
})
video.addEventListener("playing", (e)=> { // if the video is playing
    console.log("playing")
    audio.play()
})
video.addEventListener("seeked", (e)=> {  // if the user changed the position in video, update also in the audio element
    console.log("seeked")
    audio.currentTime = video.currentTime;
})
video.addEventListener("seeking", (e)=> {  // if the user changed the position in video, update also in the audio element
    console.log("seeking")
    audio.pause();
})
video.addEventListener("ratechange", (e)=> {  // if the video playback speed changed
    console.log("ratechange")
    audio.playbackRate = video.playbackRate;
})

