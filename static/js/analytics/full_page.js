document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("filter-form");
  const resultsDiv = document.getElementById("analytics-results");
  const exportBtn = document.getElementById("export-button");
  const pdfWrapper = document.getElementById("pdf-wrapper");

  if (!form || !resultsDiv) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(form);
    const params = new URLSearchParams(formData).toString();

    fetch(`/analytics/full/?${params}`)
      .then(res => res.json())
      .then(data => {
        resultsDiv.innerHTML = "";
        exportBtn.disabled = false;

        document.getElementById("pdf-resident-name").textContent =
          form.querySelector("#resident option:checked")?.textContent.trim() || "—";

        const dateFrom = form.querySelector("#date_from").value;
        const dateTo = form.querySelector("#date_to").value;
        document.getElementById("pdf-period").textContent = dateFrom && dateTo ? `${dateFrom} — ${dateTo}` : "—";

        for (const [metric, content] of Object.entries(data)) {
          const col = document.createElement("div");
          const isHeatmap = ["heatmap"].includes(content.type);
          col.className = "col-12";

          if (isHeatmap) {
            col.classList.add("page-break-custom");
          }

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

  exportBtn?.addEventListener("click", function () {
    const clone = pdfWrapper.cloneNode(true);
    const header = clone.querySelector("#pdf-header");
    header.style.display = "block";

    const pageBreak = document.createElement("div");
    pageBreak.className = "page-break";
    header.after(pageBreak);

    const canvases = document.querySelectorAll("canvas");
    const cloneCanvases = clone.querySelectorAll("canvas");

    canvases.forEach((canvas, index) => {
      const imgData = canvas.toDataURL("image/png");
      const img = new Image();
      img.src = imgData;
      img.style.width = "100%";

      const parent = cloneCanvases[index]?.parentNode;
      if (parent) {
        parent.innerHTML = "";
        parent.appendChild(img);
      }
    });

    const fioRaw = document.getElementById("pdf-resident-name").textContent.trim();
    const fioSafe = fioRaw.replace(/\s+/g, "_");
    const period = document.getElementById("pdf-period").textContent.trim().replace(/\s*—\s*/g, "_");
    const filename = `${fioSafe}-${period || Date.now()}.pdf`;

    html2pdf().set({
      margin: [0.8, 0.5, 0.5, 0.5],
      filename: filename,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: {
        scale: 2,
        useCORS: true,
        allowTaint: false,
        logging: false,
        scrollY: 0
      },
      jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
    }).from(clone).save();
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
        scales: {
          y: { min: 0, max: 100 },
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: ctx => content.value_labels?.[ctx.dataIndex] || ctx.parsed.y,
            },
          },
        },
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
        plugins: {
          tooltip: {
            callbacks: {
              label: ctx => content.value_labels?.[ctx.dataIndex] || ctx.parsed.y,
            },
          },
        },
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
      const container = document.createElement("div");
      container.className = "table-responsive mt-3";

      const table = document.createElement("table");
      table.className = "table table-borderless table-sm text-center align-middle heatmap-row-separator";

      const thead = document.createElement("thead");
      const headerRow = document.createElement("tr");
      headerRow.innerHTML = `<th>Роль \\ Дата</th>` + content.rows.map(role => `<th>${role}</th>`).join("");
      thead.appendChild(headerRow);

      const tbody = document.createElement("tbody");

      content.columns.forEach((date, dateIndex) => {
        const row = document.createElement("tr");
        row.innerHTML = `<th>${date}</th>` + content.rows.map((_, roleIndex) => {
          const val = content.values[roleIndex][dateIndex];
          const color = val === "responsible" ? "text-success fw-bold" :
                        val === "irresponsible" ? "text-danger fw-bold" : "text-muted";
          return `<td class="${color}">${val ?? "-"}</td>`;
        }).join("");
        tbody.appendChild(row);
      });

      table.append(thead, tbody);
      container.appendChild(table);
      ctx.replaceWith(container);
    },

    timeline: () => {
      const container = document.createElement("div");
      container.className = "timeline-clean";

      for (const [date, entries] of Object.entries(content.timeline || {})) {
        entries.forEach(entry => {
          const row = document.createElement("div");
          row.className = "timeline-clean-row";

          const dateBlock = document.createElement("div");
          dateBlock.className = "timeline-date";
          dateBlock.textContent = date;

          const entryBlock = document.createElement("div");
          entryBlock.className = "timeline-clean-entry";

          const title = document.createElement("div");
          title.className = "timeline-task";
          title.textContent = entry.task_title || "—";

          const stage = document.createElement("div");
          stage.className = "timeline-stage";
          stage.textContent = entry.stage || "—";

          const comment = document.createElement("div");
          comment.className = "timeline-comment";
          comment.textContent = entry.comment || "—";

          entryBlock.append(title, stage, comment);
          row.append(dateBlock, entryBlock);
          container.appendChild(row);
        });
      }

      ctx.replaceWith(container);
    }
  };

  const configFn = configMap[content.type];
  if (!configFn) return;
  if (["heatmap", "timeline"].includes(content.type)) return configFn();

  const canvas = document.createElement("canvas");
  const ratio = window.devicePixelRatio || 1;
  canvas.width = ctx.offsetWidth * ratio;
  canvas.height = ctx.offsetHeight * ratio;
  ctx.appendChild(canvas);

  const context = canvas.getContext("2d");
  context.setTransform(ratio, 0, 0, ratio, 0, 0);

  const config = configFn();
  new Chart(canvas, config);
}