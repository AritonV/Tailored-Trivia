<script>
  import { gameState } from '$lib/store';
  import { goto } from '$app/navigation';
  import PlayerIcon from '$lib/components/PlayerIcon.svelte';
  
  $: if ($gameState.gamePhase === 'question') {
    goto('/player/answer');
  }
  // Subscribe to game state changes to handle navigation
  $: if ($gameState.currentPlayer === $gameState.playerId && $gameState.gamePhase === 'choosing') {
    goto('/player/category');
  }

  function printState() {
    console.log($gameState);
    $gameState.players[$gameState.currentPlayer].score += 1;
  }
</script>

<div class="min-h-screen bg-gray-900 text-white p-4 flex items-center justify-center">
  <div class="text-center">
    {#if $gameState.gamePhase === 'choosing'}
      <div class="mb-8 flex items-center justify-center">
        <PlayerIcon 
          name={$gameState.players[$gameState.currentPlayer]?.name}
          score={$gameState.players[$gameState.currentPlayer]?.score}
          connected={true}
          size="lg"
        />
      </div>
      <p class="text-xl mb-4">
        {$gameState.players[$gameState.currentPlayer]?.name} is choosing a category...
      </p>
    {:else if $gameState.gamePhase === 'generating'}
      <div class="mb-8 flex items-center justify-center">
        <PlayerIcon 
          name={$gameState.players[$gameState.playerId]?.name}
          score={$gameState.players[$gameState.playerId]?.score}
          connected={true}
          size="lg"
        />
      </div>
      <p class="text-xl mb-4">Waiting for the question to generate...</p>
    {:else}
      <div class="mb-8 flex items-center justify-center">
        <PlayerIcon 
          name={$gameState.players[$gameState.playerId]?.name}
          score={$gameState.players[$gameState.playerId]?.score}
          connected={true}
          size="lg"
        />
      </div>
      <p class="text-xl mb-4">Waiting for the game to start...</p>
    {/if}
    
    <div class="text-gray-400">
      Room Code: {$gameState.roomCode}
    </div>
    <button on:click={printState}>Print Game State</button>
  </div>
</div>