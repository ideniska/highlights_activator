function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$("#signin").click(function () {
    console.log("inside click")
    $(".login-popup").addClass("active");
    console.log($('.login-popup').attr('class').split(' ')[1])
});

$(function () {
    $("#loginForm").submit(loginHandler);
});



function loginHandler (event) {
    console.log('start login handler')
    let form = $(this)
    console.log(form.serialize())
    event.preventDefault()
    $.ajax({
        url: '/api/login/',
        type: 'post',
        data: form.serialize(),
        success: function (data) {
            console.log('success',data);
            window.location.href = '/dashboard/'
            },
        error: function (data) {
            console.log('error',data);
            var error = document.getElementById("error");
            $("#error").html("")
            var errors = data.responseJSON;
            for (const [key, value] of Object.entries(errors)) {
                 console.log(`${key}: ${value}`);
                 $("#error").append(`${value} <br>`);
                };
            error.style.color = "red";
            },
    })
};