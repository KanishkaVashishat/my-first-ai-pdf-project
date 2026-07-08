const API_URL = "http://127.0.0.1:8000";

const chatBox = document.getElementById("chat-box");
const sendBtn = document.getElementById("send-btn");
const pdfInput = document.getElementById("pdf-file");
const input = document.getElementById("user-input");

function getTime() {
    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });
}

function addMessage(message, sender) {

    const div = document.createElement("div");

    div.className = sender === "user"
        ? "user-message"
        : "ai-message";

    div.innerHTML = `
        <div>${message}</div>
        <small style="color:gray;">${getTime()}</small>
    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {

    const message = input.value.trim();

    if (message === "") return;

    addMessage(message, "user");

    input.value = "";

    sendBtn.disabled = true;
    sendBtn.innerText = "Thinking...";

    const typing = document.createElement("div");

    typing.className = "ai-message";
    typing.id = "typing";

    typing.innerHTML = `
        🤖 <b>AI</b><br>
        <span style="font-size:20px;">● ● ●</span>
    `;

    chatBox.appendChild(typing);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch(API_URL + "/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        const typingDiv = document.getElementById("typing");

        if (typingDiv) {
            typingDiv.remove();
        }

        addMessage(data.reply, "ai");

    }

    catch (error) {

        const typingDiv = document.getElementById("typing");

        if (typingDiv) {
            typingDiv.remove();
        }

        addMessage("❌ Unable to connect to backend.", "ai");

    }

    finally {

        sendBtn.disabled = false;
        sendBtn.innerText = "Send";
        input.focus();

    }

}

async function uploadPDF() {

    const file = pdfInput.files[0];

    if (!file) {

        alert("Please choose a PDF.");

        return;

    }

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch(API_URL + "/upload", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        addMessage(
            `📄 <b>${file.name}</b> uploaded successfully.`,
            "ai"
        );

    }

    catch (error) {

        addMessage("❌ PDF upload failed.", "ai");

    }

}

function clearChat() {

    if (!confirm("Clear all messages?")) return;

    chatBox.innerHTML = "";

    addMessage(
        "👋 Chat cleared. Upload another PDF to continue.",
        "ai"
    );

}

input.addEventListener("keydown", function (e) {

    if (e.key === "Enter") {

        sendMessage();

    }

});