<script>
    import { base } from '$app/paths';
</script>


<nav>
    <a href="{base}/teacher/assignment/create">Create Assignment</a>
    <a href="{base}/teacher/assignment/list">List Assignments</a>
    <a href="{base}/teacher/assignment/add">Add Students To Assignment</a>
    <a href="{base}/teacher/assignment/delete">Remove Students From An Assignment</a>
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