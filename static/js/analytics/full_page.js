document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("filter-form");
  const resultsDiv = document.getElementById("analytics-results");

  if (!form || !resultsDiv) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const params = new URLSearchParams(formData).toString();

    fetch(`/analytics/full/?${params}`)
      .then(res => res.json())
      .then(data => {
        resultsDiv.innerHTML = "";

        for (const [metric, content] of Object.entries(data)) {
          const col = document.createElement("div");
          col.className = "col-12";

          const chartId = `chart-${metric}`;
          const isCustom = ["heatmap", "timeline"].includes(content.type);

          col.innerHTML = `
            <div class="card shadow-sm p-3 analytics-block">
              <h5 class="card-title mb-3">${content.title || metric}</h5>
              <div class="${isCustom ? "" : "chart-wrapper"}" id="${chartId}"></div>
            </div>
          `;

          resultsDiv.appendChild(col);

          const target = document.getElementById(chartId);
          renderChart(target, content);
        }
      })
      .catch(err => {
        console.error("Ошибка загрузки аналитики:", err);
        resultsDiv.innerHTML = `<p class="text-danger">Ошибка загрузки данных</p>`;
      });
  });
});

function renderChart(ctx, content) {
  if (!ctx || !content?.type) return;

  const configMap = {
    line: () => ({
      type: "line",
      data: {
        labels: content.labels || [],
        datasets: [{
          label: content.title,
          data: content.values || [],
          borderColor: "#0d6efd",
          backgroundColor: "rgba(13, 110, 253, 0.2)",
          tension: 0.3,
          fill: true,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        devicePixelRatio: window.devicePixelRatio || 1,
      },
    }),

    bar: () => ({
      type: "bar",
      data: {
        labels: content.labels || [],
        datasets: [{
          label: content.title,
          data: content.values || [],
          backgroundColor: "#198754",
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        devicePixelRatio: window.devicePixelRatio || 1,
      },
    }),

    pie: () => ({
      type: "pie",
      data: {
        labels: content.labels || [],
        datasets: [{
          label: content.title,
          data: content.values || [],
          backgroundColor: ["#0d6efd", "#6c757d", "#198754", "#dc3545", "#ffc107"],
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        devicePixelRatio: window.devicePixelRatio || 1,
      },
    }),

    heatmap: () => {
      const table = document.createElement("table");
      table.className = "table table-bordered table-sm text-center mt-3";

      const thead = document.createElement("thead");
      const headerRow = document.createElement("tr");
      headerRow.innerHTML = `<th>Роль/Дата</th>${content.columns.map(col => `<th>${col}</th>`).join("")}`;
      thead.appendChild(headerRow);

      const tbody = document.createElement("tbody");
      content.rows.forEach((rowName, i) => {
        const row = document.createElement("tr");
        row.innerHTML = `<th>${rowName}</th>` + content.columns.map((_, j) => {
          const val = content.values[i][j];
          const color = val === "responsible" ? "bg-success text-white" :
                        val === "irresponsible" ? "bg-danger text-white" : "";
          return `<td class="${color}">${val ?? "-"}</td>`;
        }).join("");
        tbody.appendChild(row);
      });

      table.append(thead, tbody);
      ctx.replaceWith(table);
    },

    timeline: () => {
      const container = document.createElement("div");
      container.className = "timeline-container mt-3";

      for (const [date, entries] of Object.entries(content.timeline || {})) {
        const section = document.createElement("div");
        section.className = "mb-3";
        section.innerHTML = `<h6>${date}</h6>`;

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
  if (["heatmap", "timeline"].includes(content.type)) return configFn();

  // 🎯 Retina (HD) canvas setup
  const canvas = document.createElement("canvas");
  canvas.style.width = "100%";
  canvas.style.height = "100%";
  const ratio = window.devicePixelRatio || 1;
  canvas.width = ctx.offsetWidth * ratio;
  canvas.height = ctx.offsetHeight * ratio;
  ctx.appendChild(canvas);

  const context = canvas.getContext("2d");
  context.setTransform(ratio, 0, 0, ratio, 0, 0);

  const config = configFn();
  new Chart(canvas, config);
}