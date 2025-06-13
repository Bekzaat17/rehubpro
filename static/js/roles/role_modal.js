document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".resident-row").forEach(row => {
    row.addEventListener("click", () => {
      const residentId = row.dataset.residentId;
      openRoleModal(residentId);
    });
  });
});

// Загрузка модалки
function openRoleModal(residentId) {
  fetch(`/roles/resident/${residentId}/modal/`, {
    headers: { "X-Requested-With": "XMLHttpRequest" }
  })
    .then(res => res.text())
    .then(html => {
      document.getElementById("roleModalContent").innerHTML = html;
      const roleModal = new bootstrap.Modal(document.getElementById("roleModal"));
      roleModal.show();
      initRoleModalEvents(residentId);
    })
    .catch(err => console.error("Error loading modal:", err));
}

// Инициализация событий внутри модалки
function initRoleModalEvents(residentId) {
  const container = document.getElementById("roleModalContent");

  // Назначение роли
  const assignForm = container.querySelector("#assign-role-form");
  if (assignForm) {
    assignForm.addEventListener("submit", async e => {
      e.preventDefault();
      const formData = new FormData(assignForm);
      formData.append("action", "assign");
      const resp = await fetch(`/roles/resident/${residentId}/modal/`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken")
        },
        body: formData
      });
      const data = await resp.json();
      if (data.success) openRoleModal(residentId);
      else alert(data.message || "Ошибка назначения");
    });
  }

  // Обработка кнопки "Завершить" — показать поле комментария
  container.querySelectorAll(".end-role-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const assignmentId = btn.dataset.assignmentId;

      // Показать секцию ввода комментария
      const commentSection = container.querySelector("#end-role-comment-section");
      const commentInput = commentSection.querySelector("#end-role-comment");
      const confirmBtn = commentSection.querySelector("#confirm-end-role");

      commentInput.value = "";
      commentSection.classList.remove("d-none");
      commentSection.scrollIntoView({ behavior: "smooth" });

      // Удалить предыдущий обработчик (если был), затем добавить новый
      const newBtn = confirmBtn.cloneNode(true);
      confirmBtn.parentNode.replaceChild(newBtn, confirmBtn);

      newBtn.addEventListener("click", async () => {
        const comment = commentInput.value;
        const formData = new FormData();
        formData.append("action", "end");
        formData.append("assignment_id", assignmentId);
        formData.append("comment", comment);
        const resp = await fetch(`/roles/resident/${residentId}/modal/`, {
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
          },
          body: formData
        });
        const data = await resp.json();
        if (data.success) {
          openRoleModal(residentId);
        } else {
          alert(data.message || "Ошибка завершения");
        }
      });
    });
  });
}

// Получить CSRF из cookie
function getCookie(name) {
  const v = `; ${document.cookie}`.split(`; ${name}=`);
  return v.length === 2 ? v.pop().split(';').shift() : '';
}