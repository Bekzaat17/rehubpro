document.addEventListener("DOMContentLoaded", function () {
  const residentModal = new bootstrap.Modal(document.getElementById("residentTaskModal"));
  const modalBody = document.querySelector("#residentTaskModal .modal-body");

  const modalResidentName = document.getElementById("modalResidentName");
  const modalTaskTitle = document.getElementById("modalTaskTitle");
  const modalTaskStatus = document.getElementById("modalTaskStatus");
  const modalAssignedAt = document.getElementById("modalAssignedAt");

  const assignTaskBtn = document.getElementById("assignTaskBtn");
  const addProgressBtn = document.getElementById("addProgressBtn");

  let currentResidentId = null;
  let currentTaskId = null;

  // Открытие модалки по клику на строку резидента
  document.querySelectorAll(".resident-row").forEach(row => {
    row.addEventListener("click", () => {
      const { residentId, residentName, taskId, taskTitle, taskStatus, assignedAt } = row.dataset;

      currentResidentId = residentId;
      currentTaskId = taskId;

      modalResidentName.textContent = residentName;
      modalTaskTitle.textContent = taskTitle || "—";
      modalTaskStatus.textContent = taskStatus || "—";
      modalAssignedAt.textContent = assignedAt || "—";

      clearDynamicForms();

      assignTaskBtn.classList.add("d-none");
      addProgressBtn.classList.add("d-none");

      if (!taskId || taskStatus === "completed") {
        assignTaskBtn.classList.remove("d-none");
        assignTaskBtn.onclick = () => openAssignTaskForm(residentId);
      } else if (["writing", "submitting"].includes(taskStatus)) {
        addProgressBtn.classList.remove("d-none");
        addProgressBtn.onclick = () => openAddProgressForm(taskId);
      }

      console.log(123456);
      // В конце функции .resident-row click:
      fetch(`/tasks/progress-history/resident/${residentId}`)
        .then(res => res.json())
        .then(data => renderProgressHistory(data));

      residentModal.show();
    });
  });

  function openAssignTaskForm(residentId) {
    clearDynamicForms();

    fetch(`/tasks/available/?resident_id=${residentId}`)
      .then(res => res.json())
      .then(data => {
        modalBody.insertAdjacentHTML("beforeend", `
          <hr id="assignTaskFormHr">
          <form id="assignTaskForm">
            <div class="mb-2">
              <label class="form-label">Выберите задание</label>
              <select class="form-select" name="task_id" required>
                <option value="">—</option>
                ${data.available_tasks.map(task => `<option value="${task.id}">${task.title}</option>`).join("")}
              </select>
            </div>
            <button class="btn btn-primary w-100" type="submit">Назначить</button>
          </form>
        `);

        document.getElementById("assignTaskForm").addEventListener("submit", e => {
          e.preventDefault();
          const taskId = new FormData(e.target).get("task_id");

          fetch("/tasks/assign/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
              resident_id: residentId,
              task_id: taskId
            })
          }).then(() => location.reload());
        });
      });
  }

  function openAddProgressForm(taskId) {
    clearDynamicForms();

    modalBody.insertAdjacentHTML("beforeend", `
      <hr id="progressFormHr">
      <form id="progressForm">
        <div class="mb-2">
          <label class="form-label">Этап</label>
          <select class="form-select" name="stage" required>
            <option value="">—</option>
            <option value="writing">Пишет</option>
            <option value="submitting">Сдаёт</option>
            <option value="completed">Выполнено</option>
          </select>
        </div>
        <div class="mb-2">
          <label class="form-label">Комментарий</label>
          <textarea class="form-control" name="comment" rows="2"></textarea>
        </div>
        <button class="btn btn-success w-100" type="submit">Добавить прогресс</button>
      </form>
    `);

    document.getElementById("progressForm").addEventListener("submit", e => {
      e.preventDefault();
      const form = new FormData(e.target);

      fetch("/tasks/add-progress/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
          task_id: taskId,
          stage: form.get("stage"),
          comment: form.get("comment")
        })
      }).then(() => location.reload());
    });
  }

  function clearDynamicForms() {
    modalBody.querySelector("#assignTaskForm")?.remove();
    modalBody.querySelector("#assignTaskFormHr")?.remove();
    modalBody.querySelector("#progressForm")?.remove();
    modalBody.querySelector("#progressFormHr")?.remove();
  }

  function getCookie(name) {
    return document.cookie
      .split("; ")
      .find(row => row.startsWith(name + "="))
      ?.split("=")[1];
  }

  function renderProgressHistory(history) {
    console.log(123);
    console.log(history);
    const modalBody = document.querySelector("#residentTaskModal .modal-body");

    // Удалим старый блок, если есть
    document.getElementById("progressHistoryBlock")?.remove();

    const historyBlock = document.createElement("div");
    historyBlock.id = "progressHistoryBlock";
    historyBlock.innerHTML = `
      <hr>
      <h6>📚 История прогресса</h6>
      <div class="accordion" id="progressAccordion"></div>
    `;
    modalBody.appendChild(historyBlock);

    const accordion = historyBlock.querySelector("#progressAccordion");

    history.forEach((taskItem, index) => {
      const taskId = taskItem.task.id;
      const taskTitle = taskItem.task.title;
      const assignedAt = taskItem.task.assigned_at;

      const itemId = `task-${taskId}`;

      const progressesHtml = taskItem.progresses.map(p => `
        <div class="border rounded p-2 mb-2">
          <div><strong>Этап:</strong> ${p.stage}</div>
          <div><strong>Комментарий:</strong> ${p.comment || "—"}</div>
          <div class="text-muted"><small>${p.created_at}</small></div>
        </div>
      `).join("");

      accordion.insertAdjacentHTML("beforeend", `
        <div class="accordion-item">
          <h2 class="accordion-header" id="heading-${itemId}">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-${itemId}" aria-expanded="false">
              ${taskTitle} <span class="ms-auto text-muted small">(${assignedAt})</span>
            </button>
          </h2>
          <div id="collapse-${itemId}" class="accordion-collapse collapse" aria-labelledby="heading-${itemId}" data-bs-parent="#progressAccordion">
            <div class="accordion-body" style="max-height: 200px; overflow-y: auto;">
              ${progressesHtml || "<em>Нет прогресса</em>"}
            </div>
          </div>
        </div>
      `);
    });
  }
});