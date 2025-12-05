<script>
    import { User, Mail, Eye, EyeClosed, X } from 'lucide-svelte';
    import { goto } from '$app/navigation';

    let { isOpen = true, onClose = () => {} } = $props();

    let showPassword = $state(false);
    let password = $state('');
    let rePassword = $state('');
    let fullName = $state('');
    let email = $state('');

    function togglePassword() {
        showPassword = !showPassword;
    }

    async function handleSubmit(e) {
      e.preventDefault();

      await fetch('/api/signup', {
        method: 'POST',
        body: JSON.stringify({ email, password, fullName })
      });

      // hide the modal
          onClose();

      // redirect after login
      goto('/')
    }

    function handleBackdropClick(e) {
        if (e.target === e.currentTarget) {
            onClose();
        }
    }
</script>

{#if isOpen}
    <!-- Backdrop with blur -->
    <div
        class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 flex items-center justify-center"
        onclick={handleBackdropClick}
        role="button"
        tabindex="-1"
    >
        <!-- Signup Box -->
        <div class="relative h-[550px] w-[450px] border-black border-3 rounded-2xl shadow-[8px_8px_0px_0px_black] overflow-hidden z-50 animate-in">

            <!-- Close Button -->
            <button
                onclick={onClose}
                class="absolute top-4 right-4 z-50 bg-white border-2 border-black rounded-full p-1.5 hover:bg-gray-100 transition-colors"
                aria-label="Close"
            >
                <X size={20} />
            </button>

            <div class="bg-primary h-[75%] flex flex-col justify-center items-center">

                <div class="uppercase bg-dark text-light text-center font-extrabold text-4xl mb-4 p-2 w-[90%]">
                    <span>you new here eh?</span>
                </div>

                <form class="flex flex-col items-center" onsubmit={handleSubmit}>
                    <div class="m-2">

                        <div class="relative mb-2">
                            <input
                                type="text"
                                bind:value={fullName}
                                placeholder="FULL NAME"
                                required
                                class="text-black bg-white border-3 p-2 w-[400px] text-l rounded-3xl placeholder-black"
                            >
                            <div class="bg-black absolute right-2 top-1/2 -translate-y-1/2 rounded-full p-1 pointer-events-none">
                                <User color="#fff" />
                            </div>
                        </div>

                        <div class="relative mb-2">
                            <input
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

                        <div class="relative">
                            <input
                                type={showPassword ? "text" : "password"}
                                bind:value={rePassword}
                                placeholder="CONFIRM PASSWORD"
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

                    <!-- Centered Button -->
                    <button
                        type="submit"
                        class="bg-black text-white py-2 px-6 rounded-3xl font-semibold m-2 cursor-pointer hover:shadow-[3px_3px_0px_0px_white] transition-all"
                    >
                        Sign Up
                    </button>
                </form>

            </div>

            <div class="flex flex-col items-center bg-white h-[25%] justify-center">

                <div class="relative bg-secondary text-black px-4 py-1 rounded-sm text-sm font-semibold flex items-center gap-1 mb-4 -top-3.5">
                    <span>OR</span>
                </div>

                <button
                    type="button"
                    class="bg-primary text-white py-2 px-6 rounded-3xl font-semibold cursor-pointer hover:shadow-[3px_3px_0px_0px_black] transition-all -mt-2"
                >
                    Login
                </button>

            </div>

        </div>
    </div>
{/if}

<style>
    .animate-in {
        animation: scaleIn 0.2s ease-out;
    }

    @keyframes scaleIn {
        from {
            transform: scale(0.95);
            opacity: 0;
        }
        to {
            transform: scale(1);
            opacity: 1;
        }
    }
</style>
