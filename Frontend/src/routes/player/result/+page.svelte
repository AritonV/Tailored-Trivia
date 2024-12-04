<script>
  import { gameState } from '$lib/store';
  import { goto } from '$app/navigation';
  import { socket } from '$lib/socket';
  import { onMount } from 'svelte';

  onMount(() => {
    for (let [id, isCorrect] of Object.entries($gameState.scores)) {
      if (isCorrect) {
        gameState.update(state => ({
          ...state,
          timeLeft: 6,
          players: {
            ...state.players,
            [id]: {
              ...state.players[id],
              score: state.players[id].score + 1
            }
          }
        }));
      }
    }
    console.log($gameState);
  });

  let resultsText = '';

  $: if ($gameState.scores[$gameState.playerId]) {
    resultsText = 'Correct!';
  } else {
    resultsText = 'Incorrect';
  }

  // 5 seconds timer before starting the next question
  let time = 5;
  let winner = false;

  $: time = $gameState.timeLeft;

  $: if (time <= 0) {
    gameState.update(state => ({
      ...state,
      gamePhase: 'choosing',
      currentPlayer: null,
      currentQuestion: null,
      selectedCategory: null,
      selectedDifficulty: null,
      scores: {},
      timeLeft: 20
    }));
    for (let playerId in $gameState.players) {
      if ($gameState.players[playerId].score == $gameState.pointsToWin) {
        gameState.update(state => ({
          ...state,
          winnerPlayer: playerId
        }));
        winner = true;
        break;
      }
    }
    if (winner) {
      goto('/player/winner');
    } else {
      goto('/player/category');
    }
  }

  function win() {
    goto('/player/win');
  }
</script>

<div class={`
w-full min-h-screen text-white p-4 flex justify-center items-center
${$gameState.scores[$gameState.playerId] ? 'bg-green-500' : 'bg-red-500'}
`}>
{resultsText}
</div>