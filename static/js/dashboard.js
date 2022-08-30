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
            $(".like-button").html('<div id="like">'+showCurrentLike(like, current_quote)+'</div>');
            $(".dashboard-delete").html('<div id="dash-delete" data-quoteId="'+current_quote+'"><i class="fa-solid fa-ban"></i></div>');
            $(".dashboard-edit").html('<div id="dash-edit" data-quoteId="'+current_quote+'"><i class="fa-solid fa-pen-to-square"></i></div>');
            $(".dashboard-share").html(
              '<div class="dropdown"><div data-bs-toggle="dropdown" aria-expanded="false" id="dash-share"\
               data-quoteId="'+current_quote+'"><i class="fa-solid fa-share-nodes"></i></div><ul class="dropdown-menu">\
               <li><a class="dropdown-item" href="#">Twitter</a></li><li><a class="dropdown-item" href="#">Facebook</a></li>\
               <li><a class="dropdown-item" href="#">Copy</a></li></ul></div>'
              );
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


// SHARE
$(document).on('click', '#dash-share', function(){

  shareQuote($(this).data("quoteid"));
  
});


function shareQuote(quoteId) { 
};

// EDIT AND COMMENT
$(document).on('click', '#dash-edit', function(){
  editQuote($(this).data("quoteid"));
  addComment($(this).data("quoteid"));
});

// EDIT QUOTE, SHOW COMMENT BOX, SHOW CANCEL & SAVE BUTTONS
function editQuote(quoteid) {
  $("#quote-text").attr('contenteditable', 'true');
  $(".card-text").html('<h5>Edit:</h5>');
  $("#quote-text").css({
    "background" : "#FEFAE0",
  });
  $(".comment").html('Add note:<div class="comment-box"></div>');
  $(".comment-box").css({
    "visibility" : "visible",
    "height": "100px",
  });
  $(".comment-box").attr('contenteditable', 'true');
  $(".comment-box-buttons").css({
    "visibility" : "visible",
    "height": "30px",
  });
};

// CANCEL EDIT
$(document).on('click', '#cancel', function(){
  $("#quote-text").attr('contenteditable', 'false');
  $(".card-text").html('');
  $("#quote-text").css({
    "background" : "white",
  });
  $(".comment").html('');
  $(".comment-box").css({
    "visibility" : "hidden",
    "height": "0",
  });
  $(".comment-box").attr('contenteditable', 'false');
  $(".comment-box-buttons").css({
    "visibility" : "hidden",
    "height": "0",
  });
});