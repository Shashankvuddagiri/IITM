document.addEventListener('DOMContentLoaded', function() {
    const optimizeButton = document.getElementById('optimize-finance');
    const dashboardContainer = document.getElementById('dashboard-container');
    const dashboardFrame = document.getElementById('dashboard-frame');
    const fileUpload = document.getElementById('file-upload');

    optimizeButton.addEventListener('click', function() {
        dashboardContainer.style.display = 'block';
        optimizeButton.style.display = 'none';
        window.scrollTo(0, dashboardContainer.offsetTop);
    });

    function refreshDashboard() {
        dashboardFrame.src = dashboardFrame.src;
    }

    function handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                refreshDashboard();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while uploading the file.');
            });
        }
    }

    fileUpload.addEventListener('change', handleFileUpload);
});

