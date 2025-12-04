<script>
	import EditorBox from "./EditorBox.svelte";

</script>
<form action="">
<div class="bg-primary py-[72px] mb-10">
    <div class=' h-full z-50 bg-[repeating-linear-gradient(to_right,#febe3c_0px,#febe3c_0.1px,transparent_1px,transparent_20px)]'>
  <div class="flex justify-center items-center flex-col">
    <!--Title -->
    <span class=" uppercase bg-dark text-light text-center font-extrabold text-4xl mb-4 p-2">Submit Your Startup Pitch</span>
  </div>
    </div>
</div>
<div class="flex justify-center flex-row">
    <div>
        <!-- Title -->
        <p>Title</p>
        <input required type="text" class="text-black bg-white border-3 p-2 w-full text-l rounded-3xl placeholder-black" placeholder='Title of your Pitch'>
        <!-- Description -->
        <p>Description</p>
        <textarea name="" id="" required placeholder="Short description of your startup idea" class="text-black bg-white border-3 p-2 w-full h-30 text-l rounded-3xl placeholder-black"></textarea>
        <!-- Category -->
        <p>category</p>
        <input required class="text-black bg-white border-3 p-2 w-full text-l rounded-3xl placeholder-black" placeholder='Categories, more than one use comma'>
        <!-- Title -->
        <p>image/video link</p>
        <input required class="text-black bg-white border-3 p-2 w-full text-l rounded-3xl placeholder-black" placeholder='Link to your startup image/video'>
        <!-- Editor Box -->
        <p>pitch</p>
        <EditorBox/>
        <!-- Submit button -->
        <button type="submit" class=" my-4 uppercase font-bold bg-primary text-white p-2 w-full text-l rounded-3xl border-3 border-black cursor-pointer">Submit your pitch</button>

    </div>
</div>
</form>

<style>
    p{
        text-transform: capitalize;
        font-weight: bold;
        padding: 15px 0px 5px 0 ;
    }
</style>
