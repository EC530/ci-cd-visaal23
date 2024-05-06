const conversations = {
    '1': {
        user: 'Gracie Morris',
        avatar: 'images/avatar-2.jpg',
        status: 'online',
        messages: [
            { type: 'received', text: 'Hi Dr. Oliver, just wanted to let you know about my eczema.', time: '10:21 am' },
            { type: 'sent', text: 'Thanks for reaching out, Gracie.', time: '10:22 am' }
        ]
    },
    '2': {
        user: 'Oliver Barnes',
        avatar: 'images/avatar-1.jpg',
        status: 'offline',
        messages: [
            { type: 'received', text: 'I need advice on my current medication.', time: 'Yesterday' }
        ]
    },
    '3': {
        user: 'Adam King',
        avatar: 'images/avatar-4.jpg',
        status: 'online',
        messages: [
            { type: 'received', text: 'Can we discuss my treatment plan?', time: '24.02.19' }
        ]
    }
};

let selectedUserId = '1'; // Default to the first user

document.addEventListener('DOMContentLoaded', function() {
    loadMessagePreviews();
    loadConversation(selectedUserId); // Load first conversation by default
});

function loadMessagePreviews() {
    const container = document.getElementById('messagePreviews');
    container.innerHTML = Object.keys(conversations).map(userId => {
        const { user, avatar, status, messages } = conversations[userId];
        return `
            <div class="message__short" data-user-id="${userId}" onclick="selectUser('${userId}')">
                <div class="message__short-header">
                    <div class="messages__short-thumb"><img src="${avatar}" alt="${user}"/><span class="status status--${status}"></span></div>
                    <div class="messages__short-name">${user}</div>
                    <div class="messages__short-date">${messages[messages.length - 1].time}</div>  
                </div>
                <div class="message__short-content">
                    <p class="messages__short-text">${messages[messages.length - 1].text.substring(0, 50)}...</p>
                </div>
            </div>
        `;
    }).join('');
}

function selectUser(userId) {
    selectedUserId = userId;
    loadConversation(userId);
}

function sendMessage(event) {
    event.preventDefault();
    const textarea = document.querySelector('.messages__footer-textarea');
    const messageText = textarea.value.trim();

    if (messageText === '') {
        console.log("No message entered");
        return;
    }

    conversations[selectedUserId].messages.push({
        type: 'sent',
        text: messageText,
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    });

    loadConversation(selectedUserId);
    textarea.value = '';
}

function loadConversation(userId) {
    const data = conversations[userId];
    document.querySelector('.messages__header-thumb').innerHTML = `<img src="${data.avatar}" alt="${data.user}"/><span class="status status--${data.status}"></span>`;
    document.querySelector('.messages__header-user').textContent = data.user;

    const messagesContainer = document.querySelector('.conversation');
    messagesContainer.innerHTML = data.messages.map(msg => `
        <li class="conversation__row conversation__row--${msg.type}">
            <div class="conversation__content">
                <p>${msg.text}</p>
                <span class="conversation__time">${msg.time}</span>
            </div>
            <div class="conversation__avatar"><img src="${data.avatar}" alt="" /></div>
        </li>
    `).join('');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}