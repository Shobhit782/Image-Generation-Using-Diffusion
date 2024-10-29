/*
function showLoadingScreen() {
  const loadingScreen = document.getElementById('loadingScreen');
  const progressBar = document.getElementById('progress');
  loadingScreen.style.display = 'flex';  // Show the loading screen

  let progress = 0;
  progressBar.style.width = '0%';

  // Simulate the progress bar animation
  const interval = setInterval(() => {
    if (progress < 100) {
      progress += 2;  // Increase progress incrementally
      progressBar.style.width = progress + '%';
    } else {
      clearInterval(interval);
    }
  }, 100);  // Adjust speed of progress (100ms for smoother animation)
}

document.getElementById('art-form').addEventListener('submit', (event) => {
  event.preventDefault();
  showLoadingScreen();  // Start the progress bar

  const formData = new FormData(event.target);  // Get the form data

  fetch('/generate', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      // Create and display the generated image
      const generatedImage = document.createElement('img');
      generatedImage.src = data.artwork_url;
      generatedImage.id = "generatedArtwork";  // Give it an ID for styling

      // Create the close button (X) for the image
      const closeButton = document.createElement('span');
      closeButton.id = "closeButton";
      closeButton.innerHTML = "&times;";  // Cross sign (×)
      closeButton.onclick = function () {
        document.body.removeChild(generatedImage);  // Remove the image
        document.body.removeChild(closeButton);     // Remove the close button
      };

      document.body.appendChild(generatedImage);  // Add the image to the body
      document.body.appendChild(closeButton);     // Add the close button to the body

      // Hide the loading screen
      const loadingScreen = document.getElementById('loadingScreen');
      loadingScreen.style.display = 'none';
    })
    .catch(error => {
      console.error('Error generating art:', error);
    });
});
*/
function showLoadingScreen() {
  const loadingScreen = document.getElementById('loadingScreen');
  const progressBar = document.getElementById('progress');
  loadingScreen.style.display = 'flex';

  let progress = 0;
  progressBar.style.width = '0%';

  // Simulate the progress bar increasing
  const interval = setInterval(() => {
    if (progress < 90) {  // Stop at 90%, we'll finish when the server responds
      progress += 1;
      progressBar.style.width = progress + '%';
    }
  }, 100);  // Increment every 100ms

  return interval;  // Return interval to clear it later
}

document.getElementById('art-form').addEventListener('submit', (event) => {
  event.preventDefault();

  // Start the progress bar animation
  const interval = showLoadingScreen();

  const formData = new FormData(event.target);  // Get the form data

  fetch('/generate', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      // Clear the progress interval once done
      clearInterval(interval);

      // Complete the progress bar to 100% before hiding
      const progressBar = document.getElementById('progress');
      progressBar.style.width = '100%';

      // Create and display the generated image
      const generatedImage = document.createElement('img');
      generatedImage.src = data.artwork_url;
      generatedImage.id = "generatedArtwork";

      // Create the close button (X) for the image
      const closeButton = document.createElement('span');
      closeButton.id = "closeButton";
      closeButton.innerHTML = "&times;";
      closeButton.onclick = function () {
        document.body.removeChild(generatedImage);  // Remove the image
        document.body.removeChild(closeButton);     // Remove the close button
      };

      document.body.appendChild(generatedImage);  // Add the image to the body
      document.body.appendChild(closeButton);     // Add the close button to the body

      // Hide the loading screen
      const loadingScreen = document.getElementById('loadingScreen');
      setTimeout(() => {
        loadingScreen.style.display = 'none';
      }, 500);  // Small delay for smooth transition
    })
    .catch(error => {
      console.error('Error generating art:', error);
      clearInterval(interval);  // Clear the progress interval in case of error
    });
});
