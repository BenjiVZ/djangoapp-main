document.addEventListener('DOMContentLoaded', function() {
    const filterButton = document.getElementById('filter-button');
    const filterContainer = document.getElementById('intelligent-filter-container');
    let filterActive = false;

    filterButton.addEventListener('click', function() {
        filterActive = !filterActive;
        if (filterActive) {
            filterButton.style.backgroundColor = '#ff4500';
            filterButton.textContent = 'Desactivar Filtrado';
            filterContainer.style.display = 'block';
            loadFilterChat();
        } else {
            filterButton.style.backgroundColor = '#2EE59D';
            filterButton.textContent = 'Filtrado Inteligente';
            filterContainer.style.display = 'none';
        }
    });

    function loadFilterChat() {
        fetch('/intelligent_filter_chat/')
            .then(response => response.text())
            .then(html => {
                filterContainer.innerHTML = html;
                // Initialize the filter chat functionality
                initializeFilterChat();
            });
    }

    function initializeFilterChat() {
        const filterChatLog = document.getElementById('filter-chat-log');
        const filterUserMessage = document.getElementById('filter-user-message');
        const filterSendButton = document.getElementById('filter-send-button');

        filterSendButton.addEventListener('click', sendFilterMessage);
        filterUserMessage.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendFilterMessage();
            }
        });

        function sendFilterMessage() {
            const message = filterUserMessage.value;
            if (message.trim() === '') return;

            filterChatLog.innerHTML += `<div class="message user-message">${message}</div>`;

            fetch('/intelligent_filter/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ "message": message })
            })
            .then(response => response.json())
            .then(data => {
                data.forEach((msg) => {
                    filterChatLog.innerHTML += `<div class="message bot-message">${msg.text}</div>`;
                });

                filterChatLog.scrollTop = filterChatLog.scrollHeight;
                filterUserMessage.value = '';
            });
        }
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});