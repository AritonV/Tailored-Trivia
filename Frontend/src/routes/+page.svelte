<script>
  import { goto } from '$app/navigation';

  function goToHost() {
    console.log('Going to host');
    goto('/host/lobby');
  }

  function goToJoin() {
    goto('/player/join');
  }
</script>

<div class="min-h-screen bg-gray-900 text-white flex items-center justify-center">
  <div class="text-center space-y-8">
    <h1 class="text-4xl font-bold mb-8">Trivia Game</h1>
      
    <div class="space-x-4">
      <button
        on:click={goToHost}
        class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-8 rounded-xl"
      >
        Host Game
      </button>
          
      <button
        on:click={goToJoin}
        class="bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-8 rounded-xl"
      >
        Join Game
      </button>
    </div>
  </div>
</div>