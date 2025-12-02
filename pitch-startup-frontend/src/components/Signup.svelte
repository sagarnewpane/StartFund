<script>
    import { User, Mail, Eye, EyeClosed } from 'lucide-svelte';

    let showPassword = $state(false);
    let password = $state('');
    let rePassword = $state('');
    let fullName = $state('');
    let email = $state('');

    function togglePassword() {
        showPassword = !showPassword;
    }

    function handleSubmit() {
        console.log('Form submitted');
        console.log('Full Name:', fullName);
        console.log('Email:', email);
        console.log('Password:', password);
        console.log('Re-Password:', rePassword);
    }
</script>

<!-- Center the whole box -->
<div class="h-screen w-full flex items-center justify-center">

    <div class="h-[550px] w-[450px] border-black border-3 rounded-2xl shadow-[5px_5px_0px_0px] shadow-2xl overflow-hidden">

        <div class="bg-primary h-[75%] flex flex-col justify-center items-center">

            <div class="uppercase bg-dark text-light text-center font-extrabold text-4xl mb-4 p-2 w-[90%]">
                <span>you new here eh?</span>
            </div>

            <form class="flex flex-col items-center">
                <div class="m-2">

                    <div class="relative mb-2">
                        <input
                            type="input"
                            bind:value={fullName}
                            placeholder="FULL NAME"
                            required
                            class="text-black bg-white border-3 p-2 w-[400px] text-l rounded-3xl placeholder-black"
                        >
                        <button class="bg-black absolute right-2 top-1/2 -translate-y-1/2 cursor-pointer rounded-full p-1">
                            <User color="#fff" />
                        </button>
                    </div>

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

                    <div class="relative mb-2">
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

                    <div class="relative">
                        <input
                            type={showPassword ? "text" : "password"}
                            bind:value={rePassword}
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

                <!-- Centered Button -->
                <button
                    type="submit"
                    onclick={handleSubmit}
                    class="bg-black text-white py-2 px-6 rounded-3xl font-semibold m-2 cursor-pointer"
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

</div>
