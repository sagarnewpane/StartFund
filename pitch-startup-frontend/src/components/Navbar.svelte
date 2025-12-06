<script>
    import { enhance } from '$app/forms'; // Makes the form submit without a full page reload

    // Receive the user object from the layout
    let { user } = $props();
</script>

<header>
    <div class="bg-light min-w-screen min-h-10 flex justify-between p-4 items-center">
        <div>
            <a href="/">
                <img src="./Icon.png" alt="Logo" width="140">
            </a>
        </div>

        <div class="flex items-center gap-4">
            {#if !user}
                <a
                    href="/signup"
                    class="text-black font-semibold hover:underline"
                >
                    Sign Up
                </a>

                <a
                    href="/login"
                    class="bg-primary text-white py-2 px-4 rounded-3xl font-semibold border-2 border-black hover:shadow-[3px_3px_0px_0px_black] transition-all"
                >
                    Login
                </a>

            {:else}
                <span class="font-semibold text-gray-700">
                    Hello, {user.username || 'User'}
                </span>

                <form action="/logout" method="POST" use:enhance>
                    <button
                        type="submit"
                        class="bg-red-500 text-white py-2 px-4 rounded-3xl font-semibold border-2 border-black hover:shadow-[3px_3px_0px_0px_black] transition-all"
                    >
                        Logout
                    </button>
                </form>
            {/if}
        </div>
    </div>
</header>
