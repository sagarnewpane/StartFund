<script>
    import Card from './Card.svelte';

    // Props - will receive data from parent component
    let { profileData = {
        user: {
            id: "user123",
            email: "john@example.com",
            full_name: "John Doe",
            created_at: "2024-01-15T10:30:00"
        },
        startups: [
            {
                id: "startup123",
                title: "AI Startup",
                description: "Revolutionary AI platform that helps businesses automate their workflows and increase productivity",
                category: "AI",
                funding_goal: 100000,
                total_funded: 45000,
                status: "active",
                image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400",
                created_at: "2024-02-01",
                username: "John Doe",
                userAvatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=John"
            },
            {
                id: "startup124",
                title: "FinTech Revolution",
                description: "Next-generation payment processing system for modern businesses",
                category: "FinTech",
                funding_goal: 150000,
                total_funded: 120000,
                status: "active",
                image: "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400",
                created_at: "2024-01-20",
                username: "John Doe",
                userAvatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=John"
            },
            {
                id: "startup125",
                title: "Green Energy App",
                description: "Smart energy management for sustainable homes",
                category: "CleanTech",
                funding_goal: 80000,
                total_funded: 80000,
                status: "funded",
                image: "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=400",
                created_at: "2024-01-10",
                username: "John Doe",
                userAvatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=John"
            }
        ],
        investments: [
            {
                id: "inv123",
                amount: 5000,
                invested_at: "2024-01-20T14:30:00",
                startup: {
                    id: "startup456",
                    title: "HealthTech App",
                    category: "HealthTech",
                    image_url: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400"
                }
            },
            {
                id: "inv124",
                amount: 10000,
                invested_at: "2024-02-05T14:30:00",
                startup: {
                    id: "startup457",
                    title: "EdTech Platform",
                    category: "Education",
                    image_url: "https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=400"
                }
            }
        ],
        stats: {
            total_startups: 3,
            total_raised: 245000,
            total_invested: 15000,
            total_investments: 2
        }
    } } = $props();

    let activeTab = $state('startups'); // 'startups' or 'investments'

    // Helper function to format date
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
</script>

