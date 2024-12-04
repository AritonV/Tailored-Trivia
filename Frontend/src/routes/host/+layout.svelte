<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { gameState } from '$lib/store';
  import { socket } from '$lib/socket';

  onMount(async () => {
    // Redirect to home if not a host
    const unsubscribe = gameState.subscribe(state => {
      // if (!state.isHost) {
      //   goto('/');
      // }
    });

    return () => {
      unsubscribe();
    };
  });
</script>

<slot />