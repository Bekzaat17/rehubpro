// 📁 residents_table.js

// Глобальная функция для отрисовки таблицы
window.refreshResidentTableData = function () {
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

        // Клик на строку открывает модалку
        tr.addEventListener("click", () => {
          openResidentModal(row.id);
        });
        tr.style.cursor = "pointer";

        const numberTd = document.createElement("td");
        numberTd.textContent = index + 1;
        tr.appendChild(numberTd);

        row.cells.forEach((cell, cellIndex) => {
          const td = document.createElement("td");
          td.innerHTML = cell;

          switch (cellIndex) {
            case 2: td.classList.add("col-colored-2"); break;
            case 3: td.classList.add("col-colored-3"); break;
            case 4: td.classList.add("col-colored-4"); break;
            case 5: td.classList.add("col-colored-5"); break;
            case 6: td.classList.add("col-colored-6"); break;
            case 7: td.classList.add("col-colored-7"); break;
          }

          tr.appendChild(td);
        });

        body.appendChild(tr);
      });
    })
    .catch(error => {
      console.error("Ошибка при получении данных:", error);
    });
};

document.addEventListener("DOMContentLoaded", function () {
  refreshResidentTableData();
});