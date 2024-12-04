<script>
  import { gameState } from '$lib/store';
  import { goto } from '$app/navigation';
  import PlayerIcon from '$lib/components/PlayerIcon.svelte';
  
  $: choosingPlayer = $gameState.players[$gameState.currentPlayer];
  $: if ($gameState.gamePhase === 'question') {
    goto('/host/question');
  }
  function showPlayers() {
    console.log($gameState);
  }
</script>

<div class="min-h-screen flex flex-col justify-center items-center bg-gray-900 text-white p-8">
  <div class="max-w-4xl mx-auto text-center">
    <div class="mb-12 flex flex-col justify-center items-center">
      {#if $gameState.gamePhase === 'generating'}
      <h2 class="text-2xl mt-4">
        The bot is cooking up a question...
      </h2>
      {:else}
      <PlayerIcon 
        name={choosingPlayer?.name}
        score={choosingPlayer?.score}
        connected={true}
        size="lg"
        isCurrentPlayer={true}
      />
      <h2 class="text-2xl mt-4">
        {choosingPlayer?.name} is choosing the category...
      </h2>
      {/if}
    </div>
    <button on:click={showPlayers}>Show State</button>
  </div>
</div>