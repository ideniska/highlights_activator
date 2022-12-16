$(function () {
  randomQuote();
});

var current_quote = 0

function randomQuote() {
  $.ajax({
    url: '/api/q2/random',
    type: 'get',
    success: successRandomQuoteHandler,
    error: function (error) {
      $("#quote-text").html(`You don't have any quotes yet. <a href="/upload">Upload <i class="mdi mdi-cloud-upload me-1"></i></a>`);
    }
  });
}

function successRandomQuoteHandler(data) {
  console.log(data.results[0])
  let api_response = data.results[0]
  let quote = api_response.text;
  let comment = api_response.comment;
  let quote_date = api_response.date_added
  let book = api_response.book
  let book_id = api_response.book_id
  let like = api_response.like
  let cover_url = api_response.cover

  $("#book-title").html(`From: <a href="/by-book-api/${book_id}">${book}</a>`);
  $(".book-cover").html('<img src=' + cover_url + '>');
  $("#quote-text").html(quote);
  if (comment) {
    console.log(comment);
    $(".comment-box").html(comment);
    $(".comment-box").css({
      "visibility": "visible",
      "height": "100px",
    })
  };
  $("#date-added").html(quote_date);
  let current_quote = api_response.quote_id;
  console.log(current_quote);
  $("#like-button").html('<div id="like">' + showCurrentLike(like, current_quote) + '</div>');
  $("#dashboard-delete").attr("quoteid", current_quote);
  $("#dashboard-edit").attr("quoteid", current_quote);
  $(".dashboard-share").html(socialMediaDropdown(current_quote));
}

const socialMediaDropdown = (current_quote) => {
  return `
      <div class="dropdown">
        <div data-bs-toggle="dropdown" aria-expanded="false" id="dash-share" data-quoteId="${current_quote}">
          <i class="fa-solid fa-share-nodes"></i>
        </div>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="#">Twitter</a></li>
          <li><a class="dropdown-item" href="#">Facebook</a></li>
          <li><a class="dropdown-item" href="#">Copy</a></li>
        </ul>
      </div>
  `
}

function showCurrentLike(like, current_quote) {
  if (like) {
    console.log(current_quote);
    return '<span class="liked" id ="heart" data-quoteId="' + current_quote + '"><i class="ri-heart-fill"></i></span>'
  }
  console.log(current_quote);
  return '<span id ="heart" data-quoteId="' + current_quote + '"><i class="ri-heart-line"></i></span>'
};


// LIKE
$(document).on('click', '#heart', function () {
  if ($(this).hasClass("liked")) {
    $(this).html('<i class="ri-heart-line" aria-hidden="true"></i>');
    $(this).removeClass("liked");
    changeLikeStatus($(this).data("quoteid"));
  } else {
    $(this).html('<i class="ri-heart-fill" aria-hidden="true"></i>');
    $(this).addClass("liked");
    changeLikeStatus($(this).data("quoteid"));
  }
});

function changeLikeStatus(quoteId) {
  const csrftoken = getCookie('csrftoken');
  console.log("This is", quoteId)
  $.ajax({
    type: "POST",
    url: `/api/q2/${quoteId}/like/`,
    data: {
      quote_id: quoteId,
      csrfmiddlewaretoken: csrftoken,
    },
    success: function (data) {
      console.log("success", data)
    },
    error: function (data) {
      console.log("error", data)
    }
  })
}


// DELETE
$(document).on('click', '#dashboard-delete', function () {
  console.log("Clicked");
  console.log($("#dashboard-delete").attr("quoteid"));
  deleteQuote($("#dashboard-delete").attr("quoteid"));
});


function deleteQuote(quoteId) {
  const csrftoken = getCookie('csrftoken');
  console.log("This is", quoteId)
  $.ajax({
    type: "DELETE",
    url: `/api/q/${quoteId}/`,
    headers: {
      "X-CSRFToken": csrftoken
    },
    data: {
      quote_id: quoteId,
    },
    success: function (data) {
      console.log("Deleted", data);
      window.location.reload();
    },
    error: function (data) {
      console.log("error", data)
    }
  })
}


// SHARE
$(document).on('click', '#dash-share', function () {

  shareQuote($(this).data("quoteid"));

});


function shareQuote(quoteId) {};

// EDIT AND COMMENT
$(document).on('click', '#dashboard-edit', function () {
  editQuote($(this).data("quoteid"));
});

// EDIT QUOTE, SHOW COMMENT BOX, SHOW CANCEL & SAVE BUTTONS
function editQuote() {
  $("#quote-text").attr('contenteditable', 'true');
  $(".card-text").html('<h5>Edit:</h5>');
  `  $(".comment-text").html('<h5>Comment:</h5>');`
  $("#quote-text").css({
    "background": "#FEFAE0",
  });
  //$(".comment").html('Add note:<div class="comment-box"></div>');
  $(".comment-box").css({
    "visibility": "visible",
    "height": "100px",
  });
  $(".comment-box").attr('contenteditable', 'true');
  $(".comment-box-buttons").css({
    "visibility": "visible",
    "height": "30px",
  });
};

// CANCEL EDIT
$(document).on('click', '#cancel', function () {
  $(".card-text").html('');
  $("#quote-text").attr('contenteditable', 'false');
  $(".comment-box").attr('contenteditable', 'false');
  $("#quote-text").css({
    "background": "white",
  });
  $(".comment-box-buttons").css({
    "visibility": "hidden",
    "height": "0",
  });

  // If no comment clear draft text from comment box
  if (!comment) {
    $(".comment").html('');
    $(".comment-box").css({
      "visibility": "hidden",
      "height": "0",
    });
  }
});

// SAVE EDIT
$(document).on('click', '#save', function () {
  sessionStorage.setItem("quote-text", $('#quote-text').html());
  sessionStorage.setItem("note-text", $('.comment-box').html());
  $("#quote-text").attr('contenteditable', 'false');
  $(".card-text").html('');
  $("#quote-text").css({
    "background": "white",
  });
  $(".comment").html('');
  $(".comment-box").css({
    "visibility": "hidden",
    "height": "0",
  });
  $(".comment-box").attr('contenteditable', 'false');
  $(".comment-box-buttons").css({
    "visibility": "hidden",
    "height": "0",
  });
  var editedQuote = sessionStorage.getItem('quote-text');
  var addedNote = sessionStorage.getItem('note-text');
  saveToServer(current_quote, editedQuote, addedNote);
});


function saveToServer(current_quote, editedQuote, addedNote) {
  const csrftoken = getCookie('csrftoken');
  console.log("This is", current_quote)
  $.ajax({
    type: "PUT",
    url: `/api/q/${quoteId}/`,
    headers: {
      "X-CSRFToken": csrftoken
    },
    data: {
      quote_id: current_quote,
      text: editedQuote,
      comment: addedNote,
    },
    success: function (data) {
      console.log("success", data);
    },
    error: function (data) {
      console.log("error", data)
    }
  })
}