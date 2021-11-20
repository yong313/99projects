let checkingVariable = false;

function email_valid_checker() {
  checkingVariable = true;
  let checkedEmail = $("#email-id").val();
  const encodedEmail = window.btoa(checkedEmail);

  localStorage.setItem("checkedEmail", encodedEmail);

  $.ajax({
    type: "POST",
    url: "/api/email",
    data: { email_give: checkedEmail },
    success: function (response) {
      if (response["msg"] == "Not available") {
        checkingVariable = false;
        alert("이미 사용중입니다.");
      } else {
        alert("사용 가능합니다.");
      }
    },
  });
}

function user_register() {
  if (checkingVariable != true) {
    return alert("중복검사를 해주세요!");
  }

  let email = $("#email-id").val();
  let pw = $("#password").val();
  let pw_check = $("#password_check").val();
  let name = $("#name").val();

  if (pw != pw_check) {
    return alert("비밀번호를 확인해주세요!");
  } else {
    const checkedEmail = localStorage.getItem("checkedEmail");
    const decodedEmail = window.atob(checkedEmail);

    if (decodedEmail !== email) {
      checkingVariable = false;
      return alert("중복검사를 다시 해주세요!");
    }
    $.ajax({
      type: "POST",
      url: "/api/user",
      data: {
        email_give: email,
        pw_give: pw,
        name_give: name,
      },
      success: function (response) {
        if (response["msg"] == "success") {
          alert("회원가입 완료!");
          localStorage.removeItem("checkedEmail");
          window.location.href = "/";
        }
      },
    });
  }
}
