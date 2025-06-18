document.addEventListener("DOMContentLoaded", () => {
  const tables = document.querySelectorAll(".reference-table");
  const modal = new bootstrap.Modal(document.getElementById("referenceModal"));
  const form = document.getElementById("referenceForm");

  // Загружаем данные справочников
  tables.forEach((table) => {
    const reference = table.dataset.reference;
    fetch(`/references/api/${reference}/`)
      .then((r) => r.json())
      .then((data) => {
        const tbody = table.querySelector("tbody");
        tbody.innerHTML = "";
        data.data.forEach((item) => {
          const row = createRow(item, reference);
          tbody.appendChild(row);
        });
      });
  });

  // Обработка кнопки "Добавить"
  document.querySelectorAll("[data-bs-target='#referenceModal']").forEach((btn) => {
    btn.addEventListener("click", () => {
      form.reset();
      form.reference.value = btn.dataset.reference;
      form.id.value = "";
      document.querySelector(".score-group").classList.toggle("d-none", !usesScore(btn.dataset.reference));
    });
  });

  // Обработка редактирования
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("btn-edit")) {
      const data = JSON.parse(e.target.dataset.item);
      form.name.value = data.name;
      form.id.value = data.id;
      form.reference.value = e.target.dataset.reference;
      if ("score" in data) {
        document.querySelector(".score-group").classList.remove("d-none");
        form.score.value = data.score;
      } else {
        document.querySelector(".score-group").classList.add("d-none");
      }
      modal.show();
    }
  });

  // Удаление
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("btn-delete")) {
      if (!confirm("Отключить элемент?")) return;
      fetch(`/references/api/${e.target.dataset.reference}/`, {
        method: "DELETE",
        body: JSON.stringify({ id: e.target.dataset.id }),
      }).then(() => location.reload());
    }
  });

  // Сохранение
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const reference = form.reference.value;
    const data = new FormData(form);
    fetch(`/references/api/${reference}/`, {
      method: "POST",
      body: data,
    })
      .then((r) => r.json())
      .then(() => location.reload());
  });

  function createRow(item, reference) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.name}</td>
      <td>${item.is_active ? "✅" : "❌"}</td>
      <td>${item.score !== undefined ? item.score : ""}</td>
      <td>
        <button class="btn btn-sm btn-warning btn-edit" 
                data-item='${JSON.stringify(item)}' 
                data-reference="${reference}">✏️</button>
        <button class="btn btn-sm btn-danger btn-delete" 
                data-id="${item.id}" 
                data-reference="${reference}">🗑️</button>
      </td>
    `;
    return tr;
  }

  function usesScore(reference) {
    return [
        "emotionalstate",
        "dailydynamics",
        "motivation",
        "familyactivity",
        "mrpactivity",
        "physicalstate"
    ].includes(reference); // 👈 можно вынести в global config
  }
});