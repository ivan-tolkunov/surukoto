const recordButton = document.getElementById('record');
const recordButtonText = document.getElementById('record-text');

let recorder = null;

recordButton.onclick = async () => {
    if (recordButton.classList[1] == "palette-5") {
        return;
    }
    if (recorder) {
        recordButtonText.innerHTML = 'Processing...';
        recordButton.classList = 'blobs palette-5';
        recorder.stop();
        recorder = null;
        return;
    }

    const chunks = [];
    const stream = await navigator.mediaDevices.getUserMedia({audio: true});

    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = async () => {
        recordButton.classList = 'blobs palette-5';
        const blob = new Blob(chunks, {'type': 'audio/webm;'});
        const formData = new FormData();
        formData.append('audio_file', blob, "voice-command.webm");
        const csrftoken = getCookie('csrftoken');
        const response = await fetch('/todos/process-voice-command/', {
            method: 'POST',
            body: formData,
            headers: {'X-CSRFToken': csrftoken},
        });
        const data = await response.text();
        window.location.reload();
        console.log(data);
    };

    recordButtonText.innerHTML = 'Recording...';
    recordButton.classList = 'blobs palette-2';
    recorder.start();
};

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