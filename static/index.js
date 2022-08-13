var content = document.querySelector(".dashboard-books");
var button = document.getElementById("show-more");


button.onclick = function() {
    content.classList.toggle('dashboard-books');
    console.log('click');
}


// var checkboxes = document.querySelectorAll("#checkbox");
// let enabledSettings = [];

// /*
// For IE11 support, replace arrow functions with normal functions and
// use a polyfill for Array.forEach:
// https://vanillajstoolkit.com/polyfills/arrayforeach/
// */

// // Use Array.forEach to add an event listener to each checkbox.
// checkboxes.forEach(function(checkbox) {
//     checkbox.addEventListener('change', function() {
//       enabledSettings = 
//         Array.from(checkboxes) // Convert checkboxes to an array to use filter and map.
//         .filter(i => i.checked) // Use Array.filter to remove unchecked checkboxes.
//         .map(i => i.value) // Use Array.map to extract only the checkbox values from the array of objects.
        
//       console.log(enabledSettings)
//     })
//   });


document.addEventListener("DOMContentLoaded", function (event) {
    var _selector = document.querySelector('input[type=checkbox]');
    _selector.addEventListener('change', function (event) {
        if (_selector.checked) {
            console.log('Checkbox changed')
        };
    });
});

function test_func(bookId) {
    console.log("This is", bookId)
    $.ajax({
        type: "POST",
        url: "/",
        data: {
            book_id: bookId,
        },
        success: function(data) {
            console.log("success", data)
        },
        error: function(data) {
            console.log("error", data)
        }
    })
}

// создать вью которое будет обрабатывать этот запрос
// TODO как сделать запрос на сервер из js/ jquery ajax