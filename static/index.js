//동영상 좋아요 색상변경 - 블루
const twinkle = document.querySelector("#twinkle");
twinkle.addEventListener("click", onoff);

function like_color_change_blue() {
  document.getElementById("like_color_change").style.color = "#3ea6ff";
  document.getElementById("like_color_change").style.transition = "0.35s";
  document.getElementById("like_color_change_2").style.color = "#3ea6ff";
  document.getElementById("like_color_change_2").style.transition = "0.35s";
}

//동영상 싫어요 색상변경 - 레드
function like_color_change_red() {
  document.getElementById("dislike_color_change").style.color = "#fa4e4e";
  document.getElementById("dislike_color_change").style.transition = "0.35s";
  document.getElementById("dislike_color_change_2").style.color = "#fa4e4e";
  document.getElementById("dislike_color_change_2").style.transition = "0.35s";
}

function onoff({ target }) {
  if (target.classList.contains("uuu")) {
    const { sheet } = Object.assign(
      document.head.appendChild(document.createElement("style")),
      { type: "text/css" }
    );
    const placeholderStyle =
      sheet.rules[sheet.insertRule("::placeholder {}")].style;
    placeholderStyle.color = "#ffffff";

    document.getElementsByClassName("header")[0].style.backgroundColor =
      "#171717";
    document.getElementsByClassName("header")[0].style.borderBottom =
      "1px solid #ffffff";
    document.getElementsByClassName("header")[0].style.transition = "all 0.3s";

    document.getElementsByClassName("user_link_text")[0].style.backgroundColor =
      "#232323";
    document.getElementsByClassName(
      "user_link_button"
    )[0].style.backgroundColor = "#232323";
    document.getElementsByClassName("withdrawal")[0].style.backgroundColor =
      "#232323";
    document.getElementsByClassName("logout_button")[0].style.backgroundColor =
      "#232323";

    document.getElementsByClassName("user_link_button")[0].style.color =
      "#ffffff";
    document.getElementsByClassName("withdrawal")[0].style.color = "#ffffff";
    document.getElementsByClassName("logout_button")[0].style.color = "#ffffff";

    document.getElementsByClassName("name_text")[0].style.color = "#ffffff";
    document.getElementsByClassName("youtuber_name_text")[0].style.color =
      "#ffffff";
    document.getElementsByClassName("user_comment")[0].style.backgroundColor =
      "#171717";
    document.getElementsByClassName("user_comment")[0].style.transition =
      "all 0.3s";
    document.getElementsByClassName("user_comment")[0].style.color = "#ffffff";

    document.getElementsByClassName("left_box")[0].style.backgroundColor =
      "#171717";
    document.getElementsByClassName("left_box")[0].style.transition =
      "all 0.3s";

    document.getElementsByClassName("right_box")[0].style.backgroundColor =
      "#171717";
    document.getElementsByClassName("right_box")[0].style.transition =
      "all 0.3s";

    document.getElementsByClassName("video_play")[0].style.boxShadow =
      "0px 8px 12px #333333";
    document.getElementsByClassName("chat_output")[0].style.boxShadow =
      "0px 5px 12px #333333";
    document.getElementsByClassName("chat_rank")[0].style.boxShadow =
      "0px 5px 12px #333333";

    document.getElementsByClassName("chat_rank")[0].style.color = "#ffffff";
    document.getElementsByClassName("chat_output")[0].style.color = "#ffffff";

    document.getElementsByClassName("logo")[0].style.display = "none";
    document.getElementsByClassName("logo_2")[0].style.display = "block";
    document.getElementsByClassName("logo_2")[1].style.transition = "0.3s";
  }
}
