const commentMainInput = document.querySelector("#comment_main_input");
const commentMainButton = document.querySelector("#submit_comment");
const commentList = document.querySelector("#comment_list");
window.addEventListener("load", (event) => {
  showComment();
});
commentMainButton.addEventListener("click", commentSave);

commentList.addEventListener("click", commentLike);

// 댓글 등록시 댓글저장하면서 댓글 클라이언트사이드랜더링
async function commentSave() {
  const comment = commentMainInput.value;
  const thumbnail = `${videoThumbnail}`;
  commentMainInput.value = "";
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    },
    body: `comment=${comment}&thumbnail=${thumbnail}`,
  };
  const response = await fetch("/api/comment_save", options);
  const result = await response.json();
  const msg = await result["msg"];
  console.log(msg);
  commentList.innerHTML = "";
  showComment();
}

// 전체댓글 클라이언트사이드 랜더링
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
    let thumbnail = comments[i]["thumbnail"];
    let likeNum = comments[i]["like_num"];
    let color = comments[i]["color"];
    let temp_html = `
        <div class="list_1" data-no="${commentId}">
          <a href="#" class="list_thumnail">
            <img src="${thumbnail}" alt="" style="width: 80px;height: 45px;">
          </a>
          <div class="list_like">
            <i class="far fa-thumbs-up likeBtn ${color}"></i>
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
    `;
    commentList.insertAdjacentHTML("afterbegin", `${temp_html}`);
  }
}

// 좋아요 눌렀을시
async function commentLike({ target }) {
  if (target.classList.contains("likeBtn")) {
    const comment_id = target.parentElement.parentElement.dataset.no;
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
      },
      body: `comment_id=${comment_id}`,
    };
    const response = await fetch("/api/comment_like", options);
    const result = await response.json();
    const likeNum = await result["like_num"];
    const color = await result["color"];
    target.parentElement.children[1].innerText = likeNum;
    if (color === "grey") {
      target.classList.remove("likeBtn_color");
      target.classList.add("unlikeBtn_color");
    } else {
      target.classList.remove("unlikeBtn_color");
      target.classList.add("likeBtn_color");
    }
  }
}
