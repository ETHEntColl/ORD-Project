var perspectives = ['side', 'bottom', 'top'];

async function waitForModelToBeVisible(viewer) {
    console.log(`Waiting for model to be visible for viewer ID: ${viewer.id}`);
    while (!viewer.modelIsVisible) {
        await new Promise(resolve => setTimeout(resolve, 20));
    }
    console.log(`Model is visible for viewer ID: ${viewer.id}`);
}

async function captureImageFromViewer(viewer, perspective) {
    console.log(`Capturing image for perspective: ${perspective}`);
    const blob = await viewer.toBlob({ idealAspect: false, mimeType: "image/png" });
    if (blob) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${document.getElementById("name").innerHTML}_${perspective}_3d.png`;
        a.click();
        URL.revokeObjectURL(url);
        console.log(`Downloaded image for perspective: ${perspective}`);
    } else {
        console.error(`Failed to capture blob for perspective: ${perspective}`);
    }
}

async function downloadPosterToBlob() {
    console.log("Starting model loading!");

    for (let i = 0; i < perspectives.length; i++) {
        const perspective = perspectives[i];
        const viewer = document.getElementById(perspective);

        // Make the current viewer visible
        viewer.style.display = "flex";

        // Wait for the model to be fully visible
        await waitForModelToBeVisible(viewer);

        // Add a short delay to ensure rendering is complete
        await new Promise(resolve => setTimeout(resolve, 200));

        // Capture the image from the viewer
        await captureImageFromViewer(viewer, perspective);

        // Hide the current viewer
        viewer.style.display = "none";

        // Prepare the next perspective viewer if exists
        if (i < perspectives.length - 1) {
            const nextPerspective = perspectives[i + 1];
            document.getElementById(nextPerspective).style.display = "flex";
            console.log(`Next layout loaded: ${nextPerspective}`);
        }
    }
}

// Start the download process
downloadPosterToBlob();