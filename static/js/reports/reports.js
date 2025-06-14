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

          if (data.success) {
            card.style.borderLeft = "5px solid green";
            errorBox.style.display = "none";
          } else {
            errorBox.style.display = "block";
            errorBox.innerText = typeof data.errors === "string"
              ? data.errors
              : Object.values(data.errors).join(", ");
            card.style.borderLeft = "5px solid red";
          }
        })
        .catch(error => {
          console.error("Ошибка:", error);
        });
    });
  });
});