<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { socket } from '$lib/socket.js';
	
	onMount(() => {
			if (browser) {
					// Initialize socket connection when in browser
					socket.connect();
			}
			
			return () => {
					if (browser) {
							socket.disconnect();
					}
			};
	});
</script>

<slot />
