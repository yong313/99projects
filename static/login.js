const inputId = document.querySelector("#input_id");
const inputPw = document.querySelector("#input_pw");

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
  // await안쓸경우(function앞에 async도 빼줘야됨):
  // fetch("/api/login", options)
  // .then((res)=>res.json())
  // .then(result => console.log(result['msg']));
  const response = await fetch("/api/login", options);
  const result = await response.json();
  if (result["msg"] == "success") {
    document.cookie = `mytoken = ${result["token"]}`;
    alert("환영합니다!");
    window.location.href = "/home";
  } else {
    alert("ID와 비밀번호를 확인해주세요");
  }
  // $.ajax({
  //     type: 'POST',
  //     url: '/api/login',
  //     data: {email: email, password: pw},
  //     success: function (response) {
  //         if (response['msg'] == 'success') {
  //             $.cookie('mytoken', response['token']);
  //             alert('환영합니다!')
  //             localStorage.setItem('jwt', response['token'])
  //             window.location.href = '/home'
  //         } else {
  //             alert('ID와 비밀번호를 확인해주세요!')
  //         }
  //     }
  // })
}

function signIn() {
  window.location.href = "/register";
}
