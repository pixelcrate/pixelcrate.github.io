function lookupGame() {
  const input = document.getElementById('gameIdInput').value.trim();
  const zip = parseInt(input, 10);
  if (isNaN(zip)) {
    alert('Please enter a valid integer game ID.');
    return;
  }
  window.location.href = '/games/?id=' + zip;
}

document.getElementById('gameIdInput').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') lookupGame();
});

document.addEventListener('DOMContentLoaded', function () {
  // Fetch the JSON data for the games
  fetch('games_cleaned.json')  // Replace with the correct path to your JSON file
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json(); // Parse JSON
    })
    .then(data => {
      displayGames(data); // Call the function to display games
    })
    .catch(error => {
      console.error("Error fetching games data: ", error);
    });
});

function displayGames(games) {
  const gameContainer = document.getElementById('gameContainer');
  gameContainer.innerHTML = ''; // Clear any previous content

  // Loop through the games and create cards for each
  games.forEach(game => {
    if (game.error) return;  // Skip games with errors

    const gameCard = document.createElement('div');
    gameCard.classList.add('game-card');

    // Optionally add an icon (use a placeholder image if no icon exists)
    const gameIcon = document.createElement('img');
    gameIcon.src = game.icon || 'default-icon.png';  // Placeholder icon
    gameCard.appendChild(gameIcon);

    // Game name
    const gameName = document.createElement('h3');
    gameName.textContent = game.name;
    gameCard.appendChild(gameName);

    // Embed the game with iframe
    const gameIframe = document.createElement('iframe');
    gameIframe.src = game.game; // Use the game URL from JSON
    gameIframe.width = "100%";
    gameIframe.height = "400px";  // Adjust as needed
    gameIframe.frameBorder = "0"; // Optional: remove iframe border
    gameCard.appendChild(gameIframe);

    // Add the game card to the container
    gameContainer.appendChild(gameCard);
})
}
