document.addEventListener("DOMContentLoaded", function () {
  const draggables = document.querySelectorAll(".draggable-task");
  const containers = document.querySelectorAll(".task-list");

  draggables.forEach((task) => {
    task.setAttribute("draggable", true);

    task.addEventListener("dragstart", () => {
      task.classList.add("dragging");
    });

    task.addEventListener("dragend", () => {
      task.classList.remove("dragging");
    });
  });

    containers.forEach((container) => {
      container.addEventListener("dragover", (e) => {
        e.preventDefault();
        const dragging = document.querySelector(".dragging");
        const afterElement = getDragAfterElement(container, e.clientY);
        if (afterElement == null) {
          container.appendChild(dragging);
        } else {
          container.insertBefore(dragging, afterElement);
        }
      });

      container.addEventListener("drop", function (e) {
        e.preventDefault();
        const task = document.querySelector(".dragging");
        const taskId = task.getAttribute("data-task-id");
        const newStatus = container.getAttribute("data-status");

        // Обновляем атрибут внутри DOM (если используется где-то)
        task.setAttribute("data-status", newStatus);

        // Обновляем статус задачи на сервере
        fetch(`/update-status/${taskId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({ status: newStatus }),
        })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            console.log("Статус задачи обновлён");
          } else {
            console.error("Ошибка при обновлении:", data.error);
          }
        })
        .catch((error) => {
          console.error("Ошибка запроса:", error);
        });
      });
    });


  function getDragAfterElement(container, y) {
    const elements = [...container.querySelectorAll(".draggable-task:not(.dragging)")];
    return elements.reduce((closest, child) => {
      const box = child.getBoundingClientRect();
      const offset = y - box.top - box.height / 2;
      if (offset < 0 && offset > closest.offset) {
        return { offset: offset, element: child };
      } else {
        return closest;
      }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
  }

  function getCSRFToken() {
    let name = "csrftoken";
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});