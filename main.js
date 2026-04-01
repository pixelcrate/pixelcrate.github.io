let allGames = [];

document.addEventListener('DOMContentLoaded', function () {
  fetch('games_cleaned.json')
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return response.json();
    })
    .then(data => {
      allGames = data.filter(g => !g.error);
      displayGames(allGames);
    })
    .catch(error => {
      console.error("Error fetching games data: ", error);
    });
});

function filterGames() {
  const query = document.getElementById('searchBar').value.trim().toLowerCase();
  const filtered = allGames.filter(g => g.name.toLowerCase().includes(query));
  displayGames(filtered);
}

function displayGames(games) {
  const gameContainer = document.getElementById('gameContainer');
  gameContainer.innerHTML = '';

  games.forEach(game => {

    const gameCard = document.createElement('div');
    gameCard.classList.add('game-card');
    gameCard.style.cursor = 'pointer';
    gameCard.addEventListener('click', function () {
      window.location.href = '/games/?id=' + game.zip;
    });

    const gameIcon = document.createElement('img');
    gameIcon.src = game.icon;
    gameIcon.alt = game.name;
    gameIcon.classList.add('game-icon');
    gameCard.appendChild(gameIcon);

    const gameName = document.createElement('h3');
    gameName.textContent = game.name;
    gameCard.appendChild(gameName);

    gameContainer.appendChild(gameCard);
  });
}
