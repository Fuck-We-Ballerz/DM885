<script>
    import { base } from '$app/paths';
    import { onMount } from 'svelte';
    export let data;
    export let {keycloak} = data;
    
    onMount(() => {
        if(!keycloak){
            window.location.reload();
        }
    });
</script>

<nav>
    <a href="{base}/admin/create">Add Teacher</a>
    <a href="{base}/admin/pause">Pause/Unpause Teachers</a>
    <a href="{base}/admin/delete">Delete Teachers/Students</a>
    <a href="{base}/admin/logout">Logout</a>

</nav>
<slot></slot>
<style>
    nav {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: #f4f4f4;
        padding: 1rem;
    }
    nav a {
        text-decoration: none;
        color: #333;
    }
</style>