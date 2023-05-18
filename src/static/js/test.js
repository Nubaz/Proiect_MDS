function getPontaj(id) {
    let pontaj = Array.from(document.getElementById("pontaj-" + id).children).splice(0,5).map(e => e.innerText);
    
    // Stergere pontaj
    let date = Array.from(document.getElementById("p-sters").children);
    for(let i in date) {
        date[i].lastElementChild.innerText = pontaj[i];
    }

    document.getElementById("id-p-sters").value = pontaj[0];

    // Modificare pontaj
    document.getElementById("id-p-mod").value = pontaj[0];
    document.getElementById("nume-proiect-mod").value = pontaj[2];
    document.getElementById("descriere-tasks-mod").value = pontaj[3];
    document.getElementById("nr-ore-mod").value = pontaj[4];
}