// Pole všech okresů – použije se pro výběr v dropdownu
const okresy = [
    "Benešov", "Beroun", "Blansko", "Brno-město", "Brno-venkov", "Bruntál", "Břeclav",
    "Cheb", "Chomutov", "Chrudim", "Česká Lípa", "České Budějovice", "Český Krumlov",
    "Děčín", "Domažlice", "Frýdek-Místek", "Havlíčkův Brod", "Hodonín", "Hradec Králové",
    "Jablonec nad Nisou", "Jeseník", "Jičín", "Jihlava", "Jindřichův Hradec", "Karlovy Vary",
    "Karviná", "Kladno", "Klatovy", "Kolín", "Kroměříž", "Kutná Hora", "Liberec",
    "Litoměřice", "Louny", "Mělník", "Mladá Boleslav", "Most", "Náchod", "Nový Jičín",
    "Nymburk", "Olomouc", "Opava", "Ostrava-město", "Pardubice", "Pelhřimov", "Písek",
    "Plzeň-jih", "Plzeň-město", "Plzeň-sever", "Prachatice", "Praha 10", "Praha 2", "Praha 3",
    "Praha 4", "Praha 5", "Praha 6", "Praha 7", "Praha 8", "Praha 9", "Praha-východ", "Praha-západ",
    "Prostějov", "Přerov", "Příbram", "Rakovník", "Rokycany", "Rychnov nad Kněžnou",
    "Semily", "Sokolov", "Strakonice", "Svitavy", "Šumperk", "Tábor", "Tachov", "Teplice",
    "Trutnov", "Třebíč", "Uherské Hradiště", "Ústí nad Labem", "Ústí nad Orlicí", "Vsetín",
    "Vyškov", "Zlín", "Znojmo", "Žďár nad Sázavou"
];

// Elementy z HTML pro dropdown
const dropdownMenu = document.getElementById("dropdown-menu");
const dropdownItemsContainer = document.getElementById("dropdown-items");
const dropdownSearch = document.getElementById("dropdown-search");

// Vygeneruje položky do dropdown menu podle pole okresů
function generateDropdownItems() {
    dropdownItemsContainer.innerHTML = ""; // Vyčistí staré položky
    okresy.forEach(okres => {
        const item = document.createElement("div");
        item.className = "dropdown-item";
        item.textContent = okres;
        item.onclick = () => selectOkres(okres); // Po kliknutí nastaví daný okres
        dropdownItemsContainer.appendChild(item);
    });
}

// Otevře/zavře dropdown a znovu načte položky
function toggleDropdown() {
    dropdownMenu.classList.toggle("show"); // Přepíná viditelnost menu
    dropdownSearch.value = ""; // Vyčistí hledání
    generateDropdownItems(); // Vygeneruje všechny položky znovu
}

// Nastaví vybraný okres a uloží ho do inputu
function selectOkres(okres) {
    const dropdownButton = document.querySelector(".dropdown-button");
    const hiddenInput = document.getElementById("okres");

    if (!dropdownButton || !hiddenInput) {
        console.error("❌ Dropdown button nebo skrytý input nenalezen.");
        return;
    }

    dropdownButton.textContent = okres; // Zobrazí vybraný okres na tlačítku
    hiddenInput.value = okres; // Uloží ho do skrytého inputu pro odeslání
    dropdownMenu.classList.remove("show"); // Zavře menu
}

// Dynamické vyhledávání v dropdownu
dropdownSearch.addEventListener("input", () => {
    const searchTerm = dropdownSearch.value.toLowerCase(); // Získá hledaný text
    const filteredOkresy = okresy.filter(okres => okres.toLowerCase().includes(searchTerm)); // Najde odpovídající

    dropdownItemsContainer.innerHTML = ""; // Vyčistí staré položky
    filteredOkresy.forEach(okres => {
        const item = document.createElement("div");
        item.className = "dropdown-item";
        item.textContent = okres;
        item.onclick = () => selectOkres(okres);
        dropdownItemsContainer.appendChild(item);
    });
});

// Inicializace dropdownu při načtení
generateDropdownItems();

