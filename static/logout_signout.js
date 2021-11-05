
const logoutBtn = document.querySelector('#logout')
const signoutBtn = document.querySelector('#signout')

logoutBtn.addEventListener('click', logout)
signoutBtn.addEventListener('click', signout)

function logout() {
            window.location.href='/'
            localStorage.clear();
        }
function signout() {
    let userToken = localStorage.getItem('jwt')
    localStorage.clear();
    $.ajax({
        type: 'POST',
        url: '/api/signout',
        data:{token: userToken},
        success: function(response) {
            alert(response['msg'])
            window.location.href='/'
        }
    })
}

