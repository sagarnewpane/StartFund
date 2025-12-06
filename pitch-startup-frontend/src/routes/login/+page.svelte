<script>
    import Login from "../../components/Login.svelte";

    // 1. Receive form data (errors/messages) from the server action
    let { form } = $props();
</script>

<Login {form} />
