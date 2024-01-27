var player
var lecture_list

document.onreadystatechange = function(){
    if(document.readyState == 'interactive'){
        player = document.getElementById("player")
        lecture_list = document.getElementById("lecture_list")

        maintainPlayerRatio()
    }
}

function maintainPlayerRatio(){
    var width = player.clientWidth
    var height = (width*9)/16
    player.height = height
    lecture_list.style.maxHeight = height+"px"

}

window.onresize = maintainPlayerRatio