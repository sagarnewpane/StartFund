<script>
    import { resolve } from '$app/paths';
    import Login from './Login.svelte';
    import Signup from './Signup.svelte';

    let showLogin = $state(false);
    let showSignup = $state(false);
    let {user} = $props();

    function handleModalClose(){
      showLogin = false
      showSignup = false
    }

    async function handleLogout(){
      await fetch('/api/logout', {method: 'POST'});

      resolve('/')
    }
</script>

<header>
    <div class="bg-light min-w-screen min-h-10 flex justify-between p-4">
        <div>
            <a href={resolve('/')}><img src="./Icon.png" alt="" width="140"></a>
        </div>
        <div class="flex">
            {#if !user}
            <button
                onclick={() => showSignup = true}
                class="text-black font-semibold mr-4 hover:underline"
            >
                Sign Up
            </button>
            <button
                onclick={() => showLogin = true}
                class="bg-primary text-white py-2 px-4 rounded-3xl font-semibold border-2 border-black hover:shadow-[3px_3px_0px_0px_black] transition-all"
            >
                Login
            </button>
            {:else}
            <button onclick={handleLogout}>Logout</button>
            {/if}
        </div>
    </div>
</header>

<!-- Modals -->
<Login
    isOpen={showLogin}
    onClose={handleModalClose}
/>

<Signup
    isOpen={showSignup}
    onClose={handleModalClose}
/>
