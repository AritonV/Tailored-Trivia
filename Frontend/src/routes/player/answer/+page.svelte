<script>
  import { gameState } from '$lib/store';
  import { goto } from '$app/navigation';
  import { socket } from '$lib/socket';
  import { onMount } from 'svelte';

  let questionText = $gameState.currentQuestion.question;
  let answer = '';
  let timeLeft = 30;
  let once = true;
  let once2 = true;
  
  $: if (timeLeft <= 0 && $gameState.gamePhase === 'question' && once) {
    once = false;
    onTimeout();
  }  
  
  $: timeLeft = $gameState.timeLeft;
  
  function onTimeout() {
    socket.emit('answer_submitted', {
      "room_code": $gameState.roomCode,
      "player_id": $gameState.playerId,
      "answer": answer,
      "correct_answer": $gameState.currentQuestion.correct_answer
    });
  }

  function handleAnswer() {
    answer = event.srcElement.innerText;
  }

  $: if ($gameState.gamePhase === 'results' && once2) {
    once2 = false;
    gameState.update(state => ({
      ...state,
      timeLeft: 5
    }));
    goto('/player/result');
  }
</script>

<div class="min-h-screen bg-gray-900 text-white p-4 flex flex-col items-center gap-8">
  <div>
    <h1 class="text-3xl font-bold text-center">{questionText}</h1>
  </div>
  <div class="flex justify-center items-center w-32 h-24 text-4xl font-bold py-2 px-4 rounded-3xl bg-gray-400 border-8">
    {timeLeft}s
  </div>
  <div class="flex flex-col gap-4 justify-center">
    {#each $gameState.currentQuestion.answers as answer, index}
      <button on:click={handleAnswer} class="bg-cyan-700 hover:bg-cyan-800 text-white text-2xl font-bold py-4 px-8 rounded-xl border-4 disabled:opacity-50 disabled:cursor-not-allowed">
        {answer}
      </button>
    {/each}
  </div>
  <div class="text-center text-lg font-bold">
    <div>
      Currently selected answer:
    </div>
    <div>
      {answer}
    </div>
  </div>
</div>