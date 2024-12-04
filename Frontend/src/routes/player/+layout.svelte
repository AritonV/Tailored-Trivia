<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { gameState } from '$lib/store';

  onMount(() => {
    // Redirect to join page if not connected as player
    const unsubscribe = gameState.subscribe(state => {
      if (!state.playerId && window.location.pathname !== '/player/join') {
        goto('/player/join');
      }
    });

    return () => {
      unsubscribe();
    };
  });
</script>

<slot />