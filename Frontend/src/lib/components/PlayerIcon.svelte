<script>
  import trophy from '$lib/images/trophy.png';

  export let name = null;
  export let noName = false;
  export let connected = true;
  export let score = 0;
  export let results = false;
  export let isCorrect = false;
  export let isCurrentPlayer = false;
  export let winner = false;
  export let size = '';
  
  const colors = [
    'bg-blue-500',
    'bg-green-500',
    'bg-yellow-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-indigo-500',
    'bg-red-500',
    'bg-orange-500'
  ];
  
  // Generate consistent color based on name
  $: playerColor = name ? 
    colors[name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % colors.length] :
    'bg-gray-700';

  // Add animation class when it's the current player's turn
  $: animationClass = isCurrentPlayer ? 'animate-pulse-subtle' : '';
</script>

<style>
  @keyframes pulse-subtle {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
  }

  @keyframes swivel {
    0%, 100% {
      transform: rotate(-10deg) scale(1);
    }
    50% {
      transform: rotate(10deg) scale(1.1);
    }
  }

  .animate-pulse-subtle {
    animation: pulse-subtle 2s ease-in-out infinite;
  }

  .animate-trophy {
    animation: swivel 1.5s ease-in-out infinite;
    transform-origin: center bottom;
  }

  /* Add transition for smoother animation start/stop */
  .avatar {
    transition: transform 0.2s ease-in-out;
  }

  /* Trophy positioning */
  .trophy-container {
    position: absolute;
    bottom: -4px;
    right: -4px;
    width: 40%;
    height: 40%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .trophy-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
</style>

<div class="text-center">
  <div class="relative mb-2">
    <div class={`
      avatar
      rounded-full flex items-center justify-center font-bold
      ${size == 'lg' ? 'w-24 h-24' : size == 'xl' ? 'w-48 h-48' : 'w-16 h-16'}
      ${size == 'lg' ? 'text-4xl' : size == 'xl' ? 'text-6xl' : 'text-2xl'}
      ${connected ? playerColor : 'bg-gray-700 opacity-30'}
      ${isCurrentPlayer ? 'ring-4 ring-white' : ''}
      ${results ? isCorrect ? 'ring-8 ring-green-400' : 'ring-8 ring-red-400' : ''}
      ${animationClass}
    `}>
      {#if name}
        {name[0].toUpperCase()}
      {:else}
        ?
      {/if}

      {#if winner}
        <div class="trophy-container animate-trophy">
          <img 
            src="{trophy}" 
            alt="Winner Trophy" 
            class="trophy-image"
          />
        </div>
      {/if}
    </div>
    
    {#if score > 0}
      <div class="absolute -top-2 -right-2 bg-white text-gray-900 rounded-full w-8 h-8 flex items-center justify-center text-base font-bold">
        {score}
      </div>
    {/if}
  </div>
  
  {#if name}
    <div class={`
    font-medium truncate
    ${size == 'lg' ? 'text-2xl' : size == 'xl' ? 'text-5xl' : 'text-2xl'}
    `}>
      {#if !noName}
        {name}
      {/if}
    </div>
  {/if}
</div>