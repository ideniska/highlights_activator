$(function () {
    bookList();
});

var requestedPage = false;

// GET BOOK LIST FROM API AND SHOW IT AS A TABLE
function bookList () {
    $.ajax({
        url: $(location).attr('href'),
        type: 'get',
        success: console.log(data,  $(location).attr('href')),
    })
};




function QuoteListHandler (data) {
  console.log('QuoteListHandler');
  // for (row of data.results) {
  //     $('.datarows').attr('data-href', data.next);
  //     $('.datarows').append('<tr class="infinite-item"><td><a href="'+row.book_id+'">'+row.title+'</a></td><td>'+row.quotes_count+'</td><td>'+bookVisibility(row.visibility, row.book_id)+'</td></tr>');
  // }
  $.each(data.results, function (i, row) {
    $('.datarows').attr('data-href', data.next);
    $('.datarows').append('<tr class="infinite-item"><td><a href="'+row.book_id+'">'+row.title+'</a></td><td>'+row.quotes_count+'</td><td>'+bookVisibility(row.visibility, row.book_id)+'</td></tr>');
    });
  return true;
} 




