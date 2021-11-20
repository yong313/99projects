const logoutBtn = document.querySelector("#logout");
const signoutBtn = document.querySelector("#signout");

logoutBtn.addEventListener("click", logout);
signoutBtn.addEventListener("click", signout);

async function logout() {
  const options = {
    //   로그아웃 get방식 맞나? 어차피 데이터 줄거아니니까 상관없을듯
    method: "DELETE",
  };
  const response = await fetch("/api/logout", options);
  //   json()왜 붙여주는 거였더라..?
  const result = await response.json();
  //   msg로 판별하는 거 맞나? 고민필요 경우1)서버에서 불리언 타입으로 설정 경우2) 서버에서 response status로 직접 설정해서 프론트에서 status가 맞도록(아마 이게 가장 확장성 좋은 방식일듯)
  if (result["ok"]) {
    alert("로그 아웃하셨습니다");
    window.location.href = "/";
  } else {
    alert("로그 아웃을 실패하셨습니다");
  }
}
async function signout() {
  //비밀번호 넣는 check있으면 좋을듯
  if (confirm("회원 탈퇴 하시겠습니까?")) {
    const options = {
      //   회원탈퇴 get방식 맞나? 어차피 데이터 줄거아니니까 get이 맞을듯 그래도 확실히 고민해보자 get post 구분기준
      method: "DELETE",
    };
    const response = await fetch("/api/user", options);
    const result = await response.json();
    if (result["ok"]) {
      alert("회원 탈퇴 되셨습니다");
      window.location.href = "/";
    } else {
      alert("회원 탈퇴를 실패하셨습니다");
    }
  }
}
