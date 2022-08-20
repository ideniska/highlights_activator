$(function () {
    quoteList();
});


// GET FAV QUOTE LIST FROM API AND SHOW IT AS CARDS
function quoteList () {
    $.ajax({
        url: '/api/favorites/',
        type: 'get',
        success: function (data) {
            $.each(data, function (i, quote) {
            $('.col-md-4').append(
              '<div data-quoteid="'+quote.quote_id+'" class="card"><div class="card-header">'+quote.book+'</div><div class="card-body"><h5 class="card-title"></h5><p class="card-text"></p><blockquote class="blockquote mb-0"><p id="quote-text">'+quote.text+'</p><footer class="blockquote-footer">'+quote.date_added+'<cite title="Source Title"></footer></blockquote><br><a href="" class="btn btn-success" id="like">LIKE</a></div></div><br>'
            );
            });
        }
    })
};

// SAVE CHANGED QUOTE LIKE TO DB
$(document).on('click','#like', function() {
  console.log('This quote liked: ', $(this).data("quotid"));
  //likeQuote($(this).data("quotid"));
});


function likeQuote(quote_id) {
  const csrftoken = getCookie('csrftoken');
console.log("Quote #", quote_id)
$.ajax({
    type: "POST",
    url: `/api/quote/${quote_id}/like/`,
    data: {
        quote_id: quote_id,
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
