document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".report-form").forEach(form => {
    form.addEventListener("submit", function (event) {
      event.preventDefault();

      const reportId = this.dataset.reportId;
      const formData = new FormData(this);

      fetch(`/reports/save/${reportId}/`, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
      })
        .then(response => response.json())
        .then(data => {
          const card = document.getElementById(`report-card-${reportId}`);
          const errorBox = document.getElementById(`error-box-${reportId}`);
          const collapseElement = document.getElementById(`collapse-${reportId}`);

          // Удаляем старые классы и добавляем нужный
          card.classList.remove("border-left-success", "border-left-danger");

          if (data.success) {
            card.classList.add("border-left-success");
            errorBox.classList.add("d-none");
            errorBox.innerText = "";

            const bsCollapse = bootstrap.Collapse.getOrCreateInstance(collapseElement);
            bsCollapse.hide();
          } else {
            card.classList.add("border-left-danger");
            errorBox.classList.remove("d-none");
            errorBox.innerText = typeof data.errors === "string"
              ? data.errors
              : Object.values(data.errors).join(", ");
          }
        })
        .catch(error => {
          console.error("Ошибка:", error);
        });
    });
  });
});