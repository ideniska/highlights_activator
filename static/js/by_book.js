$(function () {
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


// SHOW MORE BUTTON
var content = document.querySelector(".dashboard-books");
var button = document.getElementById("show-more");


button.onclick = function() {
    content.classList.toggle('dashboard-books');
    console.log('click');
}


// Checkbox changed event
document.addEventListener("DOMContentLoaded", function (event) {
  var _selector = document.querySelector('input[type=checkbox]');
  _selector.addEventListener('change', function (event) {
      if (_selector.checked) {
          console.log('Checkbox changed')
      };
  });
});



