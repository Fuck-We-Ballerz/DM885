<script>
    import { onMount } from 'svelte';
    export let data;
    export let { keycloak } = data;
    
    onMount(() => {
        if(!keycloak){
            window.location.reload();
        }
    });
</script>

<nav>
    <a href="/teacher/assignment">List Assignments</a>
    <a href="/teacher/assignment/create">Create Assignment</a>
    <a href="/teacher/logout">Logout</a>
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