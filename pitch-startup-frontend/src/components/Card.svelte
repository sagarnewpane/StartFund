<script>

    let {title, description, userAvatar, created_at, funding_goal, total_funded, username, image, status} = $props();
</script>

<div class="h-[400px] w-[300px] border-black border-3 rounded-2xl shadow-[5px_5px_0px_0px] shadow-2xl p-4">
    <!-- Date and View  -->
    <div class="flex justify-between">
        <div class=" py-1.5 px-1.5 font-light">
            {created_at}
        </div>
        <div class="bg-secondary font-semibold rounded-3xl py-1.5 px-1.5">
            ${total_funded} / ${funding_goal}
        </div>
    </div>
    <!-- Name, Title and Avatar -->
    <div class="flex justify-between py-3">
        <div class="flex flex-col">
            <span class="font-semibold">{username}</span>
            <span class="font-bold text-2xl">{title}</span>
        </div>
        <div class="flex justify-center items-center w-[50px]">
            <img src={userAvatar} alt="avatar">
        </div>
    </div>
    <!-- Description and Image/Video -->
    <div class="my-2">
        <p class="line-clamp-2 mb-1">{description}</p>
        <div class="rounded-2xl">
            <img src={image} alt="" class="rounded-xl">
        </div>
    </div>
    <!-- Categories and Details -->
    <div class="flex justify-between mt-3">
        <span class="truncate w-30"></span>
        <button class="bg-primary rounded-3xl py-1 px-2 text-white">{status}</button>

    </div>


</div>
