$(function () {
    console.log('Here');
    bookList();
});

function bookList () {
    $.ajax({
        url: '/api/by-book/',
        type: 'get',
        success: function (data) {
            console.log("SUCCESS", data);
            $('.book-table').DataTable(
                {
                  paging: false,
                  "order": [1, 'desc'],
                  "searching": false,
                  "info": false,
                  "data": data.results,
                  "columns": [
                    { "data": "title" },
                    { "data": "quotes_count" },
                    { "data": "visibility" },
                  ]
                }
              );
        }
    })
}

// TODO How to handle datatable with ajax request
// TODO How to pass data to html


