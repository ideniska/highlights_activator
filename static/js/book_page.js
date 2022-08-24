$(function () {
    bookList();
  }

);

var requestedPage=false;
var parts=$(location).attr('href').split('/');
var lastSegment=parts.pop() || parts.pop(); // handle potential trailing slash
var url='http://127.0.0.1:8000/api/by-book/'+lastSegment+'/'


// GET BOOK LIST FROM API AND SHOW IT AS A TABLE
function bookList () {
  $.ajax( {

      url: url,
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
  $(".book-title").html(data[0].book);

  $.each(data, function (i, row) {
      $('.datarows').append('<tr><td>'+row.text+'</td><td>'+row.date_added+'</td><td id="like">'+showCurrentLike(row.like, row.quote_id)+'<div id="delete" data-quoteId="'+row.quote_id+'"><i class="fa-solid fa-ban"></i></div></td></tr>');
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
$(document).on('click', '#delete', function(){
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