<script>
  import { gameState } from '$lib/store';
  import { goto } from '$app/navigation';
  import PlayerIcon from '$lib/components/PlayerIcon.svelte';
  import { socket } from '$lib/socket';
  import { onMount } from 'svelte';

  onMount(() => {
    socket.emit('start_timer', {
      "room_code": $gameState.roomCode,
      "time": 20
    });
  });

  let questionText = $gameState.currentQuestion.question;
  let timeLeft = 10;
  let once = true;

  $: timeLeft = $gameState.timeLeft;

  $: if ($gameState.gamePhase === 'results' && once) {
    once = false;
    gameState.update(state => ({
      ...state,
      timeLeft: 5
    }));
    socket.emit('start_timer', {
      "room_code": $gameState.roomCode,
      "time": 5
    });
    goto('/host/result');
  }
</script>

<div class="w-full min-h-screen bg-gray-900 text-white p-4 flex flex-col">
  <div class="w-full mt-4 flex justify-center gap-16">
    {#each Object.entries($gameState.players) as [id, player]}
    <PlayerIcon 
      name={player.name}
      connected={true}
      score={player.score}
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
        {timeLeft}s
      </div>
    </div>
    <div class="flex flex-col flex-1 gap-4 items-center justify-center">
      {#each $gameState.currentQuestion.answers as answer, index}
        <h1 class="w-3/4 text-5xl text-center font-bold bg-cyan-800 rounded-lg border-4 p-2">{answer}</h1>
      {/each}
    </div>
  </div>
</div>