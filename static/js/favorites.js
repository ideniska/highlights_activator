$(function () {
    quoteList();
});


// GET FAV QUOTE LIST FROM API AND SHOW IT AS CARDS
function quoteList () {
    $.ajax({
        url: '/api/favorites/',
        type: 'get',
        success: function (data) {
            console.log(data);
            QuoteListHandler(data);
            },
    })
};


function QuoteListHandler (data) {
    console.log('QuoteListHandler');  
    $.each(data, function (i, row) {
        $('.col-md-4').append(
            '<div class="card"><div class="card-header">'+row.book+'</div><div class="card-body"><h5 class="card-title"></h5><p class="card-text"></p><blockquote class="blockquote mb-0"><p id="quote-text">'+row.text+'</p><footer class="blockquote-footer">'+row.date_added+'<cite title="Source Title"></footer></blockquote><br><div><div class="like-button" style="display: inline-block;"><div id="like">'+showCurrentLike(row.like, row.quote_id)+'</div></div><div id="fav-delete" data-quoteId="'+row.quote_id+'"style="display: inline-block;"><i class="fa-solid fa-ban"></i></div></div></div></div><br>'
        )
      }
  
    );
    return true;
  };

  function showCurrentLike(like, current_quote) {
    if (like) {
      return '<span class="liked" id ="heart" data-quoteId="'+current_quote+'"><i class="fa fa-heart fa-lg" aria-hidden="true"></i></span>'
    }
    console.log(current_quote);
    return '<span id ="heart" data-quoteId="'+current_quote+'"><i class="fa fa-heart-o fa-lg" aria-hidden="true"></i></span>'
  };


  $(document).on('click', '#heart', function(){
    if($(this).hasClass("liked")){
      $(this).html('<i class="fa fa-heart-o fa-lg" aria-hidden="true"></i>');
      $(this).removeClass("liked");
      changeLikeStatus($(this).data("quoteid"));
    }else{
      $(this).html('<i class="fa fa-heart fa-lg" aria-hidden="true"></i>');
      $(this).addClass("liked");
      changeLikeStatus($(this).data("quoteid"));
    }
  });

  function changeLikeStatus(quoteId) {
    const csrftoken = getCookie('csrftoken');
    console.log("This is", quoteId)
    $.ajax({
        type: "POST",
        url: `/api/quote/${quoteId}/like/`,
        data: {
            quote_id: quoteId,
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


// DELETE BUTTON
$(document).on('click', '#fav-delete', function(){
  deleteQuote($(this).data("quoteid"));
  }
);


function deleteQuote(quoteId) {
  const csrftoken = getCookie('csrftoken');
  console.log("This is", quoteId)
  $.ajax({
      type: "DELETE",
      url: `/api/quote/${quoteId}/delete/`,
      headers: {"X-CSRFToken": csrftoken},
      data: {
          quote_id: quoteId,
          csrfmiddlewaretoken: csrftoken,
      },
      success: function(data) {
          console.log("success", data);
          $(this).remove();
      },
      error: function(data) {
          console.log("error", data)
      }
  })
}