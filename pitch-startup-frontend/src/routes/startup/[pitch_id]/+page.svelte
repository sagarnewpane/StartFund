<script>
    import PitchDetails from '../../../components/PitchDetails.svelte';
    import Card from '../../../components/Card.svelte';
    import { resolve } from '$app/paths';

</script>


<PitchDetails/>
<div class="m-7 ">
    <p class="font-semibold text-xl mb-3">Similar Start Ups</p>
    <a href={resolve(`/startup/${'test'}`)}><Card/></a>
</div>
