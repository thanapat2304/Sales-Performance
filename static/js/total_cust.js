$(document).ready(function() {
    $('#table1').DataTable({
        pageLength: 12
    });

    $('#table2').DataTable({
    });
});

function toggleTable(tableId) {
    document.getElementById('page1').classList.add('hidden');
    document.getElementById('page2').classList.add('hidden');

    document.getElementById(tableId).classList.remove('hidden');
}