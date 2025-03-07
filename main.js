// main.js

// Update file input display
const fileInput = document.getElementById('fileUpload');
const fileChosen = document.getElementById('file-chosen');

fileInput.addEventListener('change', function() {
  if (this.files && this.files[0]) {
    fileChosen.textContent = this.files[0].name;
  } else {
    fileChosen.textContent = 'No file chosen';
  }
});

// Handle form submission
document.getElementById('modelForm').addEventListener('submit', async function(event) {
  event.preventDefault();
  
  const selectedModel = document.getElementById('modelSelect').value;
  const file = fileInput.files[0];

  if (!file) {
    alert('No file selected!');
    return;
  }

  // 1) Upload the file to the FastAPI backend
  const formData = new FormData();
  formData.append('file', file);

  try {
    // POST to /upload/ (from prototype_imputation.py)
    const response = await fetch('http://127.0.0.1:8001/upload/', {
      method: 'POST',
      body: formData
    });


    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || 'Upload failed');
    }

    // 2) Redirect to processing page with model in query param
    window.location.href = `processing.html?model=${selectedModel}`;

  } catch (error) {
    console.error('Upload error:', error);
    alert('Upload error: ' + error.message);
  }
});
