$(function () {
    bookList();
});

var requestedPage = false;

// GET BOOK LIST FROM API AND SHOW IT AS A TABLE
function bookList () {
    $.ajax({
        url: $('.datarows').attr('data-href'),
        type: 'get',
        success: function(data) {
          if (BookListHandler(data)) {requestedPage = false;};
        },
    })
};


$(window).scroll(function() {
  var pagination = $(".datarows")
    if ($(this).height()-pagination.height() <= $(this).scrollTop() && !requestedPage) {
      let nextUrl = $('.datarows').attr('data-href')
      if (nextUrl) {
        requestedPage = true;
        console.log($(this).height(), $(this).scrollTop() , pagination.height());
        console.log('True')
        bookList();
      }
    };
})

function BookListHandler (data) {
  console.log('BookListHandler');
  for (row of data.results) {
      $('.datarows').attr('data-href', data.next);
      $('.datarows').append('<tr class="infinite-item"><td><a href="'+row.book_id+'">'+row.title+'</a></td><td>'+row.quotes_count+'</td><td>'+bookVisibility(row.visibility, row.book_id)+'</td></tr>');
  }
  // $.each(data.results, function (i, row) {
  //   $('.datarows').attr('data-href', data.next);
  //   $('.datarows').append('<tr class="infinite-item"><td><a href="'+row.book_id+'">'+row.title+'</a></td><td>'+row.quotes_count+'</td><td>'+bookVisibility(row.visibility, row.book_id)+'</td></tr>');
  //   });
  return true;
} 


function bookVisibility (visibility, book_id) {
  if (visibility) {
    return '<div class="form-check form-switch"><input data-bookId="'+book_id+'"class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckChecked" checked></div>';
  }
  return '<div class="form-check form-switch"><input data-bookId="'+book_id+'"class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault"></div>';
};


// SAVE CHANGED BOOK VISIBILITY TO DB
$(document).on('change','.form-check-input', function() {
  change_visibility($(this).data("bookid"));
});


function change_visibility(bookId) {
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

var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0]
});

//   console.log(this.data('bookId'));

// SORT TABLE
// const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

// const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
//     v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
//     )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

// // do the work...
// document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
//     const table = th.closest('table');
//     Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
//         .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
//         .forEach(tr => table.appendChild(tr) );
// })));


//TABLE VIA DATATABLE
// function bookList () {
//   $.ajax({
//       url: '/api/by-book/',
//       type: 'get',
//       success: function (data) {
//           console.log("SUCCESS", data);
//           $('.book-table').DataTable(
//               {
//                 paging: false,
//                 "order": [1, 'desc'],
//                 "searching": false,
//                 "info": false,
//                 "data": data.results,
//                 "columns": [
//                   { "data": "title" },
//                   { "data": "quotes_count" },
//                   { "data": "visibility" },
//                 ]
//               }
//             );
//       }
//   })
// }