// Funkce pro získání predikce na základě aktuální GPS polohy
function getPredictionFromLocation() {
    navigator.geolocation.getCurrentPosition(pos => {
        fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                lat: pos.coords.latitude,
                lon: pos.coords.longitude
            })
        }).then(r => r.json()).then(data => {
            const el = document.getElementById("vysledek-aktualne");

            if (data.error) {
                el.innerHTML = `<div class="error">${data.error}</div>`; // Zobrazí chybu
            } else {
                const vikendText = data.vikend === 1 ? "ano" : "ne";
                const svatekText = data.svatek === 1 ? "ano" : "ne";

                // Výstup predikce
                el.innerHTML = `
                    <p><strong>Okres:</strong> ${data.okres}</p>
                    <p><strong>Nafta:</strong> ${data.nafta} Kč</p>
                    <p><strong>Natural:</strong> ${data.natural} Kč</p>
                    <p><strong>Datum:</strong> ${data.datum}</p>
                    <hr>
                    <small><strong>USD:</strong> ${data.usd}, <strong>Ropa:</strong> ${data.ropa} Kč</small><br>
                    <small><strong>Svátek:</strong> ${svatekText}, <strong>Víkend:</strong> ${vikendText}</small>
                `;
            }
        });
    }, () => alert("❌ Nepodařilo se získat polohu."));
}

// Predikce budoucích cen dle vybraného okresu a data
function predictFuture() {
    const okres = document.getElementById("okres")?.value;
    const start = document.getElementById("start-date")?.value;
    const end = document.getElementById("end-date")?.value;
    const typPaliva = document.getElementById("typ-paliva")?.value;

    const el = document.getElementById("vysledek-budoucnost");
    const analyza = document.getElementById("analyza-dnu");

    // Ověří, že jsou všechny údaje vyplněny
    if (!okres || !start || !end) {
        alert("❗ Vyplňte všechny údaje pro predikci.");
        el.innerHTML = "";
        analyza.innerHTML = "";
        return;
    }

    fetch("/api/predict_future", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ okres, start, end, typ_paliva: typPaliva })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error || !data.predictions || data.predictions.length === 0) {
                el.innerHTML = `<div class="error">${data.error || "Žádná data nenalezena."}</div>`;
                analyza.innerHTML = "";
                return;
            }

            el.innerHTML = "";
            analyza.innerHTML = "";

            const labels = [];
            const naftaData = [];
            const naturalData = [];

            data.predictions.forEach(p => {
                const nafta = p.nafta !== undefined ? `${p.nafta} Kč` : "N/A";
                const natural = p.natural !== undefined ? `${p.natural} Kč` : "N/A";

                // Výpis dat
                el.innerHTML += `
                    <div class="pred-box">
                        <strong>${p.datum}</strong> → 
                        ${p.nafta !== undefined ? `Nafta: ${nafta}` : ""}
                        ${p.natural !== undefined ? `Natural: ${natural}` : ""}
                    </div>
                `;

                // Data do grafu
                labels.push(p.datum);
                if (p.nafta !== undefined) naftaData.push(p.nafta);
                if (p.natural !== undefined) naturalData.push(p.natural);
            });

            // vykreslení grafu pomocí Chart.js
            const ctx = document.getElementById("graf").getContext("2d");
            if (window.predikceGraf) window.predikceGraf.destroy(); // Zničí starý graf, pokud existuje

            const datasets = [];
            if (naftaData.length > 0) {
                datasets.push({
                    label: "Nafta",
                    data: naftaData,
                    borderWidth: 2,
                    borderColor: "rgba(255, 99, 132, 1)",
                    fill: false,
                    tension: 0.3
                });
            }
            if (naturalData.length > 0) {
                datasets.push({
                    label: "Natural",
                    data: naturalData,
                    borderWidth: 2,
                    borderColor: "rgba(54, 162, 235, 1)",
                    fill: false,
                    tension: 0.3
                });
            }

            window.predikceGraf = new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "top"
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: "Cena v Kč"
                            }
                        }
                    }
                }
            });
        })
        .catch(err => {
            console.error("❌ Chyba:", err);
            el.innerHTML = `<div class="error">❌ Chyba při načítání dat ze serveru.</div>`;
            analyza.innerHTML = "";
        });
}

// Nastaví vybraný typ paliva podle kliknutého tlačítka
function setTypPaliva(button) {
    document.querySelectorAll(".palivo-button").forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");
    document.getElementById("typ-paliva").value = button.getAttribute("data-value"); // Uloží typ paliva do inputu
}
