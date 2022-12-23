var parts = $(location).attr('href').split('/');
var lastSegment = parts.pop() || parts.pop(); // handle potential trailing slash
lastSegment_decoded = atob(lastSegment)
var url = '/api/share/' + lastSegment_decoded + '/'

$(function () {
    getQuote();
});

function getQuote() {
    $.ajax({
        url: url,
        type: 'get',
        success: successQuoteHandler,
    })
};

function successQuoteHandler(data) {
    console.log(data)
    let quote = data.text;
    let book = data.book
    $(".card-header").html(`From: ${book}`);
    $(".card-text").html(quote);
}