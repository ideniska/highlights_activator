var content = document.querySelector(".dashboard-books");
var button = document.getElementById("show-more");


button.onclick = function() {
    content.classList.toggle('dashboard-books');
    console.log('click');
}

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

document.addEventListener("DOMContentLoaded", function (event) {
    var _selector = document.querySelector('input[type=checkbox]');
    _selector.addEventListener('change', function (event) {
        if (_selector.checked) {
            console.log('Checkbox changed')
        };
    });
});

// fetch(request).then(function(response) {
    
// });

function test_func(bookId) {
    const csrftoken = getCookie('csrftoken');
    console.log("This is", bookId)
    $.ajax({
        type: "POST",
        url: `/api/book/${bookId}/visibility/`,
        data: {
            book_id: bookId,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function(data) {
            console.log("success", data)
        },
        error: function(data) {
            console.log("error", data)
        }
    })
}

// создать вью которое будет обрабатывать этот запрос
// TODO как сделать запрос на сервер из js/ jquery ajax