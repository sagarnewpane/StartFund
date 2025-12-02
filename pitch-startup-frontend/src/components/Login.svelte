<script>
    import { Mail, Eye, EyeClosed } from 'lucide-svelte';

    let showPassword = $state(false);
    let email = $state('');
    let password = $state('');

    function togglePassword() {
        showPassword = !showPassword;
    }

    function handleSubmit() {
        console.log('Login submitted');
        console.log('Email:', email);
        console.log('Password:', password);
    }
</script>

<div class="absolute h-[450px] w-[450px] border-black border-3 rounded-2xl shadow-[5px_5px_0px_0px] shadow-2xl overflow-hidden">
    <div class="bg-primary h-[70%] flex justify-center flex-col items-center">
        <div class="uppercase bg-dark text-light text-center font-extrabold text-4xl mb-4 p-2 w-[70%]">
            <span>what's your<br>credentials?</span>
        </div>

        <form class="flex flex-col items-center">
            <div class="m-2">
                <div class="relative mb-2">
                    <input
                        type="email"
                        bind:value={email}
                        placeholder="EMAIL"
                        required
                        class="text-black bg-white border-3 p-2 w-[400px] text-l rounded-3xl placeholder-black"
                    >
                    <button class="bg-black absolute right-2 top-1/2 -translate-y-1/2 cursor-pointer rounded-full p-1">
                        <Mail color="#fff" />
                    </button>
                </div>

                <div class="relative">
                    <input
                        type={showPassword ? "text" : "password"}
                        bind:value={password}
                        placeholder="PASSWORD"
                        required
                        class="text-black bg-white border-3 p-2 w-[400px] text-l rounded-3xl placeholder-black"
                    >
                    <button
                        class="bg-black absolute right-2 top-1/2 -translate-y-1/2 cursor-pointer rounded-full p-1"
                        onclick={togglePassword}
                    >
                        {#if showPassword}
                            <Eye color="#fff" />
                        {:else}
                            <EyeClosed color="#fff" />
                        {/if}
                    </button>
                </div>
            </div>

            <button
                type="submit"
                onclick={handleSubmit}
                class="bg-black text-white py-2 px-4 rounded-3xl font-semibold m-2 cursor-pointer"
            >
                Login
            </button>
        </form>
    </div>

    <div class="flex flex-col items-center">
        <div class="relative bg-secondary text-black px-4 py-1 rounded-sm text-sm font-semibold flex items-center gap-1 mb-4 -top-3.5">
            <span>OR</span>
        </div>
        <button class="bg-primary text-white py-2 px-6 rounded-3xl font-semibold cursor-pointer">
            Sign Up
        </button>
    </div>
</div>
