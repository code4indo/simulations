document.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('imageUpload');
    const processBtn = document.getElementById('processBtn');
    const originalImage = document.getElementById('originalImage');
    const processedImage = document.getElementById('processedImage');
    const loadingIndicator = document.getElementById('loadingIndicator');

    // Simple simulation - in a real app, this would connect to an API
    processBtn.addEventListener('click', function() {
        if (!imageUpload.files || imageUpload.files.length === 0) {
            alert('Please select an image first');
            return;
        }

        // Show loading indicator
        loadingIndicator.classList.remove('hidden');
        
        // Display original image
        const file = imageUpload.files[0];
        const reader = new FileReader();
        
        reader.onload = function(e) {
            originalImage.src = e.target.result;
            
            // Simulate processing delay
            setTimeout(function() {
                // In a real application, this is where you would call your API
                // For this demo, we'll just use the same image
                simulateUnetProcessing(e.target.result).then(processedImageSrc => {
                    processedImage.src = processedImageSrc;
                    loadingIndicator.classList.add('hidden');
                });
            }, 2000);
        };
        
        reader.readAsDataURL(file);
    });

    // U-Net simulation function (placeholder)
    async function simulateUnetProcessing(imageSrc) {
        // This is just a placeholder. In a real app, you would:
        // 1. Send the image to a backend service
        // 2. Process it with a real U-Net model
        // 3. Return the processed image
        
        // For demo purposes, we're applying a simple image filter
        return applySimpleFilter(imageSrc);
    }

    // Simple filter as placeholder
    function applySimpleFilter(src) {
        return new Promise((resolve) => {
            const img = new Image();
            img.src = src;
            
            img.onload = function() {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                
                canvas.width = img.width;
                canvas.height = img.height;
                
                // Draw original image
                ctx.drawImage(img, 0, 0);
                
                // Apply simple edge detection-like effect
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = imageData.data;
                
                // Simple image processing effect
                for (let i = 0; i < data.length; i += 4) {
                    // Invert colors as a simple demo effect
                    data[i] = 255 - data[i];     // red
                    data[i + 1] = 255 - data[i + 1]; // green
                    data[i + 2] = 255 - data[i + 2]; // blue
                }
                
                ctx.putImageData(imageData, 0, 0);
                resolve(canvas.toDataURL('image/jpeg'));
            };
        });
    }
});
