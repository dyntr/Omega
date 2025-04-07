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

const okresSelect = document.getElementById("okres");
okresy.forEach(okres => {
    const option = document.createElement("option");
    option.value = okres;
    option.textContent = okres;
    okresSelect.appendChild(option);
});

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
                el.innerHTML = `<div class="error">${data.error}</div>`;
            } else {
                const vikendText = data.vikend === 1 ? "ano" : "ne";
                const svatekText = data.svatek === 1 ? "ano" : "ne";

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
    }, () => alert("Nepodařilo se získat polohu."));
}

function predictFuture() {
    const okres = document.getElementById("okres").value;
    const start = document.getElementById("start-date").value;
    const end = document.getElementById("end-date").value;

    const el = document.getElementById("vysledek-budoucnost");
    const analyza = document.getElementById("analyza-dnu");

    if (!okres || !start || !end) {
        alert("Vyplňte všechny údaje pro predikci.");
        el.innerHTML = "";
        analyza.innerHTML = "";
        return;
    }

    fetch("/api/predict_future", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ okres, start, end })
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

            let bestDay = null;
            let worstDay = null;

            data.predictions.forEach((p, index) => {
                const nafta = typeof p.nafta === "object" ? p.nafta.hodnota : p.nafta;
                const natural = typeof p.natural === "object" ? p.natural.hodnota : p.natural;

                // Výpis jednotlivých dnů
                el.innerHTML += `
                    <div class="pred-box">
                        <strong>${p.datum}</strong> → Nafta: ${nafta} Kč, Natural: ${natural} Kč
                    </div>
                `;

                // Data pro graf
                labels.push(p.datum);
                naftaData.push(nafta);
                naturalData.push(natural);

                // Hledání nejlepšího/nejhoršího dne
                if (!bestDay || nafta < bestDay.nafta) bestDay = { datum: p.datum, nafta };
                if (!worstDay || nafta > worstDay.nafta) worstDay = { datum: p.datum, nafta };
            });

            // Analýza nejlepšího/nejhoršího dne
            analyza.innerHTML = `
                <p><strong>📉 Nejlepší den na tankování:</strong> ${bestDay.datum} (${bestDay.nafta} Kč)</p>
                <p><strong>📈 Nejdražší den:</strong> ${worstDay.datum} (${worstDay.nafta} Kč)</p>
            `;

            // Vykreslení grafu
            const ctx = document.getElementById("graf").getContext("2d");
            if (window.predikceGraf) window.predikceGraf.destroy();

            window.predikceGraf = new Chart(ctx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: "Nafta",
                            data: naftaData,
                            borderWidth: 2,
                            borderColor: "rgba(255, 99, 132, 1)",
                            fill: false,
                            tension: 0.3
                        },
                        {
                            label: "Natural",
                            data: naturalData,
                            borderWidth: 2,
                            borderColor: "rgba(54, 162, 235, 1)",
                            fill: false,
                            tension: 0.3
                        }
                    ]
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
            console.error("Chyba:", err);
            el.innerHTML = `<div class="error">❌ Chyba při načítání dat ze serveru.</div>`;
            analyza.innerHTML = "";
        });
}
