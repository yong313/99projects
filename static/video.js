function videoSave() {
    let videoUrl = $('#video_save').val();
    
    $.ajax({
        type:'POST',
        url:'/api/video/save',
        data:{videoUrl: videoUrl},
        success: function(response) {
            if(response['msg']=='success') {
                return alert('저장 완료!')
            } else {
                return alert('이미 저장된 동영상입니다!')
            }
        }
    })
}

function videoLoad() {
    $.ajax({
        type:'GET',
        url:'/api/video/load',
        data:{},
        success: function (response) {
            let videoTitle = response['videoTitle']
            let embedUrl = response['embedUrl']
            let videoThumbnail = response['videoThumbnail']

            console.log(videoTitle,embedUrl,videoThumbnail)
        }
    })
}
