function getPontaj(id) {
    var row = document.getElementById("pontaj-" + id);
    var numeAngajat = row.cells[0].textContent;
    var numeProiect = row.cells[2].textContent;
    var descriereTasks = row.cells[3].textContent;
    var nrOre = row.cells[4].textContent;

    document.getElementById("nume-angajat").textContent = numeAngajat;
    document.getElementById("nume-proiect").textContent = numeProiect;
    document.getElementById("descriere-tasks").textContent = descriereTasks;
    document.getElementById("nr-ore-mod").textContent = nrOre;

    document.getElementById("pontaj-id").value = pontajId;
}

function attachPontajId() {
    var pontajId = document.getElementById("pontaj-id").value;
    document.getElementById("pontaj-id").value = pontajId;
}