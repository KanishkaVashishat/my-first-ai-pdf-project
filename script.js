const API_BASE = "";

const fileInput = document.getElementById("fileInput");
const uploadDrop = document.getElementById("uploadDrop");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const volumeMeta = document.getElementById("volumeMeta");
const clearPdfBtn = document.getElementById("clearPdfBtn");
const clearChatBtn = document.getElementById("clearChatBtn");

const chatLog = document.getElementById("chatLog");
const emptyState = document.getElementById("emptyState");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const askBtn = chatForm.querySelector(".ask-btn");

const marginaliaBody = document.getElementById("marginaliaBody");

let pdfReady = false;

// ---------- Helpers ----------

function setStatus(active, text, meta) {
  pdfReady = active;
  statusDot.classList.toggle("active", active);
  statusText.textContent = text;
  volumeMeta.innerHTML = meta || "";
}

function appendMessage(role, text) {
  emptyState.style.display = "none";

  const msg = document.createElement("div");
  msg.className = `msg ${role}`;

  const label = document.createElement("span");
  label.className = "msg-label";
  label.textContent = role === "user" ? "You" : "The Assistant";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  msg.appendChild(label);
  msg.appendChild(bubble);
  chatLog.appendChild(msg);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function renderSources(sources) {
  marginaliaBody.innerHTML = "";

  if (!sources || sources.length === 0) {
    marginaliaBody.innerHTML = `<p class="marginalia-empty">No passages were drawn on for this answer.</p>`;
    return;
  }

  sources.forEach((chunk, i) => {
    const note = document.createElement("div");
    note.className = "note";

    const index = document.createElement("span");
    index.className = "note-index";
    index.textContent = `Passage ${i + 1}`;

    const text = document.createElement("div");
    text.className = "note-text";
    text.textContent = chunk.length > 220 ? chunk.slice(0, 220) + "…" : chunk;

    note.appendChild(index);
    note.appendChild(text);
    marginaliaBody.appendChild(note);
  });
}

// ---------- Upload ----------

uploadDrop.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;

  setStatus(false, "Indexing volume…");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`$/upload`, {
      method: "POST",
      body: formData
    });
    const data = await res.json();

    if (data.error) {
      setStatus(false, "No volume open");
      alert(data.error);
      return;
    }

    setStatus(
      true,
      data.filename,
      `${data.characters.toLocaleString()} characters · ${data.chunks} passages indexed`
    );
  } catch (err) {
    console.error(err);
    setStatus(false, "No volume open");
    alert("Could not reach the backend. Is it running on port 8000?");
  }
});

// ---------- Chat ----------

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const message = messageInput.value.trim();
  if (!message) return;

  if (!pdfReady) {
    alert("Place a PDF on the desk first.");
    return;
  }

  appendMessage("user", message);
  messageInput.value = "";
  askBtn.disabled = true;

  try {
    const res = await fetch(`$/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await res.json();

    appendMessage("assistant", data.reply);
    renderSources(data.sources);
  } catch (err) {
    console.error(err);
    appendMessage("assistant", "Something went wrong reaching the backend.");
  } finally {
    askBtn.disabled = false;
  }
});

// ---------- Clear buttons ----------

clearPdfBtn.addEventListener("click", async () => {
  await fetch(`$/clear-pdf`, { method: "POST" });
  setStatus(false, "No volume open");
  marginaliaBody.innerHTML = `<p class="marginalia-empty">Passages the assistant drew on will appear here, annotated like margin notes.</p>`;
});

clearChatBtn.addEventListener("click", async () => {
  await fetch(`$/clear-chat`, { method: "POST" });
  chatLog.innerHTML = "";
  chatLog.appendChild(emptyState);
  emptyState.style.display = "block";
  marginaliaBody.innerHTML = `<p class="marginalia-empty">Passages the assistant drew on will appear here, annotated like margin notes.</p>`;
});

// ---------- Initial state check ----------

(async function init() {
  try {
    const res = await fetch(`$/pdf-info`);
    const data = await res.json();

    if (data.uploaded) {
      setStatus(
        true,
        data.filename || "Untitled volume",
        `${data.characters.toLocaleString()} characters · ${data.chunks_indexed} passages indexed`
      );
    }
  } catch (err) {
    // Backend not running yet — silent, upload will surface the error.
  }
})();