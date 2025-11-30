document.addEventListener('DOMContentLoaded', () => {
    const fileModeBtn = document.getElementById('fileModeBtn');
    const cameraModeBtn = document.getElementById('cameraModeBtn');
    const fileSection = document.getElementById('fileSection');
    const cameraSection = document.getElementById('cameraSection');
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const snapBtn = document.getElementById('snapBtn');
    const retakeBtn = document.getElementById('retakeBtn');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');

    let stream = null;

    // Switch to File Mode
    fileModeBtn.addEventListener('click', () => {
        fileModeBtn.classList.add('active');
        cameraModeBtn.classList.remove('active');
        fileSection.style.display = 'block';
        cameraSection.style.display = 'none';
        stopCamera();
    });

    // Switch to Camera Mode
    cameraModeBtn.addEventListener('click', async () => {
        cameraModeBtn.classList.add('active');
        fileModeBtn.classList.remove('active');
        fileSection.style.display = 'none';
        cameraSection.style.display = 'block';
        await startCamera();
    });

    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            video.srcObject = stream;
            video.style.display = 'block';
            canvas.style.display = 'none';
            snapBtn.style.display = 'inline-block';
            retakeBtn.style.display = 'none';
        } catch (err) {
            console.error("Error accessing webcam: ", err);
            alert("Could not access webcam. Please ensure you have granted permission.");
        }
    }

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
    }

    // Take Photo
    snapBtn.addEventListener('click', () => {
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        video.style.display = 'none';
        canvas.style.display = 'block';
        snapBtn.style.display = 'none';
        retakeBtn.style.display = 'inline-block';

        // Convert to file and set to input
        canvas.toBlob((blob) => {
            const file = new File([blob], "webcam-capture.jpg", { type: "image/jpeg" });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
        }, 'image/jpeg');
    });

    // Retake Photo
    retakeBtn.addEventListener('click', () => {
        video.style.display = 'block';
        canvas.style.display = 'none';
        snapBtn.style.display = 'inline-block';
        retakeBtn.style.display = 'none';
        fileInput.value = ''; // Clear the input
    });

    // Cleanup on page unload
    window.addEventListener('beforeunload', stopCamera);
});
