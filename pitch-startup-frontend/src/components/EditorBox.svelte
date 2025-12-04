<script>
    import { Editor } from '@tiptap/core';
    import StarterKit from '@tiptap/starter-kit';
    import { onMount, onDestroy } from 'svelte';
    import { Bold, Italic, List, ListOrdered, Heading1, Heading2 } from 'lucide-svelte';

    let element;
    let editor;

    onMount(() => {
        editor = new Editor({
            element: element,
            extensions: [StarterKit],
            content: '<p>Describe your idea and what problem it solves...</p>',
            onTransaction: () => {
                editor = editor;
            }
        });
    });

    onDestroy(() => {
        if (editor) {
            editor.destroy();
        }
    });

    function toggleBold() {
        editor.chain().focus().toggleBold().run();
    }

    function toggleItalic() {
        editor.chain().focus().toggleItalic().run();
    }

    function toggleBulletList() {
        editor.chain().focus().toggleBulletList().run();
    }

    function toggleOrderedList() {
        editor.chain().focus().toggleOrderedList().run();
    }

    function toggleHeading(level) {
        editor.chain().focus().toggleHeading({ level }).run();
    }

    function setParagraph() {
        editor.chain().focus().setParagraph().run();
    }
</script>

<div class="max-w-4xl mx-auto">
    <div class="border-3 border-gray-800 rounded-lg overflow-hidden shadow-lg bg-white" style="height: 500px; width: 600px;">
        <!-- Toolbar -->
        <div class="bg-gray-50 border-b-3 border-gray-800 p-3 flex items-center gap-2 flex-shrink-0">
            <button
                onclick={() => toggleHeading(1)}
                class="p-2 hover:bg-gray-200 rounded transition-colors flex items-center gap-1"
                title="Heading 1"
            >
                <Heading1 size={20} />
            </button>
            <button
                onclick={() => toggleHeading(2)}
                class="p-2 hover:bg-gray-200 rounded transition-colors flex items-center gap-1"
                title="Heading 2"
            >
                <Heading2 size={20} />
            </button>

            <div class="w-px h-6 bg-gray-300 mx-1"></div>

            <button
                onclick={toggleBold}
                class="p-2 hover:bg-gray-200 rounded transition-colors font-bold"
                title="Bold"
            >
                <Bold size={20} />
            </button>
            <button
                onclick={toggleItalic}
                class="p-2 hover:bg-gray-200 rounded transition-colors"
                title="Italic"
            >
                <Italic size={20} />
            </button>

            <div class="w-px h-6 bg-gray-300 mx-1"></div>

            <button
                onclick={toggleBulletList}
                class="p-2 hover:bg-gray-200 rounded transition-colors"
                title="Bullet List"
            >
                <List size={20} />
            </button>
            <button
                onclick={toggleOrderedList}
                class="p-2 hover:bg-gray-200 rounded transition-colors"
                title="Numbered List"
            >
                <ListOrdered size={20} />
            </button>
        </div>

        <!-- Editor -->
        <div
            bind:this={element}
            class="p-6 bg-white overflow-y-auto flex-grow"
            style="flex: 1; overflow-y: auto;"
        ></div>
    </div>
</div>

<style>
    :global(.ProseMirror) {
        outline: none;
        min-height: 100%;
    }

    :global(.ProseMirror p.is-editor-empty:first-child::before) {
        content: attr(data-placeholder);
        float: left;
        color: #adb5bd;
        pointer-events: none;
        height: 0;
    }

    :global(.ProseMirror h1) {
        font-size: 2em;
        font-weight: bold;
        margin-top: 0.75em;
        margin-bottom: 0.5em;
        line-height: 1.2;
    }

    :global(.ProseMirror h2) {
        font-size: 1.5em;
        font-weight: bold;
        margin-top: 0.75em;
        margin-bottom: 0.5em;
        line-height: 1.3;
    }

    :global(.ProseMirror p) {
        margin: 0.5em 0;
        line-height: 1.6;
    }

    :global(.ProseMirror ul) {
        list-style-type: disc;
        padding-left: 1.5em;
        margin: 0.75em 0;
    }

    :global(.ProseMirror ol) {
        list-style-type: decimal;
        padding-left: 1.5em;
        margin: 0.75em 0;
    }

    :global(.ProseMirror li) {
        margin: 0.25em 0;
        line-height: 1.6;
    }

    :global(.ProseMirror li p) {
        margin: 0;
    }

    :global(.ProseMirror strong) {
        font-weight: bold;
    }

    :global(.ProseMirror em) {
        font-style: italic;
    }
</style>
