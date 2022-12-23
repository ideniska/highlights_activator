$(function () {
  getTenQuotes();
});


function getTenQuotes() {
  $.ajax({
    url: '/api/q2/daily',
    type: 'get',
    success: function (data) {
      console.log(data);
      if (data.length == 0) {
        $("#quote-text").html("You don't have any quotes yet.");
        $("#quote-text2").html("");
      };
      QuoteListHandler(data);
    },
    error: function () {
      $("#quote-text").html("You don't have any quotes yet.");
      $("#quote-text2").html("");
    }
  })
};


function QuoteListHandler(data) {
  console.log('QuoteListHandler');
  console.log(data.results);
  let active = 'active'
  $.each(data.results, function (i, row) {
    console.log(i)
    if (i > 0) {
      active = ''
    };
    $('.carousel-inner').append(carouselItem(row.quote_id, row.book_id, row.book, row.text, row.date_added, row.comment, row.like, active));
    if (row.comment) {
      console.log(row.comment);
      $(".comment-box", "#" + row.quote_id).css({
        "visibility": "visible",
        "height": "100px",
      });
    };
  });
  return true;
};

const carouselItem = (quote_id, book_id, book, text, date_added, comment, like, active) => {
  return `
        <div class="carousel-item ${active}">
          <div id="${quote_id}" class="card">
            <div class="card-body pb-1" style="margin: 0% 10% 0% 10%">
              <div class="d-flex">
                <div class="w-100">
                    <div class="dropdown float-end text-muted">
                      <a href="#" class="dropdown-toggle arrow-none card-drop"
                          data-bs-toggle="dropdown" aria-expanded="false">
                          <i class="mdi mdi-dots-horizontal"></i>
                      </a>
                      <div class="dropdown-menu dropdown-menu-end">
                          <!-- item-->
                          <a class="dropdown-item" id="daily-edit" quoteid=${quote_id}>Edit</a>
                          <!-- item-->
                          <a class="dropdown-item" id="daily-delete" quoteid=${quote_id}>Delete</a>
                      </div>
                    </div>
                  <h5 class="m-0" id="book-title">From: <a href="/by-book-api/${book_id}">${book}</a></h5>
                  <p class="text-muted" id="date-added"><small>${date_added}</small></p>
                </div>
               </div>
              <hr class="m-0" />
              <p class="card-text"></p>
              <div class="font-16 text-center text-dark my-3">
                  <i class="mdi mdi-format-quote-open font-20"></i><span id="quote-text">${text}</span>
              </div>
              <p class="comment-text"></p>
              <div class="comment-box">${comment}</div>
              <hr class="m-0" />
              <div class="my-1">
                <a id="like-button" class="btn btn-sm btn-link text-muted ps-0"><div id="like">${showCurrentLike(like, quote_id)}</div></a>
                <a class="btn btn-sm btn-link text-muted"><i class='uil uil-share-alt'></i>Share</a>
                <span class="comment-box-buttons"><a class="btn btn-sm btn-link text-muted comment-box-buttons" id="cancel" quoteid="${quote_id}">
                  <i class='uil uil-times'></i> Cancel</a>
                  <a class="btn btn-sm btn-link text-muted comment-box-buttons" id="save" quoteid="${quote_id}">
                  <i class='uil uil-bookmark'></i> Save</a></span>
              </div>
            </div> 
          </div>
        </div>
            `
};

function showCurrentLike(like, quoteId) {
  if (like) {
    return '<span class="liked" id ="heart" data-quoteId="' + quoteId + '"><i class="fa fa-heart fa-lg" aria-hidden="true"></i></span>'
  }
  return '<span id ="heart" data-quoteId="' + quoteId + '"><i class="fa fa-heart-o fa-lg" aria-hidden="true"></i></span>'
};


// DELETE
$(document).on('click', '#daily-delete', function () {
  console.log($(this))
  deleteQuote($(this).attr("quoteid"));
});

