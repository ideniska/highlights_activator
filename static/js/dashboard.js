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
            $(".card-text").html(quote_date);
            $("#quote-text").html(quote);
            $(".blockquote-footer").html(book);
            current_quote = data[randItem].quote_id;
            console.log(current_quote);
            
        }
    });
}

function likeQuote(current_quote) {
    const csrftoken = getCookie('csrftoken');
  console.log("Quote #", current_quote)
  $.ajax({
      type: "POST",
      url: `/api/quote/${current_quote}/like/`,
      data: {
          quote_id: current_quote,
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

// TODO API should send 1 quote not 2957
// https://stackoverflow.com/questions/962619/how-to-pull-a-random-record-using-djangos-orm