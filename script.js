function sendMessage() {
    let input = document.getElementById("input").value;

    let chatBox = document.getElementById("chat");

    chatBox.innerHTML += "<p><b>You:</b> " + input + "</p>";

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: input
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);

        chatBox.innerHTML += "<p><b>AI:</b> " + data.reply + "</p>";
    });
}
async function clearChat() {

    const response = await fetch("http://127.0.0.1:8000/clear-chat", {
        method: "POST"
    });

    const data = await response.json();

    alert(data.message);

}