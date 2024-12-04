<script>
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { gameState } from '$lib/store';
  import { resetGame } from '$lib/store';
  import { socket } from '$lib/socket';
  import PlayerIcon from '$lib/components/PlayerIcon.svelte';
  import { on } from 'svelte/events';
  
  let startingGame = false;
  
  onMount(async () => {
    // Create game room when host enters lobby
    socket.emit('create_game');
  });

  onDestroy(() => {
    // reset game state when leaving host page
    if ($gameState.gamePhase == 'lobby' &&  $gameState.gamePhase != 'choosing') {
      resetGame();
    }
  });
  
  function startGame() {
    startingGame = true;
    socket.emit('start_game', { room_code: $gameState.roomCode });
    
    // Navigate to next game phase after emitting event
    goto('/host/category');
  }
</script>

<div class="min-h-screen bg-gray-900 text-white p-8">
  <div class="max-w-4xl mx-auto">
    <div class="text-center mb-8">
      <h1 class="text-4xl font-bold">{$gameState.roomCode}</h1>
      <p class="mt-2 text-gray-400">Share this code with players</p>
    </div>
    
    <div class="grid grid-cols-4 place-items-center gap-6 mb-8">
      {#each Object.entries($gameState.players) as [id, player]}
        <PlayerIcon 
          name={player.name}
          connected={true}
          score={player.score}
        />
      {/each}
      
      {#each Array(8 - Object.keys($gameState.players).length) as _}
        <PlayerIcon connected={false} />
      {/each}
    </div>
    
    <div class="text-center">
      <button
        class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-full disabled:opacity-50 disabled:cursor-not-allowed"
        disabled={Object.keys($gameState.players).length < 2 || startingGame}
        on:click={startGame}
      >
        {#if startingGame}
            Starting...
        {:else}
            Start Game ({Object.keys($gameState.players).length}/8 Players)
        {/if}
      </button>
    </div>
  </div>
</div>