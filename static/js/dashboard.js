$(function () {
    randomQuote();
});

var current_quote = 0

function randomQuote () {
    $.ajax({
        url: '/api/random/',
        type: 'get',
        success: function (data) {
            console.log("SUCCESS", data);
            var randItem = Math.floor(Math.random() * data.length);
            console.log(data.randItem);
            quote = data[randItem].text;
            quote_date = data[randItem].date_added
            book = data[randItem].book
            like = data[randItem].like
            $(".card-header").html(book);
            $("#quote-text").html(quote);
            $(".blockquote-footer").html(quote_date);
            current_quote = data[randItem].quote_id;
            console.log(current_quote);
            $(".like-button").html('<div id="like">'+showCurrentLike(like, current_quote)+'</div>')
            $(".dashboard-delete").html('<div id="dash-delete" data-quoteId="'+current_quote+'"><i class="fa-solid fa-ban"></i></div>')

        }
    });
}


function showCurrentLike(like, current_quote) {
    if (like) {
        console.log(current_quote);
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


// DELETE
$(document).on('click', '#dash-delete', function(){
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
      },
      success: function(data) {
          console.log("success", data);
          window.location.reload();
      },
      error: function(data) {
          console.log("error", data)
      }
  })
}