document.addEventListener('DOMContentLoaded', function () {
  fetch('games_cleaned.json')
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return response.json();
    })
    .then(data => {
      displayGames(data);
    })
    .catch(error => {
      console.error("Error fetching games data: ", error);
    });
});

function displayGames(games) {
  const gameContainer = document.getElementById('gameContainer');
  gameContainer.innerHTML = '';

  games.forEach(game => {
    if (game.error) return;

    const gameCard = document.createElement('div');
    gameCard.classList.add('game-card');
    gameCard.style.cursor = 'pointer';
    gameCard.addEventListener('click', function () {
      window.location.href = '/games/?id=' + game.zip;
    });

    // Icon placeholder — will be replaced when icons are added
    const gameIcon = document.createElement('div');
    gameIcon.classList.add('game-icon-placeholder');
    gameCard.appendChild(gameIcon);

    const gameName = document.createElement('h3');
    gameName.textContent = game.name;
    gameCard.appendChild(gameName);

    gameContainer.appendChild(gameCard);
  });
}
