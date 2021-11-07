const inputId = document.querySelector("#input_id");
const inputPw = document.querySelector("#input_pw");

//로그인 창에 이메일 비밀번호 누르면 실행되는 함수
async function login_info() {
  const email = inputId.value;
  const pw = inputPw.value;
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    },
    body: `email=${email}&password=${pw}`,
  };
  const response = await fetch("/api/login", options);
  const result = await response.json();
  //서버에서 로그인이 성공시
  if (result["msg"] == "success") {
    document.cookie("mytoken"=response["token"]);
    // //jwt를 localStorage에 저장
    alert("환영합니다!");
    // 메인페이지로 이동
    window.location.href = "/home";

    //서버에서 로그인 실패시
  } else {
    alert("ID와 비밀번호를 확인해주세요");
  }
}

function signIn() {
  window.location.href = "/register";
}
