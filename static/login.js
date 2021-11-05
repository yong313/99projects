function login_info() {
    let email = $('#input_id').val();
    let pw = $('#input_pw').val();

    $.ajax({
        type: 'POST',
        url: '/api/login',
        data: {email: email, password: pw},
        success: function (response) {
            if (response['msg'] == 'success') {
                $.cookie('mytoken', response['token']);
                alert('환영합니다!')
                localStorage.setItem('jwt', response['token'])
                window.location.href = '/home'
            } else {
                alert('ID와 비밀번호를 확인해주세요!')
            }
        }
    })
}

function signIn() {
    window.location.href = '/register'
}