<div class="min-h-screen bg-light">
    <!-- Hero Section with Profile Info -->
    <div class="bg-primary py-16 border-b-4 border-black">
        <div class="bg-[repeating-linear-gradient(to_right,#febe3c_0px,#febe3c_0.1px,transparent_1px,transparent_20px)] py-8">
            <div class="max-w-6xl mx-auto px-4">
                <div class="bg-white border-3 border-black rounded-2xl shadow-[8px_8px_0px_0px_black] p-8">
                    <div class="flex flex-col md:flex-row gap-8 items-start">
                        <!-- Avatar -->
                        <div class="flex-shrink-0">
                            <div class="w-32 h-32 bg-secondary rounded-full border-3 border-black flex items-center justify-center text-5xl font-bold shadow-[5px_5px_0px_0px_black]">
                                {profileData.user.full_name.charAt(0)}
                            </div>
                        </div>

                        <!-- User Info -->
                        <div class="flex-grow">
                            <h1 class="text-4xl font-extrabold mb-2">{profileData.user.full_name}</h1>
                            <p class="text-lg text-gray-600 mb-4">{profileData.user.email}</p>
                            <div class="flex gap-2 items-center mb-4">
                                <span class="bg-secondary px-3 py-1 rounded-full text-sm font-semibold border-2 border-black">
                                    Member since {formatDate(profileData.user.created_at)}
                                </span>
                            </div>

                            <!-- Stats Grid -->
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                                <div class="bg-light border-2 border-black rounded-xl p-4 shadow-[3px_3px_0px_0px_black]">
                                    <div class="text-2xl font-bold text-primary">{profileData.stats.total_startups}</div>
                                    <div class="text-sm font-semibold">Startups</div>
                                </div>
                                <div class="bg-light border-2 border-black rounded-xl p-4 shadow-[3px_3px_0px_0px_black]">
                                    <div class="text-2xl font-bold text-primary">${profileData.stats.total_raised.toLocaleString()}</div>
                                    <div class="text-sm font-semibold">Total Raised</div>
                                </div>
                                <div class="bg-light border-2 border-black rounded-xl p-4 shadow-[3px_3px_0px_0px_black]">
                                    <div class="text-2xl font-bold text-primary">{profileData.stats.total_investments}</div>
                                    <div class="text-sm font-semibold">Investments</div>
                                </div>
                                <div class="bg-light border-2 border-black rounded-xl p-4 shadow-[3px_3px_0px_0px_black]">
                                    <div class="text-2xl font-bold text-primary">${profileData.stats.total_invested.toLocaleString()}</div>
                                    <div class="text-sm font-semibold">Total Invested</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Tabs Section -->
    <div class="max-w-6xl mx-auto px-4 py-8">
        <div class="flex gap-4 mb-8">
            <button
                onclick={() => activeTab = 'startups'}
                class="px-6 py-3 font-bold text-lg rounded-3xl border-3 border-black transition-all {activeTab === 'startups' ? 'bg-primary text-white shadow-[4px_4px_0px_0px_black]' : 'bg-white hover:shadow-[4px_4px_0px_0px_black]'}"
            >
                My Startups ({profileData.startups.length})
            </button>
            <button
                onclick={() => activeTab = 'investments'}
                class="px-6 py-3 font-bold text-lg rounded-3xl border-3 border-black transition-all {activeTab === 'investments' ? 'bg-primary text-white shadow-[4px_4px_0px_0px_black]' : 'bg-white hover:shadow-[4px_4px_0px_0px_black]'}"
            >
                My Investments ({profileData.investments.length})
            </button>
        </div>

        <!-- Startups Tab -->
        {#if activeTab === 'startups'}
            {#if profileData.startups.length > 0}
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {#each profileData.startups as startup}
                        <Card
                            title={startup.title}
                            description={startup.description}
                            userAvatar={startup.userAvatar}
                            created_at={startup.created_at}
                            funding_goal={startup.funding_goal}
                            total_funded={startup.total_funded}
                            username={startup.username}
                            image={startup.image}
                            status={startup.status}
                        />
                    {/each}
                </div>
            {:else}
                <div class="bg-white border-3 border-black rounded-2xl shadow-[5px_5px_0px_0px_black] p-12 text-center">
                    <p class="text-xl font-bold text-gray-500">No startups yet</p>
                    <p class="text-gray-600 mt-2">Create your first startup to get started!</p>
                    <button class="mt-6 bg-primary text-white font-semibold px-6 py-3 rounded-3xl border-3 border-black hover:shadow-[4px_4px_0px_0px_black] transition-all">
                        Create Startup
                    </button>
                </div>
            {/if}
        {/if}

        <!-- Investments Tab -->
        {#if activeTab === 'investments'}
            {#if profileData.investments.length > 0}
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {#each profileData.investments as investment}
                        <div class="bg-white border-3 border-black rounded-2xl shadow-[5px_5px_0px_0px_black] p-6 hover:shadow-[8px_8px_0px_0px_black] transition-all flex flex-col h-full">
                            <!-- Startup Image -->
                            {#if investment.startup.image_url}
                                <div class="mb-4 rounded-xl overflow-hidden border-2 border-black">
                                    <img src={investment.startup.image_url} alt={investment.startup.title} class="w-full h-48 object-cover" />
                                </div>
                            {/if}

                            <!-- Investment Details -->
                            <div class="flex-grow">
                                <h3 class="text-xl font-bold mb-3 leading-tight">{investment.startup.title}</h3>
                                <div class="mb-3">
                                    <span class="inline-block bg-light px-3 py-1.5 rounded-full text-sm font-semibold border-2 border-black">
                                        {investment.startup.category}
                                    </span>
                                </div>
                            </div>

                            <!-- Investment Amount -->
                            <div class="border-t-2 border-gray-200 pt-4 mt-auto">
                                <div class="flex items-center justify-between mb-2">
                                    <span class="text-sm font-semibold text-gray-600">Investment Amount</span>
                                    <span class="bg-secondary px-3 py-1 rounded-full text-sm font-bold border-2 border-black">
                                        ${investment.amount.toLocaleString()}
                                    </span>
                                </div>
                                <div class="text-xs text-gray-500">
                                    Invested on {formatDate(investment.invested_at)}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="bg-white border-3 border-black rounded-2xl shadow-[5px_5px_0px_0px_black] p-12 text-center">
                    <p class="text-xl font-bold text-gray-500">No investments yet</p>
                    <p class="text-gray-600 mt-2">Start investing in promising startups!</p>
                    <button class="mt-6 bg-primary text-white font-semibold px-6 py-3 rounded-3xl border-3 border-black hover:shadow-[4px_4px_0px_0px_black] transition-all">
                        Browse Startups
                    </button>
                </div>
            {/if}
        {/if}
    </div>
</div>
