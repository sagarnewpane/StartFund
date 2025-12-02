<script>
    export const ssr = false;
    import Card from "../components/Card.svelte";
    import Hero from "../components/Hero.svelte";
	import Login from "../components/Login.svelte";
	import Signup from "../components/Signup.svelte";
</script>

<section>
    <Hero/>
    <div class="p-6">
    <Card/>
    </div>
</section>
