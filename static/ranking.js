const chatRank = document.querySelector('#chat_rank')

chatRank.addEventListener('click',commentLike)

window.addEventListener('DOMContentLoaded', (event) => {
  showRanking()

})

async function showRanking() {
  const options = {
    method: "get",
  };
  const response = await fetch("/api/comment_ranking", options);
  const result = await response.json();
  const rankers = result["rankers"];
  for (let i = 0; i < rankers.length; i++) {
      let comment = rankers[i]["content"];
      let commentId = rankers[i]["_id"];
      let userName = rankers[i]["user_name"];
      let thumbnail = rankers[i]["thumbnail"]
      let likeNum = rankers[i]["like_num"]
      const temp_html = `
        <div class="list_1" data-no="${commentId}">
          <a href="#" class="list_thumnail">
            <img src="${thumbnail}" alt="" style="width: 80px;height: 45px;">
          </a>
          <div class="list_like">
            <i class="far fa-thumbs-up likeBtn" id="rank_gold" ></i>
            <p class="like_number" id="rank_gold">${likeNum}</p>
          </div>
          <div class="list_user_info">
            <div class="list_user_form">
              <p class="list_user_name">${userName}</p>
              <div class="rank_gold"></div>
            </div>
            <p class="list_user_text">
              ${comment}
            </p>
          </div>
        </div>
      </div>
      
    `
      chatRank.insertAdjacentHTML('beforeend', `${temp_html}`)

  }
}