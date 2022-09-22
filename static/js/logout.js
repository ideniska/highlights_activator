$(function () {
    $("#confirmLogout").click(logoutHandler);
});



function logoutHandler () {
    console.log('start logout handler');
    const refresh_token = getCookie('refresh');
    console.log(refresh_token)
    $.ajax({
        url: '/api/logout/',
        type: 'post',
        data: {'refresh':refresh_token},
        success: function (data) {
            console.log('success',data);
            window.location.href = '/landing/'
            },
        error: function (data) {
            console.log('error',data);
            },
    })
};