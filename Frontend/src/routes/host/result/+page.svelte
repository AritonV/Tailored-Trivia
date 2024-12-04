<script>
  import { gameState } from '$lib/store';
  import { goto } from '$app/navigation';
  import PlayerIcon from '$lib/components/PlayerIcon.svelte';
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
    console.log($gameState);
    socket.emit('start_game', {
      "room_code": $gameState.roomCode
    });
    console.log($gameState);
    for (let playerId in $gameState.players) {
      console.log("scores:");
      console.log($gameState.players[playerId].score);
      if ($gameState.players[playerId].score === $gameState.pointsToWin) {
        console.log("GOTO WINNER");
        gameState.update(state => ({
          ...state,
          winnerPlayer: playerId
        }));
        winner = true;
        break; // Add return to prevent further execution
      }
    }
    if (winner) {
      goto('/host/winner');
    } else {
      goto('/host/category');
    }
  }

  function win() {
    goto('/host/win');
  }

  let questionText = $gameState.currentQuestion.question;

</script>

<div class="w-full min-h-screen bg-gray-900 text-white p-4 flex flex-col">
  <div class="w-full mt-4 flex justify-center gap-16">
    {#each Object.entries($gameState.players) as [id, player]}
    <PlayerIcon 
      name={player.name}
      connected={true}
      score={player.score}
      results={true}
      isCorrect={$gameState.scores[id]}
      size="lg"
    />
    {/each}
  </div>
  <div class="w-full mt-4 px-8 pb-32 flex flex-col flex-1 justify-evenly">
    <div class="flex flex-col flex-1 justify-center items-center">
      <h1 class="text-5xl font-bold text-center mb-8">
        {questionText}
      </h1>
      <div class="flex justify-center items-center w-48 h-32 text-4xl font-bold py-4 px-8 rounded-3xl bg-gray-400 border-8">
        {time}s
      </div>
    </div>
    <div class="flex flex-col flex-1 gap-4 items-center justify-center">
      {#each $gameState.currentQuestion.answers as answer, index}
        {#if answer === $gameState.currentQuestion.correct_answer}
          <h1 class="w-3/4 text-5xl text-center font-bold bg-green-600 rounded-lg border-4 p-8">{answer}</h1>
        {:else}
          <h1 class="w-3/4 text-5xl text-center text-gray-600 font-bold bg-gray-700 rounded-lg border-4 border-gray-600 p-2">{answer}</h1>
        {/if}
      {/each}
    </div>
  </div>
</div>