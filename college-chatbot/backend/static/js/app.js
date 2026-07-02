// Backend API URL
const API_URL = '/chat';

const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendQuickAction(actionText) {
    const input = document.getElementById('user-input');
    if(input) {
        input.value = actionText;
        sendMessage();
    }
}

async function sendMessage() {
    if(!userInput) return;
    
    const text = userInput.value.trim();
    if (!text) return;

    // Add user message
    appendMessage(text, 'user');
    userInput.value = '';
    
    // Simulate thinking/typing
    showTypingIndicator();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: text })
        });
        
        const data = await response.json();
        removeTypingIndicator();
        appendMessage(data.response, 'bot');
    } catch (error) {
        removeTypingIndicator();
        appendMessage("Error connecting to the backend server. Make sure the Python server is running on port 8000.", 'bot');
    }
}

function appendMessage(text, sender) {
    if(!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    if(!chatMessages) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot typing-indicator-container';
    messageDiv.id = 'typing-indicator';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content typing-indicator';
    
    contentDiv.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// Admin Login Logic
function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Mock authentication
    if(username && password) {
        localStorage.setItem('isAdminLoggedIn', 'true');
        window.location.href = 'admin-dashboard.html';
    }
}
