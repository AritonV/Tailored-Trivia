<script>
  import { gameState } from '$lib/store';
  import { resetGame } from '$lib/store';
  import { goto } from '$app/navigation';
  import PlayerIcon from '$lib/components/PlayerIcon.svelte';

  let winnerPlayer = $gameState.players[$gameState.winnerPlayer];

  function PlayAgain() {
    resetGame();
    console.log($gameState);
    goto('/player/join');
  }
</script>

<div class="min-h-screen flex flex-col justify-center items-center bg-gray-900 text-white p-8">
  <div class="max-w-4xl mx-auto text-center flex flex-col gap-8">
    <div class="mb-12 flex flex-col justify-center items-center">
      <PlayerIcon 
        name={winnerPlayer?.name}
        noName={true}
        connected={true}
        size="xl"
        isCurrentPlayer={true}
        winner={true}
      />
      <h2 class="text-6xl mt-4">
        {winnerPlayer?.name} is the winner!
      </h2>
    </div>
    <button
    class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-full"
    on:click={PlayAgain}
    >
      Play Again
    </button>
  </div>
</div>