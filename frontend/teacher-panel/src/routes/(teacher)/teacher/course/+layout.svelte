<script>
    import { base } from '$app/paths';
</script>


<nav>
    <a href="{base}/teacher/course/create">Create Course</a>
    <a href="{base}/teacher/course/add">Add Students To Course</a>
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