document.addEventListener("DOMContentLoaded", function () {
    const modal = new bootstrap.Modal(document.getElementById("reminderModal"));
    const form = document.getElementById("reminderForm");
    const createBtn = document.getElementById("createReminderBtn");
    const deleteBtn = document.getElementById("deleteReminderBtn");

    const datetimeInput = document.getElementById("datetimeInput");
    const isActiveInput = document.getElementById("isActiveInput");

    function openModal(data = null) {
        form.reset();
        form.reminder_id.value = data?.id || "";
        document.getElementById("reminderModalTitle").textContent = data ? "Редактировать" : "Новое напоминание";
        deleteBtn.classList.toggle("d-none", !data);

        if (data) {
            form.title.value = data.title;
            form.text.value = data.text;
            form.datetime.value = data.datetime.slice(0, 16);
            form.repeat.value = data.repeat;
            form.is_active.checked = data.is_active;
            deleteBtn.dataset.id = data.id;
        } else {
            // По умолчанию галочка "Активно" включена
            isActiveInput.checked = true;
        }

        modal.show();
    }

    // ✅ Включаем "Активно", если изменили дату/время
    if (datetimeInput && isActiveInput) {
        datetimeInput.addEventListener("change", () => {
            if (datetimeInput.value) {
                isActiveInput.checked = true;
            }
        });
    }

    createBtn.addEventListener("click", () => openModal());

    document.querySelectorAll(".reminder-row").forEach(row => {
        row.addEventListener("click", () => {
            const id = row.dataset.id;
            fetch(`/reminders/${id}/`)
                .then(res => res.json())
                .then(data => openModal(data));
        });
    });

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const id = form.reminder_id.value;
        const url = id ? `/reminders/create/?id=${id}` : "/reminders/create/";
        const method = "POST";

        const formData = new FormData(form);
        fetch(url, {
            method,
            headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
            body: formData,
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    modal.hide();
                    refreshTable();
                } else {
                    alert("Ошибка при сохранении");
                }
            });
    });

    deleteBtn.addEventListener("click", function () {
        if (!confirm("Удалить напоминание?")) return;
        const id = deleteBtn.dataset.id;

        fetch(`/reminders/delete/${id}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            }
        }).then(res => res.json()).then(data => {
            if (data.success) {
                modal.hide();
                refreshTable();
            } else {
                alert("Ошибка удаления");
            }
        });
    });

    function refreshTable() {
        fetch("/reminders/list/")
            .then(res => res.text())
            .then(html => {
                document.getElementById("remindersTableWrapper").innerHTML = html;
                document.querySelectorAll(".reminder-row").forEach(row => {
                    row.addEventListener("click", () => {
                        const id = row.dataset.id;
                        fetch(`/reminders/${id}/`)
                            .then(res => res.json())
                            .then(data => openModal(data));
                    });
                });
            });
    }
});