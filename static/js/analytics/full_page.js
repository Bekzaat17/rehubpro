// 📊 full_page.js — отрисовка аналитики с графиками Chart.js

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("filter-form");
  const resultsDiv = document.getElementById("analytics-results");

  if (!form || !resultsDiv) {
    console.error("Форма или resultsDiv не найдены");
    return;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const params = new URLSearchParams(formData).toString();

    fetch(`/analytics/full/?${params}`)
      .then(res => res.json())
      .then(data => {
        resultsDiv.innerHTML = "";

        for (const [metric, content] of Object.entries(data)) {
          const block = document.createElement("div");
          block.className = "col-12";

          const chartId = `chart-${metric}`;

          block.innerHTML = `
            <div class="card shadow-sm p-3">
              <h5 class="card-title mb-3">${content.title || metric}</h5>
              <canvas id="${chartId}"></canvas>
            </div>
          `;

          resultsDiv.appendChild(block);

          const ctx = document.getElementById(chartId);
          renderChart(ctx, content);
        }
      })
      .catch(err => {
        console.error("Ошибка загрузки аналитики:", err);
        resultsDiv.innerHTML = `<p class="text-danger">Ошибка загрузки данных</p>`;
      });
  });
});

function renderChart(ctx, content) {
  if (!ctx || !content || !content.type) return;

  const configMap = {
    line: () => ({
      type: "line",
      data: {
        labels: content.labels || [],
        datasets: [
          {
            label: content.title,
            data: content.values || [],
            borderColor: "#0d6efd",
            backgroundColor: "rgba(13, 110, 253, 0.2)",
            tension: 0.3,
            fill: true,
          },
        ],
      },
    }),

    bar: () => ({
      type: "bar",
      data: {
        labels: content.labels || [],
        datasets: [
          {
            label: content.title,
            data: content.values || [],
            backgroundColor: "#198754",
          },
        ],
      },
    }),

    pie: () => ({
      type: "pie",
      data: {
        labels: content.labels || [],
        datasets: [
          {
            label: content.title,
            data: content.values || [],
            backgroundColor: ["#0d6efd", "#6c757d", "#198754", "#dc3545", "#ffc107"],
          },
        ],
      },
    }),

    heatmap: () => {
      // Временная табличная отрисовка (в будущем можно будет заменить на Chart.js плагин)
      const html = document.createElement("table");
      html.className = "table table-bordered table-sm text-center mt-3";
      const thead = document.createElement("thead");
      const tbody = document.createElement("tbody");

      const headerRow = document.createElement("tr");
      headerRow.innerHTML = `<th>Роль/Дата</th>${content.columns.map(col => `<th>${col}</th>`).join("")}`;
      thead.appendChild(headerRow);

      content.rows.forEach((rowName, i) => {
        const row = document.createElement("tr");
        row.innerHTML = `<th>${rowName}</th>` + content.columns.map((_, j) => {
          const val = content.values[i][j];
          const color = val === "responsible" ? "bg-success text-white" : val === "irresponsible" ? "bg-danger text-white" : "";
          return `<td class="${color}">${val ?? "-"}</td>`;
        }).join("");
        tbody.appendChild(row);
      });

      html.appendChild(thead);
      html.appendChild(tbody);

      ctx.replaceWith(html);
    },

    timeline: () => {
      const container = document.createElement("div");
      container.className = "timeline-container mt-3";

      for (const [date, entries] of Object.entries(content.timeline || {})) {
        const section = document.createElement("div");
        section.className = "mb-3";

        const heading = document.createElement("h6");
        heading.textContent = date;
        section.appendChild(heading);

        const list = document.createElement("ul");
        list.className = "list-group list-group-flush";

        entries.forEach(entry => {
          const item = document.createElement("li");
          item.className = "list-group-item";
          item.innerHTML = `<strong>${entry.task_title}</strong> (${entry.task_type}) — <em>${entry.stage}</em><br/><small>${entry.comment}</small>`;
          list.appendChild(item);
        });

        section.appendChild(list);
        container.appendChild(section);
      }

      ctx.replaceWith(container);
    },
  };

  const configFn = configMap[content.type];
  if (!configFn) return;
  const config = configFn();
  if (content.type === "heatmap" || content.type === "timeline") return; // уже отрисовано вручную

  new Chart(ctx, config);
}