function getPontaj(id) {
    var row = document.getElementById("pontaj-" + id);
    var numeAngajat = row.cells[0].textContent;
    var numeProiect = row.cells[2].textContent;
    var descriereTasks = row.cells[3].textContent;
    var nrOre = row.cells[4].textContent;

    document.getElementById("nume-angajat").textContent = numeAngajat;
    document.getElementById("nume-proiect").textContent = numeProiect;
    document.getElementById("descriere-tasks").textContent = descriereTasks;
    document.getElementById("nr-ore").textContent = nrOre;

    document.getElementById("pontaj-id").value = id;
}

function attachPontajId() {
    var pontajId = document.getElementById("pontaj-id").value;
    document.getElementById("pontaj-id").value = pontajId;
}

function filterTable(tableId, tbNr) {
    var filterNume = document.getElementById("filter-nume-" + tbNr).value.toLowerCase();
    var filterProiect = document.getElementById("filter-proiect-" + tbNr).value.toLowerCase();
    var filterTasks = document.getElementById("filter-tasks-" + tbNr).value.toLowerCase();

    var table = document.getElementById(tableId);
    var rows = table.getElementsByTagName('tr');

    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        var nume = row.cells[0].textContent.toLowerCase();
        var numeProiect = row.cells[2].textContent.toLowerCase();
        var descriereTasks = row.cells[3].textContent.toLowerCase();

        var showRow = true;

        if (filterNume && !nume.includes(filterNume)) {
            showRow = false;
        }

        if (filterProiect && !numeProiect.includes(filterProiect)) {
            showRow = false;
        }

        if (filterTasks && !descriereTasks.includes(filterTasks)) {
            showRow = false;
        }

        row.style.display = showRow ? '' : 'none';
    }
}

document.getElementById('filter-nume-1').addEventListener('input', function() {
    filterTable('t1', '1');
});

document.getElementById('filter-proiect-1').addEventListener('input', function() {
    filterTable('t1', '1');
});

document.getElementById('filter-tasks-1').addEventListener('input', function() {
    filterTable('t1', '1');
});

document.getElementById('filter-nume-2').addEventListener('input', function() {
    filterTable('t2', '2');
});

document.getElementById('filter-proiect-2').addEventListener('input', function() {
    filterTable('t2', '2');
});

document.getElementById('filter-tasks-2').addEventListener('input', function() {
    filterTable('t2', '2');
});