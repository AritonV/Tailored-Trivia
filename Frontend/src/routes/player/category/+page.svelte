<script>
  import { goto } from '$app/navigation';
  import { gameState } from '$lib/store';
  import { socket } from '$lib/socket';
  
  let difficulty = '';
  let category = '';
  let error = '';

  function handleSubmit() {
    error = '';
    if (difficulty == "") {
      error = "Please select a difficulty";
    }
    else if (category == "") {
      error = "Please select a category";
    }
    else {
      socket.emit('category_selected', {
        "room_code": $gameState.roomCode,
        "category": category,
        "difficulty": difficulty
      });
      goto('/player/wait');
    }
  }

  $: if ($gameState.gamePhase === 'generating') {
    goto('/player/wait');
  }
</script>

<div class="min-h-screen w-full bg-slate-900 flex items-center justify-center p-4">
  <div class="w-full max-w-md">
    <div class="mb-8">
      <div class="text-gray-200 text-lg mb-3">Difficulty:</div>
      <div class="flex gap-3 w-full">
        <button
          on:click={() => difficulty = 'easy'}
          class="flex-1 px-6 py-3 rounded-md transition-colors text-lg"
          class:bg-green-500={difficulty === 'easy'}
          class:text-white={difficulty === 'easy'}
          class:bg-green-700={difficulty !== 'easy'}
          class:text-green-500={difficulty !== 'easy'}
          class:opacity-50={difficulty !== 'easy'}
        >
          Easy
        </button>
        <button
          on:click={() => difficulty = 'medium'}
          class="flex-1 px-6 py-3 rounded-md transition-colors text-lg"
          class:bg-orange-500={difficulty === 'medium'}
          class:text-white={difficulty === 'medium'}
          class:bg-orange-700={difficulty !== 'medium'}
          class:text-orange-500={difficulty !== 'medium'}
          class:opacity-50={difficulty !== 'medium'}
        >
          Medium
        </button>
        <button
          on:click={() => difficulty = 'hard'}
          class="flex-1 px-6 py-3 rounded-md transition-colors text-lg"
          class:bg-red-500={difficulty === 'hard'}
          class:text-white={difficulty === 'hard'}
          class:bg-red-700={difficulty !== 'hard'}
          class:text-red-500={difficulty !== 'hard'}
          class:opacity-50={difficulty !== 'hard'}
        >
          Hard
        </button>
      </div>
    </div>

    <div class="mb-8">
      <div class="text-gray-200 text-lg mb-3">Category:</div>
      <input
        type="text"
        bind:value={category}
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-md text-gray-200 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Enter category..."
      />
    </div>

    <button
      on:click={handleSubmit}
      class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-md transition-colors text-lg"
    >
      Submit
    </button>

    {#if error != ''}
      <div class="mt-4 p-4 bg-red-900/50 border border-red-500 rounded-lg text-center">
        {error}
      </div>
    {/if}
  </div>
</div>

<style>
  button:hover:not(.bg-green-500, .bg-orange-500, .bg-red-500) {
    opacity: 0.7;
  }
</style>