const recordRadio = document.querySelector('input[value="record"]');
const uploadRadio = document.querySelector('input[value="upload"]');
const recordSection = document.getElementById("recordSection");
const uploadSection = document.getElementById("uploadSection");
const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const playback = document.getElementById("playback");
const showAudioBtn = document.getElementById("showAudioBtn");
const feedbackSection = document.getElementById("feedbackSection");
const feedbackBox = document.getElementById("feedbackBox");
const scoreBox = document.getElementById("scoreBox");
const fileInput = document.getElementById("file");
const submitBtn = document.querySelector(".submit-btn");
const form = document.getElementById("practiceForm");
const textInput = document.getElementById("text");

let mediaRecorder;
let audioForSubmit = null;
let audioForShow = null;

// Update submit button state
function updateSubmitState() {
    if (recordRadio.checked) {
        submitBtn.disabled = !textInput.value || !audioForSubmit;
    } else {
        submitBtn.disabled = !textInput.value || fileInput.files.length === 0;
    }
}

// Toggle record/upload sections
function toggleSections() {
    if (recordRadio.checked) {
        recordSection.style.display = "block";
        uploadSection.style.display = "none";
    } else {
        recordSection.style.display = "none";
        uploadSection.style.display = "block";
    }
    updateSubmitState();
}
toggleSections();
recordRadio.onchange = toggleSections;
uploadRadio.onchange = toggleSections;

// Text input
textInput.addEventListener("input", () => {
    updateSubmitState();
    feedbackSection.style.display = "none";
    feedbackBox.innerHTML = "";
    scoreBox.textContent = "";
});

// Recording
recordBtn.onclick = async () => {
    // Clear previous feedback
    feedbackSection.style.display = "none";
    feedbackBox.innerHTML = "";
    scoreBox.textContent = "";

    audioForSubmit = null;
    audioForShow = null;
    playback.style.display = "none";
    playback.src = "";
    submitBtn.disabled = true;

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.onstop = () => {
        const newBlob = new Blob(audioChunks, { type: "audio/webm" });
        audioForSubmit = newBlob;
        audioForShow = newBlob;
        playback.src = URL.createObjectURL(audioForShow);
        playback.style.display = "block";
        showAudioBtn.style.display = "inline-block";
        updateSubmitState();
    };

    mediaRecorder.start();
    recordBtn.classList.add("recording");
    stopBtn.classList.add("active");
    recordBtn.disabled = true;
    stopBtn.disabled = false;
};

// Stop recording
stopBtn.onclick = () => {
    if (mediaRecorder) mediaRecorder.stop();
    recordBtn.disabled = false;
    stopBtn.disabled = true;
    recordBtn.classList.remove("recording");
    stopBtn.classList.remove("active");
};

// Show/hide playback
showAudioBtn.onclick = () => {
    playback.style.display = playback.style.display === "none" ? "block" : "none";
};

// File upload
fileInput.onchange = () => {
    audioForSubmit = fileInput.files.length > 0 ? fileInput.files[0] : null;
    audioForShow = audioForSubmit;
    playback.src = audioForShow ? URL.createObjectURL(audioForShow) : "";
    playback.style.display = audioForShow ? "block" : "none";
    showAudioBtn.style.display = audioForShow ? "inline-block" : "none";
    updateSubmitState();
};

// Form submit → fast scoring + TTS + LLM feedback
form.onsubmit = async (e) => {
    e.preventDefault();
    submitBtn.textContent = "Submitting...";
    submitBtn.disabled = true;

    const text = textInput.value;
    const formData = new FormData();
    formData.append("text", text);

    if (audioForSubmit) {
        formData.append("file", new File([audioForSubmit], "recording.webm", { type: "audio/webm" }));
    } else {
        alert("No audio to submit.");
        submitBtn.textContent = "Submit";
        return;
    }

    try {
        // 1️⃣ Call fast scoring API
        const response = await fetch("/audio-score", { method: "POST", body: formData });
        const data = await response.json();

        feedbackSection.style.display = "block";
        scoreBox.textContent = `Score: ${data.score}`;
        feedbackBox.innerHTML = `
            <p><strong>Correct IPA:</strong> ${data.correct_ipa}</p>
            <p><strong>Your Attempt IPA:</strong> ${data.attempt_ipa}</p>
        `;

        // 2️⃣ Call TTS API
        const ttsForm = new FormData();
        ttsForm.append("text", text);

        const ttsRes = await fetch("/tts", { method: "POST", body: ttsForm });
        const ttsBlob = await ttsRes.blob();
        const ttsUrl = URL.createObjectURL(ttsBlob);

        // Display student vs correct audio
        const audioCompareDiv = document.createElement("div");
        audioCompareDiv.classList.add("audio-comparison");
        audioCompareDiv.innerHTML = `
            <h4>Compare Pronunciation</h4>
            <p><strong>Your Voice:</strong></p>
            <audio controls src="${URL.createObjectURL(audioForShow)}"></audio>
            <p><strong>Correct Voice:</strong></p>
            <audio controls src="${ttsUrl}"></audio>
        `;
        feedbackBox.appendChild(audioCompareDiv);

        // 3️⃣ Call LLM feedback
        const llmForm = new FormData();
        llmForm.append("text", text);
        llmForm.append("correct_ipa", data.correct_ipa);
        llmForm.append("attempt_ipa", data.attempt_ipa);
        llmForm.append("score", data.score);

        const llmRes = await fetch("/llm-feedback", { method: "POST", body: llmForm });
        const llmData = await llmRes.json();

        const llmDiv = document.createElement("div");
        llmDiv.classList.add("llm-feedback");
        llmDiv.innerHTML = `<strong>LLM Feedback:</strong> ${llmData.feedback}`;
        feedbackBox.appendChild(llmDiv);

        audioForSubmit = null;
        updateSubmitState();
    } catch (err) {
        feedbackSection.style.display = "block";
        scoreBox.textContent = "Error";
        feedbackBox.textContent = "Invalid server response.";
        console.error(err);
    } finally {
        submitBtn.textContent = "Submit";
    }
};