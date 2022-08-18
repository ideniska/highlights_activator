$(function () {
    bookList();
});

function bookList () {
    $.ajax({
        url: '/api/by-book/',
        type: 'get',
        success: function (data) {
            console.log("SUCCESS", data);
            $.each(data.results, function (i, row) {
              console.log(row);
              $('.datarows').append('<tr><td>'+row.title+'</td><td>'+row.quotes_count+'</td><td>'+row.visibility+'</td></tr>');
            });
        }
    })
}

// SORT TABLE
// const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

// const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
//     v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
//     )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

// // do the work...
// document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
//     const table = th.closest('table');
//     Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
//         .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
//         .forEach(tr => table.appendChild(tr) );
// })));


//TABLE VIA DATATABLE
// function bookList () {
//   $.ajax({
//       url: '/api/by-book/',
//       type: 'get',
//       success: function (data) {
//           console.log("SUCCESS", data);
//           $('.book-table').DataTable(
//               {
//                 paging: false,
//                 "order": [1, 'desc'],
//                 "searching": false,
//                 "info": false,
//                 "data": data.results,
//                 "columns": [
//                   { "data": "title" },
//                   { "data": "quotes_count" },
//                   { "data": "visibility" },
//                 ]
//               }
//             );
//       }
//   })
// }

