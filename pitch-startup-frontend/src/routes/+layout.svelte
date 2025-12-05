<script>
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Navbar from '../components/Navbar.svelte';

	let { children, data } = $props(); // ⬅ get data from server load
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<Navbar user={data.user} />  <!-- ⬅ pass user to Navbar -->

{@render children()}
