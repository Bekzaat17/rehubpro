document.addEventListener("DOMContentLoaded", function () {
    fetch("/residents/data/")
        .then(response => response.json())
        .then(data => {
            const headerRow = document.getElementById("residents-header");
            const body = document.getElementById("residents-body");

            if (!headerRow || !body) {
                console.error("Таблица не найдена в DOM");
                return;
            }

            // Очищаем старые данные
            headerRow.innerHTML = "";
            body.innerHTML = "";

            // Добавляем колонку нумерации
            const numberTh = document.createElement("th");
            numberTh.textContent = "№";
            headerRow.appendChild(numberTh);

            // Рендер заголовков
            data.columns.forEach((col) => {
                const th = document.createElement("th");
                th.textContent = col;
                headerRow.appendChild(th);
            });

            // Рендер строк таблицы
            data.rows.forEach((row, index) => {
                const tr = document.createElement("tr");

                // Номер строки
                const numberTd = document.createElement("td");
                numberTd.textContent = index + 1;
                tr.appendChild(numberTd);

                row.forEach((cell, cellIndex) => {
                    const td = document.createElement("td");

                    // Используем innerHTML для отображения HTML-тегов
                    td.innerHTML = cell;

                    // Добавляем стили для определённых колонок
                    switch (cellIndex) {
                        case 2:
                            td.classList.add("col-colored-2"); // Текущее задание
                            break;
                        case 3:
                            td.classList.add("col-colored-3"); // Последний прогресс
                            break;
                        case 4:
                            td.classList.add("col-colored-4"); // Активные роли
                            break;
                        case 5:
                            td.classList.add("col-colored-5"); // Заметки
                            break;
                        case 6:
                            td.classList.add("col-colored-6"); // Тип зависимости
                            break;
                        default:
                            break;
                    }

                    tr.appendChild(td);
                });

                body.appendChild(tr);
            });
        })
        .catch(error => {
            console.error("Ошибка при получении данных:", error);
        });
});