// LIKE
$(document).on('click', '#heart', function () {
  if ($(this).hasClass("liked")) {
    $(this).html('<i class="fa fa-heart-o fa-lg" aria-hidden="true"></i>');
    $(this).removeClass("liked");
    changeLikeStatus($(this).data("quoteid"));
  } else {
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
      console.log("success", data)
      console.log(document.getElementById(quoteId));
      document.getElementById(quoteId).remove();
      $(".carousel-control-next").click();
    },
    error: function (data) {
      console.log("error", data)
    }
  })
}


// TODO use remove() to delete card from a screen after clicking on delete button

// EDIT AND COMMENT
$(document).on('click', '#daily-edit', function () {
  editQuote($(this).attr("quoteid"));
});

// EDIT QUOTE, SHOW COMMENT BOX, SHOW CANCEL & SAVE BUTTONS
function editQuote(quote_id) {
  $("#quote-text", "#" + quote_id).attr('contenteditable', 'true');
  $(".card-text", "#" + quote_id).html('<h5>Edit:</h5>');
  $("#quote-text", "#" + quote_id).css({
    "background": "#FEFAE0",
  });
  //$(".comment", "#"+quote_id).html('Add note:<div class="comment-box"></div>');
  $(".comment-box", "#" + quote_id).css({
    "visibility": "visible",
    "height": "100px",
  });
  $(".comment-box", "#" + quote_id).attr('contenteditable', 'true');
  $(".comment-box-buttons", "#" + quote_id).css({
    "visibility": "visible",
    "height": "30px",
  });
};

// CANCEL EDIT
$(document).on('click', '#cancel', function () {
  cancelEditQuote($(this).attr("quoteid"));
});

function cancelEditQuote(quote_id) {
  $("#quote-text", "#" + quote_id).attr('contenteditable', 'false');
  $(".card-text", "#" + quote_id).html('');
  $(".comment-text", "#" + quote_id).html('');
  $("#quote-text", "#" + quote_id).css({
    "background": "white",
  });
  $(".comment-box", "#" + quote_id).attr('contenteditable', 'false');
  $(".comment-box-buttons", "#" + quote_id).css({
    "visibility": "hidden",
    "height": "0",
  });

  if (!$(".comment-box", "#" + quote_id).text().length) {
    $(".comment", "#" + quote_id).html('');
    $(".comment-box", "#" + quote_id).css({
      "visibility": "hidden",
      "height": "0",
    });
  }
};

// SAVE EDIT
$(document).on('click', '#save', function () {
  saveEditQuote($(this).attr("quoteid"));
});

function saveEditQuote(quote_id) {
  sessionStorage.setItem("quote-text", $('#quote-text', "#" + quote_id).html());
  sessionStorage.setItem("note-text", $('.comment-box', "#" + quote_id).html());
  $("#quote-text", "#" + quote_id).attr('contenteditable', 'false');
  $(".card-text", "#" + quote_id).html('');
  $("#quote-text", "#" + quote_id).css({
    "background": "white",
  });
  $(".comment", "#" + quote_id).html('');
  $(".comment-box", "#" + quote_id).css({
    "visibility": "hidden",
    "height": "0",
  });
  $(".comment-box", "#" + quote_id).attr('contenteditable', 'false');
  $(".comment-box-buttons", "#" + quote_id).css({
    "visibility": "hidden",
    "height": "0",
  });
  var editedQuote = sessionStorage.getItem('quote-text');
  var addedNote = sessionStorage.getItem('note-text');
  saveToServer(quote_id, editedQuote, addedNote);
};


function saveToServer(quote_id, editedQuote, addedNote) {
  const csrftoken = getCookie('csrftoken');
  console.log("This is", quote_id)
  $.ajax({
    type: "PUT",
    url: `/api/q/${quote_id}/`,
    headers: {
      "X-CSRFToken": csrftoken
    },
    data: {
      quote_id: quote_id,
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
};