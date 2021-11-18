const chatRank = document.querySelector("#chat_rank");

chatRank.addEventListener("click", commentLike);

window.addEventListener("DOMContentLoaded", (event) => {
  showRanking();
});

async function showRanking() {
  const options = {
    method: "get",
  };
  const response = await fetch("/api/comments/rank", options);
  const result = await response.json();
  const rankers = result["rankers"];
  const temp_html = `
        <div class="list_1" data-no="${rankers[0]["_id"]}">
          <a href="#" class="list_thumnail">
            <img src="${rankers[0]["thumbnail"]}" alt="" style="width: 80px;height: 45px;">
          </a>
          <div class="list_like">
            <i class="far fa-thumbs-up likeBtn" id="rank_gold" ></i>
            <p class="like_number" id="rank_gold">${rankers[0]["like_num"]}</p>
          </div>
          <div class="list_user_info">
            <div class="list_user_form">
              <p class="list_user_name">${rankers[0]["user_name"]}</p>
              <div class="rank_gold"></div>
            </div>
            <p class="list_user_text">
              ${rankers[0]["content"]}
            </p>
          </div>
        </div>
      </div>
      <div class="list_1" data-no="${rankers[1]["_id"]}">
          <a href="#" class="list_thumnail">
            <img src="${rankers[1]["thumbnail"]}" alt="" style="width: 80px;height: 45px;">
          </a>
          <div class="list_like">
            <i class="far fa-thumbs-up likeBtn" id="rank_gold" ></i>
            <p class="like_number" id="rank_gold">${rankers[1]["like_num"]}</p>
          </div>
          <div class="list_user_info">
            <div class="list_user_form">
              <p class="list_user_name">${rankers[1]["user_name"]}</p>
              <div class="rank_silver"></div>
            </div>
            <p class="list_user_text">
              ${rankers[1]["content"]}
            </p>
          </div>
        </div>
      </div>
      <div class="list_1" data-no="${rankers[2]["_id"]}">
          <a href="#" class="list_thumnail">
            <img src="${rankers[2]["thumbnail"]}" alt="" style="width: 80px;height: 45px;">
          </a>
          <div class="list_like">
            <i class="far fa-thumbs-up likeBtn" id="rank_gold" ></i>
            <p class="like_number" id="rank_gold">${rankers[2]["like_num"]}</p>
          </div>
          <div class="list_user_info">
            <div class="list_user_form">
              <p class="list_user_name">${rankers[2]["user_name"]}</p>
              <div class="rank_bronze"></div>
            </div>
            <p class="list_user_text">
              ${rankers[2]["content"]}
            </p>
          </div>
        </div>
      </div>
      
    `;
  chatRank.insertAdjacentHTML("beforeend", `${temp_html}`);
}
