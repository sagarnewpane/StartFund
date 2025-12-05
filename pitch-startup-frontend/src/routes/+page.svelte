<script>
    export const ssr = false;
    import Card from "../components/Card.svelte";
    import Hero from "../components/Hero.svelte";
	import Login from "../components/Login.svelte";
	import Signup from "../components/Signup.svelte";
	import SubmitPitch from "../components/SubmitPitch.svelte";
	import PitchDetails from "../components/PitchDetails.svelte";
</script>

<section>
    <Hero/>
    <div class="m-7">
        <p class="font-semibold text-xl my-3">Trending Start Ups</p>
        <a href={`/startup/${'test'}`}><Card/></a>

    </div>

</section>
