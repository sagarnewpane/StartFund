<script>
    let {
        title = "AI Startup Platform",
        description = "Revolutionary AI platform that helps businesses automate their workflows and increase productivity with cutting-edge technology",
        userAvatar = "https://api.dicebear.com/7.x/avataaars/svg?seed=John",
        created_at = "2024-01-15",
        funding_goal = 100000,
        total_funded = 45000,
        username = "John Doe",
        image = "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400",
        status = "active"
    } = $props();
</script>


<div class="h-[400px] w-[300px] border-black border-3 rounded-2xl shadow-[5px_5px_0px_0px] shadow-2xl p-4 flex flex-col">
    <!-- Date and Funding -->
    <div class="flex justify-between items-center mb-3">
        <div class="py-1.5 px-1.5 font-light text-sm">
            {created_at}
        </div>
        <div class="bg-secondary font-semibold rounded-3xl py-1.5 px-2 text-xs whitespace-nowrap">
            ${total_funded} / ${funding_goal}
        </div>
    </div>

    <!-- Name, Title and Avatar -->
    <div class="flex gap-3 mb-3">
        <div class="flex flex-col flex-1 min-w-0">
            <span class="font-semibold text-sm">{username}</span>
            <h3 class="font-bold text-xl leading-tight break-words">{title}</h3>
        </div>
        <div class="flex-shrink-0 w-[50px] h-[50px]">
            <img src={userAvatar} alt="avatar" class="w-full h-full object-cover rounded-full">
        </div>
    </div>

    <!-- Description and Image/Video -->
    <div class="flex-1 flex flex-col min-h-0">
        <p class="line-clamp-2 mb-2 text-sm">{description}</p>
        <div class="flex-1 min-h-0 rounded-xl overflow-hidden">
            <img src={image} alt={title} class="w-full h-full object-cover">
        </div>
    </div>

    <!-- Status Button -->
    <div class="flex justify-end mt-3">
        <button class="bg-primary rounded-3xl py-1.5 px-4 text-white font-semibold text-sm">
            {status}
        </button>
    </div>
</div>
