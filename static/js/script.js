// static/js/script.js
function sendMessage() {
    const inputField = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
    const userInput = inputField.value.trim();

    if (!userInput) return;

    // Hiển thị tin nhắn người dùng
    chatBox.innerHTML += `<div class="message user"><strong>Bạn:</strong> ${userInput}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Hiển thị hiệu ứng "Bot đang gõ..."
    const loadingId = `bot-msg-${Date.now()}`;
    chatBox.innerHTML += `<div class="message bot" id="${loadingId}"><strong>Bot:</strong> <span class="typing">Đang gõ...</span></div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Gửi dữ liệu đến server
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userInput })
    })
    .then(res => res.json())
    .then(data => {
        // Hiệu ứng gõ từng ký tự
        const typingEl = document.getElementById(loadingId).querySelector(".typing");
        typingEl.innerHTML = "";
        let i = 0;
        const text = data.answer;
        const typingInterval = setInterval(() => {
            if (i < text.length) {
                typingEl.innerHTML += text.charAt(i);
                i++;
                chatBox.scrollTop = chatBox.scrollHeight;
            } else {
                clearInterval(typingInterval);
            }
        }, 20);
    })
    .catch(err => {
        const typingEl = document.getElementById(loadingId).querySelector(".typing");
        typingEl.innerHTML = `Lỗi kết nối: ${err}`;
    });

    inputField.value = "";
}
