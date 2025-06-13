document.addEventListener("DOMContentLoaded", () => {
  const modal = new bootstrap.Modal(document.getElementById("roleModal"));
  const roleForm = document.getElementById("roleForm");

  document.getElementById("addRoleBtn").addEventListener("click", () => {
    roleForm.reset();
    document.getElementById("roleId").value = "";
    modal.show();
  });

  document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const row = btn.closest("tr");
      document.getElementById("roleId").value = row.dataset.roleId;
      document.getElementById("roleName").value = row.children[0].textContent.trim();
      document.getElementById("roleSlug").value = row.children[1].textContent.trim();
      document.getElementById("roleDescription").value = row.children[2].textContent.trim();
      modal.show();
    });
  });

  document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const roleId = btn.closest("tr").dataset.roleId;
      if (confirm("Удалить эту роль?")) {
        fetch(`/roles/manage/api/${roleId}/`, {
          method: "DELETE",
          headers: { "X-CSRFToken": getCSRFToken() },
        })
        .then(() => location.reload());
      }
    });
  });

  roleForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(roleForm);
    const roleId = formData.get("id");

    const url = roleId
      ? `/roles/manage/api/${roleId}/`
      : "/roles/manage/api/";

    const method = roleId ? "PUT" : "POST";

    fetch(url, {
      method: method,
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
      body: method === "POST" ? formData : new URLSearchParams(formData),
    })
    .then(res => res.json())
    .then(() => location.reload());
  });

  function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
  }
});