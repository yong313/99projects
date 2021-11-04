const commentMainInput = document.querySelector('#comment_main_input')
const commentMainButton = document.querySelector('#submit_comment')
const commentList = document.querySelector('#comment_list')
window.addEventListener('DOMContentLoaded', (event) => {
  showComment()

})
commentMainButton.addEventListener('click',commentSave)

commentList.addEventListener('click',commentLike)

async function commentSave() {
  const comment = commentMainInput.value;
  const thumbnail = 'https://i.ytimg.com/vi/ZO-zPJpQEb0/maxresdefault.jpg'
  commentMainInput.value = "";
  const options = {
    method: "POST",
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    },
    body: `comment=${comment}&thumbnail=${thumbnail}`
  };
  const response = await fetch("/api/comment_save", options);
  const result = await response.json();
  const msg = await result["msg"];
  console.log(msg)
  commentList.innerHTML=''
  showComment()
}

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
    commentList.insertAdjacentHTML('beforeend',`${temp_html}`)

  }
}

async function commentLike({target}){
  if (target.classList.contains('likeBtn')){
    const comment_id = target.parentElement.parentElement.dataset.no
    const options = {
    method: "POST",
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    },
    body: `comment_id=${comment_id}`
  };
  const response = await fetch("/api/comment_like", options);
  const result = await response.json();
  const likeNum = await result["like_num"];
  target.parentElement.children[1].innerText = likeNum
  }
}
