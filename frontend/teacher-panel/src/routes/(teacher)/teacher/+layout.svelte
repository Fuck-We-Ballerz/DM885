<script>
    import { base } from '$app/paths';
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
    <a href="{base}/teacher/assignment">List Assignments</a>
    <a href="{base}/teacher/assignment/create">Create Assignment</a>
    <a href="{base}/teacher/assignment/add">Add Students To Assignment</a>
    <a href="{base}/teacher/assignment/delete">Remove Students From An Assignment</a>
    <a href="{base}/teacher/course/create">Create Course</a>
    <a href="{base}/teacher/course/add">Add Students To Course</a>
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