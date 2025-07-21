document.addEventListener("DOMContentLoaded", () => {
    const bell = document.getElementById('notification-bell');
    const count = document.getElementById('notification-count');
    const list = document.getElementById('notification-list');

    let unreadCount = 0;

    function updateCounter() {
        if (unreadCount > 0) {
            count.innerText = unreadCount;
            count.style.display = 'inline-block';
        } else {
            count.style.display = 'none';
        }
    }

    function getCookie(name) {
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

    function createNotificationElement(data, autoDismiss = false) {
        const li = document.createElement('li');
        li.className = "notification-item d-flex flex-column";
        li.dataset.id = data.id;

        const title = document.createElement('h6');
        title.textContent = data.title;

        const message = document.createElement('p');
        message.textContent = data.message;

        const button = document.createElement('button');
        button.className = "btn btn-sm btn-outline-secondary align-self-end mt-1";
        button.textContent = "Прочитано";

        let autoDismissTimer = null;
        let isRead = false;

        const markAsRead = () => {
            if (isRead) return;
            isRead = true;

            clearTimeout(autoDismissTimer);
            li.classList.add("fade-out");
            setTimeout(() => li.remove(), 500);

            unreadCount -= 1;
            updateCounter();

            fetch("/notifications/mark-read/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: `id=${data.id}`,
            });

            if (list.children.length === 0) {
                const empty = document.createElement("li");
                empty.className = "text-muted small text-center";
                empty.textContent = "Нет новых уведомлений";
                list.appendChild(empty);
            }
        };

        button.onclick = markAsRead;

        li.appendChild(title);
        li.appendChild(message);
        li.appendChild(button);

        if (autoDismiss) {
            autoDismissTimer = setTimeout(() => {
                li.classList.add("fade-out");
                setTimeout(() => li.remove(), 500);
                // Не уменьшаем счётчик — пользователь не нажал "Прочитано"
            }, 30000);
        }

        return li;
    }

    function fetchUnreadCount() {
        fetch("/notifications/unread-count/")
            .then(response => response.json())
            .then(data => {
                unreadCount = data.unread || 0;
                updateCounter();
            });
    }

    function fetchUnreadNotifications() {
        fetch("/notifications/unread/")
            .then(response => response.json())
            .then(data => {
                list.innerHTML = '';
                const items = data.notifications;

                unreadCount = items.length;
                updateCounter();

                if (items.length === 0) {
                    const empty = document.createElement("li");
                    empty.className = "text-muted small text-center";
                    empty.textContent = "Нет новых уведомлений";
                    list.appendChild(empty);
                } else {
                    items.forEach(n => {
                        const li = createNotificationElement(n);
                        list.appendChild(li);
                    });
                }
            });
    }

    function connect() {
        if (typeof CURRENT_USER_ID === "undefined") return;

        const protocol = window.location.protocol === "https:" ? "wss" : "ws";
        const socket = new WebSocket(`${protocol}://${window.location.host}/ws/notifications/`);

        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            unreadCount += 1;
            updateCounter();

            // Удалим "Нет новых уведомлений"
            if (list.children.length === 1 && list.children[0].classList.contains("text-muted")) {
                list.innerHTML = '';
            }

            const li = createNotificationElement(data, true);
            list.prepend(li);

            // Автооткрытие меню (если оно закрыто)
            const dropdown = bootstrap.Dropdown.getOrCreateInstance(bell);
            dropdown.show();
        };

        socket.onclose = function () {
            console.warn("❌ WebSocket закрыт, переподключение...");
            setTimeout(connect, 3000);
        };
    }

    bell.addEventListener("click", () => {
        fetchUnreadNotifications();
    });

    fetchUnreadCount();
    connect();
});