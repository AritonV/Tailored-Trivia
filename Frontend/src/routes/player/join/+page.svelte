<script>
  import { goto } from '$app/navigation';
  import { gameState } from '$lib/store';
  import { socket } from '$lib/socket';
  
  let playerName = '';
  let roomCode = '';
  
  // Subscribe to game state to handle navigation after successful join
  $: if ($gameState.playerId) {
    goto('/player/wait');
  }
  
  function handleJoin() {
    if (playerName.trim() && roomCode.trim()) {
      socket.emit('join_game', {
        room_code: roomCode.toUpperCase(),
        name: playerName.trim()
      });
    }
  }
</script>

<div class="min-h-screen bg-gray-900 text-white p-4 flex items-center justify-center">
  <div class="w-full max-w-sm">
    <h1 class="text-3xl font-bold text-center mb-8">Join Game</h1>
    
    <div class="space-y-4">
      <div>
        <label for="room-code" class="block text-sm font-medium mb-1">Room Code</label>
        <input
          id="room-code"
          type="text"
          bind:value={roomCode}
          placeholder="Enter Room Code"
          maxlength="4"
          class="w-full bg-gray-800 border border-gray-700 rounded-lg p-4 text-center text-2xl uppercase tracking-widest"
        />
      </div>
      
      <div>
        <label for="player-name" class="block text-sm font-medium mb-1">Your Name</label>
        <input
          id="player-name"
          type="text"
          bind:value={playerName}
          placeholder="Enter Your Name"
          maxlength="12"
          class="w-full bg-gray-800 border border-gray-700 rounded-lg p-4"
        />
      </div>
      
      <button
        on:click={handleJoin}
        disabled={!playerName.trim() || !roomCode.trim()}
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-6 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Join Game
      </button>
    </div>
    
    {#if $gameState.error}
      <div class="mt-4 p-4 bg-red-900/50 border border-red-500 rounded-lg text-center">
        {$gameState.error}
      </div>
    {/if}
  </div>
</div>