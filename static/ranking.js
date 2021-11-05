const chatRank = document.querySelector('#check_rank')

window.addEventListener('DOMContentLoaded', (event) => {
  showComment()

})

async function showComment() {
  const options = {
    method: "get",
  };
  const response = await fetch("/api/comment_read", options);
  const result = await response.json();
  const comments = result["all_comments"];
  for (let i = 0; i < comments.length; i++) {
    let comment = comments[i]["content"];
    let commentId = comments[i]["_id"];
    let userName = comments[i]["user_name"];
    let thumbnail = comments[i]["thumbnail"]
    let likeNum = comments[i]["like_num"]
    let temp_html= `
        <div class="list_1" data-no="${commentId}">
          <a href="#" class="list_thumnail">
            <img src="${thumbnail}" alt="" style="width: 80px;height: 45px;">
          </a>
          <div class="list_like">
            <i class="far fa-thumbs-up likeBtn"></i>
            <p class="like_number">${likeNum}</p>
          </div>
          <div class="list_user_info">
            <p class="list_user_name">
              ${userName}
            </p>
            <p class="list_user_text">
            ${comment}
            </p>
          </div>
        </div>
    `
    commentList.insertAdjacentHTML('afterbegin',`${temp_html}`)

  }
}