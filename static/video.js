const nextVideo = document.querySelector("#next_video");
const leftBox = document.querySelector("#left_box");
const urlBtn = document.querySelector("#url-button");
nextVideo.addEventListener("click", videoLoad);
urlBtn.addEventListener("click", videoSave);
let videoThumbnail;

// const firstVideoThumbnail = document.querySelector('#first_thumbnail')
// console.log(firstVideoThumbnail)

window.addEventListener("load", (event) => {
  videoLoad();
});

async function videoSave() {
  const urlInput = document.querySelector("#url-input");
  const videoUrl = urlInput.value;
  urlInput.value = "";
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    },
    body: `videoUrl=${videoUrl}`,
  };
  const response = await fetch("/api/video/save", options);
  const result = await response.json();
  const msg = await result["msg"];
  console.log(msg);
  alert('동영상 저장 완료!')
}

async function videoLoad() {
  const options = {
    method: "get",
  };
  const response = await fetch("/api/video/load", options);
  const result = await response.json();
  const videoTitle = result["videoTitle"];
  const embedUrl = result["embedUrl"];
  videoThumbnail = result["videoThumbnail"];
  const videoUrl = result["videoUrl"];
  const youtuber = result["youtuber"];
  const temp_html = `
    <div class="video_play">
        <iframe width="100%" height="100%" src="${embedUrl}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>
      <div class="video_information">
        <div class="info_1">
          <p class="rank_text">:교차된_검: 분노의 투기장 - ARENA of ANGER :교차된_검:</p>
          <p class="name_text">${videoTitle}</p>
          <p class="views_text">조회수 554,905회 2021. 10. 30.</p>
        </div>
        <div class="info_2">
          <div class="youtuber_pic"></div>
          <div class="youtuber_info">
            <p class="youtuber_name_text">${youtuber}</p>
            <p class="subscriber_number">구독자 127만명</p>
          </div>
        </div>
        <div class="info_3">
          <div class="like" >
            <i class="far fa-thumbs-up"  id="like_color_change"></i>
            <p class="info_like_number" id="like_color_change_2">
              230,4058
            </p>
          </div>
          <div class="dislike" >
            <i class="far fa-thumbs-down" id="dislike_color_change"></i>
            <p class="info_like_number" id="dislike_color_change_2">
              3058
            </p>
          </div>
        </div>
      </div>
    `;
  leftBox.innerHTML = `${temp_html}`;
}
