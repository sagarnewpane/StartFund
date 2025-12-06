<script>
    import { Mail, Eye, EyeClosed, X } from 'lucide-svelte';
    import { enhance } from '$app/forms';
    import { goto, invalidateAll } from '$app/navigation'; // <--- Added invalidateAll

    // 1. Defined onClose in props (with a safe default)
    let { form, onClose = () => goto('/') } = $props();

    // 2. Removed redundant 'errorMessage' state.
    // We will use 'form.message' directly because 'update()' handles it automatically.

    let password = $state('');
    let email = $state('');
    let showPassword = $state(false);

    function togglePassword() {
        showPassword = !showPassword;
    }

    const submitLogin = () => {
        return async ({ result, update }) => {
            if (result.type === 'redirect') {
                // A. Update authentication state (cookies)
                await invalidateAll();
                // B. Redirect
                await goto(result.location);
            }
            else {
                // C. If failure, this updates the 'form' prop with the error message
                await update();
            }
        };
    };
</script>

<div
    class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 flex items-center justify-center"
    onkeydown={(e) => e.key === 'Escape' && onClose()}
    role="button"
    tabindex="0"
>
    <div
        class="relative h-[450px] w-[450px] border-black border-3 rounded-2xl shadow-[8px_8px_0px_0px_black] overflow-hidden z-50 animate-in cursor-default"
        onclick={(e) => e.stopPropagation()}
        role="document"
        tabindex="0"
        onkeydown={null}
    >

        <button
            onclick={onClose}
            class="absolute top-4 right-4 z-50 bg-white border-2 border-black rounded-full p-1.5 hover:bg-gray-100 transition-colors"
            aria-label="Close"
        >
            <X size={20} />
        </button>

        <div class="bg-primary h-[75%] flex flex-col justify-center items-center">

            <div class="uppercase bg-dark text-light text-center font-extrabold text-4xl mb-4 p-2 w-[90%]">
                <span>trying to login?</span>
            </div>

            <form
                class="flex flex-col items-center"
                method="POST"
                action="/login"
                use:enhance={submitLogin}
            >
                {#if form?.message}
                    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-1 rounded relative mb-2 text-sm font-bold">
                        {form.message}
                    </div>
                {/if}

                <div class="m-2">
                    <div class="relative mb-2">
                        <input
                            name="username"
                            type="email"
                            bind:value={email}
                            placeholder="EMAIL"
                            required
                            class="text-black bg-white border-3 p-2 w-[400px] text-l rounded-3xl placeholder-black"
                        >
                        <div class="bg-black absolute right-2 top-1/2 -translate-y-1/2 rounded-full p-1 pointer-events-none">
                            <Mail color="#fff" />
                        </div>
                    </div>

                    <div class="relative mb-2">
                        <input
                            name="password"
                            type={showPassword ? "text" : "password"}
                            bind:value={password}
                            placeholder="PASSWORD"
                            required
                            class="text-black bg-white border-3 p-2 w-[400px] text-l rounded-3xl placeholder-black"
                        >
                        <button
                            type="button"
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
                    class="bg-black text-white py-2 px-6 rounded-3xl font-semibold m-2 cursor-pointer hover:shadow-[3px_3px_0px_0px_white] transition-all"
                >
                    Login
                </button>
            </form>

        </div>

        <div class="flex flex-col items-center bg-white h-[25%] justify-center">
            <div class="relative bg-secondary text-black px-4 py-1 rounded-sm text-sm font-semibold flex items-center gap-1 mb-4 -top-7.5">
                <span>OR</span>
            </div>
            <button
                type="button"
                onclick={() => goto('/signup')}
                class="bg-primary text-white py-2 px-6 rounded-3xl font-semibold cursor-pointer hover:shadow-[3px_3px_0px_0px_black] transition-all -mt-2"
            >
                Sign Up
            </button>
        </div>

    </div>
</div>

<style>
    .animate-in { animation: scaleIn 0.2s ease-out; }
    @keyframes scaleIn {
        from { transform: scale(0.95); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
</style>
