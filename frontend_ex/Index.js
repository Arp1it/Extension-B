const socket = new WebSocket("ws://127.0.0.1:5000/audio");

let speaking = false;
let micStarted = false;

const speak = (audioData) => {

    speaking = true;

    let audio;

    if (audioData.startsWith("http")) {
        audio = new Audio(audioData);
    } 
    
    else {
        try {
            const binary = atob(audioData);
            const bytes = new Uint8Array(binary.length);

            for (let i = 0; i < binary.length; i++) {
                bytes[i] = binary.charCodeAt(i);
            }

            const audioBlob = new Blob([bytes], { type: "audio/mpeg" });
            const url = URL.createObjectURL(audioBlob);

            audio = new Audio(url);

            audio.onended = () => {
                speaking = false;
                URL.revokeObjectURL(url);
            };
        } catch (e) {
            console.error("Invalid audio format:", e);
            speaking = false;
            return;
        }
    }

    audio.onended = () => {
        speaking = false;
        console.log("Assistant finished speaking");
    };

    audio.play();
};


socket.onmessage = (event) => {

    const msg = JSON.parse(event.data);

    if (msg.type === "audio") {
        speak(msg.data);
    }

    if (msg.type === "open") {
        console.log("Opening:", msg.data);
        window.open(msg.data, "_blank");
    }
};


socket.onopen = () => {
    console.log("WebSocket connected");
};


async function startMic() {

    if (micStarted) return;
    micStarted = true;

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const audioContext = new AudioContext({ sampleRate: 16000 });

    if (audioContext.state !== "running") {
        await audioContext.resume();
    }

    const source = audioContext.createMediaStreamSource(stream);

    const processor = audioContext.createScriptProcessor(4096, 1, 1);

    const silence = audioContext.createGain();
    silence.gain.value = 0;

    source.connect(processor);
    processor.connect(silence);
    silence.connect(audioContext.destination);

    processor.onaudioprocess = (e) => {

        if (speaking) return;
        if (socket.readyState !== WebSocket.OPEN) return;

        const input = e.inputBuffer.getChannelData(0);
        const float32 = new Float32Array(input);

        socket.send(float32.buffer);
    };
}


window.onload = async () => {

    console.log("Page loaded");

    try {
        await navigator.mediaDevices.getUserMedia({ audio: true });
        console.log("Mic permission granted");
    } catch {
        console.log("Waiting for permission...");
    }

    if (socket.readyState === WebSocket.OPEN) {
        startMic();
    } else {
        socket.addEventListener("open", startMic, { once: true });
    }
};