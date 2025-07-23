document.addEventListener("DOMContentLoaded", function () {
  let currentResidentId = null;

  // Открытие модалки
  window.openResidentModal = function (residentId) {
    currentResidentId = residentId;

    const modalElement = document.getElementById("residentModal");
    if (!modalElement) return console.error("Модалка не найдена");

    const modal = new bootstrap.Modal(modalElement);
    modal.show();

    // Очистка вкладок (с проверкой наличия элементов)
    document.getElementById("residentGeneralForm")?.reset();
    const dependencySelect = document.getElementById("residentDependency");
    if (dependencySelect) dependencySelect.innerHTML = "";

    const tasksBlock = document.getElementById("residentTasksContent");
    if (tasksBlock) tasksBlock.innerHTML = "Задания загружаются...";

    const rolesBlock = document.getElementById("residentRolesContent");
    if (rolesBlock) rolesBlock.innerHTML = "Роли загружаются...";

    // Загрузка данных
    fetch(`/residents/api/residents/${residentId}/profile/`)
      .then((res) => {
        if (!res.ok) throw new Error("Ошибка загрузки профиля");
        return res.json();
      })
      .then((data) => {
        fillGeneralTab(data);
        fillTasksTab(data.tasks || []);
        fillRolesTab(data.roles || []);
      })
      .catch((err) => {
        alert("Не удалось загрузить данные резидента.");
        console.error(err);
      });
  };

  // 🧾 Вкладка "Общее"
  function fillGeneralTab(data) {
    document.getElementById("residentModalLabel").textContent = `Личное дело: ${data.full_name || ""}`;
    document.getElementById("residentName").value = data.full_name || "";
    document.getElementById("residentBirthdate").value = data.birthdate || "";
    document.getElementById("residentNotes").value = data.notes || "";

    const select = document.getElementById("residentDependency");
    if (!select) return;
    select.innerHTML = "";

    (data.dependency_choices || []).forEach(([value, label]) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      if (value === data.dependency_type) option.selected = true;
      select.appendChild(option);
    });

    const statusSelect = document.getElementById("residentStatus");
    if (statusSelect) {
      statusSelect.innerHTML = "";
      (data.status_choices || []).forEach(([value, label]) => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = label;
        if (value === data.status) option.selected = true;
        statusSelect.appendChild(option);
      });
    }
  }

  // 📋 Вкладка "Задания"
  function fillTasksTab(tasks) {
    const container = document.getElementById("residentTasksContent");
    if (!container) return;

    if (!tasks.length) {
      container.innerHTML = "<p>Нет данных за последние 14 дней.</p>";
      return;
    }

    let html = `<div class="table-responsive"><table class="table table-bordered table-sm">
      <thead><tr><th>Дата</th><th>Задание</th><th>Статус</th><th>Комментарий</th></tr></thead><tbody>`;

    tasks.forEach((t) => {
      html += `<tr>
        <td>${t.date || ""}</td>
        <td>${t.task_title || ""}</td>
        <td>${t.status_display || ""}</td>
        <td>${t.comment || ""}</td>
      </tr>`;
    });

    html += `</tbody></table></div>`;
    container.innerHTML = html;
  }

  // 🗂 Вкладка "Роли"
  function fillRolesTab(roles) {
    const container = document.getElementById("residentRolesContent");
    if (!container) return;

    if (!roles.length) {
      container.innerHTML = "<p>Нет назначенных ролей.</p>";
      return;
    }

    let html = `<div class="table-responsive"><table class="table table-bordered table-sm">
      <thead><tr><th>Роль</th><th>Назначена</th><th>Снята</th></tr></thead><tbody>`;

    roles.forEach((r) => {
      html += `<tr>
        <td>${r.role_title || ""}</td>
        <td>${r.assigned_at || ""}</td>
        <td>${r.unassigned_at || ""}</td>
      </tr>`;
    });

    html += `</tbody></table></div>`;
    container.innerHTML = html;
  }

  // 💾 Сохранение изменений
  document.getElementById("saveResidentBtn")?.addEventListener("click", function () {
    if (!currentResidentId) return;

    const payload = {
      notes: document.getElementById("residentNotes")?.value,
      dependency_type: document.getElementById("residentDependency")?.value,
      status: document.getElementById("residentStatus")?.value,
    };

    fetch(`/residents/api/residents/${currentResidentId}/profile/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify(payload),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Ошибка при сохранении");
        alert("Изменения сохранены");

        // Обновить таблицу резидентов
        if (typeof window.refreshResidentTableData === "function") {
          window.refreshResidentTableData();
        }
      })
      .catch((err) => {
        console.error(err);
        alert("Не удалось сохранить изменения.");
      });
  });

  // 🛑 Завершение лечения
  document.getElementById("dischargeResidentBtn")?.addEventListener("click", function () {
    if (!currentResidentId) return;

    if (!confirm("Вы уверены, что хотите завершить лечение резидента?")) return;

    fetch(`/residents/api/residents/${currentResidentId}/discharge/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Ошибка при завершении лечения");
        alert("Лечение завершено");

        // Закрыть модалку
        bootstrap.Modal.getInstance(document.getElementById("residentModal"))?.hide();

        // Обновить таблицу
        if (typeof window.refreshResidentTableData === "function") {
          window.refreshResidentTableData();
        }
      })
      .catch((err) => {
        console.error(err);
        alert("Не удалось завершить лечение.");
      });
  });

  // 🔐 CSRF
  function getCSRFToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || "";
  }
});