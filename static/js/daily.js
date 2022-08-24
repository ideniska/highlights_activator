$(function () {
    bookList();
  }

);


// GET BOOK LIST FROM API AND SHOW IT AS A TABLE
function bookList () {
  $.ajax( {

      url: 'http://127.0.0.1:8000/api/daily/',
      type: 'get',
      success: function (data) {
        console.log(data);
        QuoteListHandler (data);
      }
    }
  )
};


function QuoteListHandler (data) {
  console.log('QuoteListHandler');
  // for (row of data.results) {
  //     $('.datarows').attr('data-href', data.next);
  //     $('.datarows').append('<tr class="infinite-item"><td><a href="'+row.book_id+'">'+row.title+'</a></td><td>'+row.quotes_count+'</td><td>'+bookVisibility(row.visibility, row.book_id)+'</td></tr>');
  // }

  $.each(data, function (i, row) {
      $('.carousel-inner').append(
        '<div class="carousel-item"><div class="card"><div class="card-header">'+row.book+'</div><div class="card-body"><h5 class="card-title"></h5><p class="card-text"></p><blockquote class="blockquote mb-0"><p id="quote-text">'+row.text+'</p><footer class="blockquote-footer">'+row.date_added+'<cite title="Source Title"></footer></blockquote><br><div><div class="like-button" style="display: inline-block;"><div id="like">'+showCurrentLike(row.like, row.quote_id)+'</div></div><div id="daily-delete" style="display: inline-block;" data-quoteid="'+row.quote_id+'"><i class="fa-solid fa-ban"></i></div></div></div></div></div>'
        );
    }

  );
  return true;
};


function showCurrentLike(like, quoteId) {
  if (like) {
    return '<span class="liked" id ="heart" data-quoteId="'+quoteId+'"><i class="fa fa-heart fa-lg" aria-hidden="true"></i></span>'
  }
  return '<span id ="heart" data-quoteId="'+quoteId+'"><i class="fa fa-heart-o fa-lg" aria-hidden="true"></i></span>'
};


// DELETE
$(document).on('click', '#daily-delete', function(){
    console.log($(this))
    deleteQuote($(this).data("quoteid"));
    }
  );

// LIKE
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
          console.log("success", data)
      },
      error: function(data) {
          console.log("error", data)
      }
  })
}