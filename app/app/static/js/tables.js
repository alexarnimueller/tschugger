$(document).ready(function() {
    $('#paymentsTable').DataTable(
        { "order": [[ 1, "desc" ]],
           aLengthMenu: [
            [10, 25, 50, 100, -1],
            [10, 25, 50, 100, "All"]
          ],
        "columnDefs": [{"targets": [ 8 ], "visible": false, "searchable": true}],  // hide email column}
    });

    $('#peopleTable').DataTable(
        { "order": [[ 2, "asc" ]],
          aLengthMenu: [
            [10, 25, 50, 100, -1],
            [10, 25, 50, 100, "All"]
        ],
        "columnDefs": [{"targets": [ 8 ], "visible": false, "searchable": true},  // hide email column
        {"targets": [6], "width": "15%"}], // width of comment column
    });

    $('#feeTable').DataTable(
        { "order": [[ 0, "desc" ]],
          "paging": false
    });
});
