$(function () {
    console.log('Here');
    bookList();
});

function bookList () {
    $.ajax({
        url: '/api/by-book/',
        type: 'get',
        success: function (data) {
            console.log("SUCCESS", data)
        }
    })
}

// TODO How to handle datatable with ajax request
// TODO How to pass data to html


