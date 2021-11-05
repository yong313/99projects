const nextVideo = document.querySelector('#next_video')
const leftBox = document.querySelector('#left_box')
const urlBtn = document.querySelector('#url-button')
nextVideo.addEventListener('click', videoLoad)
urlBtn.addEventListener('click', videoSave)
let videoThumbnail;

console.log('hi')

window.addEventListener('DOMContentLoaded', (event) => {
  videoLoad()

})

async function videoSave() {
    const urlInput = document.querySelector('#url-input')
    const videoUrl = urlInput.value
    urlInput.value = ''
    const options = {
    method: "POST",
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    },
    body: `videoUrl=${videoUrl}`
  };
  const response = await fetch("/api/video/save", options);
  const result = await response.json();
  const msg = await result["msg"];
  console.log(msg)

}

async function videoLoad() {
    const options = {
    method: "get",
  };
  const response = await fetch("/api/video/load", options);
  const result = await response.json();
  const videoTitle = result['videoTitle']
  const embedUrl = result['embedUrl']
  videoThumbnail = result['videoThumbnail']
  const videoUrl = result['videoUrl']
  const youtuber = result['youtuber']
    const temp_html= `
    <div class="video_play">
      <iframe width="100%" height="100%" src="${embedUrl}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
    <!--동영상정보-->
    <div class="video_information">
      <!--동영상정보: 실시간 순위 / 동영상 제목 / 좋아요&싫어요-->
      <div class="info_1">
        <p class="rank_text">⚔️ 분노의 투기장 - ARENA of ANGER ⚔️</p>
        <p class="name_text">${videoTitle}</p>
      </div>
      <!--유투버사진 / 유투버이름 / 구독자 숫자-->
      <div class="info_2">
        <div class="youtuber_pic"></div>
        <div class="youtuber_info">
          <p class="youtuber_name_text">${youtuber}</p>
        </div>
      </div>
    <!--좋아요&싫어요-->
    </div>
    
    `
    leftBox.innerHTML=`${temp_html}`



}

console.log(videoThumbnail)