const chatWindow = document.getElementById('chat-window');
const typingIndicator = document.getElementById('typing-indicator');
const messageInput = document.getElementById('message');
const imageInput = document.getElementById('image_input');
const BACKEND_URL = 'https://da-bot-vjpp.onrender.com';
function handleEnter(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
}

function appendMessage(role, content, isImage = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    if (isImage) {
        bubble.innerHTML = `<img src="${content}" class="image-preview">`;
    } else {
        // Parse markdown for text content
        bubble.innerHTML = marked.parse(content);
    }

    msgDiv.appendChild(bubble);
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function handleImageSelect() {
    if (imageInput.files.length > 0) {
        sendMessage();
    }
}

async function sendMessage() {
    const userId = document.getElementById('user_id').value || 'user_01';
    const text = messageInput.value.trim();
    const file = imageInput.files[0];

    if (!text && !file) return;

    messageInput.value = '';

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            appendMessage('user', e.target.result, true);
        };
        reader.readAsDataURL(file);

        typingIndicator.style.display = 'block';
        chatWindow.scrollTop = chatWindow.scrollHeight;

        const formData = new FormData();
        formData.append('user_id', userId);
        formData.append('image', file);

        try {
            const response = await fetch(`${BACKEND_URL}/image-chat`, {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data.reply) {
                appendMessage('ai', data.reply);
            } else if (data.error) {
                appendMessage('ai', `Error: ${data.error}`);
            } else {
                appendMessage('ai', "Image analyzed, but no response received.");
            }
        } catch (e) {
            appendMessage('ai', "Error uploading image.");
        } finally {
            typingIndicator.style.display = 'none';
            imageInput.value = '';
        }

    } else {
        appendMessage('user', text);
        typingIndicator.style.display = 'block';
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            const response = await fetch(`${BACKEND_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    query: text
                })
            });
            const data = await response.json();
            if (data.reply) {
                appendMessage('ai', data.reply);
            } else if (data.error) {
                appendMessage('ai', `Error: ${data.error}`);
            } else {
                appendMessage('ai', "Message processed, but no response received.");
            }
        } catch (e) {
            appendMessage('ai', "Error connecting to server.");
        } finally {
            typingIndicator.style.display = 'none';
        }
    }
}
