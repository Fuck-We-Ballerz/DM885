<script>
    import { base } from '$app/paths';
    import { onMount } from 'svelte';
    export let data;
    export let { keycloak } = data;
    
    onMount(() => {
        if(!keycloak){
            window.location.href = `${base}/`;
        }else if(!keycloak.authenticated){
            window.location.reload();
        }
    });
</script>

<nav>
    <a href="{base}/teacher/course">Courses</a>
    <a href="{base}/teacher/assignment">Assignments</a>
    <a href="{base}/teacher/submission">Submissions</a>
    <a href="{base}/teacher/logout">Logout</a>
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