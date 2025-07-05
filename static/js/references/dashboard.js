document.addEventListener("DOMContentLoaded", () => {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");
  const tables = document.querySelectorAll(".reference-table");
  const modal = new bootstrap.Modal(document.getElementById("referenceModal"));
  const form = document.getElementById("referenceForm");
  const tabContainer = document.getElementById("referenceTabs");

  // Загрузка данных
  function loadTable(reference, traitType) {
    const table = document.querySelector(`.reference-table[data-reference="${reference}"][data-trait-type="${traitType}"]`);
    if (!table) return;

    fetch(`/references/api/${reference}/?type=${traitType}`)
      .then((r) => r.json())
      .then((data) => {
        const tbody = table.querySelector("tbody");
        tbody.innerHTML = "";
        data.data.forEach((item) => {
          const row = createRow(item, reference, traitType);
          tbody.appendChild(row);
        });
      });
  }

  tables.forEach((table) => {
    const reference = table.dataset.reference;
    const traitType = table.dataset.traitType || "";
    loadTable(reference, traitType);
  });

  // Кнопка "Добавить"
  document.querySelectorAll("[data-bs-target='#referenceModal']").forEach((btn) => {
    btn.addEventListener("click", () => {
      form.reset();
      form.reference.value = btn.dataset.reference;
      if (form.trait_type) form.trait_type.value = btn.dataset.traitType || "";
      form.id.value = "";
      form.is_active.checked = true;

      document.querySelector(".score-group").classList.toggle(
        "d-none",
        !usesScore(btn.dataset.reference)
      );
    });
  });

  // Редактирование
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

      if ("type" in data && form.trait_type) {
        form.trait_type.value = data.type;
      }

      form.is_active.checked = data.is_active ?? true;

      modal.show();
    }
  });

  // Удаление
  document.addEventListener("click", (e) => {
    if (e.target.classList.contains("btn-delete")) {
      if (!confirm("Отключить элемент?")) return;

      const reference = e.target.dataset.reference;
      const traitType = e.target.dataset.traitType || "";

      fetch(`/references/api/${reference}/?type=${traitType}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ id: e.target.dataset.id }),
      }).then(() => location.reload());
    }
  });

  // Сохранение
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const reference = form.reference.value;
    const traitType = form.trait_type ? form.trait_type.value : "";

    if (!form.is_active.checked) {
      const hidden = document.createElement("input");
      hidden.type = "hidden";
      hidden.name = "is_active";
      hidden.value = "";
      form.appendChild(hidden);
    }

    const data = new FormData(form);
    const activeTabId = document.querySelector('.nav-link.active')?.id;
    const scrollPosition = tabContainer?.scrollLeft || 0;

    fetch(`/references/api/${reference}/?type=${traitType}`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      body: data,
    })
      .then((r) => r.json())
      .then(() => {
        modal.hide();
        loadTable(reference, traitType);

        // 🟢 Восстановить активную вкладку
        if (activeTabId) {
          const tabTrigger = document.getElementById(activeTabId);
          if (tabTrigger) new bootstrap.Tab(tabTrigger).show();
        }

        // 🟢 Восстановить scroll
        if (tabContainer) {
          setTimeout(() => {
            tabContainer.scrollLeft = scrollPosition;
          }, 100);
        }
      });
  });

  function createRow(item, reference, traitType = "") {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.name}</td>
      <td>${item.is_active ? "✅" : "❌"}</td>
      <td>${item.score !== undefined ? item.score : ""}</td>
      <td>
        <button class="btn btn-sm btn-warning btn-edit" 
                data-item='${JSON.stringify(item)}' 
                data-reference="${reference}"
                data-trait-type="${traitType}">✏️</button>
        <button class="btn btn-sm btn-danger btn-delete" 
                data-id="${item.id}" 
                data-reference="${reference}"
                data-trait-type="${traitType}">🗑️</button>
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
      "physicalstate",
    ].includes(reference);
  }

  document.querySelector(".scroll-left")?.addEventListener("click", () => {
    tabContainer.scrollBy({ left: -200, behavior: "smooth" });
  });

  document.querySelector(".scroll-right")?.addEventListener("click", () => {
    tabContainer.scrollBy({ left: 200, behavior: "smooth" });
  });
});