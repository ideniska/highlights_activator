var content = document.querySelector(".dashboard-books")
var button = document.getElementById("show-more")


button.onclick = function() {
    content.classList.toggle('dashboard-books');
    console.log('click');
}


