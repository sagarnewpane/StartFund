<script>
    import SearchIcon from '$lib/assets/search.png';
</script>
<div class="bg-primary py-[72px] ">
    <div class=' h-full z-50 bg-[repeating-linear-gradient(to_right,#febe3c_0px,#febe3c_0.1px,transparent_1px,transparent_20px)]'>
    <!-- Yellow tag -->
  <div class="flex justify-center items-center flex-col">
    <div class="bg-secondary text-black px-4 py-1 rounded-sm text-sm font-semibold flex items-center gap-1 mb-4">
      <span>PITCH, VOTE, AND GROW</span>
      <span class="rotate text-xl">▴</span>
    </div>
    <!--Title -->
    <span class=" uppercase bg-dark text-light text-center font-extrabold text-4xl mb-4 p-2">Pitch Your Startup,<br> Connect with Entrepreneurs</span>
    <!--Subtitle-->
    <p class="text-light mb-4">Submit Ideas, Vote on Pitches, and Get Noticed in Virtual Competitions</p>
    <!-- Search -->
    <div class="relative">
     <input type="search" placeholder="SEARCH STARTUP" class=" text-black bg-white border-3 p-2 w-[400px] text-l rounded-3xl placeholder-black placeholder-bold placeholder-opacity-75" >
     <button class="absolute right-2 top-1/2 -translate-y-1/2  cursor-pointer"><img class="" src={SearchIcon} alt="" width="32px"></button>
    </div>
  </div>
    </div>
</div>


<style>
  .placeholder-bold::placeholder {
    font-weight: 600; /* bold */
  }
</style>
