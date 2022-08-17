$(function () {
    randomQuote();
});


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
            
        }
    });
}