const TASK_TYPE_LABELS = {
    short_term: "Краткосрочное",
    long_term: "Долгосрочное",
    test: "Тестовое"
};

document.addEventListener("DOMContentLoaded", function () {
    loadTemplates();
});

function loadTemplates() {
    fetch("/tasks/templates/api/")
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector("#templateTable tbody");
            tbody.innerHTML = "";
            data.forEach(template => {
                const row = document.createElement("tr");
                row.classList.add("clickable-row");
                row.style.cursor = "pointer";
                row.onclick = () => openTemplateModal(template.id, template.title, template.description, template.task_type);
                row.innerHTML = `
                    <td>${template.title}</td>
                    <td>${template.description}</td>
                    <td>${TASK_TYPE_LABELS[template.task_type] || template.task_type}</td>
                `;
                tbody.appendChild(row);
            });
        });
}

function openTemplateModal(id = null, title = '', description = '', taskType = 'short_term') {
    document.getElementById("templateId").value = id || '';
    document.getElementById("title").value = title || '';
    document.getElementById("description").value = description || '';
    document.getElementById("taskType").value = taskType || 'short_term';

    const deleteBtn = document.getElementById("deleteBtn");
    if (id) {
        deleteBtn.style.display = "inline-block";
    } else {
        deleteBtn.style.display = "none";
    }

    const modal = new bootstrap.Modal(document.getElementById("taskTemplateModal"));
    modal.show();
}

function submitTemplateForm(event) {
    event.preventDefault();
    const id = document.getElementById("templateId").value;
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const task_type = document.getElementById("taskType").value;

    fetch("/tasks/templates/api/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ id, title, description, task_type })
    })
    .then(res => res.json())
    .then(() => {
        bootstrap.Modal.getInstance(document.getElementById("taskTemplateModal")).hide();
        loadTemplates();
    });
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


function deleteTemplate() {
    const id = document.getElementById("templateId").value;
    if (!id) return;

    if (!confirm("Вы уверены, что хотите удалить этот шаблон?")) return;

    fetch(`/tasks/templates/api/${id}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        }
    })
    .then(res => {
        if (res.ok) {
            bootstrap.Modal.getInstance(document.getElementById("taskTemplateModal")).hide();
            loadTemplates();
        } else {
            alert("Ошибка при удалении шаблона.");
        }
    });
}