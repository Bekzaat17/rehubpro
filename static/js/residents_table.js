document.addEventListener("DOMContentLoaded", function () {
    fetch("/residents/data/")
        .then(response => response.json())
        .then(data => {
            console.log("Полученные данные:", data);

            const headerRow = document.getElementById("residents-header");
            const body = document.getElementById("residents-body");

            if (!headerRow || !body) {
                console.error("Таблица не найдена в DOM");
                return;
            }

            // Рендерим заголовки
            headerRow.innerHTML = "";

            // Добавляем первый столбец для нумерации
            const numberTh = document.createElement("th");
            numberTh.textContent = "№";
            headerRow.appendChild(numberTh);

            data.columns.forEach(col => {
                const th = document.createElement("th");
                th.textContent = col;
                headerRow.appendChild(th);
            });

            // Рендерим строки
            body.innerHTML = "";
            data.rows.forEach((row, index) => {
                const tr = document.createElement("tr");

                // Добавляем ячейку с номером строки
                const numberTd = document.createElement("td");
                numberTd.textContent = index + 1;
                tr.appendChild(numberTd);

                row.forEach(cell => {
                    const td = document.createElement("td");
                    td.textContent = cell;
                    tr.appendChild(td);
                });

                body.appendChild(tr);
            });
        })
        .catch(error => {
            console.error("Ошибка при получении данных:", error);
        });
});