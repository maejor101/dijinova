document.addEventListener("DOMContentLoaded", function(event) {
    const html5QrcodeScanner = new Html5QrcodeScanner(
        "reader", { fps: 10, qrbox: 250 }
    );

    function onScanSuccess(decodedText, decodedResult) {
        console.log(`Code scanned = ${decodedText}`, decodedResult);

        const resultElement = document.getElementById('result');
        resultElement.textContent = `Scanned: ${decodedText}`;

        // Optionally, you can stop the scanner after a successful scan
        html5QrcodeScanner.clear();
    }

    html5QrcodeScanner.render(onScanSuccess);

    // Add code to start the camera stream
    const videoElement = document.createElement('video');
    videoElement.style.display = 'none'; // Hide the raw video element

    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then(stream => {
            videoElement.srcObject = stream;
            document.body.appendChild(videoElement); // Append to DOM to start streaming
        })
        .catch(error => console.error('Camera access error:', error));
});
